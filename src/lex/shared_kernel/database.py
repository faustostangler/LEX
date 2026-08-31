"""Database Engine and Connection Pool Factory for LEX System (ADR-009 §4.13).

Provides centralized, bounded, and recycle-safe SQLAlchemy Engine management
preventing QueuePool exhaustion and stale connection leaks (CWE-400 mitigation).
"""

from functools import lru_cache
from typing import Any

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from lex.shared_kernel.config import get_settings

# Standard Connection Pool Operational Constants (ADR-009 §4.13)
DEFAULT_POOL_SIZE: int = 5
DEFAULT_MAX_OVERFLOW: int = 5
DEFAULT_POOL_TIMEOUT_SECONDS: int = 30
DEFAULT_POOL_RECYCLE_SECONDS: int = 1800  # Recycle after 30 minutes


def get_engine(
    database_url: str | None = None,
    pool_size: int = DEFAULT_POOL_SIZE,
    max_overflow: int = DEFAULT_MAX_OVERFLOW,
    pool_recycle: int = DEFAULT_POOL_RECYCLE_SECONDS,
    pool_pre_ping: bool = True,
    echo: bool = False,
    **kwargs: Any,
) -> Engine:
    """Creates a bounded, pre-ping verified SQLAlchemy Engine (CWE-400 mitigation).

    Args:
        database_url: Target database DSN. If None, loaded from LexSettings.
        pool_size: Base connection pool capacity (default: 5).
        max_overflow: Maximum connections allowed beyond pool_size (default: 5).
        pool_recycle: Lifetime before refreshing idle connections (default: 1800s).
        pool_pre_ping: Issue health check before handing out connections.
        echo: If True, log SQL statements.
        **kwargs: Additional arguments passed to create_engine.

    Returns:
        SQLAlchemy Engine instance with hardened connection pool bounds.
    """
    if database_url is None:
        settings = get_settings()
        database_url = str(settings.database_url)

    # SQLite (e.g. memory testing) does not accept pool_size/max_overflow with StaticPool/NullPool
    if database_url.startswith("sqlite"):
        return create_engine(database_url, echo=echo, **kwargs)

    return create_engine(
        database_url,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_timeout=DEFAULT_POOL_TIMEOUT_SECONDS,
        pool_recycle=pool_recycle,
        pool_pre_ping=pool_pre_ping,
        echo=echo,
        **kwargs,
    )


@lru_cache(maxsize=1)
def get_singleton_engine() -> Engine:
    """Returns a singleton Engine instance for process-level reuse."""
    return get_engine()


def get_session_factory(
    engine: Engine | None = None,
    expire_on_commit: bool = True,
) -> sessionmaker[Session]:
    """Creates a sessionmaker bound to the centralized engine."""
    eng = engine or get_singleton_engine()
    return sessionmaker(bind=eng, expire_on_commit=expire_on_commit)
