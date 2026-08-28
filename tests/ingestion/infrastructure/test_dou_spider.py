"""Precision Unit Tests for FederalDouSpider.

Verifies date range generation, DOU section indexing, and PDF request dispatching
specified in SPEC-001 (Section 4 Scenario 1).
"""

from datetime import date

from scrapy.http import HtmlResponse, Request, Response

from lex.ingestion.infrastructure.dto import RawGazettePayload
from lex.ingestion.infrastructure.scrapy_project.spiders.federal.dou_spider import (
    FederalDouSpider,
)


class TestFederalDouSpider:
    """Acceptance tests for FederalDouSpider."""

    def test_spider_initialization_and_metadata(self) -> None:
        """Scenario: FederalDouSpider initializes with BR territory and federal tier."""
        spider = FederalDouSpider(start_date="2024-01-02", end_date="2024-01-02")
        assert spider.name == "federal_dou"
        assert spider.territory_code == "BR"
        assert spider.tier == "federal"
        assert spider.start_date == date(2024, 1, 2)
        assert spider.end_date == date(2024, 1, 2)

    def test_spider_start_requests_generates_all_sections(self) -> None:
        """Scenario: start_requests generates index URLs for all sections."""
        spider = FederalDouSpider(start_date="2024-01-02", end_date="2024-01-02")
        requests = list(spider.start_requests())

        # 5 sections for 1 date = 5 index requests
        assert len(requests) == 5

        first_req = requests[0]
        assert "pesquisa.in.gov.br/imprensa/jsp/visualiza/index.jsp" in first_req.url
        assert "data=02/01/2024" in first_req.url
        assert first_req.meta["gazette_date"] == date(2024, 1, 2)
        assert "section" in first_req.meta

    def test_spider_parse_index_dispatches_pdf_page_requests(self) -> None:
        """Scenario: parse_index extracts totalPaginas and yields page download requests."""
        spider = FederalDouSpider(start_date="2024-01-02", end_date="2024-01-02")

        html = """
        <html>
            <body>
                <input type="hidden" id="totalPaginas" name="totalPaginas" value="3" />
                <span id="edicao">Edição 1</span>
            </body>
        </html>
        """
        request = Request(
            url="https://pesquisa.in.gov.br/imprensa/jsp/visualiza/index.jsp?data=02/01/2024&jornal=1",
            meta={
                "gazette_date": date(2024, 1, 2),
                "jornal": 1,
                "section": "secao_1",
            },
        )
        response = HtmlResponse(
            url=request.url,
            body=html.encode("utf-8"),
            request=request,
        )

        page_requests = list(spider.parse_index(response))
        assert len(page_requests) == 3

        for i, req in enumerate(page_requests, start=1):
            assert f"pagina={i}" in req.url
            assert "jornal=1" in req.url
            assert req.meta["page"] == i
            assert req.meta["total_pages"] == 3

    def test_spider_parse_pdf_page_yields_raw_gazette_payload(self) -> None:
        """Scenario: parse_pdf_page receives PDF byte stream and yields RawGazettePayload."""
        spider = FederalDouSpider(start_date="2024-01-02", end_date="2024-01-02")

        pdf_binary = b"%PDF-1.4 mock binary content"
        request = Request(
            url="https://pesquisa.in.gov.br/imprensa/servlet/INPDFViewer?jornal=1&pagina=1&data=02/01/2024",
            meta={
                "gazette_date": date(2024, 1, 2),
                "jornal": 1,
                "section": "secao_1",
                "page": 1,
                "total_pages": 1,
            },
        )
        response = Response(
            url=request.url,
            body=pdf_binary,
            request=request,
        )

        items = list(spider.parse_pdf_page(response))
        assert len(items) == 1

        payload = items[0]
        assert isinstance(payload, RawGazettePayload)
        assert payload.territory_code == "BR"
        assert payload.tier == "federal"
        assert payload.date_obj == date(2024, 1, 2)
        assert payload.section == "secao_1"
        assert payload.raw_content == pdf_binary
        assert payload.source_url == response.url
