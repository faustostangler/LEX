"""Federal DOU Spider for Brazilian Official Gazette (Diário Oficial da União).

Scrapes Section 1 (DO1), Section 2 (DO2), Section 3 (DO3), and Extra (DOE) editions directly
from the modern Imprensa Nacional portal (www.in.gov.br/leiturajornal).
Yields discrete RawNormativeActPayload items for every published normative act without string joins.
"""

import asyncio
import json
import re
from collections.abc import AsyncIterator, Generator
from datetime import date

import httpx
from bs4 import BeautifulSoup
from scrapy.http import HtmlResponse, Request, Response

from lex.ingestion.infrastructure.dto import (
    RawGazettePayload,
    RawNormativeActPayload,
)
from lex.ingestion.infrastructure.scrapy_project.spiders.base import (
    BaseGazetteSpider,
)


class FederalDouSpider(BaseGazetteSpider):
    """Spider for crawling the Federal Official Gazette (DOU)."""

    name = "federal_dou"
    territory_code = "BR"
    tier = "federal"
    allowed_domains = ["www.in.gov.br", "in.gov.br", "pesquisa.in.gov.br"]

    # Modern in.gov.br section identifiers
    MODERN_SECTIONS: dict[str, str] = {
        "do1": "secao_1",
        "do2": "secao_2",
        "do3": "secao_3",
        "doe": "extra",
    }

    LEITURA_JORNAL_URL = "https://www.in.gov.br/leiturajornal"
    ARTICLE_BASE_URL = "https://www.in.gov.br/web/dou/-/"

    def start_requests(self) -> Generator[Request, None, None]:
        """Generate starting index requests for each configured DOU section and target date."""
        for target_date in self.date_range():
            date_formatted = target_date.strftime("%d-%m-%Y")
            for sec_key, sec_name in self.MODERN_SECTIONS.items():
                url = f"{self.LEITURA_JORNAL_URL}?data={date_formatted}&secao={sec_key}"
                yield Request(
                    url=url,
                    callback=self.parse_modern_section,
                    errback=self.handle_request_error,
                    meta={
                        "gazette_date": target_date,
                        "section_key": sec_key,
                        "section_name": sec_name,
                        "is_extra": (sec_key == "doe"),
                    },
                    dont_filter=True,
                )

    async def parse_modern_section(
        self, response: Response
    ) -> AsyncIterator[RawGazettePayload | RawNormativeActPayload]:
        """Parse modern in.gov.br leiturajornal page, yielding edition header and discrete acts."""
        if not isinstance(response, HtmlResponse):
            return

        meta = response.meta
        target_date: date = meta["gazette_date"]
        section_name: str = meta["section_name"]
        is_extra: bool = meta.get("is_extra", False)

        # Extract embedded JSON data in <script id="params" type="application/json">
        script_match = re.search(
            r'<script id="params"[^>]*>(.*?)</script>', response.text, re.DOTALL
        )
        if not script_match:
            return

        try:
            params_data = json.loads(script_match.group(1).strip())
        except (json.JSONDecodeError, ValueError):
            return

        articles = params_data.get("jsonArray", [])
        if not articles:
            return

        edition_number = str(articles[0].get("editionNumber", "1")) if articles else "1"
        total_acts = len(articles)

        # 1. Yield Edition Container Metadata
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=f"DOU {section_name} - {target_date.isoformat()} ({total_acts} acts)",
            total_acts=total_acts,
            date_obj=target_date,
            section=section_name,
            edition_number=edition_number,
            is_extra_edition=is_extra,
            power="executive",
        )

        self.logger.info(
            f"Streaming {total_acts} discrete acts for {section_name} ({target_date})..."
        )

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        }

        # 2. Concurrently fetch and stream each discrete act payload
        sem = asyncio.Semaphore(25)

        async with httpx.AsyncClient(
            headers=headers,
            timeout=20.0,
            limits=httpx.Limits(max_connections=50, max_keepalive_connections=30),
        ) as client:

            async def _fetch_act(
                art: dict[str, object],
            ) -> RawNormativeActPayload | None:
                url_title = str(art.get("urlTitle", "")).strip()
                hierarchy_str = str(art.get("hierarchyStr", "")).strip()
                title = str(art.get("title", "")).strip()
                preview = str(art.get("content", "")).strip()
                art_type_raw = str(art.get("artType", "")).strip()

                hierarchy_parts = [p.strip() for p in hierarchy_str.split("/") if p.strip()]
                article_url = f"{self.ARTICLE_BASE_URL}{url_title}" if url_title else response.url

                body_text = ""
                ementa: str | None = None
                authority_name: str | None = None
                authority_role: str | None = None

                if url_title:
                    try:
                        async with sem:
                            resp = await client.get(article_url)
                            if resp.status_code == 200:
                                soup = BeautifulSoup(resp.text, "html.parser")
                                div = soup.find("div", class_="texto-dou") or soup.find(
                                    "div", id="materia"
                                )
                                if div:
                                    body_text = div.get_text(separator="\n", strip=True)

                                ementa_el = soup.find(class_="ementa")
                                if ementa_el:
                                    ementa = ementa_el.get_text(strip=True)

                                assina_el = soup.find(class_="assina")
                                if assina_el:
                                    authority_name = assina_el.get_text(strip=True)

                                cargo_el = soup.find(class_="cargo")
                                if cargo_el:
                                    authority_role = cargo_el.get_text(strip=True)
                    except (httpx.HTTPError, TimeoutError) as exc:
                        self.logger.debug(f"Article fetch failed for {url_title}: {exc}")

                if not body_text:
                    body_text = preview or title

                if not body_text:
                    return None

                # Derive parsed typology, number and year
                (
                    act_type,
                    act_number,
                    act_year,
                ) = self._parse_act_type_and_number(
                    title,
                    default_type=art_type_raw or "OUTROS",
                    target_year=target_date.year,
                )

                return RawNormativeActPayload(
                    territory_code=self.territory_code,
                    source_url=article_url,
                    raw_content=body_text,
                    title=title or act_type,
                    act_type=act_type,
                    date_obj=target_date,
                    act_number=act_number,
                    act_year=act_year,
                    ementa=ementa,
                    hierarchy=hierarchy_parts,
                    authority_name=authority_name,
                    authority_role=authority_role,
                    edition_number=edition_number,
                    section=section_name,
                    is_extra_edition=is_extra,
                    classification_source="pre_segmented_source",
                    classification_confidence=1.0,
                )

            tasks = [_fetch_act(art) for art in articles]
            results = await asyncio.gather(*tasks)

            for act_payload in results:
                if act_payload is not None:
                    yield act_payload

    @staticmethod
    def _parse_act_type_and_number(
        title: str, default_type: str, target_year: int
    ) -> tuple[str, str | None, int | None]:
        """Extract legal act typology, number, and publication year from title string."""
        if not title:
            return default_type.upper(), None, target_year

        match = re.search(
            r"^([A-ZÁÉÍÓÚÂÊÔÃÕÇ\s\/\-]+?)(?:\s+(?:[Nn][º°o\.]\s*))([0-9\.\-\/]+)?(?:.*?(?:DE\s+\d+\s+DE\s+[A-Za-zçãéíóúáâêô]+\s+DE\s+(\d{4})))?",
            title,
            re.IGNORECASE,
        )
        if match:
            act_type = match.group(1).strip().upper()
            num = match.group(2).strip() if match.group(2) else None
            year = int(match.group(3)) if match.group(3) else target_year
            return act_type, num, year

        first_word = title.split()[0].upper() if title.split() else default_type.upper()
        return first_word, None, target_year

    def handle_request_error(self, failure: object) -> None:
        """Handle request network failures gracefully."""
        self.logger.warning(f"Request failed for DOU spider: {failure}")
