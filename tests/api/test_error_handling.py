"""API Integration Tests for Centralized Exception Handling and RFC-7807 Compliance.

Tests that unhandled database and infrastructure exceptions are sanitized, logged with trace_id,
and never leak internal schema or queries to HTTP clients (CWE-209 mitigation).
"""

import uuid
from collections.abc import Generator

import pytest
from fastapi import APIRouter
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from lex.api.main import create_app
from lex.ingestion.infrastructure.persistence.models import Base


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Hermetic in-memory SQLite database session."""
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
    """FastAPI TestClient with extra simulated fault routes for error testing."""
    app = create_app(session=db_session)
    fault_router = APIRouter(prefix="/api/v1/faults", tags=["Fault Testing"])

    @fault_router.get("/sqlalchemy-error")
    def trigger_sqlalchemy_error() -> None:
        raise OperationalError(
            statement="SELECT * FROM secret_internal_table WHERE id = 1",
            params={},
            orig=Exception("FATAL: relation 'secret_internal_table' does not exist"),
        )

    @fault_router.get("/unhandled-exception")
    def trigger_unhandled_exception() -> None:
        raise RuntimeError("Internal infra failure: secret_token_xyz_12345 leaked")

    app.include_router(fault_router)
    return TestClient(app, raise_server_exceptions=False)


class TestApiErrorHandling:
    """Test suite for API exception sanitization and RFC-7807 compliance."""

    def test_unhandled_sqlalchemy_error_sanitized(self, client: TestClient) -> None:
        """Asserts that SQLAlchemy errors return RFC-7807 500 without leaking SQL details."""
        response = client.get("/api/v1/faults/sqlalchemy-error")
        assert response.status_code == 500

        data = response.json()
        assert data["status"] == 500
        assert data["title"] == "Internal Database Error"
        assert "trace_id" in data
        assert data["instance"] == "/api/v1/faults/sqlalchemy-error"
        assert "Please contact support with the trace_id" in data["detail"]

        # Ensure no SQL or table names leak to client (CWE-209 mitigation)
        assert "secret_internal_table" not in response.text
        assert "relation 'secret_internal_table' does not exist" not in response.text

        # Verify trace header
        assert "X-Trace-ID" in response.headers
        assert response.headers["X-Trace-ID"] == data["trace_id"]

    def test_unhandled_generic_exception_sanitized(self, client: TestClient) -> None:
        """Asserts that general unexpected exceptions return RFC-7807 500 sanitized."""
        response = client.get("/api/v1/faults/unhandled-exception")
        assert response.status_code == 500

        data = response.json()
        assert data["status"] == 500
        assert data["title"] == "Internal Server Error"
        assert "trace_id" in data
        assert data["instance"] == "/api/v1/faults/unhandled-exception"

        # Ensure internal sensitive exception message is omitted
        assert "secret_token_xyz_12345" not in response.text

        # Verify trace header
        assert "X-Trace-ID" in response.headers
        assert response.headers["X-Trace-ID"] == data["trace_id"]

    def test_custom_trace_id_propagated(self, client: TestClient) -> None:
        """Asserts that client-supplied X-Request-ID is preserved across error responses."""
        custom_trace = str(uuid.uuid4())
        response = client.get(
            "/api/v1/faults/unhandled-exception",
            headers={"X-Request-ID": custom_trace},
        )
        assert response.status_code == 500
        data = response.json()
        assert data["trace_id"] == custom_trace
        assert response.headers["X-Trace-ID"] == custom_trace

    def test_health_check_includes_trace_id(self, client: TestClient) -> None:
        """Asserts that successful 200 responses also receive X-Trace-ID header."""
        response = client.get("/health")
        assert response.status_code == 200
        assert "X-Trace-ID" in response.headers
