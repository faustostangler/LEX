"""SQLAlchemy Declarative Models for the Consolidation Bounded Context.

Maps the CQRS Mutation Ledger, JIT Backfill Discovery Queue, and Materialized
Compiled Normative Acts Read Model with PostgreSQL 16 LZ4 TOAST and JSONB indexing.
"""

import uuid
from datetime import UTC, date, datetime
from typing import Any

from sqlalchemy import (
    JSON,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from lex.ingestion.infrastructure.persistence.models import Base


class NormativeActMutationModel(Base):
    """Relational model for the immutable Write Model normative_act_mutations ledger."""

    __tablename__ = "normative_act_mutations"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    target_act_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("normative_acts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    target_node_path: Mapped[str] = mapped_column(String(120), nullable=False)
    author_act_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("normative_acts.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    author_dispositivo_ref: Mapped[str | None] = mapped_column(String(100), nullable=True)
    mutation_type: Mapped[str] = mapped_column(String(30), nullable=False)
    new_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    new_structured_payload: Mapped[dict[str, Any] | None] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"),
        nullable=True,
    )
    publication_date: Mapped[date] = mapped_column(Date, nullable=False)
    effective_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    extraction_source: Mapped[str] = mapped_column(String(30), nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    mutation_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "target_act_id",
            "target_node_path",
            "author_act_id",
            "mutation_type",
            name="uq_mutation_natural_key",
        ),
        Index("ix_mutations_target_effective", "target_act_id", "effective_date"),
        Index("ix_mutations_target_node", "target_act_id", "target_node_path"),
    )


class LegislationBackfillQueueModel(Base):
    """Relational model for the JIT discovery and historical backfill queue."""

    __tablename__ = "legislation_backfill_queue"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    canonical_urn: Mapped[str] = mapped_column(String(250), unique=True, nullable=False, index=True)
    territory_id: Mapped[str] = mapped_column(String(20), nullable=False)
    act_type: Mapped[str] = mapped_column(String(50), nullable=False)
    act_number: Mapped[str] = mapped_column(String(50), nullable=False)
    act_year: Mapped[int] = mapped_column(Integer, nullable=False)
    citation_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="PENDING", nullable=False)
    last_requested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    __table_args__ = (Index("ix_backfill_queue_priority", text("citation_count DESC"), "status"),)


class CompiledNormativeActModel(Base):
    """Materialized Read Model projection for consolidated legislation."""

    __tablename__ = "compiled_normative_acts"

    act_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("normative_acts.id", ondelete="CASCADE"),
        primary_key=True,
    )
    compiled_version_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    total_mutations_applied: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_mutation_effective_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    compiled_ast: Mapped[dict[str, Any]] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"),
        nullable=False,
    )
    compiled_html: Mapped[str] = mapped_column(Text, nullable=False)
    compiled_markdown: Mapped[str] = mapped_column(Text, nullable=False)
    active_articles_count: Mapped[int] = mapped_column(Integer, nullable=False)
    revoked_articles_count: Mapped[int] = mapped_column(Integer, nullable=False)
    last_compiled_at: Mapped[datetime] = mapped_column(
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

    __table_args__ = (Index("ix_compiled_acts_ast_gin", "compiled_ast", postgresql_using="gin"),)
