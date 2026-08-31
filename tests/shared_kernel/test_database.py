"""Unit Tests for Centralized Database Factory (ADR-009 §4.13).

Verifies engine connection pool bounds, pool recycling, singleton behavior,
and session factory creation across PostgreSQL and SQLite dialects (CWE-400).
"""

from sqlalchemy.pool import QueuePool

from lex.shared_kernel.database import (
    DEFAULT_MAX_OVERFLOW,
    DEFAULT_POOL_RECYCLE_SECONDS,
    DEFAULT_POOL_SIZE,
    get_engine,
    get_session_factory,
    get_singleton_engine,
)


class TestDatabaseFactory:
    """Test suite for centralized database factory and connection pool bounds."""

    def test_get_engine_postgresql_configures_bounded_pool(self) -> None:
        """Scenario: PostgreSQL engines configure bounded QueuePool with recycling."""
        dsn = "postgresql://user:pass@localhost:5432/lex_test"
        engine = get_engine(database_url=dsn)

        assert isinstance(engine.pool, QueuePool)
        assert engine.pool.size() == DEFAULT_POOL_SIZE
        assert engine.pool._max_overflow == DEFAULT_MAX_OVERFLOW
        assert engine.pool._recycle == DEFAULT_POOL_RECYCLE_SECONDS
        assert engine.pool._pre_ping is True

    def test_get_engine_sqlite_in_memory_compatibility(self) -> None:
        """Scenario: SQLite engines instantiate cleanly without incompatible pool kwargs."""
        engine = get_engine(database_url="sqlite:///:memory:")
        assert engine.dialect.name == "sqlite"

    def test_get_singleton_engine_returns_same_instance(self) -> None:
        """Scenario: get_singleton_engine caches and returns the process singleton."""
        engine1 = get_singleton_engine()
        engine2 = get_singleton_engine()
        assert engine1 is engine2

    def test_get_session_factory_creates_usable_sessions(self) -> None:
        """Scenario: get_session_factory returns sessionmaker bound to engine."""
        engine = get_engine(database_url="sqlite:///:memory:")
        factory = get_session_factory(engine=engine, expire_on_commit=False)

        with factory() as session:
            assert session.bind is engine
            assert session.expire_on_commit is False
