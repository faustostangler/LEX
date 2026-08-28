"""ASPX WebForms Gazette Spider Archetype.

Base class for state DOE portals implemented with legacy ASP.NET WebForms
requiring ViewState extraction and form postbacks.
"""

from collections.abc import Generator
from datetime import date
from typing import Any
from urllib.parse import urljoin

from scrapy.http import FormRequest, HtmlResponse, Request, Response

from lex.ingestion.infrastructure.dto import RawGazettePayload
from lex.ingestion.infrastructure.scrapy_project.spiders.base import BaseGazetteSpider


class AspxViewerGazetteSpider(BaseGazetteSpider):
    """Archetype mixin for ASP.NET WebForms state gazette portals."""

    form_url: str
    pdf_link_xpath: str = "//a[contains(@href, '.pdf') or contains(@href, 'Download')]"

    def start_requests(self) -> Generator[Request, None, None]:
        """Initiate session by fetching initial WebForms page with ViewState tokens."""
        for target_date in self.date_range():
            yield Request(
                url=self.form_url,
                callback=self.parse,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def parse(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Extract links or postback form with target date."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.pdf_link_xpath}/@href").getall()

        if links:
            for link in links:
                full_url = urljoin(response.url, link)
                yield Request(
                    url=full_url,
                    callback=self.parse_pdf_payload,
                    meta={"gazette_date": target_date},
                    dont_filter=True,
                )
        else:
            # If no direct links, perform WebForms postback with date
            viewstate = response.xpath("//input[@id='__VIEWSTATE']/@value").get() or ""
            event_validation = response.xpath("//input[@id='__EVENTVALIDATION']/@value").get() or ""

            formdata = {
                "__VIEWSTATE": viewstate,
                "__EVENTVALIDATION": event_validation,
                "txtData": target_date.strftime("%d/%m/%Y"),
                "btnConsultar": "Consultar",
            }
            yield FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.parse_postback_results,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def parse_postback_results(self, response: Response) -> Generator[Request, None, None]:
        """Parse postback response HTML and dispatch PDF links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.pdf_link_xpath}/@href").getall()

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
