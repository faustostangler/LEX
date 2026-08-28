"""Precision Unit Tests for GazetteIngestionPipeline.

Verifies translation and persistence pipeline integration specified in
SPEC-001 (Section 4 Scenario 1 & 2).
"""

from datetime import UTC, date, datetime
from unittest.mock import MagicMock

from scrapy import Spider

from lex.ingestion.application.ports import StreamTextExtractorPort
from lex.ingestion.domain.entities import GazetteEdition
from lex.ingestion.domain.value_objects import (
    DocumentHash,
    FederativeTier,
    GazetteDate,
    TerritoryId,
)
from lex.ingestion.infrastructure.adapters.gazette_mapper import GazetteMapper
from lex.ingestion.infrastructure.dto import RawGazettePayload
from lex.ingestion.infrastructure.scrapy_project.pipelines.ingestion_pipeline import (
    GazetteIngestionPipeline,
)


class DummyExtractor(StreamTextExtractorPort):
    """In-memory test double for StreamTextExtractorPort."""

    def extract_text(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        return "PROCESSED FULL TEXT"


class DummyRepository:
    """In-memory mock repository for pipeline tests."""

    def __init__(self) -> None:
        self.saved_editions: list[GazetteEdition] = []

    def save(self, edition: GazetteEdition) -> None:
        self.saved_editions.append(edition)

    def get_by_territory_and_date(
        self,
        territory_id: object,
        date: object,
        section: object = None,
    ) -> None:
        return None

    def exists_by_hash(self, file_hash: object) -> bool:
        return False


class DummyMapper(GazetteMapper):
    """In-memory test double for GazetteMapper."""

    def __init__(self) -> None:
        super().__init__(text_extractor=DummyExtractor())

    def to_domain(self, payload: RawGazettePayload) -> GazetteEdition:
        text = "PROCESSED FULL TEXT"
        return GazetteEdition(
            territory_id=TerritoryId.from_code(payload.territory_code),
            tier=FederativeTier(payload.tier),
            date=GazetteDate.from_date(payload.date_obj or date(2024, 1, 2)),
            edition_number=payload.edition_number,
            section=payload.section,
            is_extra_edition=payload.is_extra_edition,
            power=payload.power,
            source_url=payload.source_url,
            file_hash=DocumentHash.from_text(text),
            char_count=len(text),
            full_text=text,
            scraped_at=datetime(2024, 1, 2, 12, 0, 0, tzinfo=UTC),
        )


class TestGazetteIngestionPipeline:
    """Acceptance tests for GazetteIngestionPipeline."""

    def test_process_raw_payload_item(self) -> None:
        """Scenario: Pipeline maps RawGazettePayload and saves to repository."""
        repo = DummyRepository()
        mapper = DummyMapper()
        pipeline = GazetteIngestionPipeline(repository=repo, mapper=mapper)

        spider = MagicMock(spec=Spider)
        spider.name = "test_spider"

        payload = RawGazettePayload(
            territory_code="BR",
            tier="federal",
            source_url="https://pesquisa.in.gov.br",
            raw_content="RAW TEXT",
            date_obj=date(2024, 1, 2),
        )

        result = pipeline.process_item(payload, spider)

        assert result == payload
        assert len(repo.saved_editions) == 1
        assert repo.saved_editions[0].territory_id.code == "BR"
        assert repo.saved_editions[0].full_text == "PROCESSED FULL TEXT"

    def test_process_non_payload_item_passthrough(self) -> None:
        """Scenario: Non-RawGazettePayload items pass through unchanged."""
        repo = DummyRepository()
        mapper = DummyMapper()
        pipeline = GazetteIngestionPipeline(repository=repo, mapper=mapper)

        spider = MagicMock(spec=Spider)
        other_item = {"some": "data"}

        result = pipeline.process_item(other_item, spider)

        assert result == other_item
        assert len(repo.saved_editions) == 0
