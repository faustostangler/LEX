"""Unit and Integration Tests for PostgresTreatmentRepository.

Verifies persistence of AST, NER metadata, and atomic auto-materialization of
Stub entities for un-ingested target laws (CRIT-02 & ADR-010).
"""

import uuid
from collections.abc import Generator
from datetime import UTC, date, datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from lex.consolidation.infrastructure.persistence.models import (
    LegislationBackfillQueueModel,
    NormativeActMutationModel,
)
from lex.ingestion.domain.value_objects import (
    DocumentHash,
    GazetteDate,
)
from lex.ingestion.infrastructure.persistence.models import (
    Base,
    GazetteEditionModel,
    NormativeActModel,
)
from lex.treatment.domain.entities import NormativeActMutation
from lex.treatment.domain.value_objects import (
    CanonicalNodePath,
    MutationType,
)
from lex.treatment.infrastructure.persistence.postgres_repository import (
    PostgresTreatmentRepository,
)


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Hermetic in-memory SQLite database session."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


class TestPostgresTreatmentRepository:
    """Test suite for PostgresTreatmentRepository."""

    @pytest.mark.anyio
    async def test_save_mutations_for_un_ingested_target_auto_creates_stub(
        self, db_session: Session
    ) -> None:
        """Scenario: Saving mutations for un-ingested base statute creates a Stub act (ADR-010)."""
        # 1. Setup author act in DB
        edition = GazetteEditionModel(
            id=uuid.uuid4(),
            territory_id="BR",
            tier="federal",
            date=date(2024, 1, 15),
            edition_number="10",
            section="1",
            is_extra_edition=False,
            power="executive",
            source_url="https://in.gov.br/dou/2024-01-15",
            summary_sha256="author_edition_hash".ljust(64, "0"),
            total_acts=1,
            ingestion_status="completed",
            scraped_at=datetime.now(UTC),
        )
        db_session.add(edition)
        db_session.flush()

        author_act_id = uuid.uuid4()
        author_act = NormativeActModel(
            id=author_act_id,
            edition_id=edition.id,
            territory_id="BR",
            date=date(2024, 1, 15),
            section="1",
            edition_number="10",
            is_extra_edition=False,
            act_type="LEI",
            act_number="14.800",
            act_year=2024,
            title="Lei nº 14.800/2024",
            ementa="Altera a Lei nº 8.666/1993",
            hierarchy=[],
            source_url="https://in.gov.br/act/14800",
            content_sha256="author_act_content_hash".ljust(64, "0"),
            char_count=500,
            raw_content="Lei 14800 raw content",
            classification_source="pre_segmented_source",
            classification_confidence=1.0,
            hierarchical_group=1,
            hierarchical_rank=70,
            publication_nature="normativa_abstrata",
            canonical_urn="urn:lex:br:federal:lei:2024-01-15;14800",
            is_stub=False,
            scraped_at=datetime.now(UTC),
        )
        db_session.add(author_act)
        db_session.commit()

        # 2. Target act (Lei 8.666/1993) does NOT exist in DB
        target_urn = "urn:lex:br:federal:lei:1993;8666"
        target_act_id = uuid.uuid5(uuid.NAMESPACE_DNS, target_urn)
        assert db_session.get(NormativeActModel, target_act_id) is None

        # 3. Create mutation referencing target_act_id
        mut = NormativeActMutation(
            id=uuid.uuid4(),
            target_act_id=target_act_id,
            target_node_path=CanonicalNodePath.from_string("art_3.inc_1"),
            author_act_id=author_act_id,
            mutation_type=MutationType.ALTERACAO_NR,
            new_text="I - legalidade e eficiência; (NR)",
            publication_date=GazetteDate.from_date(date(2024, 1, 15)),
            effective_date=GazetteDate.from_date(date(2024, 1, 15)),
            extraction_source="lc95_deterministic_regex",
            confidence_score=1.0,
            mutation_sha256=DocumentHash.from_text("mutation_test_hash"),
            target_canonical_urn=target_urn,
            target_title="Lei nº 8.666/1993",
            target_act_type="LEI",
            target_act_number="8.666",
            target_act_year=1993,
        )

        repo = PostgresTreatmentRepository(session=db_session)
        await repo.save_mutations([mut])

        # 4. Assert Stub entity auto-creation and domain invariant compliance
        stub_act = db_session.get(NormativeActModel, target_act_id)
        assert stub_act is not None
        assert stub_act.is_stub is True
        assert stub_act.canonical_urn == target_urn
        assert stub_act.act_year == 1993
        assert stub_act.act_type == "LEI"
        assert stub_act.source_url.startswith("https://")
        assert len(stub_act.content_sha256) == 64
        assert int(stub_act.content_sha256, 16) > 0  # Valid hex SHA-256

        # Assert pure domain re-hydration succeeds without DomainInvariantViolationError
        from lex.ingestion.infrastructure.persistence.postgres_repository import (
            PostgresGazetteRepository,
        )
        gazette_repo = PostgresGazetteRepository(session=db_session)
        domain_act = gazette_repo.to_domain_act(stub_act)
        assert domain_act.is_stub is True
        assert domain_act.canonical_urn == target_urn

        # 5. Assert Backfill Queue item creation
        backfill_item = (
            db_session.query(LegislationBackfillQueueModel)
            .filter_by(canonical_urn=target_urn)
            .first()
        )
        assert backfill_item is not None
        assert backfill_item.citation_count == 1
        assert backfill_item.status == "PENDING"

        # 6. Assert Mutation persistence
        saved_mut = db_session.get(NormativeActMutationModel, mut.id)
        assert saved_mut is not None
        assert saved_mut.target_act_id == target_act_id
        assert saved_mut.author_act_id == author_act_id
