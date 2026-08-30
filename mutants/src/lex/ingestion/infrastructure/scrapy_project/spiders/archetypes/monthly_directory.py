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


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut: MutantDict = {}  # type: ignore
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut: MutantDict = {}  # type: ignore
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut: MutantDict = {}  # type: ignore


class MonthlyDirectoryGazetteSpider(BaseGazetteSpider):
    """Archetype mixin for calendar/directory driven state gazette portals."""

    directory_url_template: str
    edition_link_xpath: str = "//a[contains(@href, '.pdf')]"

    @_mutmut_mutated(mutants_xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut)
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

    def xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_orig(self) -> Generator[Request, None, None]:
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

    def xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_1(self) -> Generator[Request, None, None]:
        """Generate directory consultation requests for each date in target date range."""
        for target_date in self.date_range():
            url = None
            yield Request(
                url=url,
                callback=self.parse,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_2(self) -> Generator[Request, None, None]:
        """Generate directory consultation requests for each date in target date range."""
        for target_date in self.date_range():
            url = self.directory_url_template.format(
                year=None,
                month=target_date.month,
                day=target_date.day,
            )
            yield Request(
                url=url,
                callback=self.parse,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_3(self) -> Generator[Request, None, None]:
        """Generate directory consultation requests for each date in target date range."""
        for target_date in self.date_range():
            url = self.directory_url_template.format(
                year=target_date.year,
                month=None,
                day=target_date.day,
            )
            yield Request(
                url=url,
                callback=self.parse,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_4(self) -> Generator[Request, None, None]:
        """Generate directory consultation requests for each date in target date range."""
        for target_date in self.date_range():
            url = self.directory_url_template.format(
                year=target_date.year,
                month=target_date.month,
                day=None,
            )
            yield Request(
                url=url,
                callback=self.parse,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_5(self) -> Generator[Request, None, None]:
        """Generate directory consultation requests for each date in target date range."""
        for target_date in self.date_range():
            url = self.directory_url_template.format(
                month=target_date.month,
                day=target_date.day,
            )
            yield Request(
                url=url,
                callback=self.parse,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_6(self) -> Generator[Request, None, None]:
        """Generate directory consultation requests for each date in target date range."""
        for target_date in self.date_range():
            url = self.directory_url_template.format(
                year=target_date.year,
                day=target_date.day,
            )
            yield Request(
                url=url,
                callback=self.parse,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_7(self) -> Generator[Request, None, None]:
        """Generate directory consultation requests for each date in target date range."""
        for target_date in self.date_range():
            url = self.directory_url_template.format(
                year=target_date.year,
                month=target_date.month,
                )
            yield Request(
                url=url,
                callback=self.parse,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_8(self) -> Generator[Request, None, None]:
        """Generate directory consultation requests for each date in target date range."""
        for target_date in self.date_range():
            url = self.directory_url_template.format(
                year=target_date.year,
                month=target_date.month,
                day=target_date.day,
            )
            yield Request(
                url=None,
                callback=self.parse,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_9(self) -> Generator[Request, None, None]:
        """Generate directory consultation requests for each date in target date range."""
        for target_date in self.date_range():
            url = self.directory_url_template.format(
                year=target_date.year,
                month=target_date.month,
                day=target_date.day,
            )
            yield Request(
                url=url,
                callback=None,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_10(self) -> Generator[Request, None, None]:
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
                meta=None,
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_11(self) -> Generator[Request, None, None]:
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
                dont_filter=None,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_12(self) -> Generator[Request, None, None]:
        """Generate directory consultation requests for each date in target date range."""
        for target_date in self.date_range():
            url = self.directory_url_template.format(
                year=target_date.year,
                month=target_date.month,
                day=target_date.day,
            )
            yield Request(
                callback=self.parse,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_13(self) -> Generator[Request, None, None]:
        """Generate directory consultation requests for each date in target date range."""
        for target_date in self.date_range():
            url = self.directory_url_template.format(
                year=target_date.year,
                month=target_date.month,
                day=target_date.day,
            )
            yield Request(
                url=url,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_14(self) -> Generator[Request, None, None]:
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
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_15(self) -> Generator[Request, None, None]:
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
                )

    def xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_16(self) -> Generator[Request, None, None]:
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
                meta={"XXgazette_dateXX": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_17(self) -> Generator[Request, None, None]:
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
                meta={"GAZETTE_DATE": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_18(self) -> Generator[Request, None, None]:
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
                dont_filter=False,
            )

    @_mutmut_mutated(mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut)
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

    def xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_orig(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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

    def xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_1(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse directory HTML page to extract PDF file links."""
        if isinstance(response, HtmlResponse):
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

    def xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_2(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse directory HTML page to extract PDF file links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = None
        links = response.xpath(f"{self.edition_link_xpath}/@href").getall()

        for link in links:
            full_url = urljoin(response.url, link)
            yield Request(
                url=full_url,
                callback=self.parse_pdf_payload,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_3(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse directory HTML page to extract PDF file links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["XXgazette_dateXX"]
        links = response.xpath(f"{self.edition_link_xpath}/@href").getall()

        for link in links:
            full_url = urljoin(response.url, link)
            yield Request(
                url=full_url,
                callback=self.parse_pdf_payload,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_4(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse directory HTML page to extract PDF file links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["GAZETTE_DATE"]
        links = response.xpath(f"{self.edition_link_xpath}/@href").getall()

        for link in links:
            full_url = urljoin(response.url, link)
            yield Request(
                url=full_url,
                callback=self.parse_pdf_payload,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_5(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse directory HTML page to extract PDF file links."""
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

    def xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_6(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse directory HTML page to extract PDF file links."""
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

    def xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_7(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse directory HTML page to extract PDF file links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.edition_link_xpath}/@href").getall()

        for link in links:
            full_url = None
            yield Request(
                url=full_url,
                callback=self.parse_pdf_payload,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_8(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse directory HTML page to extract PDF file links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.edition_link_xpath}/@href").getall()

        for link in links:
            full_url = urljoin(None, link)
            yield Request(
                url=full_url,
                callback=self.parse_pdf_payload,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_9(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse directory HTML page to extract PDF file links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.edition_link_xpath}/@href").getall()

        for link in links:
            full_url = urljoin(response.url, None)
            yield Request(
                url=full_url,
                callback=self.parse_pdf_payload,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_10(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse directory HTML page to extract PDF file links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.edition_link_xpath}/@href").getall()

        for link in links:
            full_url = urljoin(link)
            yield Request(
                url=full_url,
                callback=self.parse_pdf_payload,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_11(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse directory HTML page to extract PDF file links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.edition_link_xpath}/@href").getall()

        for link in links:
            full_url = urljoin(response.url, )
            yield Request(
                url=full_url,
                callback=self.parse_pdf_payload,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_12(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse directory HTML page to extract PDF file links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.edition_link_xpath}/@href").getall()

        for link in links:
            full_url = urljoin(response.url, link)
            yield Request(
                url=None,
                callback=self.parse_pdf_payload,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_13(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse directory HTML page to extract PDF file links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.edition_link_xpath}/@href").getall()

        for link in links:
            full_url = urljoin(response.url, link)
            yield Request(
                url=full_url,
                callback=None,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_14(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                meta=None,
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_15(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                dont_filter=None,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_16(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse directory HTML page to extract PDF file links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.edition_link_xpath}/@href").getall()

        for link in links:
            full_url = urljoin(response.url, link)
            yield Request(
                callback=self.parse_pdf_payload,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_17(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse directory HTML page to extract PDF file links."""
        if not isinstance(response, HtmlResponse):
            return

        target_date: date = response.meta["gazette_date"]
        links = response.xpath(f"{self.edition_link_xpath}/@href").getall()

        for link in links:
            full_url = urljoin(response.url, link)
            yield Request(
                url=full_url,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_18(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_19(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                )

    def xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_20(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                meta={"XXgazette_dateXX": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_21(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                meta={"GAZETTE_DATE": target_date},
                dont_filter=True,
            )

    def xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_22(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                dont_filter=False,
            )

    @_mutmut_mutated(mutants_xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut)
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

    def xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_orig(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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

    def xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_1(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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

    def xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_2(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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

    def xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_3(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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

    def xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_4(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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

    def xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_5(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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

    def xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_6(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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

    def xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_7(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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

    def xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_8(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            power="executive",
        )

    def xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_9(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            power="executive",
        )

    def xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_10(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            power="executive",
        )

    def xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_11(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            date_obj=meta["gazette_date"],
            power="executive",
        )

    def xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_12(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            power="executive",
        )

    def xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_13(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            )

    def xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_14(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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

    def xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_15(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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

    def xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_16(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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

    def xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_17(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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

mutants_xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut['_mutmut_orig'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut['xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_1'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_1 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut['xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_2'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_2 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut['xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_3'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_3 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut['xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_4'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_4 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut['xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_5'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_5 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut['xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_6'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_6 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut['xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_7'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_7 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut['xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_8'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_8 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut['xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_9'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_9 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut['xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_10'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_10 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut['xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_11'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_11 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut['xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_12'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_12 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut['xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_13'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_13 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut['xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_14'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_14 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut['xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_15'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_15 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut['xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_16'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_16 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut['xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_17'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_17 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut['xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_18'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁstart_requests__mutmut_18 # type: ignore # mutmut generated

mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut['_mutmut_orig'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_1'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_1 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_2'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_2 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_3'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_3 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_4'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_4 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_5'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_5 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_6'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_6 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_7'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_7 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_8'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_8 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_9'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_9 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_10'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_10 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_11'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_11 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_12'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_12 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_13'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_13 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_14'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_14 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_15'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_15 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_16'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_16 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_17'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_17 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_18'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_18 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_19'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_19 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_20'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_20 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_21'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_21 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_22'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse__mutmut_22 # type: ignore # mutmut generated

mutants_xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut['_mutmut_orig'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_1'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_1 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_2'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_2 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_3'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_3 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_4'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_4 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_5'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_5 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_6'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_6 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_7'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_7 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_8'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_8 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_9'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_9 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_10'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_10 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_11'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_11 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_12'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_12 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_13'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_13 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_14'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_14 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_15'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_15 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_16'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_16 # type: ignore # mutmut generated
mutants_xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut['xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_17'] = MonthlyDirectoryGazetteSpider.xǁMonthlyDirectoryGazetteSpiderǁparse_pdf_payload__mutmut_17 # type: ignore # mutmut generated
