"""Federal DOU Spider for Brazilian Official Gazette (Diário Oficial da União).

Scrapes Section 1 (DO1), Section 2 (DO2), Section 3 (DO3), and Extra (DOE) editions directly
from the modern Imprensa Nacional portal (www.in.gov.br/leiturajornal).
Yields discrete RawNormativeActPayload items for every published normative act without string joins.
Supports Zero-Scrape Idempotent Early-Exit (ADR-004) to avoid re-scraping completed editions.
"""

import asyncio
import json
import re
from collections.abc import AsyncIterator, Generator
from datetime import date
from typing import Any, Self

import httpx
from bs4 import BeautifulSoup
from scrapy.crawler import Crawler
from scrapy.http import HtmlResponse, Request, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from tqdm import tqdm

from lex.ingestion.application.ports import GazetteRepositoryPort
from lex.ingestion.domain.value_objects import (
    GazetteDate,
    IngestionStatus,
    TerritoryId,
)
from lex.ingestion.infrastructure.dto import (
    RawGazettePayload,
    RawNormativeActPayload,
)
from lex.ingestion.infrastructure.persistence.postgres_repository import (
    PostgresGazetteRepository,
)
from lex.ingestion.infrastructure.scrapy_project.spiders.base import (
    BaseGazetteSpider,
)
from lex.shared_kernel.config import LexSettings

# -----------------------------------------------------------------------------
# Module Constants & Operational Defaults (ADR-003)
# -----------------------------------------------------------------------------
DEFAULT_CONCURRENT_SEMAPHORE: int = 50
DEFAULT_HTTP_TIMEOUT_SECONDS: float = 20.0
DEFAULT_MAX_CONNECTIONS: int = 80
DEFAULT_MAX_KEEPALIVE_CONNECTIONS: int = 50
DEFAULT_TQDM_MIN_INTERVAL_SECONDS: float = 0.2
DEFAULT_TQDM_BAR_FORMAT: str = (
    "{desc}: {percentage:3.0f}%|{bar}| {n:4d}/{total:4d} [{elapsed}<{remaining}, {rate_fmt}]"
)

LEITURA_JORNAL_BASE_URL: str = "https://www.in.gov.br/leiturajornal"
ARTICLE_READ_BASE_URL: str = "https://www.in.gov.br/web/dou/-/"

DEFAULT_BROWSER_HEADERS: dict[str, str] = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
}

MODERN_SECTIONS_MAP: dict[str, str] = {
    "doe": "extra",
    "do1": "secao_1",
    "do2": "secao_2",
    "do3": "secao_3",
}

SECTION_CODE_MAP: dict[str, str] = {
    "extra": "E",
    "secao_1": "1",
    "secao_2": "2",
    "secao_3": "3",
}

SCRIPT_PARAMS_PATTERN: re.Pattern[str] = re.compile(
    r'<script\b[^>]*\bid=["\']params["\'][^>]*>(.*?)</script>', re.DOTALL
)
ACT_TYPOLOGY_PATTERN: re.Pattern[str] = re.compile(
    r"^([A-ZÁÉÍÓÚÂÊÔÃÕÇ\s\/\-]+?)(?:\s+(?:[Nn][º°o\.]\s*))([0-9\.\-\/]+)?(?:.*?(?:DE\s+\d+\s+DE\s+[A-Za-zçãéíóúáâêô]+\s+DE\s+(\d{4})))?",
    re.IGNORECASE,
)


