"""Federal DOU Spider for Brazilian Official Gazette (Diário Oficial da União).

Scrapes Section 1, Section 2, Section 3, Extra, and Suplementar editions directly
from the Imprensa Nacional INPDFViewer portal (pesquisa.in.gov.br).
"""

import re
from collections.abc import Generator
from datetime import date

from scrapy.http import HtmlResponse, Request, Response

from lex.ingestion.infrastructure.dto import RawGazettePayload
from lex.ingestion.infrastructure.scrapy_project.spiders.base import BaseGazetteSpider


class FederalDouSpider(BaseGazetteSpider):
    """Spider for crawling the Federal Official Gazette (DOU)."""

    name = "federal_dou"
    territory_code = "BR"
    tier = "federal"
    allowed_domains = ["pesquisa.in.gov.br", "in.gov.br"]

    SECTIONS: dict[int, str] = {
        1: "secao_1",
        2: "secao_2",
        3: "secao_3",
        1000: "extra",
        515: "suplementar",
    }

    INDEX_URL = "https://pesquisa.in.gov.br/imprensa/jsp/visualiza/index.jsp"
    PDF_VIEWER_URL = "https://pesquisa.in.gov.br/imprensa/servlet/INPDFViewer"

    def start_requests(self) -> Generator[Request, None, None]:
        """Generate starting index requests for each configured DOU section and target date."""
        for target_date in self.date_range():
            formatted_date = target_date.strftime("%d/%m/%Y")
            for jornal_id, section_name in self.SECTIONS.items():
                url = f"{self.INDEX_URL}?data={formatted_date}&jornal={jornal_id}"
                yield Request(
                    url=url,
                    callback=self.parse_index,
                    meta={
                        "gazette_date": target_date,
                        "jornal": jornal_id,
                        "section": section_name,
                    },
                    dont_filter=True,
                )

    def parse_index(self, response: Response) -> Generator[Request, None, None]:
        """Parse index page to find total page count and dispatch PDF page stream requests."""
        if not isinstance(response, HtmlResponse):
            return

        total_pages = self._extract_total_pages(response)
        if total_pages <= 0:
            return

        meta = response.meta
        target_date: date = meta["gazette_date"]
        formatted_date = target_date.strftime("%d/%m/%Y")
        jornal_id: int = meta["jornal"]
        section_name: str = meta["section"]

        for page in range(1, total_pages + 1):
            pdf_url = (
                f"{self.PDF_VIEWER_URL}?jornal={jornal_id}"
                f"&pagina={page}&data={formatted_date}&captchafield=firstAccess"
            )
            yield Request(
                url=pdf_url,
                callback=self.parse_pdf_page,
                meta={
                    "gazette_date": target_date,
                    "jornal": jornal_id,
                    "section": section_name,
                    "page": page,
                    "total_pages": total_pages,
                },
                dont_filter=True,
            )

    def parse_pdf_page(self, response: Response) -> Generator[RawGazettePayload, None, None]:
        """Receive PDF byte stream from servlet and yield unvalidated RawGazettePayload DTO."""
        meta = response.meta
        target_date: date = meta["gazette_date"]
        section_name: str = meta["section"]
        jornal_id: int = meta["jornal"]

        yield RawGazettePayload(
            territory_code=self.territory_code,
            tier=self.tier,
            source_url=response.url,
            raw_content=response.body,
            date_obj=target_date,
            section=section_name,
            edition_number=str(jornal_id),
            is_extra_edition=(section_name == "extra"),
            power="executive",
        )

    @staticmethod
    def _extract_total_pages(response: HtmlResponse) -> int:
        """Extract total page count from index DOM element or script variable."""
        # 1. Check input element value
        page_val = response.xpath(
            "//input[@id='totalPaginas' or @name='totalPaginas']/@value"
        ).get()
        if page_val and page_val.isdigit():
            return int(page_val)

        # 2. Check JavaScript variable regex
        match = re.search(r"totalPaginas\s*=\s*['\"]?(\d+)['\"]?", response.text)
        if match:
            return int(match.group(1))

        return 0
