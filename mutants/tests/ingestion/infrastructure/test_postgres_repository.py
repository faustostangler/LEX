"""Precision Unit & Integration Tests for PostgresGazetteRepository.

Verifies persistence, retrieval, and idempotent deduplication specified in
SPEC-001 (Section 4 Scenario 2).
"""

from collections.abc import Generator
from datetime import UTC, date, datetime
import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from lex.ingestion.domain.entities import GazetteEdition
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
    territory_code: str = "SP",
    tier: FederativeTier = FederativeTier.STATE,
    pub_date: date | None = None,
    section: str | None = "executivo_1",
    full_text: str = "GOVERNO DO ESTADO DE SÃO PAULO - DIÁRIO OFICIAL",
) -> GazetteEdition:
    """Helper to instantiate test entities."""
    clean = full_text.strip()
    return GazetteEdition(
        id=uuid.uuid4(),
        territory_id=TerritoryId.from_code(territory_code),
        tier=tier,
        date=GazetteDate.from_date(pub_date or date(2024, 5, 10)),
        section=section,
        edition_number="12345",
        is_extra_edition=False,
        power="executive",
        source_url="https://doe.sp.gov.br/visualizar?data=2024-05-10",
        file_hash=DocumentHash.from_text(clean),
        char_count=len(clean),
        full_text=clean,
        scraped_at=datetime(2024, 5, 10, 10, 0, 0, tzinfo=UTC),
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
        assert retrieved.territory_id.code == "SP"
        assert retrieved.tier == FederativeTier.STATE
        assert retrieved.date.value == date(2024, 5, 10)
        assert retrieved.full_text == edition.full_text
        assert retrieved.file_hash.hex_digest == edition.file_hash.hex_digest

    def test_idempotent_save_on_duplicate(self, db_session: Session) -> None:
        """Scenario: Saving the same edition on re-crawl does not duplicate rows."""
        repo = PostgresGazetteRepository(session=db_session)
        edition1 = make_test_edition()
        repo.save(edition1)

        # Re-encounter same edition on later crawl run
        edition2 = make_test_edition(
            full_text="GOVERNO DO ESTADO DE SÃO PAULO - DIÁRIO OFICIAL (UPDATED SCAN)",
        )
        repo.save(edition2)

        retrieved = repo.get_by_territory_and_date(
            territory_id=edition1.territory_id,
            date=edition1.date,
            section=edition1.section,
        )

        assert retrieved is not None
        assert "UPDATED SCAN" in retrieved.full_text

    def test_exists_by_hash_true_and_false(self, db_session: Session) -> None:
        """Scenario: Check hash existence in repository."""
        repo = PostgresGazetteRepository(session=db_session)
        edition = make_test_edition()
        repo.save(edition)

        assert repo.exists_by_hash(edition.file_hash) is True

        unknown_hash = DocumentHash.from_text("COMPLETELY DIFFERENT CONTENT")
        assert repo.exists_by_hash(unknown_hash) is False
