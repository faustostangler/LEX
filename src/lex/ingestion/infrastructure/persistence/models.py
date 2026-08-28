"""SQLAlchemy Declarative Models for Gazette Ingestion Persistence.

Maps the gazette_editions relational table with TOAST-compressed full_text
and natural composite unique indexes specified in SPEC-001 (Section 2 & 4).
"""

import uuid
from datetime import UTC, date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Declarative Base for SQLAlchemy ORM models."""


class GazetteEditionModel(Base):
    """Relational model representing the gazette_editions table."""

    __tablename__ = "gazette_editions"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    territory_id: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    tier: Mapped[str] = mapped_column(String(20), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    edition_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    section: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_extra_edition: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    power: Mapped[str] = mapped_column(String(30), default="executive", nullable=False)
    source_url: Mapped[str] = mapped_column(Text, nullable=False)
    content_sha256: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    char_count: Mapped[int] = mapped_column(Integer, nullable=False)
    full_text: Mapped[str] = mapped_column(Text, nullable=False)
    scraped_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "territory_id",
            "date",
            "edition_number",
            "section",
            "is_extra_edition",
            name="uq_gazette_edition_natural_key",
        ),
        Index("ix_gazette_editions_territory_date", "territory_id", "date"),
    )
