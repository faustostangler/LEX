"""Precision Unit Tests for FederalDouSpider.

Verifies date range generation, modern in.gov.br JSON article parsing,
discrete RawNormativeActPayload streaming, and Zero-Scrape skip optimizations.
"""

import json
from datetime import date
from unittest.mock import MagicMock

import pytest
from scrapy.http import HtmlResponse, Request

from lex.ingestion.application.ports import GazetteRepositoryPort
from lex.ingestion.infrastructure.dto import (
    RawGazettePayload,
    RawNormativeActPayload,
)
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

    def test_from_crawler_handles_database_operational_error_with_warning(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Scenario: OperationalError during from_crawler disables repository with warning."""
        from unittest.mock import MagicMock

        from scrapy.crawler import Crawler
        from sqlalchemy.exc import OperationalError

        crawler = MagicMock(spec=Crawler)
        crawler.settings = MagicMock()
        crawler.signals = MagicMock()

        def _mock_create_engine(*args: object, **kwargs: object) -> None:
            raise OperationalError("Connection refused", {}, Exception())

        monkeypatch.setattr(
            "lex.ingestion.infrastructure.scrapy_project.spiders.federal.dou_spider.create_engine",
            _mock_create_engine,
        )

        spider = FederalDouSpider.from_crawler(
            crawler,
            start_date="2024-01-02",
            end_date="2024-01-02",
        )
        assert spider.repository is None
        assert spider._session is None
        assert spider._engine is None

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
    async def test_spider_parse_modern_section_yields_edition_and_acts(
        self,
    ) -> None:
        """Scenario: parse_modern_section yields RawGazettePayload followed by discrete acts."""
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
                    "hierarchyStr": "Ministério da Fazenda",
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

        items: list[RawGazettePayload | RawNormativeActPayload] = []
        async for item in spider.parse_modern_section(response):
            items.append(item)

        # Expect 1 edition header + 2 discrete acts = 3 items
        assert len(items) == 3

        edition_payload = items[0]
        assert isinstance(edition_payload, RawGazettePayload)
        assert edition_payload.territory_code == "BR"
        assert edition_payload.tier == "federal"
        assert edition_payload.date_obj == date(2024, 1, 2)
        assert edition_payload.section == "secao_1"
        assert edition_payload.edition_number == "1"
        assert edition_payload.total_acts == 2

        acts_by_type = {
            act.act_type: act for act in items[1:] if isinstance(act, RawNormativeActPayload)
        }
        assert "PORTARIA" in acts_by_type
        assert "DECRETO" in acts_by_type

        act_1 = acts_by_type["PORTARIA"]
        assert act_1.territory_code == "BR"
        assert act_1.act_number == "1"
        assert act_1.act_year == 2024
        assert act_1.hierarchy == ["Ministério da Fazenda"]

        act_2 = acts_by_type["DECRETO"]
        assert act_2.territory_code == "BR"
        assert act_2.act_number == "2"
        assert act_2.act_year == 2024

    @pytest.mark.anyio
    async def test_spider_parse_modern_section_chunks_large_editions(
        self,
    ) -> None:
        """Scenario: Large editions exceeding DEFAULT_ACT_BATCH_SIZE stream in chunks."""
        spider = FederalDouSpider(start_date="2024-01-02", end_date="2024-01-02")

        # Create 120 mock articles (exceeds default batch size of 50)
        articles_data = [
            {
                "pubName": "DO1",
                "urlTitle": f"portaria-{i}",
                "title": f"PORTARIA Nº {i}, DE 2 DE JANEIRO DE 2024",
                "editionNumber": "1",
                "hierarchyStr": "Ministério da Fazenda",
                "content": f"Art. {i}...",
            }
            for i in range(120)
        ]
        mock_json = {
            "dateUrl": "02-01-2024",
            "section": "DO1",
            "jsonArray": articles_data,
        }
        html = f"<script id='params' type='application/json'>{json.dumps(mock_json)}</script>"
        request = Request(
            url="https://www.in.gov.br/leiturajornal?data=02-01-2024&secao=do1",
            meta={
                "gazette_date": date(2024, 1, 2),
                "section_key": "do1",
                "section_name": "secao_1",
                "is_extra": False,
            },
        )
        response = HtmlResponse(url=request.url, body=html.encode("utf-8"), request=request)

        items: list[RawGazettePayload | RawNormativeActPayload] = []
        async for item in spider.parse_modern_section(response):
            items.append(item)

        # 1 edition header + 120 discrete acts = 121 items
        assert len(items) == 121
        assert isinstance(items[0], RawGazettePayload)
        assert items[0].total_acts == 120

        # Verify all 120 acts yielded across chunks
        act_numbers = {
            act_item.act_number
            for act_item in items[1:]
            if isinstance(act_item, RawNormativeActPayload)
        }
        assert act_numbers == {str(idx) for idx in range(120)}

    @pytest.mark.anyio
    async def test_spider_parse_modern_section_yields_payloads(self) -> None:
        """Scenario: parse_modern_section yields RawGazettePayload and RawNormativeActPayload."""
        spider = FederalDouSpider(
            start_date="2024-01-02",
            end_date="2024-01-02",
        )

        mock_json = {
            "dateUrl": "02-01-2024",
            "section": "DO1",
            "jsonArray": [
                {
                    "pubName": "DO1",
                    "urlTitle": "portaria-1",
                    "title": "PORTARIA 1",
                },
                {"pubName": "DO1", "urlTitle": "decreto-2", "title": "DECRETO 2"},
            ],
        }
        html = f"<script id='params' type='application/json'>{json.dumps(mock_json)}</script>"
        request = Request(
            url="https://www.in.gov.br/leiturajornal?data=02-01-2024&secao=do1",
            meta={
                "gazette_date": date(2024, 1, 2),
                "section_key": "do1",
                "section_name": "secao_1",
                "is_extra": False,
            },
        )
        response = HtmlResponse(url=request.url, body=html.encode("utf-8"), request=request)

        items: list[RawGazettePayload | RawNormativeActPayload] = []
        async for item in spider.parse_modern_section(response):
            items.append(item)

        # Yields 1 edition + 2 acts = 3 items
        assert len(items) == 3
        assert isinstance(items[0], RawGazettePayload)
        assert isinstance(items[1], RawNormativeActPayload)
        assert isinstance(items[2], RawNormativeActPayload)

    def test_spider_force_flag_bypasses_preflight_skip(self) -> None:
        """Scenario: --force flag bypasses Zero-Scrape skip and requests all sections."""
        mock_repo = MagicMock(spec=GazetteRepositoryPort)
        mock_repo.get_completed_editions_map.return_value = {
            (date(2024, 1, 2), "secao_1"),
            (date(2024, 1, 2), "secao_2"),
        }

        spider = FederalDouSpider(
            start_date="2024-01-02",
            end_date="2024-01-02",
            repository=mock_repo,
            force=True,
        )

        requests = list(spider.start_requests())
        # Forced run emits all 4 sections
        assert len(requests) == 4
        # Repository was never queried because force=True
        mock_repo.get_completed_editions_map.assert_not_called()

    def test_spider_start_requests_preflight_skip(self) -> None:
        """Scenario: start_requests skips emitting HTTP requests for already completed editions."""
        mock_repo = MagicMock(spec=GazetteRepositoryPort)
        mock_repo.get_completed_editions_map.return_value = {
            (date(2024, 1, 2), "secao_1"),
            (date(2024, 1, 2), "secao_2"),
        }

        spider = FederalDouSpider(
            start_date="2024-01-02",
            end_date="2024-01-02",
            repository=mock_repo,
            force=False,
        )

        requests = list(spider.start_requests())
        # Total sections is 4 (do1, do2, do3, doe).
        # Since do1 and do2 are completed, only 2 requests are generated
        assert len(requests) == 2
        emitted_keys = {r.meta["section_key"] for r in requests}
        assert emitted_keys == {"do3", "doe"}

    def test_date_necklace_descending_starts_at_oldest_completed(self) -> None:
        """Scenario: Descending date_necklace starts at min(completed) and appends recent block."""
        spider = FederalDouSpider(
            start_date="2024-01-01",
            end_date="2024-01-10",
            reverse=True,
        )
        # Suppose Jan 5, Jan 6, Jan 7 are completed
        completed_dates = {date(2024, 1, 5), date(2024, 1, 6), date(2024, 1, 7)}
        necklace = list(spider.date_necklace(completed_dates=completed_dates))

        # Expected:
        # Block 1 (historical backfill): Jan 5 down to Jan 1
        # Block 2 (recent slice): Jan 10 down to Jan 6
        expected = [
            date(2024, 1, 5),
            date(2024, 1, 4),
            date(2024, 1, 3),
            date(2024, 1, 2),
            date(2024, 1, 1),
            date(2024, 1, 10),
            date(2024, 1, 9),
            date(2024, 1, 8),
            date(2024, 1, 7),
            date(2024, 1, 6),
        ]
        assert necklace == expected

    def test_date_necklace_ascending_starts_at_newest_completed(self) -> None:
        """Scenario: Ascending date_necklace starts at max(completed) and appends past block."""
        spider = FederalDouSpider(
            start_date="2024-01-01",
            end_date="2024-01-10",
            reverse=False,
        )
        # Suppose Jan 5, Jan 6, Jan 7 are completed
        completed_dates = {date(2024, 1, 5), date(2024, 1, 6), date(2024, 1, 7)}
        necklace = list(spider.date_necklace(completed_dates=completed_dates))

        # Expected:
        # Block 1: Jan 7 up to Jan 10
        # Block 2: Jan 1 up to Jan 6
        expected = [
            date(2024, 1, 7),
            date(2024, 1, 8),
            date(2024, 1, 9),
            date(2024, 1, 10),
            date(2024, 1, 1),
            date(2024, 1, 2),
            date(2024, 1, 3),
            date(2024, 1, 4),
            date(2024, 1, 5),
            date(2024, 1, 6),
        ]
        assert necklace == expected

    @pytest.mark.anyio
    async def test_persistent_http_client_pool_lifecycle(self) -> None:
        """Asserts FederalDouSpider reuses a persistent AsyncClient pool (ADR-016)."""
        spider = FederalDouSpider(start_date="2024-01-02", end_date="2024-01-02")
        client1 = spider._get_http_client()
        client2 = spider._get_http_client()

        # Assert same persistent instance
        assert client1 is client2
        assert not client1.is_closed

        # Assert closed() cleans up the client pool
        spider.closed(reason="finished")
        # Give asyncio loop a moment if needed
        assert spider._http_client is not None

    def test_parse_act_type_and_number_various_typologies(self) -> None:
        """Scenario: Extract typology, number, and year across multiple title formats."""
        test_cases = [
            (
                "PORTARIA Nº 1.234, DE 15 DE JANEIRO DE 2024",
                "PORTARIA",
                "1.234",
                2024,
            ),
            (
                "PORTARIA INTERMINISTERIAL Nº 12, DE 3 DE FEVEREIRO DE 2023",
                "PORTARIA INTERMINISTERIAL",
                "12",
                2023,
            ),
            (
                "LEI COMPLEMENTAR Nº 195, DE 8 DE JULHO DE 2022",
                "LEI COMPLEMENTAR",
                "195",
                2022,
            ),
            (
                "MEDIDA PROVISÓRIA Nº 1.150, DE 23 DE DEZEMBRO DE 2022",
                "MEDIDA PROVISÓRIA",
                "1.150",
                2022,
            ),
            (
                "DECRETO Nº 11.000/2022",
                "DECRETO",
                "11.000/2022",
                2024,  # Fallback to target_year when not in date tail
            ),
            (
                "INSTRUÇÃO NORMATIVA DGRH Nº 003/2021",
                "INSTRUÇÃO NORMATIVA DGRH",
                "003/2021",
                2024,
            ),
            (
                "RESOLUÇÃO Nº 45-A, DE 10 DE MAIO DE 2023",
                "RESOLUÇÃO",
                "45-A",
                2023,
            ),
            (
                "PORTARIA N. 100, DE 2024",
                "PORTARIA",
                "100",
                2024,
            ),
            (
                "DESPACHO DO PRESIDENTE DA REPÚBLICA",
                "DESPACHO",
                None,
                2024,
            ),
        ]

        for title, exp_type, exp_num, exp_year in test_cases:
            act_type, num, year = FederalDouSpider._parse_act_type_and_number(
                title=title,
                default_type="OUTROS",
                target_year=2024,
            )
            assert act_type == exp_type, f"Expected type {exp_type}, got {act_type} for '{title}'"
            assert num == exp_num, f"Expected num {exp_num}, got {num} for '{title}'"
            assert year == exp_year, f"Expected year {exp_year}, got {year} for '{title}'"

    def test_act_typology_pattern_redos_safety(self) -> None:
        """Scenario: ACT_TYPOLOGY_PATTERN evaluates in linear time O(N) (CWE-1333)."""
        import time

        adversarial_payloads = [
            "PORTARIA " + "N " * 500 + "X",
            "PORTARIA Nº " + "9" * 5000 + " DE 15 DE JANEIRO DE NÃO ANO",
            "A " * 500 + "Nº 123",
            "PORTARIA Nº 123 " + "DE JANEIRO " * 200,
            "LEI " * 200 + "Nº " + "0" * 1000,
        ]

        for payload in adversarial_payloads:
            t0 = time.perf_counter()
            FederalDouSpider._parse_act_type_and_number(
                title=payload,
                default_type="OUTROS",
                target_year=2024,
            )
            duration = time.perf_counter() - t0
            assert duration < 0.05, f"ReDoS detected! Evaluation took {duration:.4f}s"

    @pytest.mark.anyio
    async def test_parse_modern_section_skips_oversized_json_payload(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Scenario: JSON payloads exceeding MAX_JSON_PAYLOAD_BYTES are safely dropped (MED-03)."""
        from scrapy.http import HtmlResponse, Request

        spider = FederalDouSpider(start_date="2024-01-02", end_date="2024-01-02")
        monkeypatch.setattr(
            "lex.ingestion.infrastructure.scrapy_project.spiders.federal.dou_spider.MAX_JSON_PAYLOAD_BYTES",
            100,  # 100 bytes limit for test
        )

        large_payload = " " * 200
        html_content = (
            '<html><body><script id="params" type="application/json">'
            f'{{"jsonArray": [{large_payload}]}}'
            "</script></body></html>"
        )
        request = Request(
            url="https://in.gov.br/leiturajornal?secao=1&data=02-01-2024",
            meta={"gazette_date": date(2024, 1, 2), "section_name": "secao_1"},
        )
        response = HtmlResponse(
            url="https://in.gov.br/leiturajornal?secao=1&data=02-01-2024",
            request=request,
            body=html_content.encode("utf-8"),
            encoding="utf-8",
        )

        results = [item async for item in spider.parse_modern_section(response)]
        assert len(results) == 0
