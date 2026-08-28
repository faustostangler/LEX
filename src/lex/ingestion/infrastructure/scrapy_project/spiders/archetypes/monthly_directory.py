"""Monthly / Calendar Directory Gazette Spider Archetype.

Base class for state DOE portals that structure gazettes by calendar paths
or query parameters (year/month/day).
"""

from collections.abc import Generator
from datetime import date
from typing import Any
from urllib.parse import urljoin

from scrapy.http import HtmlResponse, Request, Response

from lex.ingestion.infrastructure.dto import RawGazettePayload
from lex.ingestion.infrastructure.scrapy_project.spiders.base import BaseGazetteSpider


class MonthlyDirectoryGazetteSpider(BaseGazetteSpider):
    """Archetype mixin for calendar/directory driven state gazette portals."""

    directory_url_template: str
    edition_link_xpath: str = "//a[contains(@href, '.pdf')]"

    def start_requests(self) -> Generator[Request, None, None]:
        """Generate directory consultation requests for each date in target date range."""
        for target_date in self.date_range():
            url = self.directory_url_template.format(
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
        """Parse directory HTML page to extract PDF file links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.edition_link_xpath}/@href").getall()

        for link in links:
            full_url = urljoin(response.url, link)
            yield Request(
                url=full_url,
                callback=self.parse_pdf_payload,
                meta={"gazette_date": target_date},
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
            power="executive",
        )
