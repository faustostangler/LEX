"""Main FastAPI Application Entrypoint for the LEX Ecosystem.

Provides Swagger OpenAPI documentation, CORS, and dependency injection for REST routes.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from lex.api.v1.legislation import get_db_session
from lex.api.v1.legislation import router as legislation_router
from lex.shared_kernel.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager configuring database connection pools."""
    settings = get_settings()
    engine = create_engine(str(settings.database_url), echo=False)
    session_factory = sessionmaker(bind=engine)
    app.state.session_factory = session_factory
    yield
    engine.dispose()


def create_app(session: Session | None = None) -> FastAPI:
    """Application factory for the LEX REST API."""
    app = FastAPI(
        title="LEX Legislation and Regulatory API",
        description=(
            "High-performance compiled legislation, CQRS mutation ledgers, "
            "and official gazette search."
        ),
        version="1.0.0",
        lifespan=None if session is not None else lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if session is not None:
        app.dependency_overrides[get_db_session] = lambda: session
    else:

        def _get_session_from_app() -> Session:
            session_factory = getattr(app.state, "session_factory", None)
            if session_factory is None:
                settings = get_settings()
                engine = create_engine(str(settings.database_url), echo=False)
                session_factory = sessionmaker(bind=engine)
                app.state.session_factory = session_factory
            return session_factory()

        app.dependency_overrides[get_db_session] = _get_session_from_app

    app.include_router(legislation_router, prefix="/api/v1")

    @app.get("/health", tags=["Health"])
    async def health_check() -> dict[str, str]:
        """Liveness health check endpoint."""
        return {"status": "ok", "service": "lex-api"}

    return app


app = create_app()
