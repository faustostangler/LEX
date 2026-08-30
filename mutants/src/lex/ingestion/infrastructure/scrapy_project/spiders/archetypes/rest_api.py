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


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut: MutantDict = {}  # type: ignore
mutants_xǁRestApiGazetteSpiderǁparse__mutmut: MutantDict = {}  # type: ignore
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut: MutantDict = {}  # type: ignore


class RestApiGazetteSpider(BaseGazetteSpider):
    """Archetype mixin for REST API driven state gazette portals."""

    api_endpoint_template: str
    json_pdf_url_key: str = "url"
    json_edition_key: str = "edition_number"
    json_section_key: str = "section"
    json_is_extra_key: str | None = None

    @_mutmut_mutated(mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut)
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

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_orig(self) -> Generator[Request, None, None]:
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

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_1(self) -> Generator[Request, None, None]:
        """Generate API requests for each date in target date range."""
        for target_date in self.date_range():
            iso_date = None
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

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_2(self) -> Generator[Request, None, None]:
        """Generate API requests for each date in target date range."""
        for target_date in self.date_range():
            iso_date = target_date.strftime(None)
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

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_3(self) -> Generator[Request, None, None]:
        """Generate API requests for each date in target date range."""
        for target_date in self.date_range():
            iso_date = target_date.strftime("XX%Y-%m-%dXX")
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

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_4(self) -> Generator[Request, None, None]:
        """Generate API requests for each date in target date range."""
        for target_date in self.date_range():
            iso_date = target_date.strftime("%y-%m-%d")
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

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_5(self) -> Generator[Request, None, None]:
        """Generate API requests for each date in target date range."""
        for target_date in self.date_range():
            iso_date = target_date.strftime("%Y-%M-%D")
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

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_6(self) -> Generator[Request, None, None]:
        """Generate API requests for each date in target date range."""
        for target_date in self.date_range():
            iso_date = target_date.strftime("%Y-%m-%d")
            br_date = None
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

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_7(self) -> Generator[Request, None, None]:
        """Generate API requests for each date in target date range."""
        for target_date in self.date_range():
            iso_date = target_date.strftime("%Y-%m-%d")
            br_date = target_date.strftime(None)
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

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_8(self) -> Generator[Request, None, None]:
        """Generate API requests for each date in target date range."""
        for target_date in self.date_range():
            iso_date = target_date.strftime("%Y-%m-%d")
            br_date = target_date.strftime("XX%d/%m/%YXX")
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

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_9(self) -> Generator[Request, None, None]:
        """Generate API requests for each date in target date range."""
        for target_date in self.date_range():
            iso_date = target_date.strftime("%Y-%m-%d")
            br_date = target_date.strftime("%d/%m/%y")
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

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_10(self) -> Generator[Request, None, None]:
        """Generate API requests for each date in target date range."""
        for target_date in self.date_range():
            iso_date = target_date.strftime("%Y-%m-%d")
            br_date = target_date.strftime("%D/%M/%Y")
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

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_11(self) -> Generator[Request, None, None]:
        """Generate API requests for each date in target date range."""
        for target_date in self.date_range():
            iso_date = target_date.strftime("%Y-%m-%d")
            br_date = target_date.strftime("%d/%m/%Y")
            url = None
            yield Request(
                url=url,
                callback=self.parse,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_12(self) -> Generator[Request, None, None]:
        """Generate API requests for each date in target date range."""
        for target_date in self.date_range():
            iso_date = target_date.strftime("%Y-%m-%d")
            br_date = target_date.strftime("%d/%m/%Y")
            url = self.api_endpoint_template.format(
                iso_date=None,
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

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_13(self) -> Generator[Request, None, None]:
        """Generate API requests for each date in target date range."""
        for target_date in self.date_range():
            iso_date = target_date.strftime("%Y-%m-%d")
            br_date = target_date.strftime("%d/%m/%Y")
            url = self.api_endpoint_template.format(
                iso_date=iso_date,
                br_date=None,
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

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_14(self) -> Generator[Request, None, None]:
        """Generate API requests for each date in target date range."""
        for target_date in self.date_range():
            iso_date = target_date.strftime("%Y-%m-%d")
            br_date = target_date.strftime("%d/%m/%Y")
            url = self.api_endpoint_template.format(
                iso_date=iso_date,
                br_date=br_date,
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

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_15(self) -> Generator[Request, None, None]:
        """Generate API requests for each date in target date range."""
        for target_date in self.date_range():
            iso_date = target_date.strftime("%Y-%m-%d")
            br_date = target_date.strftime("%d/%m/%Y")
            url = self.api_endpoint_template.format(
                iso_date=iso_date,
                br_date=br_date,
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

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_16(self) -> Generator[Request, None, None]:
        """Generate API requests for each date in target date range."""
        for target_date in self.date_range():
            iso_date = target_date.strftime("%Y-%m-%d")
            br_date = target_date.strftime("%d/%m/%Y")
            url = self.api_endpoint_template.format(
                iso_date=iso_date,
                br_date=br_date,
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

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_17(self) -> Generator[Request, None, None]:
        """Generate API requests for each date in target date range."""
        for target_date in self.date_range():
            iso_date = target_date.strftime("%Y-%m-%d")
            br_date = target_date.strftime("%d/%m/%Y")
            url = self.api_endpoint_template.format(
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

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_18(self) -> Generator[Request, None, None]:
        """Generate API requests for each date in target date range."""
        for target_date in self.date_range():
            iso_date = target_date.strftime("%Y-%m-%d")
            br_date = target_date.strftime("%d/%m/%Y")
            url = self.api_endpoint_template.format(
                iso_date=iso_date,
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

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_19(self) -> Generator[Request, None, None]:
        """Generate API requests for each date in target date range."""
        for target_date in self.date_range():
            iso_date = target_date.strftime("%Y-%m-%d")
            br_date = target_date.strftime("%d/%m/%Y")
            url = self.api_endpoint_template.format(
                iso_date=iso_date,
                br_date=br_date,
                month=target_date.month,
                day=target_date.day,
            )
            yield Request(
                url=url,
                callback=self.parse,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_20(self) -> Generator[Request, None, None]:
        """Generate API requests for each date in target date range."""
        for target_date in self.date_range():
            iso_date = target_date.strftime("%Y-%m-%d")
            br_date = target_date.strftime("%d/%m/%Y")
            url = self.api_endpoint_template.format(
                iso_date=iso_date,
                br_date=br_date,
                year=target_date.year,
                day=target_date.day,
            )
            yield Request(
                url=url,
                callback=self.parse,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_21(self) -> Generator[Request, None, None]:
        """Generate API requests for each date in target date range."""
        for target_date in self.date_range():
            iso_date = target_date.strftime("%Y-%m-%d")
            br_date = target_date.strftime("%d/%m/%Y")
            url = self.api_endpoint_template.format(
                iso_date=iso_date,
                br_date=br_date,
                year=target_date.year,
                month=target_date.month,
                )
            yield Request(
                url=url,
                callback=self.parse,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_22(self) -> Generator[Request, None, None]:
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
                url=None,
                callback=self.parse,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_23(self) -> Generator[Request, None, None]:
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
                callback=None,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_24(self) -> Generator[Request, None, None]:
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
                meta=None,
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_25(self) -> Generator[Request, None, None]:
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
                dont_filter=None,
            )

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_26(self) -> Generator[Request, None, None]:
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
                callback=self.parse,
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_27(self) -> Generator[Request, None, None]:
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
                meta={"gazette_date": target_date},
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_28(self) -> Generator[Request, None, None]:
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
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_29(self) -> Generator[Request, None, None]:
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
                )

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_30(self) -> Generator[Request, None, None]:
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
                meta={"XXgazette_dateXX": target_date},
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_31(self) -> Generator[Request, None, None]:
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
                meta={"GAZETTE_DATE": target_date},
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁstart_requests__mutmut_32(self) -> Generator[Request, None, None]:
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
                dont_filter=False,
            )

    @_mutmut_mutated(mutants_xǁRestApiGazetteSpiderǁparse__mutmut)
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_orig(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_1(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse JSON response and dispatch PDF download requests."""
        if isinstance(response, TextResponse):
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_2(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse JSON response and dispatch PDF download requests."""
        if not isinstance(response, TextResponse):
            return

        try:
            data = None
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_3(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse JSON response and dispatch PDF download requests."""
        if not isinstance(response, TextResponse):
            return

        try:
            data = json.loads(None)
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_4(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse JSON response and dispatch PDF download requests."""
        if not isinstance(response, TextResponse):
            return

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            return

        items = None
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_5(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse JSON response and dispatch PDF download requests."""
        if not isinstance(response, TextResponse):
            return

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            return

        items = data if isinstance(data, list) else data.get(None, [data])
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_6(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse JSON response and dispatch PDF download requests."""
        if not isinstance(response, TextResponse):
            return

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            return

        items = data if isinstance(data, list) else data.get("items", None)
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_7(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse JSON response and dispatch PDF download requests."""
        if not isinstance(response, TextResponse):
            return

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            return

        items = data if isinstance(data, list) else data.get([data])
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_8(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse JSON response and dispatch PDF download requests."""
        if not isinstance(response, TextResponse):
            return

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            return

        items = data if isinstance(data, list) else data.get("items", )
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_9(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse JSON response and dispatch PDF download requests."""
        if not isinstance(response, TextResponse):
            return

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            return

        items = data if isinstance(data, list) else data.get("XXitemsXX", [data])
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_10(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse JSON response and dispatch PDF download requests."""
        if not isinstance(response, TextResponse):
            return

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            return

        items = data if isinstance(data, list) else data.get("ITEMS", [data])
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_11(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse JSON response and dispatch PDF download requests."""
        if not isinstance(response, TextResponse):
            return

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            return

        items = data if isinstance(data, list) else data.get("items", [data])
        target_date: date = None

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

    def xǁRestApiGazetteSpiderǁparse__mutmut_12(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse JSON response and dispatch PDF download requests."""
        if not isinstance(response, TextResponse):
            return

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            return

        items = data if isinstance(data, list) else data.get("items", [data])
        target_date: date = response.meta["XXgazette_dateXX"]

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

    def xǁRestApiGazetteSpiderǁparse__mutmut_13(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
        """Parse JSON response and dispatch PDF download requests."""
        if not isinstance(response, TextResponse):
            return

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            return

        items = data if isinstance(data, list) else data.get("items", [data])
        target_date: date = response.meta["GAZETTE_DATE"]

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

    def xǁRestApiGazetteSpiderǁparse__mutmut_14(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            if isinstance(item, dict):
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_15(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                break

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

    def xǁRestApiGazetteSpiderǁparse__mutmut_16(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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

            pdf_url = None
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_17(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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

            pdf_url = item.get(None)
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_18(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            if pdf_url:
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_19(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                break

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

    def xǁRestApiGazetteSpiderǁparse__mutmut_20(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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

            full_pdf_url = None
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_21(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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

            full_pdf_url = urljoin(None, pdf_url)
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_22(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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

            full_pdf_url = urljoin(response.url, None)
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_23(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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

            full_pdf_url = urljoin(pdf_url)
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_24(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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

            full_pdf_url = urljoin(response.url, )
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_25(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            edition_number = None
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_26(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            edition_number = str(item.get(self.json_edition_key, "")) and None
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_27(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            edition_number = str(None) or None
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_28(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            edition_number = str(item.get(None, "")) or None
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_29(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            edition_number = str(item.get(self.json_edition_key, None)) or None
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_30(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            edition_number = str(item.get("")) or None
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_31(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            edition_number = str(item.get(self.json_edition_key, )) or None
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_32(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            edition_number = str(item.get(self.json_edition_key, "XXXX")) or None
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_33(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            section = None
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_34(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            section = str(item.get(self.json_section_key, "")) and None
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_35(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            section = str(None) or None
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_36(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            section = str(item.get(None, "")) or None
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_37(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            section = str(item.get(self.json_section_key, None)) or None
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_38(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            section = str(item.get("")) or None
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_39(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            section = str(item.get(self.json_section_key, )) or None
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_40(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            section = str(item.get(self.json_section_key, "XXXX")) or None
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_41(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
            is_extra = None

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

    def xǁRestApiGazetteSpiderǁparse__mutmut_42(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                bool(None) if self.json_is_extra_key else False
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_43(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                bool(item.get(None, False)) if self.json_is_extra_key else False
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_44(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                bool(item.get(self.json_is_extra_key, None)) if self.json_is_extra_key else False
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_45(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                bool(item.get(False)) if self.json_is_extra_key else False
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_46(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                bool(item.get(self.json_is_extra_key, )) if self.json_is_extra_key else False
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_47(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                bool(item.get(self.json_is_extra_key, True)) if self.json_is_extra_key else False
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_48(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                bool(item.get(self.json_is_extra_key, False)) if self.json_is_extra_key else True
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

    def xǁRestApiGazetteSpiderǁparse__mutmut_49(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                url=None,
                callback=self.parse_pdf_payload,
                meta={
                    "gazette_date": target_date,
                    "edition_number": edition_number,
                    "section": section,
                    "is_extra_edition": is_extra,
                },
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁparse__mutmut_50(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                callback=None,
                meta={
                    "gazette_date": target_date,
                    "edition_number": edition_number,
                    "section": section,
                    "is_extra_edition": is_extra,
                },
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁparse__mutmut_51(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                meta=None,
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁparse__mutmut_52(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                dont_filter=None,
            )

    def xǁRestApiGazetteSpiderǁparse__mutmut_53(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                callback=self.parse_pdf_payload,
                meta={
                    "gazette_date": target_date,
                    "edition_number": edition_number,
                    "section": section,
                    "is_extra_edition": is_extra,
                },
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁparse__mutmut_54(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                meta={
                    "gazette_date": target_date,
                    "edition_number": edition_number,
                    "section": section,
                    "is_extra_edition": is_extra,
                },
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁparse__mutmut_55(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁparse__mutmut_56(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                )

    def xǁRestApiGazetteSpiderǁparse__mutmut_57(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                    "XXgazette_dateXX": target_date,
                    "edition_number": edition_number,
                    "section": section,
                    "is_extra_edition": is_extra,
                },
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁparse__mutmut_58(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                    "GAZETTE_DATE": target_date,
                    "edition_number": edition_number,
                    "section": section,
                    "is_extra_edition": is_extra,
                },
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁparse__mutmut_59(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                    "XXedition_numberXX": edition_number,
                    "section": section,
                    "is_extra_edition": is_extra,
                },
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁparse__mutmut_60(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                    "EDITION_NUMBER": edition_number,
                    "section": section,
                    "is_extra_edition": is_extra,
                },
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁparse__mutmut_61(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                    "XXsectionXX": section,
                    "is_extra_edition": is_extra,
                },
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁparse__mutmut_62(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                    "SECTION": section,
                    "is_extra_edition": is_extra,
                },
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁparse__mutmut_63(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                    "XXis_extra_editionXX": is_extra,
                },
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁparse__mutmut_64(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                    "IS_EXTRA_EDITION": is_extra,
                },
                dont_filter=True,
            )

    def xǁRestApiGazetteSpiderǁparse__mutmut_65(self, response: Response, **kwargs: Any) -> Generator[Request, None, None]:
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
                dont_filter=False,
            )

    @_mutmut_mutated(mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut)
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

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_orig(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_1(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = None
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

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_2(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=None,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            edition_number=meta.get("edition_number"),
            section=meta.get("section"),
            is_extra_edition=meta.get("is_extra_edition", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_3(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=None,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            edition_number=meta.get("edition_number"),
            section=meta.get("section"),
            is_extra_edition=meta.get("is_extra_edition", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_4(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=None,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            edition_number=meta.get("edition_number"),
            section=meta.get("section"),
            is_extra_edition=meta.get("is_extra_edition", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_5(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=None,
            date_obj=meta["gazette_date"],
            edition_number=meta.get("edition_number"),
            section=meta.get("section"),
            is_extra_edition=meta.get("is_extra_edition", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_6(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=None,
            edition_number=meta.get("edition_number"),
            section=meta.get("section"),
            is_extra_edition=meta.get("is_extra_edition", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_7(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            edition_number=None,
            section=meta.get("section"),
            is_extra_edition=meta.get("is_extra_edition", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_8(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            edition_number=meta.get("edition_number"),
            section=None,
            is_extra_edition=meta.get("is_extra_edition", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_9(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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
            is_extra_edition=None,
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_10(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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
            power=None,
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_11(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            edition_number=meta.get("edition_number"),
            section=meta.get("section"),
            is_extra_edition=meta.get("is_extra_edition", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_12(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            edition_number=meta.get("edition_number"),
            section=meta.get("section"),
            is_extra_edition=meta.get("is_extra_edition", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_13(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            edition_number=meta.get("edition_number"),
            section=meta.get("section"),
            is_extra_edition=meta.get("is_extra_edition", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_14(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            date_obj=meta["gazette_date"],
            edition_number=meta.get("edition_number"),
            section=meta.get("section"),
            is_extra_edition=meta.get("is_extra_edition", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_15(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            edition_number=meta.get("edition_number"),
            section=meta.get("section"),
            is_extra_edition=meta.get("is_extra_edition", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_16(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            section=meta.get("section"),
            is_extra_edition=meta.get("is_extra_edition", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_17(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            edition_number=meta.get("edition_number"),
            is_extra_edition=meta.get("is_extra_edition", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_18(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_19(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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
            )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_20(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["XXgazette_dateXX"],
            edition_number=meta.get("edition_number"),
            section=meta.get("section"),
            is_extra_edition=meta.get("is_extra_edition", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_21(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["GAZETTE_DATE"],
            edition_number=meta.get("edition_number"),
            section=meta.get("section"),
            is_extra_edition=meta.get("is_extra_edition", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_22(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            edition_number=meta.get(None),
            section=meta.get("section"),
            is_extra_edition=meta.get("is_extra_edition", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_23(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            edition_number=meta.get("XXedition_numberXX"),
            section=meta.get("section"),
            is_extra_edition=meta.get("is_extra_edition", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_24(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            edition_number=meta.get("EDITION_NUMBER"),
            section=meta.get("section"),
            is_extra_edition=meta.get("is_extra_edition", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_25(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            edition_number=meta.get("edition_number"),
            section=meta.get(None),
            is_extra_edition=meta.get("is_extra_edition", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_26(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            edition_number=meta.get("edition_number"),
            section=meta.get("XXsectionXX"),
            is_extra_edition=meta.get("is_extra_edition", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_27(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Yield unvalidated RawGazettePayload DTO from downloaded PDF binary response."""
        meta = response.meta
        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=meta["gazette_date"],
            edition_number=meta.get("edition_number"),
            section=meta.get("SECTION"),
            is_extra_edition=meta.get("is_extra_edition", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_28(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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
            is_extra_edition=meta.get(None, False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_29(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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
            is_extra_edition=meta.get("is_extra_edition", None),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_30(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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
            is_extra_edition=meta.get(False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_31(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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
            is_extra_edition=meta.get("is_extra_edition", ),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_32(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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
            is_extra_edition=meta.get("XXis_extra_editionXX", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_33(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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
            is_extra_edition=meta.get("IS_EXTRA_EDITION", False),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_34(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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
            is_extra_edition=meta.get("is_extra_edition", True),
            power="executive",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_35(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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
            power="XXexecutiveXX",
        )

    def xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_36(self, response: Response) -> Generator[RawGazettePayload, None, None]:
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
            power="EXECUTIVE",
        )

mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['_mutmut_orig'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_orig # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_1'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_1 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_2'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_2 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_3'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_3 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_4'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_4 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_5'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_5 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_6'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_6 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_7'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_7 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_8'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_8 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_9'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_9 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_10'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_10 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_11'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_11 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_12'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_12 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_13'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_13 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_14'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_14 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_15'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_15 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_16'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_16 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_17'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_17 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_18'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_18 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_19'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_19 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_20'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_20 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_21'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_21 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_22'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_22 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_23'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_23 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_24'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_24 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_25'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_25 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_26'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_26 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_27'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_27 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_28'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_28 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_29'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_29 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_30'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_30 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_31'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_31 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁstart_requests__mutmut['xǁRestApiGazetteSpiderǁstart_requests__mutmut_32'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁstart_requests__mutmut_32 # type: ignore # mutmut generated

mutants_xǁRestApiGazetteSpiderǁparse__mutmut['_mutmut_orig'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_orig # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_1'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_1 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_2'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_2 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_3'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_3 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_4'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_4 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_5'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_5 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_6'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_6 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_7'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_7 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_8'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_8 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_9'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_9 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_10'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_10 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_11'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_11 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_12'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_12 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_13'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_13 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_14'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_14 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_15'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_15 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_16'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_16 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_17'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_17 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_18'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_18 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_19'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_19 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_20'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_20 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_21'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_21 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_22'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_22 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_23'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_23 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_24'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_24 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_25'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_25 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_26'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_26 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_27'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_27 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_28'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_28 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_29'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_29 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_30'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_30 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_31'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_31 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_32'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_32 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_33'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_33 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_34'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_34 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_35'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_35 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_36'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_36 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_37'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_37 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_38'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_38 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_39'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_39 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_40'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_40 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_41'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_41 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_42'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_42 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_43'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_43 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_44'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_44 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_45'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_45 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_46'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_46 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_47'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_47 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_48'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_48 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_49'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_49 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_50'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_50 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_51'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_51 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_52'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_52 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_53'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_53 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_54'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_54 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_55'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_55 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_56'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_56 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_57'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_57 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_58'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_58 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_59'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_59 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_60'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_60 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_61'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_61 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_62'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_62 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_63'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_63 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_64'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_64 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse__mutmut['xǁRestApiGazetteSpiderǁparse__mutmut_65'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse__mutmut_65 # type: ignore # mutmut generated

mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['_mutmut_orig'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_orig # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_1'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_1 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_2'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_2 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_3'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_3 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_4'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_4 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_5'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_5 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_6'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_6 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_7'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_7 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_8'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_8 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_9'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_9 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_10'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_10 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_11'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_11 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_12'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_12 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_13'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_13 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_14'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_14 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_15'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_15 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_16'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_16 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_17'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_17 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_18'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_18 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_19'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_19 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_20'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_20 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_21'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_21 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_22'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_22 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_23'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_23 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_24'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_24 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_25'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_25 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_26'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_26 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_27'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_27 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_28'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_28 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_29'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_29 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_30'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_30 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_31'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_31 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_32'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_32 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_33'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_33 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_34'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_34 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_35'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_35 # type: ignore # mutmut generated
mutants_xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut['xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_36'] = RestApiGazetteSpider.xǁRestApiGazetteSpiderǁparse_pdf_payload__mutmut_36 # type: ignore # mutmut generated