class FederalDouSpider(BaseGazetteSpider):
    """Spider for crawling the Federal Official Gazette (DOU)."""

    name = "federal_dou"
    territory_code = "BR"
    tier = "federal"
    allowed_domains = ["www.in.gov.br", "in.gov.br", "pesquisa.in.gov.br"]

    def __init__(
        self,
        *args: Any,
        repository: GazetteRepositoryPort | None = None,
        force: bool | str = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.repository = repository
        self.force = force.lower() in ("true", "1", "yes") if isinstance(force, str) else force
        self._session: Session | None = None

    @classmethod
    def from_crawler(cls, crawler: Crawler, *args: Any, **kwargs: Any) -> Self:
        spider = super().from_crawler(crawler, *args, **kwargs)
        try:
            settings = LexSettings()
            if settings.database_url:
                engine = create_engine(str(settings.database_url), pool_pre_ping=True)
                session_factory = sessionmaker(bind=engine)
                spider._session = session_factory()
                spider.repository = PostgresGazetteRepository(session=spider._session)
        except Exception:
            spider.repository = None
            spider._session = None
        return spider

    def closed(self, reason: str) -> None:
        """Clean up repository database session on spider shutdown."""
        if hasattr(self, "_session") and self._session is not None:
            self._session.close()

    def start_requests(self) -> Generator[Request, None, None]:
        """Generate starting index requests for each configured DOU section and target date."""
        for target_date in self.date_range():
            date_formatted = target_date.strftime("%d-%m-%Y")
            for sec_key, sec_name in MODERN_SECTIONS_MAP.items():
                url = f"{LEITURA_JORNAL_BASE_URL}?data={date_formatted}&secao={sec_key}"
                yield Request(
                    url=url,
                    callback=self.parse_modern_section,
                    errback=self.handle_request_error,
                    meta={
                        "gazette_date": target_date,
                        "section_key": sec_key,
                        "section_name": sec_name,
                        "is_extra": (sec_key == "doe"),
                        "handle_httpstatus_list": [502, 404],
                    },
                    dont_filter=True,
                )

    async def parse_modern_section(
        self, response: Response
    ) -> AsyncIterator[RawGazettePayload | RawNormativeActPayload]:
        """Parse modern in.gov.br leiturajornal page, yielding edition header and discrete acts."""
        meta = response.meta
        target_date: date = meta["gazette_date"]
        section_name: str = meta["section_name"]
        is_extra: bool = meta.get("is_extra", False)

        # Silently skip 502/404 indicating no edition published (weekend/holiday)
        if response.status in (502, 404):
            self.logger.debug(
                f"[SKIP] Sem publicação do DOU ({section_name}) em {target_date.isoformat()} "
                f"(status {response.status})."
            )
            return

        if not isinstance(response, HtmlResponse):
            return

        # Extract embedded JSON data in <script id="params" type="application/json">
        script_match = SCRIPT_PARAMS_PATTERN.search(response.text)
        if not script_match:
            self.logger.debug(
                f"[SKIP] Sem dados para DOU ({section_name}) em {target_date.isoformat()}."
            )
            return

        try:
            params_data = json.loads(script_match.group(1).strip())
        except (json.JSONDecodeError, ValueError):
            self.logger.debug(
                f"[SKIP] Script corrompido para DOU {section_name} em {target_date.isoformat()}."
            )
            return

        articles = params_data.get("jsonArray", [])
        if not articles:
            self.logger.debug(
                f"[SKIP] Zero artigos para DOU ({section_name}) em {target_date.isoformat()}."
            )
            return

        edition_number = str(articles[0].get("editionNumber", "1")) if articles else "1"
        total_acts = len(articles)

        # Check Zero-Scrape Early-Exit condition (ADR-004)
        if not self.force and self.repository is not None:
            existing_edition = self.repository.get_by_territory_and_date(
                territory_id=TerritoryId.from_code(self.territory_code),
                date=GazetteDate.from_date(target_date),
                section=section_name,
            )
            if (
                existing_edition is not None
                and existing_edition.ingestion_status == IngestionStatus.COMPLETED
                and existing_edition.total_acts == total_acts
            ):
                self.logger.debug(
                    f"[SKIP] DOU {section_name} ({target_date.isoformat()}) already fully "
                    f"ingested ({total_acts} acts). Skipping download."
                )
                return

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

        # 2. Concurrently fetch and stream each discrete act payload with real-time tqdm progress
        sem = asyncio.Semaphore(DEFAULT_CONCURRENT_SEMAPHORE)
        sec_code = SECTION_CODE_MAP.get(section_name, section_name)
        progress_desc = f"DOU {self.territory_code} {target_date.strftime('%d/%m/%Y')} {sec_code}"

        async with httpx.AsyncClient(
            headers=DEFAULT_BROWSER_HEADERS,
            timeout=DEFAULT_HTTP_TIMEOUT_SECONDS,
            limits=httpx.Limits(
                max_connections=DEFAULT_MAX_CONNECTIONS,
                max_keepalive_connections=DEFAULT_MAX_KEEPALIVE_CONNECTIONS,
            ),
        ) as client:
            with tqdm(
                total=total_acts,
                desc=progress_desc,
                unit="ato",
                bar_format=DEFAULT_TQDM_BAR_FORMAT,
                dynamic_ncols=True,
                leave=True,
                mininterval=DEFAULT_TQDM_MIN_INTERVAL_SECONDS,
            ) as pbar:

                async def _fetch_act(
                    art: dict[str, object],
                ) -> RawNormativeActPayload | None:
                    try:
                        url_title = str(art.get("urlTitle", "")).strip()
                        hierarchy_str = str(art.get("hierarchyStr", "")).strip()
                        title = str(art.get("title", "")).strip()
                        preview = str(art.get("content", "")).strip()
                        art_type_raw = str(art.get("artType", "")).strip()

                        hierarchy_parts = [p.strip() for p in hierarchy_str.split("/") if p.strip()]
                        article_url = (
                            f"{ARTICLE_READ_BASE_URL}{url_title}" if url_title else response.url
                        )

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
                    finally:
                        pbar.update(1)

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

        match = ACT_TYPOLOGY_PATTERN.search(title)
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
