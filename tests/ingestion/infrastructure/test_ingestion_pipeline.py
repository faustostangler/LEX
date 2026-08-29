"""Precision Unit Tests for GazetteIngestionPipeline.

Verifies translation and persistence pipeline integration for both GazetteEdition
and NormativeAct items specified in ADR-002.
"""

import uuid
from datetime import UTC, date, datetime
from unittest.mock import MagicMock

from scrapy import Spider

from lex.ingestion.application.ports import StreamTextExtractorPort
from lex.ingestion.domain.entities import GazetteEdition, NormativeAct
from lex.ingestion.domain.value_objects import (
    ClassificationSource,
    DocumentHash,
    FederativeTier,
    GazetteDate,
    IngestionStatus,
    TerritoryId,
)
from lex.ingestion.infrastructure.adapters.gazette_mapper import GazetteMapper
from lex.ingestion.infrastructure.dto import (
    RawGazettePayload,
    RawNormativeActPayload,
)
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
        self.saved_acts: list[NormativeAct] = []

    def save(self, edition: GazetteEdition) -> None:
        self.saved_editions.append(edition)

    def save_normative_act(self, act: NormativeAct) -> None:
        self.saved_acts.append(act)

    def save_normative_acts_bulk(self, acts: list[NormativeAct]) -> None:
        self.saved_acts.extend(acts)

    def get_by_territory_and_date(
        self,
        territory_id: object,
        date: object,
        section: object = None,
    ) -> GazetteEdition | None:
        return self.saved_editions[0] if self.saved_editions else None

    def exists_by_hash(self, file_hash: object) -> bool:
        return False

    def get_act_by_id(self, act_id: object) -> None:
        return None

    def find_acts_by_edition(self, edition_id: object) -> list[NormativeAct]:
        return []

    def exists_act_by_hash(self, content_hash: object) -> bool:
        return False


class DummyMapper(GazetteMapper):
    """In-memory test double for GazetteMapper."""

    def __init__(self) -> None:
        super().__init__(text_extractor=DummyExtractor())

    def to_domain(self, payload: RawGazettePayload) -> GazetteEdition:
        return GazetteEdition(
            id=uuid.uuid4(),
            territory_id=TerritoryId.from_code(payload.territory_code),
            tier=FederativeTier(payload.tier),
            date=GazetteDate.from_date(payload.date_obj or date(2024, 1, 2)),
            edition_number=payload.edition_number,
            section=payload.section,
            is_extra_edition=payload.is_extra_edition,
            power=payload.power,
            source_url=payload.source_url,
            summary_hash=DocumentHash.from_text("summary"),
            total_acts=payload.total_acts,
            ingestion_status=IngestionStatus.COMPLETED,
            scraped_at=datetime(2024, 1, 2, 12, 0, 0, tzinfo=UTC),
        )

    def to_normative_act(
        self,
        payload: RawNormativeActPayload,
        edition_id: uuid.UUID | None = None,
    ) -> NormativeAct:
        raw = payload.raw_content.strip()
        return NormativeAct(
            id=uuid.uuid4(),
            edition_id=edition_id or uuid.uuid4(),
            territory_id=TerritoryId.from_code(payload.territory_code),
            date=GazetteDate.from_date(payload.date_obj),
            section=payload.section,
            edition_number=payload.edition_number,
            act_type=payload.act_type,
            act_number=payload.act_number,
            act_year=payload.act_year,
            title=payload.title,
            hierarchy=payload.hierarchy,
            source_url=payload.source_url,
            content_hash=DocumentHash.from_text(raw),
            char_count=len(raw),
            raw_content=raw,
            classification_source=ClassificationSource.PRE_SEGMENTED_SOURCE,
            classification_confidence=1.0,
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
            source_url="https://www.in.gov.br",
            raw_content="RAW SUMMARY",
            total_acts=5,
            date_obj=date(2024, 1, 2),
        )

        result = pipeline.process_item(payload, spider)

        assert result == payload
        assert len(repo.saved_editions) == 1
        assert repo.saved_editions[0].territory_id.code == "BR"
        assert repo.saved_editions[0].total_acts == 5

    def test_process_raw_normative_act_item(self) -> None:
        """Scenario: Pipeline maps RawNormativeActPayload and saves to repository."""
        repo = DummyRepository()
        mapper = DummyMapper()
        pipeline = GazetteIngestionPipeline(repository=repo, mapper=mapper)

        spider = MagicMock(spec=Spider)
        spider.name = "test_spider"

        # First process edition
        edition_payload = RawGazettePayload(
            territory_code="BR",
            tier="federal",
            source_url="https://www.in.gov.br",
            date_obj=date(2024, 1, 2),
            section="secao_1",
            edition_number="1",
        )
        pipeline.process_item(edition_payload, spider)

        # Then process act
        act_payload = RawNormativeActPayload(
            territory_code="BR",
            source_url="https://www.in.gov.br/web/dou/-/portaria-1",
            raw_content="Art. 1º Fica instituído o comitê.",
            title="PORTARIA Nº 1",
            act_type="PORTARIA",
            date_obj=date(2024, 1, 2),
            section="secao_1",
            edition_number="1",
        )

        result = pipeline.process_item(act_payload, spider)
        assert result == act_payload
        assert len(repo.saved_acts) == 1
        assert repo.saved_acts[0].act_type == "PORTARIA"

    def test_process_non_payload_item_passthrough(self) -> None:
        """Scenario: Non-payload items pass through unchanged."""
        repo = DummyRepository()
        mapper = DummyMapper()
        pipeline = GazetteIngestionPipeline(repository=repo, mapper=mapper)

        spider = MagicMock(spec=Spider)
        other_item = {"some": "data"}

        result = pipeline.process_item(other_item, spider)

        assert result == other_item
        assert len(repo.saved_editions) == 0
        assert len(repo.saved_acts) == 0
