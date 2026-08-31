"""Centralized Configuration for the LEX Ecosystem.

Enforces fail-fast validation via pydantic-settings on startup, ensuring that
missing database DSNs or invalid concurrency parameters halt execution immediately.
"""

from typing import Self

from pydantic import Field, PostgresDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class LexSettings(BaseSettings):
    """Immutable, strongly typed system configuration."""

    model_config = SettingsConfigDict(
        env_prefix="LEX_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    database_url: PostgresDsn | None = Field(
        default=None,
        description="PostgreSQL 16 connection DSN (e.g. postgresql://user:pass@localhost:5432/lex)",
    )

    # In-Memory Stream Processing & Concurrency
    max_memory_spool_mb: int = Field(
        default=10,
        description="Maximum PDF payload size in MB before spooling to disk buffer",
        gt=0,
    )
    concurrent_requests_per_domain: int = Field(
        default=10,
        description="Scrapy max concurrent connections per individual government portal",
        gt=0,
    )
    autothrottle_enabled: bool = Field(
        default=True,
        description="Enable adaptive rate-limiting based on server response latency",
    )
    autothrottle_start_delay: float = Field(
        default=1.0,
        description="Initial delay in seconds for Scrapy AutoThrottle",
        gt=0.0,
    )
    autothrottle_max_delay: float = Field(
        default=15.0,
        description="Maximum delay in seconds for Scrapy AutoThrottle",
        gt=0.0,
    )
    autothrottle_target_concurrency: float = Field(
        default=5.0,
        description="Target average concurrent requests per domain",
        gt=0.0,
    )

    # Federal DOU Scraping Concurrency & Timeouts
    dou_concurrent_acts_semaphore: int = Field(
        default=25,
        description="Concurrency limit for discrete DOU act scraping per section",
        gt=0,
    )
    dou_http_timeout_seconds: float = Field(
        default=20.0,
        description="HTTP request timeout for DOU discrete act fetching",
        gt=0.0,
    )
    dou_max_connections: int = Field(
        default=50,
        description="HTTP client max connection pool size for DOU",
        gt=0,
    )
    dou_max_keepalive_connections: int = Field(
        default=30,
        description="HTTP client max keepalive connections for DOU",
        gt=0,
    )

    # Logging & Observability
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    log_file: str = Field(
        default="logs/crawler.log",
        description="Destination log file for Scrapy engine audit trail",
    )
    sentry_dsn: str = Field(
        default="",
        description="Optional Sentry DSN for error telemetry",
    )

    # Langfuse LLMOps Telemetry
    langfuse_public_key: str = Field(
        default="",
        description="Langfuse public key for generative AI tracing",
    )
    langfuse_secret_key: str = Field(
        default="",
        description="Langfuse secret key for generative AI tracing",
    )
    langfuse_host: str = Field(
        default="https://cloud.langfuse.com",
        description="Langfuse telemetry endpoint",
    )

    # API & Web Security
    cors_allowed_origins: list[str] = Field(
        default_factory=lambda: ["*"],
        description="Allowed origins for FastAPI CORS headers",
    )

    @model_validator(mode="after")
    def _validate_mandatory_settings(self) -> Self:
        """Enforces that database_url is provided via environment or settings."""
        if self.database_url is None:
            raise ValueError("Mandatory configuration missing: LEX_DATABASE_URL must be defined.")
        return self


_SETTINGS_INSTANCE: LexSettings | None = None


def get_settings() -> LexSettings:
    """Returns the cached singleton LexSettings instance, failing fast on invalid env."""
    global _SETTINGS_INSTANCE
    if _SETTINGS_INSTANCE is None:
        _SETTINGS_INSTANCE = LexSettings()
    return _SETTINGS_INSTANCE
