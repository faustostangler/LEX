"""Unit and Integration Tests for PostgresConsolidationRepository.

Tests persistence and retrieval of mutations, backfill tasks, and compiled acts.
"""

import uuid
from collections.abc import Generator
from datetime import UTC, date, datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from lex.consolidation.domain.entities import (
    CompiledNormativeAct,
    LegislationBackfillTask,
)
from lex.consolidation.domain.value_objects import CanonicalUrn
from lex.consolidation.infrastructure.persistence.postgres_repository import (
    PostgresConsolidationRepository,
)
from lex.ingestion.domain.entities import GazetteEdition, NormativeAct
from lex.ingestion.domain.value_objects import (
    DocumentHash,
    FederativeTier,
    GazetteDate,
    TerritoryId,
)
from lex.ingestion.infrastructure.persistence.models import Base
from lex.ingestion.infrastructure.persistence.postgres_repository import (
    PostgresGazetteRepository,
)
from lex.treatment.domain.entities import ActAst, DispositivoNode, NormativeActMutation
from lex.treatment.domain.value_objects import (
    CanonicalNodePath,
    DispositivoType,
    MutationType,
)


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Hermetic SQLite database session for unit testing."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


class TestPostgresConsolidationRepository:
    """Test suite for PostgresConsolidationRepository."""

    def test_save_and_retrieve_mutations(self, db_session: Session) -> None:
        """Asserts saving and chronological retrieval of mutations."""
        gazette_repo = PostgresGazetteRepository(session=db_session)
        consolidation_repo = PostgresConsolidationRepository(session=db_session)

        # Create parent edition and acts
        edition_id = uuid.uuid4()
        target_act_id = uuid.uuid4()
        author_act_id = uuid.uuid4()

        edition = GazetteEdition(
            id=edition_id,
            territory_id=TerritoryId.from_code("BR"),
            tier=FederativeTier.FEDERAL,
            date=GazetteDate.from_date(date(2020, 1, 1)),
            source_url="https://in.gov.br/ed1",
            summary_hash=DocumentHash.from_text("sum"),
            scraped_at=datetime.now(UTC),
        )
        gazette_repo.save(edition)

        target_act = NormativeAct(
            id=target_act_id,
            edition_id=edition_id,
            territory_id=TerritoryId.from_code("BR"),
            date=GazetteDate.from_date(date(2020, 1, 1)),
            act_type="LEI",
            title="Lei nº 10.000/2020",
            source_url="https://in.gov.br/act1",
            content_hash=DocumentHash.from_text("c1"),
            char_count=10,
            raw_content="Texto base",
            scraped_at=datetime.now(UTC),
        )
        author_act = NormativeAct(
            id=author_act_id,
            edition_id=edition_id,
            territory_id=TerritoryId.from_code("BR"),
            date=GazetteDate.from_date(date(2024, 1, 1)),
            act_type="LEI",
            title="Lei nº 12.000/2024",
            source_url="https://in.gov.br/act2",
            content_hash=DocumentHash.from_text("c2"),
            char_count=10,
            raw_content="Texto alterador",
            scraped_at=datetime.now(UTC),
        )
        gazette_repo.save_normative_acts_bulk([target_act, author_act])

        # Save mutation
        m = NormativeActMutation(
            target_act_id=target_act_id,
            target_node_path=CanonicalNodePath.from_string("art_1"),
            author_act_id=author_act_id,
            mutation_type=MutationType.ALTERACAO_NR,
            new_text="Novo texto (NR)",
            publication_date=GazetteDate.from_date(date(2024, 1, 1)),
            effective_date=GazetteDate.from_date(date(2024, 1, 1)),
            extraction_source="lc95",
            confidence_score=1.0,
            mutation_sha256=DocumentHash.from_text("hash"),
        )
        consolidation_repo.save_mutation(m)

        # Retrieve
        mutations = consolidation_repo.get_mutations_for_act(target_act_id)
        assert len(mutations) == 1
        assert mutations[0].target_node_path.value == "art_1"
        assert mutations[0].new_text == "Novo texto (NR)"

    def test_save_and_retrieve_compiled_act(self, db_session: Session) -> None:
        """Asserts saving and retrieving a compiled normative act."""
        gazette_repo = PostgresGazetteRepository(session=db_session)
        consolidation_repo = PostgresConsolidationRepository(session=db_session)

        edition_id = uuid.uuid4()
        act_id = uuid.uuid4()
        edition = GazetteEdition(
            id=edition_id,
            territory_id=TerritoryId.from_code("BR"),
            tier=FederativeTier.FEDERAL,
            date=GazetteDate.from_date(date(2020, 1, 1)),
            source_url="https://in.gov.br/ed1",
            summary_hash=DocumentHash.from_text("sum"),
            scraped_at=datetime.now(UTC),
        )
        gazette_repo.save(edition)
        act = NormativeAct(
            id=act_id,
            edition_id=edition_id,
            territory_id=TerritoryId.from_code("BR"),
            date=GazetteDate.from_date(date(2020, 1, 1)),
            act_type="LEI",
            title="Lei nº 10.000/2020",
            source_url="https://in.gov.br/act1",
            content_hash=DocumentHash.from_text("c1"),
            char_count=10,
            raw_content="Texto base",
            canonical_urn="urn:lex:br:federal:lei:2020;10000",
            scraped_at=datetime.now(UTC),
        )
        gazette_repo.save_normative_acts_bulk([act])

        art1 = DispositivoNode(
            node_path=CanonicalNodePath.from_string("art_1"),
            node_type=DispositivoType.ARTIGO,
            label="Art. 1º",
            text="Texto compilado.",
        )
        ast = ActAst(
            act_id=act_id,
            canonical_urn="urn:lex:br:federal:lei:2020;10000",
            title="Lei nº 10.000/2020",
            nodes=[art1],
        )
        compiled = CompiledNormativeAct(
            act_id=act_id,
            compiled_version_hash="a" * 64,
            total_mutations_applied=0,
            compiled_ast=ast,
            compiled_html="<h1>Lei 10000</h1>",
            compiled_markdown="# Lei 10000",
            active_articles_count=1,
            revoked_articles_count=0,
            last_compiled_at=datetime.now(UTC),
        )

        consolidation_repo.save_compiled_act(compiled)

        retrieved = consolidation_repo.get_compiled_act(act_id)
        assert retrieved is not None
        assert retrieved.compiled_version_hash == "a" * 64
        assert retrieved.compiled_html == "<h1>Lei 10000</h1>"

    def test_backfill_queue_priority(self, db_session: Session) -> None:
        """Asserts enqueueing and citation count incrementing in backfill queue."""
        consolidation_repo = PostgresConsolidationRepository(session=db_session)
        urn = CanonicalUrn.from_string("urn:lex:br:federal:lei:1993;8666")

        task = LegislationBackfillTask(
            canonical_urn=urn,
            territory_id="BR",
            act_type="Lei",
            act_number="8666",
            act_year=1993,
            citation_count=1,
            last_requested_at=datetime.now(UTC),
        )

        # Enqueue once
        consolidation_repo.enqueue_backfill_task(task)
        # Enqueue second time -> increments citation count
        consolidation_repo.enqueue_backfill_task(task)

        queue = consolidation_repo.get_backfill_queue(limit=10)
        assert len(queue) == 1
        assert queue[0].canonical_urn == urn
        assert queue[0].citation_count == 2
