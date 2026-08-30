"""Precision Unit & Integration Tests for PostgresGazetteRepository.

Verifies persistence, retrieval, and idempotent deduplication of GazetteEditions and NormativeActs
specified in ADR-002, ADR-006, and ADR-007.
"""

import uuid
from collections.abc import Generator
from datetime import UTC, date, datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from lex.ingestion.domain.entities import GazetteEdition, NormativeAct
from lex.ingestion.domain.value_objects import (
    ClassificationSource,
    DocumentHash,
    FederativeTier,
    GazetteDate,
    IngestionStatus,
    TerritoryId,
)
from lex.ingestion.infrastructure.persistence.models import Base
from lex.ingestion.infrastructure.persistence.postgres_repository import (
    PostgresGazetteRepository,
)
from lex.shared_kernel.value_objects import (
    HierarchicalGroup,
    HierarchicalRank,
    PublicationNature,
)


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """In-memory SQLite database session for hermetic unit testing."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


def make_test_edition(
    territory_code: str = "BR",
    tier: FederativeTier = FederativeTier.FEDERAL,
    pub_date: date | None = None,
    section: str | None = "secao_1",
    total_acts: int = 25,
) -> GazetteEdition:
    """Helper to instantiate test edition entities."""
    return GazetteEdition(
        id=uuid.uuid4(),
        territory_id=TerritoryId.from_code(territory_code),
        tier=tier,
        date=GazetteDate.from_date(pub_date or date(2024, 1, 15)),
        section=section,
        edition_number="10",
        is_extra_edition=False,
        power="executive",
        source_url="https://www.in.gov.br/leiturajornal?data=15-01-2024&secao=do1",
        summary_hash=DocumentHash.from_text("summary-hash-test"),
        total_acts=total_acts,
        ingestion_status=IngestionStatus.COMPLETED,
        scraped_at=datetime(2024, 1, 15, 10, 0, 0, tzinfo=UTC),
    )


def make_test_act(
    edition_id: uuid.UUID,
    title: str = "PORTARIA Nº 1, DE 15 DE JANEIRO DE 2024",
    act_type: str = "PORTARIA",
    act_number: str = "1",
    hierarchical_group: HierarchicalGroup = HierarchicalGroup.GRUPO_4_ORDINATORIO_MINISTERIAL,
    hierarchical_rank: int = int(HierarchicalRank.PORTARIA_NORMATIVA),
    publication_nature: PublicationNature = PublicationNature.NORMATIVA_ABSTRATA,
    canonical_urn: str = "urn:lex:br:federal:portaria:2024;1",
) -> NormativeAct:
    """Helper to instantiate test normative act entities."""
    raw = "Art. 1º Fica instituído o comitê executivo."
    return NormativeAct(
        id=uuid.uuid4(),
        edition_id=edition_id,
        territory_id=TerritoryId.from_code("BR"),
        date=GazetteDate.from_date(date(2024, 1, 15)),
        section="secao_1",
        edition_number="10",
        act_type=act_type,
        act_number=act_number,
        act_year=2024,
        title=title,
        hierarchy=["Ministério da Fazenda"],
        authority_name="MINISTRO DE ESTADO",
        source_url=f"https://www.in.gov.br/web/dou/-/{act_type.lower()}-{act_number}",
        content_hash=DocumentHash.from_text(raw),
        char_count=len(raw),
        raw_content=raw,
        classification_source=ClassificationSource.PRE_SEGMENTED_SOURCE,
        classification_confidence=1.0,
        hierarchical_group=hierarchical_group,
        hierarchical_rank=hierarchical_rank,
        publication_nature=publication_nature,
        canonical_urn=canonical_urn,
        is_stub=False,
        scraped_at=datetime(2024, 1, 15, 10, 0, 0, tzinfo=UTC),
    )


class TestPostgresGazetteRepository:
    """Acceptance tests for PostgresGazetteRepository."""

    def test_save_and_retrieve_edition(self, db_session: Session) -> None:
        """Scenario: Persist a valid GazetteEdition and retrieve it by territory and date."""
        repo = PostgresGazetteRepository(session=db_session)
        edition = make_test_edition()

        repo.save(edition)

        retrieved = repo.get_by_territory_and_date(
            territory_id=edition.territory_id,
            date=edition.date,
            section=edition.section,
        )

        assert retrieved is not None
        assert retrieved.territory_id.code == "BR"
        assert retrieved.tier == FederativeTier.FEDERAL
        assert retrieved.date.value == date(2024, 1, 15)
        assert retrieved.total_acts == 25

    def test_save_and_retrieve_normative_acts(self, db_session: Session) -> None:
        """Scenario: Persist discrete normative acts with hierarchical data and URNs."""
        repo = PostgresGazetteRepository(session=db_session)
        edition = make_test_edition()
        repo.save(edition)

        act1 = make_test_act(
            edition_id=edition.id,  # type: ignore[arg-type]
            title="PORTARIA Nº 1",
            act_type="PORTARIA",
            act_number="1",
            hierarchical_group=HierarchicalGroup.GRUPO_4_ORDINATORIO_MINISTERIAL,
            hierarchical_rank=40,
            publication_nature=PublicationNature.NORMATIVA_ABSTRATA,
            canonical_urn="urn:lex:br:federal:portaria:2024;1",
        )
        act2 = make_test_act(
            edition_id=edition.id,  # type: ignore[arg-type]
            title="DECRETO Nº 2",
            act_type="DECRETO",
            act_number="2",
            hierarchical_group=HierarchicalGroup.GRUPO_2_EXECUTIVO,
            hierarchical_rank=60,
            publication_nature=PublicationNature.NORMATIVA_ABSTRATA,
            canonical_urn="urn:lex:br:federal:decreto:2024;2",
        )

        repo.save_normative_acts_bulk([act1, act2])

        acts = repo.find_acts_by_edition(edition.id)  # type: ignore[arg-type]
        assert len(acts) == 2
        assert {a.act_type for a in acts} == {"PORTARIA", "DECRETO"}

        retrieved_act = repo.get_act_by_id(act1.id)  # type: ignore[arg-type]
        assert retrieved_act is not None
        assert retrieved_act.title == "PORTARIA Nº 1"
        assert retrieved_act.authority_name == "MINISTRO DE ESTADO"
        assert retrieved_act.hierarchical_group == HierarchicalGroup.GRUPO_4_ORDINATORIO_MINISTERIAL
        assert retrieved_act.hierarchical_rank == 40
        assert retrieved_act.publication_nature == PublicationNature.NORMATIVA_ABSTRATA
        assert retrieved_act.canonical_urn == "urn:lex:br:federal:portaria:2024;1"
        assert retrieved_act.is_stub is False

    def test_exists_by_hash_true_and_false(self, db_session: Session) -> None:
        """Scenario: Check hash existence in repository."""
        repo = PostgresGazetteRepository(session=db_session)
        edition = make_test_edition()
        repo.save(edition)

        assert repo.exists_by_hash(edition.summary_hash) is True

        unknown_hash = DocumentHash.from_text("COMPLETELY DIFFERENT CONTENT")
        assert repo.exists_by_hash(unknown_hash) is False
