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


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁAspxViewerGazetteSpiderǁstart_requests__mutmut: MutantDict = {}  # type: ignore
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut: MutantDict = {}  # type: ignore
mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut: MutantDict = {}  # type: ignore
mutants_xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut: MutantDict = {}  # type: ignore


class AspxViewerGazetteSpider(BaseGazetteSpider):
    """Archetype mixin for ASP.NET WebForms state gazette portals."""

    form_url: str
    pdf_link_xpath: str = "//a[contains(@href, '.pdf') or contains(@href, 'Download')]"

    @_mutmut_mutated(mutants_xǁAspxViewerGazetteSpiderǁstart_requests__mutmut)
    def start_requests(self) -> Generator[Request, None, None]:
        """Initiate session by fetching initial WebForms page with ViewState tokens."""
        for target_date in self.date_range():
            yield Request(
                url=self.form_url,
                callback=self.parse,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_orig(self) -> Generator[Request, None, None]:
        """Initiate session by fetching initial WebForms page with ViewState tokens."""
        for target_date in self.date_range():
            yield Request(
                url=self.form_url,
                callback=self.parse,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_1(self) -> Generator[Request, None, None]:
        """Initiate session by fetching initial WebForms page with ViewState tokens."""
        for target_date in self.date_range():
            yield Request(
                url=None,
                callback=self.parse,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_2(self) -> Generator[Request, None, None]:
        """Initiate session by fetching initial WebForms page with ViewState tokens."""
        for target_date in self.date_range():
            yield Request(
                url=self.form_url,
                callback=None,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_3(self) -> Generator[Request, None, None]:
        """Initiate session by fetching initial WebForms page with ViewState tokens."""
        for target_date in self.date_range():
            yield Request(
                url=self.form_url,
                callback=self.parse,
                meta=None,
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_4(self) -> Generator[Request, None, None]:
        """Initiate session by fetching initial WebForms page with ViewState tokens."""
        for target_date in self.date_range():
            yield Request(
                url=self.form_url,
                callback=self.parse,
                meta={"gazette_date": target_date},
                dont_filter=None,
            )

    def xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_5(self) -> Generator[Request, None, None]:
        """Initiate session by fetching initial WebForms page with ViewState tokens."""
        for target_date in self.date_range():
            yield Request(
                callback=self.parse,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_6(self) -> Generator[Request, None, None]:
        """Initiate session by fetching initial WebForms page with ViewState tokens."""
        for target_date in self.date_range():
            yield Request(
                url=self.form_url,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_7(self) -> Generator[Request, None, None]:
        """Initiate session by fetching initial WebForms page with ViewState tokens."""
        for target_date in self.date_range():
            yield Request(
                url=self.form_url,
                callback=self.parse,
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_8(self) -> Generator[Request, None, None]:
        """Initiate session by fetching initial WebForms page with ViewState tokens."""
        for target_date in self.date_range():
            yield Request(
                url=self.form_url,
                callback=self.parse,
                meta={"gazette_date": target_date},
                )

    def xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_9(self) -> Generator[Request, None, None]:
        """Initiate session by fetching initial WebForms page with ViewState tokens."""
        for target_date in self.date_range():
            yield Request(
                url=self.form_url,
                callback=self.parse,
                meta={"XXgazette_dateXX": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_10(self) -> Generator[Request, None, None]:
        """Initiate session by fetching initial WebForms page with ViewState tokens."""
        for target_date in self.date_range():
            yield Request(
                url=self.form_url,
                callback=self.parse,
                meta={"GAZETTE_DATE": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_11(self) -> Generator[Request, None, None]:
        """Initiate session by fetching initial WebForms page with ViewState tokens."""
        for target_date in self.date_range():
            yield Request(
                url=self.form_url,
                callback=self.parse,
                meta={"gazette_date": target_date},
                dont_filter=False,
            )

    @_mutmut_mutated(mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut)
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_orig(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_1(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Extract links or postback form with target date."""
        if isinstance(response, HtmlResponse):
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_2(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Extract links or postback form with target date."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = None
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_3(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Extract links or postback form with target date."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["XXgazette_dateXX"]
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_4(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Extract links or postback form with target date."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["GAZETTE_DATE"]
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_5(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Extract links or postback form with target date."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = None

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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_6(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Extract links or postback form with target date."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(None).getall()

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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_7(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Extract links or postback form with target date."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.pdf_link_xpath}/@href").getall()

        if links:
            for link in links:
                full_url = None
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_8(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Extract links or postback form with target date."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.pdf_link_xpath}/@href").getall()

        if links:
            for link in links:
                full_url = urljoin(None, link)
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_9(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Extract links or postback form with target date."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.pdf_link_xpath}/@href").getall()

        if links:
            for link in links:
                full_url = urljoin(response.url, None)
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_10(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Extract links or postback form with target date."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.pdf_link_xpath}/@href").getall()

        if links:
            for link in links:
                full_url = urljoin(link)
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_11(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Extract links or postback form with target date."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.pdf_link_xpath}/@href").getall()

        if links:
            for link in links:
                full_url = urljoin(response.url, )
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_12(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Extract links or postback form with target date."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.pdf_link_xpath}/@href").getall()

        if links:
            for link in links:
                full_url = urljoin(response.url, link)
                yield Request(
                    url=None,
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_13(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                    callback=None,
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_14(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                    meta=None,
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_15(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                    dont_filter=None,
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_16(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Extract links or postback form with target date."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.pdf_link_xpath}/@href").getall()

        if links:
            for link in links:
                full_url = urljoin(response.url, link)
                yield Request(
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_17(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_18(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_19(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_20(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                    meta={"XXgazette_dateXX": target_date},
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_21(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                    meta={"GAZETTE_DATE": target_date},
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_22(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                    dont_filter=False,
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_23(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            viewstate = None
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_24(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            viewstate = response.xpath("//input[@id='__VIEWSTATE']/@value").get() and ""
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_25(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            viewstate = response.xpath(None).get() or ""
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_26(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            viewstate = response.xpath("XX//input[@id='__VIEWSTATE']/@valueXX").get() or ""
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_27(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            viewstate = response.xpath("//input[@id='__viewstate']/@value").get() or ""
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_28(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            viewstate = response.xpath("//INPUT[@ID='__VIEWSTATE']/@VALUE").get() or ""
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_29(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            viewstate = response.xpath("//input[@id='__VIEWSTATE']/@value").get() or "XXXX"
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_30(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            event_validation = None

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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_31(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            event_validation = response.xpath("//input[@id='__EVENTVALIDATION']/@value").get() and ""

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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_32(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            event_validation = response.xpath(None).get() or ""

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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_33(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            event_validation = response.xpath("XX//input[@id='__EVENTVALIDATION']/@valueXX").get() or ""

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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_34(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            event_validation = response.xpath("//input[@id='__eventvalidation']/@value").get() or ""

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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_35(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            event_validation = response.xpath("//INPUT[@ID='__EVENTVALIDATION']/@VALUE").get() or ""

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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_36(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            event_validation = response.xpath("//input[@id='__EVENTVALIDATION']/@value").get() or "XXXX"

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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_37(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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

            formdata = None
            yield FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.parse_postback_results,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_38(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                "XX__VIEWSTATEXX": viewstate,
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_39(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                "__viewstate": viewstate,
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_40(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                "XX__EVENTVALIDATIONXX": event_validation,
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_41(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                "__eventvalidation": event_validation,
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

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_42(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                "XXtxtDataXX": target_date.strftime("%d/%m/%Y"),
                "btnConsultar": "Consultar",
            }
            yield FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.parse_postback_results,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_43(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                "txtdata": target_date.strftime("%d/%m/%Y"),
                "btnConsultar": "Consultar",
            }
            yield FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.parse_postback_results,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_44(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                "TXTDATA": target_date.strftime("%d/%m/%Y"),
                "btnConsultar": "Consultar",
            }
            yield FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.parse_postback_results,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_45(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                "txtData": target_date.strftime(None),
                "btnConsultar": "Consultar",
            }
            yield FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.parse_postback_results,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_46(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                "txtData": target_date.strftime("XX%d/%m/%YXX"),
                "btnConsultar": "Consultar",
            }
            yield FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.parse_postback_results,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_47(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                "txtData": target_date.strftime("%d/%m/%y"),
                "btnConsultar": "Consultar",
            }
            yield FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.parse_postback_results,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_48(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                "txtData": target_date.strftime("%D/%M/%Y"),
                "btnConsultar": "Consultar",
            }
            yield FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.parse_postback_results,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_49(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                "XXbtnConsultarXX": "Consultar",
            }
            yield FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.parse_postback_results,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_50(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                "btnconsultar": "Consultar",
            }
            yield FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.parse_postback_results,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_51(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                "BTNCONSULTAR": "Consultar",
            }
            yield FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.parse_postback_results,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_52(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                "btnConsultar": "XXConsultarXX",
            }
            yield FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.parse_postback_results,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_53(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                "btnConsultar": "consultar",
            }
            yield FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.parse_postback_results,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_54(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                "btnConsultar": "CONSULTAR",
            }
            yield FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.parse_postback_results,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_55(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                None,
                formdata=formdata,
                callback=self.parse_postback_results,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_56(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                formdata=None,
                callback=self.parse_postback_results,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_57(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                callback=None,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_58(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                meta=None,
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_59(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                dont_filter=None,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_60(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                formdata=formdata,
                callback=self.parse_postback_results,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_61(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                callback=self.parse_postback_results,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_62(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_63(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_64(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_65(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                meta={"XXgazette_dateXX": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_66(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                meta={"GAZETTE_DATE": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse__mutmut_67(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                dont_filter=False,
            )

    @_mutmut_mutated(mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut)
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

    def xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_orig(self, response: Response) -> Generator[Request, None, None]:
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

    def xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_1(self, response: Response) -> Generator[Request, None, None]:
        """Parse postback response HTML and dispatch PDF links."""
        if isinstance(response, HtmlResponse):
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

    def xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_2(self, response: Response) -> Generator[Request, None, None]:
        """Parse postback response HTML and dispatch PDF links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = None
        links = response.xpath(f"{self.pdf_link_xpath}/@href").getall()

        for link in links:
            full_url = urljoin(response.url, link)
            yield Request(
                url=full_url,
                callback=self.parse_pdf_payload,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_3(self, response: Response) -> Generator[Request, None, None]:
        """Parse postback response HTML and dispatch PDF links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["XXgazette_dateXX"]
        links = response.xpath(f"{self.pdf_link_xpath}/@href").getall()

        for link in links:
            full_url = urljoin(response.url, link)
            yield Request(
                url=full_url,
                callback=self.parse_pdf_payload,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_4(self, response: Response) -> Generator[Request, None, None]:
        """Parse postback response HTML and dispatch PDF links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["GAZETTE_DATE"]
        links = response.xpath(f"{self.pdf_link_xpath}/@href").getall()

        for link in links:
            full_url = urljoin(response.url, link)
            yield Request(
                url=full_url,
                callback=self.parse_pdf_payload,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_5(self, response: Response) -> Generator[Request, None, None]:
        """Parse postback response HTML and dispatch PDF links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = None

        for link in links:
            full_url = urljoin(response.url, link)
            yield Request(
                url=full_url,
                callback=self.parse_pdf_payload,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_6(self, response: Response) -> Generator[Request, None, None]:
        """Parse postback response HTML and dispatch PDF links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(None).getall()

        for link in links:
            full_url = urljoin(response.url, link)
            yield Request(
                url=full_url,
                callback=self.parse_pdf_payload,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_7(self, response: Response) -> Generator[Request, None, None]:
        """Parse postback response HTML and dispatch PDF links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.pdf_link_xpath}/@href").getall()

        for link in links:
            full_url = None
            yield Request(
                url=full_url,
                callback=self.parse_pdf_payload,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_8(self, response: Response) -> Generator[Request, None, None]:
        """Parse postback response HTML and dispatch PDF links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.pdf_link_xpath}/@href").getall()

        for link in links:
            full_url = urljoin(None, link)
            yield Request(
                url=full_url,
                callback=self.parse_pdf_payload,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_9(self, response: Response) -> Generator[Request, None, None]:
        """Parse postback response HTML and dispatch PDF links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.pdf_link_xpath}/@href").getall()

        for link in links:
            full_url = urljoin(response.url, None)
            yield Request(
                url=full_url,
                callback=self.parse_pdf_payload,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_10(self, response: Response) -> Generator[Request, None, None]:
        """Parse postback response HTML and dispatch PDF links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.pdf_link_xpath}/@href").getall()

        for link in links:
            full_url = urljoin(link)
            yield Request(
                url=full_url,
                callback=self.parse_pdf_payload,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_11(self, response: Response) -> Generator[Request, None, None]:
        """Parse postback response HTML and dispatch PDF links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.pdf_link_xpath}/@href").getall()

        for link in links:
            full_url = urljoin(response.url, )
            yield Request(
                url=full_url,
                callback=self.parse_pdf_payload,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_12(self, response: Response) -> Generator[Request, None, None]:
        """Parse postback response HTML and dispatch PDF links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.pdf_link_xpath}/@href").getall()

        for link in links:
            full_url = urljoin(response.url, link)
            yield Request(
                url=None,
                callback=self.parse_pdf_payload,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_13(self, response: Response) -> Generator[Request, None, None]:
        """Parse postback response HTML and dispatch PDF links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.pdf_link_xpath}/@href").getall()

        for link in links:
            full_url = urljoin(response.url, link)
            yield Request(
                url=full_url,
                callback=None,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_14(self, response: Response) -> Generator[Request, None, None]:
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
                meta=None,
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_15(self, response: Response) -> Generator[Request, None, None]:
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
                dont_filter=None,
            )

    def xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_16(self, response: Response) -> Generator[Request, None, None]:
        """Parse postback response HTML and dispatch PDF links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.pdf_link_xpath}/@href").getall()

        for link in links:
            full_url = urljoin(response.url, link)
            yield Request(
                callback=self.parse_pdf_payload,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_17(self, response: Response) -> Generator[Request, None, None]:
        """Parse postback response HTML and dispatch PDF links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.pdf_link_xpath}/@href").getall()

        for link in links:
            full_url = urljoin(response.url, link)
            yield Request(
                url=full_url,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_18(self, response: Response) -> Generator[Request, None, None]:
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
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_19(self, response: Response) -> Generator[Request, None, None]:
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
                )

    def xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_20(self, response: Response) -> Generator[Request, None, None]:
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
                meta={"XXgazette_dateXX": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_21(self, response: Response) -> Generator[Request, None, None]:
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
                meta={"GAZETTE_DATE": target_date},
                dont_filter=True,
            )

    def xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_22(self, response: Response) -> Generator[Request, None, None]:
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
                dont_filter=False,
            )

    @_mutmut_mutated(mutants_xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut)
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

    def xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_orig(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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

    def xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_1(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = None
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            power="executive",
        )

    def xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_2(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=None,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            power="executive",
        )

    def xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_3(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=None,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            power="executive",
        )

    def xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_4(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=None,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            power="executive",
        )

    def xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_5(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=None,
            date_obj=meta["gazette_date"],
            power="executive",
        )

    def xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_6(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=None,
            power="executive",
        )

    def xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_7(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            power=None,
        )

    def xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_8(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            power="executive",
        )

    def xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_9(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            power="executive",
        )

    def xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_10(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            power="executive",
        )

    def xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_11(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            date_obj=meta["gazette_date"],
            power="executive",
        )

    def xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_12(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            power="executive",
        )

    def xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_13(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            )

    def xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_14(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["XXgazette_dateXX"],
            power="executive",
        )

    def xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_15(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["GAZETTE_DATE"],
            power="executive",
        )

    def xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_16(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            power="XXexecutiveXX",
        )

    def xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_17(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            power="EXECUTIVE",
        )

mutants_xǁAspxViewerGazetteSpiderǁstart_requests__mutmut['_mutmut_orig'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_orig # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁstart_requests__mutmut['xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_1'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_1 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁstart_requests__mutmut['xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_2'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_2 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁstart_requests__mutmut['xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_3'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_3 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁstart_requests__mutmut['xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_4'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_4 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁstart_requests__mutmut['xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_5'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_5 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁstart_requests__mutmut['xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_6'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_6 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁstart_requests__mutmut['xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_7'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_7 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁstart_requests__mutmut['xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_8'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_8 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁstart_requests__mutmut['xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_9'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_9 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁstart_requests__mutmut['xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_10'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_10 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁstart_requests__mutmut['xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_11'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁstart_requests__mutmut_11 # type: ignore # mutmut generated

mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['_mutmut_orig'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_orig # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_1'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_1 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_2'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_2 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_3'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_3 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_4'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_4 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_5'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_5 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_6'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_6 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_7'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_7 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_8'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_8 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_9'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_9 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_10'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_10 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_11'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_11 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_12'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_12 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_13'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_13 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_14'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_14 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_15'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_15 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_16'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_16 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_17'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_17 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_18'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_18 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_19'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_19 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_20'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_20 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_21'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_21 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_22'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_22 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_23'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_23 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_24'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_24 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_25'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_25 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_26'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_26 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_27'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_27 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_28'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_28 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_29'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_29 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_30'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_30 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_31'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_31 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_32'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_32 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_33'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_33 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_34'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_34 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_35'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_35 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_36'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_36 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_37'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_37 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_38'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_38 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_39'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_39 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_40'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_40 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_41'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_41 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_42'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_42 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_43'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_43 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_44'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_44 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_45'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_45 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_46'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_46 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_47'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_47 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_48'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_48 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_49'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_49 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_50'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_50 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_51'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_51 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_52'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_52 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_53'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_53 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_54'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_54 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_55'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_55 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_56'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_56 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_57'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_57 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_58'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_58 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_59'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_59 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_60'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_60 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_61'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_61 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_62'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_62 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_63'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_63 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_64'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_64 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_65'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_65 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_66'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_66 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse__mutmut['xǁAspxViewerGazetteSpiderǁparse__mutmut_67'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse__mutmut_67 # type: ignore # mutmut generated

mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut['_mutmut_orig'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_orig # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut['xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_1'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_1 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut['xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_2'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_2 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut['xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_3'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_3 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut['xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_4'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_4 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut['xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_5'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_5 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut['xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_6'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_6 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut['xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_7'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_7 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut['xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_8'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_8 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut['xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_9'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_9 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut['xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_10'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_10 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut['xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_11'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_11 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut['xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_12'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_12 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut['xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_13'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_13 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut['xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_14'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_14 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut['xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_15'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_15 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut['xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_16'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_16 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut['xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_17'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_17 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut['xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_18'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_18 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut['xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_19'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_19 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut['xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_20'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_20 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut['xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_21'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_21 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut['xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_22'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_postback_results__mutmut_22 # type: ignore # mutmut generated

mutants_xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut['_mutmut_orig'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_orig # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut['xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_1'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_1 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut['xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_2'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_2 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut['xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_3'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_3 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut['xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_4'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_4 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut['xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_5'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_5 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut['xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_6'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_6 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut['xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_7'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_7 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut['xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_8'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_8 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut['xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_9'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_9 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut['xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_10'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_10 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut['xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_11'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_11 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut['xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_12'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_12 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut['xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_13'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_13 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut['xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_14'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_14 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut['xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_15'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_15 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut['xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_16'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_16 # type: ignore # mutmut generated
mutants_xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut['xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_17'] = AspxViewerGazetteSpider.xǁAspxViewerGazetteSpiderǁparse_pdf_payload__mutmut_17 # type: ignore # mutmut generated
