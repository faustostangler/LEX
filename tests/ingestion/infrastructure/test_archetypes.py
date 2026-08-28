"""Precision Unit Tests for Platform Archetype Spider Mixins.

Verifies RestApiGazetteSpider, MonthlyDirectoryGazetteSpider, and AspxViewerGazetteSpider
dispatching behaviors specified in ADR-001 (Section 10.1).
"""

import json
from datetime import date

from scrapy.http import HtmlResponse, Request, Response, TextResponse

from lex.ingestion.infrastructure.dto import RawGazettePayload
from lex.ingestion.infrastructure.scrapy_project.spiders.archetypes.aspx_viewer import (
    AspxViewerGazetteSpider,
)
from lex.ingestion.infrastructure.scrapy_project.spiders.archetypes.monthly_directory import (
    MonthlyDirectoryGazetteSpider,
)
from lex.ingestion.infrastructure.scrapy_project.spiders.archetypes.rest_api import (
    RestApiGazetteSpider,
)


class ConcreteRestSpider(RestApiGazetteSpider):
    """Test implementation of RestApiGazetteSpider."""

    name = "test_rest_spider"
    territory_code = "SP"
    tier = "state"
    api_endpoint_template = "https://api.doe.sp.gov.br/edicoes?data={iso_date}"
    json_pdf_url_key = "download_url"
    json_edition_key = "numero"
    json_section_key = "caderno"
    json_is_extra_key = "suplementar"


class ConcreteMonthlySpider(MonthlyDirectoryGazetteSpider):
    """Test implementation of MonthlyDirectoryGazetteSpider."""

    name = "test_monthly_spider"
    territory_code = "RJ"
    tier = "state"
    directory_url_template = (
        "https://doe.rj.gov.br/consulta?ano={year}&mes={month:02d}&dia={day:02d}"
    )
    edition_link_xpath = "//a[contains(@href, '.pdf')]"


class ConcreteAspxSpider(AspxViewerGazetteSpider):
    """Test implementation of AspxViewerGazetteSpider."""

    name = "test_aspx_spider"
    territory_code = "MG"
    tier = "state"
    form_url = "https://jornal.iof.mg.gov.br/Default.aspx"


class TestRestApiGazetteSpider:
    """Acceptance tests for RestApiGazetteSpider archetype."""

    def test_start_requests_generates_api_urls(self) -> None:
        spider = ConcreteRestSpider(start_date="2024-05-10", end_date="2024-05-10")
        requests = list(spider.start_requests())
        assert len(requests) == 1
        assert requests[0].url == "https://api.doe.sp.gov.br/edicoes?data=2024-05-10"

    def test_parse_api_response_dispatches_pdf_requests(self) -> None:
        spider = ConcreteRestSpider(start_date="2024-05-10", end_date="2024-05-10")
        payload_data = [
            {
                "download_url": "https://doe.sp.gov.br/files/20240510.pdf",
                "numero": "552",
                "caderno": "executivo_1",
                "suplementar": False,
            }
        ]
        request = Request(
            url="https://api.doe.sp.gov.br/edicoes?data=2024-05-10",
            meta={"gazette_date": date(2024, 5, 10)},
        )
        response = TextResponse(
            url=request.url,
            body=json.dumps(payload_data).encode("utf-8"),
            request=request,
        )

        pdf_requests = list(spider.parse(response))
        assert len(pdf_requests) == 1
        assert pdf_requests[0].url == "https://doe.sp.gov.br/files/20240510.pdf"

    def test_parse_pdf_payload_yields_raw_dto(self) -> None:
        spider = ConcreteRestSpider(start_date="2024-05-10", end_date="2024-05-10")
        pdf_bytes = b"%PDF-1.4 mock stream"
        request = Request(
            url="https://doe.sp.gov.br/files/20240510.pdf",
            meta={
                "gazette_date": date(2024, 5, 10),
                "edition_number": "552",
                "section": "executivo_1",
                "is_extra_edition": False,
            },
        )
        response = Response(url=request.url, body=pdf_bytes, request=request)

        items = list(spider.parse_pdf_payload(response))
        assert len(items) == 1
        assert isinstance(items[0], RawGazettePayload)
        assert items[0].territory_code == "SP"
        assert items[0].date_obj == date(2024, 5, 10)
        assert items[0].edition_number == "552"
        assert items[0].section == "executivo_1"


class TestMonthlyDirectoryGazetteSpider:
    """Acceptance tests for MonthlyDirectoryGazetteSpider archetype."""

    def test_start_requests_generates_directory_urls(self) -> None:
        spider = ConcreteMonthlySpider(start_date="2024-05-10", end_date="2024-05-10")
        requests = list(spider.start_requests())
        assert len(requests) == 1
        assert requests[0].url == "https://doe.rj.gov.br/consulta?ano=2024&mes=05&dia=10"

    def test_parse_directory_dispatches_pdf_links(self) -> None:
        spider = ConcreteMonthlySpider(start_date="2024-05-10", end_date="2024-05-10")
        html = """
        <html>
            <body>
                <a href="/downloads/do_20240510_p1.pdf">Caderno 1</a>
                <a href="/downloads/do_20240510_p2.pdf">Caderno 2</a>
            </body>
        </html>
        """
        request = Request(
            url="https://doe.rj.gov.br/consulta?ano=2024&mes=05&dia=10",
            meta={"gazette_date": date(2024, 5, 10)},
        )
        response = HtmlResponse(url=request.url, body=html.encode("utf-8"), request=request)

        requests = list(spider.parse(response))
        assert len(requests) == 2
        assert requests[0].url == "https://doe.rj.gov.br/downloads/do_20240510_p1.pdf"
        assert requests[1].url == "https://doe.rj.gov.br/downloads/do_20240510_p2.pdf"


class TestAspxViewerGazetteSpider:
    """Acceptance tests for AspxViewerGazetteSpider archetype."""

    def test_start_requests_initiates_form_page(self) -> None:
        spider = ConcreteAspxSpider(start_date="2024-05-10", end_date="2024-05-10")
        requests = list(spider.start_requests())
        assert len(requests) == 1
        assert requests[0].url == "https://jornal.iof.mg.gov.br/Default.aspx"

    def test_parse_form_extracts_viewstate_and_pdf_links(self) -> None:
        spider = ConcreteAspxSpider(start_date="2024-05-10", end_date="2024-05-10")
        html = """
        <html>
            <body>
                <form id="form1">
                    <input type="hidden" name="__VIEWSTATE" value="MOCK_VIEWSTATE_VAL" />
                    <input type="hidden" name="__EVENTVALIDATION" value="MOCK_EV_VAL" />
                    <a id="lnkPdf" href="Download.aspx?file=mg20240510.pdf">Download Diario</a>
                </form>
            </body>
        </html>
        """
        request = Request(
            url="https://jornal.iof.mg.gov.br/Default.aspx",
            meta={"gazette_date": date(2024, 5, 10)},
        )
        response = HtmlResponse(url=request.url, body=html.encode("utf-8"), request=request)

        items_or_requests = list(spider.parse(response))
        assert len(items_or_requests) == 1
        assert "Download.aspx?file=mg20240510.pdf" in items_or_requests[0].url
