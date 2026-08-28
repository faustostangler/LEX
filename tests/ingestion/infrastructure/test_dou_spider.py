"""Precision Unit Tests for FederalDouSpider.

Verifies date range generation and modern in.gov.br JSON article parsing.
"""

import json
from datetime import date

import pytest
from scrapy.http import HtmlResponse, Request

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
        """Scenario: start_requests generates index URLs for all modern sections."""
        spider = FederalDouSpider(start_date="2024-01-02", end_date="2024-01-02")
        requests = list(spider.start_requests())

        # 4 modern sections (do1, do2, do3, doe) for 1 date = 4 requests
        assert len(requests) == 4

        first_req = requests[0]
        assert "www.in.gov.br/leiturajornal" in first_req.url
        assert "data=02-01-2024" in first_req.url
        assert first_req.meta["gazette_date"] == date(2024, 1, 2)
        assert "section_name" in first_req.meta

    @pytest.mark.anyio
    async def test_spider_parse_modern_section_yields_raw_gazette_payload(self) -> None:
        """Scenario: parse_modern_section extracts JSON params and yields RawGazettePayload."""
        spider = FederalDouSpider(start_date="2024-01-02", end_date="2024-01-02")

        mock_json = {
            "dateUrl": "02-01-2024",
            "section": "DO1",
            "jsonArray": [
                {
                    "pubName": "DO1",
                    "urlTitle": "portaria-n-1",
                    "title": "PORTARIA Nº 1, DE 2 DE JANEIRO DE 2024",
                    "editionNumber": "1",
                    "hierarchyStr": "Ministério da Economia",
                    "content": "Art. 1º Fica estabelecido...",
                },
                {
                    "pubName": "DO1",
                    "urlTitle": "decreto-n-2",
                    "title": "DECRETO Nº 2, DE 2 DE JANEIRO DE 2024",
                    "editionNumber": "1",
                    "hierarchyStr": "Presidência da República",
                    "content": "Art. 1º Regulamenta...",
                },
            ],
        }

        html = f"""
        <html>
            <head>
                <script id="params" type="application/json">
                    {json.dumps(mock_json)}
                </script>
            </head>
            <body>Mock leiturajornal</body>
        </html>
        """
        request = Request(
            url="https://www.in.gov.br/leiturajornal?data=02-01-2024&secao=do1",
            meta={
                "gazette_date": date(2024, 1, 2),
                "section_key": "do1",
                "section_name": "secao_1",
                "is_extra": False,
            },
        )
        response = HtmlResponse(
            url=request.url,
            body=html.encode("utf-8"),
            request=request,
        )

        items: list[RawGazettePayload] = []
        async for item in spider.parse_modern_section(response):
            items.append(item)

        assert len(items) == 1

        payload = items[0]
        assert isinstance(payload, RawGazettePayload)
        assert payload.territory_code == "BR"
        assert payload.tier == "federal"
        assert payload.date_obj == date(2024, 1, 2)
        assert payload.section == "secao_1"
        assert payload.edition_number == "1"
        assert payload.is_extra_edition is False
        assert "PORTARIA Nº 1" in str(payload.raw_content)
        assert "DECRETO Nº 2" in str(payload.raw_content)
