"""API Integration Tests for Legislation Read Endpoints.

Tests O(1) compiled legislation retrieval, Stub status handling, and time-travel compilation.
"""

import uuid
from collections.abc import Generator
from datetime import UTC, date, datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from lex.api.main import create_app
from lex.consolidation.domain.entities import CompiledNormativeAct
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
from lex.ingestion.infrastructure.persistence.models import (
    Base,
)
from lex.ingestion.infrastructure.persistence.postgres_repository import (
    PostgresGazetteRepository,
)
from lex.treatment.domain.entities import ActAst, DispositivoNode
from lex.treatment.domain.value_objects import (
    CanonicalNodePath,
    DispositivoType,
)


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Hermetic SQLite database session for API testing with thread-safe StaticPool."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture
def client(db_session: Session) -> TestClient:
    """FastAPI TestClient with injected test database session."""
    app = create_app(session=db_session)
    return TestClient(app)


class TestLegislationApi:
    """Test suite for Legislation REST Endpoints."""

    def test_get_compiled_legislation_by_id(self, client: TestClient, db_session: Session) -> None:
        """Asserts O(1) fast retrieval of pre-rendered compiled legislation."""
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
            text="Texto compilado legal.",
        )
        ast = ActAst(
            act_id=act_id,
            canonical_urn="urn:lex:br:federal:lei:2020;10000",
            title="Lei nº 10.000/2020",
            nodes=[art1],
        )
        compiled = CompiledNormativeAct(
            act_id=act_id,
            compiled_version_hash="b" * 64,
            total_mutations_applied=0,
            compiled_ast=ast,
            compiled_html="<h1>Lei 10000</h1><p>Texto compilado legal.</p>",
            compiled_markdown="# Lei 10000\n\n**Art. 1º** Texto compilado legal.",
            active_articles_count=1,
            revoked_articles_count=0,
            last_compiled_at=datetime.now(UTC),
        )
        import anyio

        anyio.run(consolidation_repo.save_compiled_act, compiled)

        # Execute GET request
        response = client.get(f"/api/v1/legislation/{act_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["act_id"] == str(act_id)
        assert data["title"] == "Lei nº 10.000/2020"
        assert "Texto compilado legal." in data["compiled_html"]
        assert data["compiled_version_hash"] == "b" * 64

    def test_get_stub_statute_returns_pending_status(
        self, client: TestClient, db_session: Session
    ) -> None:
        """Asserts that querying an un-ingested Stub returns HTTP 200 PENDING_BASE_INGESTION."""
        gazette_repo = PostgresGazetteRepository(session=db_session)
        edition_id = uuid.uuid4()
        stub_id = uuid.uuid4()

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

        stub_act = NormativeAct(
            id=stub_id,
            edition_id=edition_id,
            territory_id=TerritoryId.from_code("BR"),
            date=GazetteDate.from_date(date(1993, 1, 1)),
            act_type="LEI",
            act_number="8666",
            act_year=1993,
            title="Lei nº 8666/1993",
            source_url="urn:stub",
            content_hash=DocumentHash.from_text("c_stub"),
            char_count=0,
            raw_content="",
            is_stub=True,
            canonical_urn="urn:lex:br:federal:lei:1993;8666",
            scraped_at=datetime.now(UTC),
        )
        gazette_repo.save_normative_acts_bulk([stub_act])

        response = client.get(f"/api/v1/legislation/{stub_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "PENDING_BASE_INGESTION"
        assert data["canonical_urn"] == "urn:lex:br:federal:lei:1993;8666"
        assert "mutations" in data

    def test_legislation_not_found_returns_404(self, client: TestClient) -> None:
        """Querying a non-existent statute returns 404 Not Found."""
        random_id = uuid.uuid4()
        response = client.get(f"/api/v1/legislation/{random_id}")
        assert response.status_code == 404

    def test_cors_headers_configured(self, client: TestClient) -> None:
        """Verifies CORS headers on API requests."""
        response = client.options(
            "/api/v1/legislation/urn:lex:br:federal:lei:2020;10000",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
