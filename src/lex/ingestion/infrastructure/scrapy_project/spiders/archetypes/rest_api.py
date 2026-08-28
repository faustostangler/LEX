"""REST API Gazette Spider Archetype.

Base class for modern state DOE portals that provide structured JSON endpoints
for edition discovery and PDF file retrieval.
"""

import json
from collections.abc import Generator
from datetime import date
from typing import Any
from urllib.parse import urljoin

from scrapy.http import Request, Response, TextResponse

from lex.ingestion.infrastructure.dto import RawGazettePayload
from lex.ingestion.infrastructure.scrapy_project.spiders.base import BaseGazetteSpider


class RestApiGazetteSpider(BaseGazetteSpider):
    """Archetype mixin for REST API driven state gazette portals."""

    api_endpoint_template: str
    json_pdf_url_key: str = "url"
    json_edition_key: str = "edition_number"
    json_section_key: str = "section"
    json_is_extra_key: str | None = None

    def start_requests(self) -> Generator[Request, None, None]:
        """Generate API requests for each date in target date range."""
        for target_date in self.date_range():
            iso_date = target_date.strftime("%Y-%m-%d")
            br_date = target_date.strftime("%d/%m/%Y")
            url = self.api_endpoint_template.format(
                iso_date=iso_date,
                br_date=br_date,
                year=target_date.year,
                month=target_date.month,
                day=target_date.day,
            )
            yield Request(
                url=url,
                callback=self.parse,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def parse(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse JSON response and dispatch PDF download requests."""
        if not isinstance(response, TextResponse):
            return

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            return

        items = data if isinstance(data, list) else data.get("items", [data])
        target_date: date = response.meta["gazette_date"]

        for item in items:
            if not isinstance(item, dict):
                continue

            pdf_url = item.get(self.json_pdf_url_key)
            if not pdf_url:
                continue

            full_pdf_url = urljoin(response.url, pdf_url)
            edition_number = str(item.get(self.json_edition_key, "")) or None
            section = str(item.get(self.json_section_key, "")) or None
            is_extra = (
                bool(item.get(self.json_is_extra_key, False)) if self.json_is_extra_key else False
            )

            yield Request(
                url=full_pdf_url,
                callback=self.parse_pdf_payload,
                meta={
                    "gazette_date": target_date,
                    "edition_number": edition_number,
                    "section": section,
                    "is_extra_edition": is_extra,
                },
                dont_filter=True,
            )

    def parse_pdf_payload(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            edition_number=meta.get("edition_number"),
            section=meta.get("section"),
            is_extra_edition=meta.get("is_extra_edition", False),
            power="executive",
        )
