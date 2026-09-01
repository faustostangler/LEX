"""SQLAlchemy Declarative Models for Gazette and Normative Acts Persistence.

Maps the gazette_editions container table and the normative_acts SSOT table
with PostgreSQL 16 LZ4 TOAST compression, JSONB indexing, and natural unique constraints.
"""

import uuid
from datetime import UTC, date, datetime
from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Declarative Base for SQLAlchemy ORM models."""


class GazetteEditionModel(Base):
    """Relational model representing the gazette_editions container table."""

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
    summary_sha256: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    total_acts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    ingestion_status: Mapped[str] = mapped_column(String(30), default="completed", nullable=False)
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

    # Relationships
    normative_acts: Mapped[list["NormativeActModel"]] = relationship(
        back_populates="edition",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "territory_id",
            "date",
            "edition_number",
            "section",
            "is_extra_edition",
            name="uq_gazette_edition_natural_key",
            postgresql_nulls_not_distinct=True,
        ),
        Index("ix_gazette_editions_territory_date", "territory_id", "date"),
    )


class NormativeActModel(Base):
    """Relational model representing the normative_acts SSOT table."""

    __tablename__ = "normative_acts"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    edition_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("gazette_editions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    territory_id: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    section: Mapped[str | None] = mapped_column(String(50), nullable=True)
    edition_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_extra_edition: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    act_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    act_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    act_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    ementa: Mapped[str | None] = mapped_column(Text, nullable=True)
    hierarchy: Mapped[list[Any]] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"),
        default=list,
        nullable=False,
    )
    authority_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    authority_role: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_url: Mapped[str] = mapped_column(Text, nullable=False)
    content_sha256: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    char_count: Mapped[int] = mapped_column(Integer, nullable=False)
    raw_content: Mapped[str] = mapped_column(Text, nullable=False)
    structured_content: Mapped[dict[str, Any] | None] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"),
        nullable=True,
    )
    classification_source: Mapped[str] = mapped_column(
        String(30), default="pre_segmented_source", nullable=False
    )
    classification_confidence: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    hierarchical_group: Mapped[int] = mapped_column(SmallInteger, default=8, nullable=False)
    hierarchical_rank: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    publication_nature: Mapped[str] = mapped_column(
        String(30), default="publicidade_operacional", nullable=False
    )
    canonical_urn: Mapped[str | None] = mapped_column(String(350), nullable=True, index=True)
    is_stub: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    metadata_json: Mapped[dict[str, Any] | None] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"),
        nullable=True,
    )
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

    # Relationships
    edition: Mapped["GazetteEditionModel"] = relationship(back_populates="normative_acts")

    __table_args__ = (
        UniqueConstraint(
            "edition_id",
            "source_url",
            "content_sha256",
            name="uq_normative_act_natural_key",
        ),
        Index("ix_normative_acts_date_type", "date", "act_type"),
        Index("ix_normative_acts_territory_date", "territory_id", "date"),
        Index("ix_normative_acts_hierarchy", "hierarchical_group", text("date DESC")),
        Index("ix_normative_acts_nature", "publication_nature"),
        Index("ix_normative_acts_section", "section"),
        Index("ix_normative_acts_urn", "canonical_urn"),
        Index("ix_normative_acts_hierarchy_gin", "hierarchy", postgresql_using="gin"),
        Index(
            "ix_normative_acts_metadata_gin",
            "metadata_json",
            postgresql_using="gin",
        ),
        Index(
            "ix_normative_acts_pending_treatment",
            "id",
            postgresql_where=text("structured_content IS NULL"),
        ),
        Index(
            "ix_normative_acts_pending_triage",
            "id",
            postgresql_where=text("(metadata_json->>'triage_status') IS NULL"),
        ),
        Index(
            "ix_normative_acts_pending_treatment_sec",
            "section",
            "id",
            postgresql_where=text("structured_content IS NULL"),
        ),
        Index(
            "ix_normative_acts_pending_triage_sec",
            "section",
            "id",
            postgresql_where=text("(metadata_json->>'triage_status') IS NULL"),
        ),
        Index(
            "ix_normative_acts_pending_triage_arrow",
            "id",
            postgresql_where=text(
                "(metadata_json -> 'triage_status') IS NULL "
                "AND publication_nature IN ('concreta_individual', 'publicidade_operacional')"
            ),
        ),
        Index(
            "ix_normative_acts_pending_triage_arrow_inc",
            "id",
            postgresql_include=["section"],
            postgresql_where=text(
                "(metadata_json -> 'triage_status') IS NULL "
                "AND publication_nature IN ('concreta_individual', 'publicidade_operacional')"
            ),
        ),
    )
