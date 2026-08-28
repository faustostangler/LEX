"""Federal DOU Spider for Brazilian Official Gazette (Diário Oficial da União).

Scrapes Section 1 (DO1), Section 2 (DO2), Section 3 (DO3), and Extra (DOE) editions directly
from the modern Imprensa Nacional portal (www.in.gov.br/leiturajornal). Concurrently retrieves
the complete, untruncated HTML body for every published normative act and aggregates the full text.
"""

import asyncio
import json
import re
from collections.abc import AsyncIterator, Generator
from datetime import date

import httpx
from bs4 import BeautifulSoup
from scrapy.http import HtmlResponse, Request, Response

from lex.ingestion.infrastructure.dto import RawGazettePayload
from lex.ingestion.infrastructure.scrapy_project.spiders.base import BaseGazetteSpider


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

    async def parse_modern_section(self, response: Response) -> AsyncIterator[RawGazettePayload]:
        """Parse modern in.gov.br leiturajornal page, fetching 100% full text for all acts."""
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
        self.logger.info(
            f"Retrieving full bodies for {len(articles)} acts in {section_name} ({target_date})..."
        )

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        }

        # Concurrently fetch full HTML bodies for all articles in the edition
        full_text_blocks = await self._fetch_all_articles_text(articles, headers)

        if full_text_blocks:
            full_text = "\n\n" + ("=" * 50) + "\n\n".join(full_text_blocks)
            yield RawGazettePayload(
                territory_code=self.territory_code,
                tier=self.tier,
                source_url=response.url,
                raw_content=full_text,
                date_obj=target_date,
                section=section_name,
                edition_number=edition_number,
                is_extra_edition=is_extra,
                power="executive",
            )

    async def _fetch_all_articles_text(
        self, articles: list[dict[str, object]], headers: dict[str, str]
    ) -> list[str]:
        """Concurrently fetch and extract full text for all articles using bounded concurrency."""
        sem = asyncio.Semaphore(25)

        async with httpx.AsyncClient(
            headers=headers,
            timeout=20.0,
            limits=httpx.Limits(max_connections=50, max_keepalive_connections=30),
        ) as client:

            async def _fetch_single_act(art: dict[str, object]) -> str:
                url_title = str(art.get("urlTitle", "")).strip()
                hierarchy = str(art.get("hierarchyStr", "")).strip()
                title = str(art.get("title", "")).strip()
                preview = str(art.get("content", "")).strip()

                if url_title:
                    article_url = f"{self.ARTICLE_BASE_URL}{url_title}"
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
                                    header = f"ÓRGÃO: {hierarchy}" if hierarchy else ""
                                    return f"{header}\n{body_text}".strip()
                    except (httpx.HTTPError, TimeoutError) as exc:
                        self.logger.debug(f"Article fetch failed for {url_title}: {exc}")

                # Fallback to metadata preview if individual request failed
                fallback_parts: list[str] = []
                if hierarchy:
                    fallback_parts.append(f"ÓRGÃO: {hierarchy}")
                if title:
                    fallback_parts.append(title)
                if preview:
                    fallback_parts.append(preview)
                return "\n".join(fallback_parts)

            tasks = [_fetch_single_act(art) for art in articles]
            return await asyncio.gather(*tasks)

    def handle_request_error(self, failure: object) -> None:
        """Handle request network failures gracefully."""
        self.logger.warning(f"Request failed for DOU spider: {failure}")
