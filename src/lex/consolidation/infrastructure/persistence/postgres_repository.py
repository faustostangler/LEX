"""PostgreSQL Implementation of ConsolidationRepositoryPort.

Handles CQRS Write Model (normative_act_mutations), JIT Backfill Discovery Queue,
and Materialized Read Model (compiled_normative_acts).
"""

import uuid
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from lex.consolidation.application.ports import ConsolidationRepositoryPort
from lex.consolidation.domain.entities import (
    CompiledNormativeAct,
    LegislationBackfillTask,
)
from lex.consolidation.domain.value_objects import CanonicalUrn
from lex.consolidation.infrastructure.persistence.models import (
    CompiledNormativeActModel,
    LegislationBackfillQueueModel,
    NormativeActMutationModel,
)
from lex.ingestion.domain.value_objects import DocumentHash, GazetteDate
from lex.treatment.domain.entities import ActAst, NormativeActMutation
from lex.treatment.domain.value_objects import (
    CanonicalNodePath,
    MutationType,
)


class PostgresConsolidationRepository(ConsolidationRepositoryPort):
    """PostgreSQL 16 persistence adapter for the Consolidation Bounded Context."""

    def __init__(self, session: Session) -> None:
        self._session = session

    async def save_mutation(self, mutation: NormativeActMutation) -> None:
        """Appends a mutation delta to the Write Model ledger."""
        mut_id = mutation.id or uuid.uuid4()
        model = NormativeActMutationModel(
            id=mut_id,
            target_act_id=mutation.target_act_id,
            target_node_path=mutation.target_node_path.value,
            author_act_id=mutation.author_act_id,
            author_dispositivo_ref=mutation.author_dispositivo_ref,
            mutation_type=mutation.mutation_type.value,
            new_text=mutation.new_text,
            new_structured_payload=mutation.new_structured_payload,
            publication_date=mutation.publication_date.value,
            effective_date=mutation.effective_date.value,
            extraction_source=mutation.extraction_source,
            confidence_score=mutation.confidence_score,
            mutation_sha256=mutation.mutation_sha256.hex_digest,
        )
        try:
            self._session.add(model)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

    async def get_mutations_for_act(self, target_act_id: UUID) -> list[NormativeActMutation]:
        """Fetches all mutations targeting a given statute, ordered chronologically."""
        stmt = (
            select(NormativeActMutationModel)
            .where(NormativeActMutationModel.target_act_id == target_act_id)
            .order_by(
                NormativeActMutationModel.effective_date.asc(),
                NormativeActMutationModel.created_at.asc(),
            )
        )
        rows = self._session.scalars(stmt).all()
        mutations: list[NormativeActMutation] = []
        for r in rows:
            mutations.append(
                NormativeActMutation(
                    id=r.id,
                    target_act_id=r.target_act_id,
                    target_node_path=CanonicalNodePath.from_string(r.target_node_path),
                    author_act_id=r.author_act_id,
                    author_dispositivo_ref=r.author_dispositivo_ref,
                    mutation_type=MutationType(r.mutation_type),
                    new_text=r.new_text,
                    new_structured_payload=r.new_structured_payload,
                    publication_date=GazetteDate.from_date(r.publication_date),
                    effective_date=GazetteDate.from_date(r.effective_date),
                    extraction_source=r.extraction_source,
                    confidence_score=r.confidence_score,
                    mutation_sha256=DocumentHash.from_text(r.mutation_sha256),
                )
            )
        return mutations

    async def save_compiled_act(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
        try:
            existing = self._session.get(CompiledNormativeActModel, compiled_act.act_id)
            if existing:
                existing.compiled_version_hash = compiled_act.compiled_version_hash
                existing.total_mutations_applied = compiled_act.total_mutations_applied
                existing.last_mutation_effective_date = compiled_act.last_mutation_effective_date
                existing.compiled_ast = compiled_act.compiled_ast.to_dict()
                existing.compiled_html = compiled_act.compiled_html
                existing.compiled_markdown = compiled_act.compiled_markdown
                existing.active_articles_count = compiled_act.active_articles_count
                existing.revoked_articles_count = compiled_act.revoked_articles_count
                existing.last_compiled_at = compiled_act.last_compiled_at
                existing.updated_at = datetime.now(UTC)
            else:
                model = CompiledNormativeActModel(
                    act_id=compiled_act.act_id,
                    compiled_version_hash=compiled_act.compiled_version_hash,
                    total_mutations_applied=compiled_act.total_mutations_applied,
                    last_mutation_effective_date=compiled_act.last_mutation_effective_date,
                    compiled_ast=compiled_act.compiled_ast.to_dict(),
                    compiled_html=compiled_act.compiled_html,
                    compiled_markdown=compiled_act.compiled_markdown,
                    active_articles_count=compiled_act.active_articles_count,
                    revoked_articles_count=compiled_act.revoked_articles_count,
                    last_compiled_at=compiled_act.last_compiled_at,
                )
                self._session.add(model)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

    async def get_compiled_act(self, act_id: UUID) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by statute UUID."""
        row = self._session.get(CompiledNormativeActModel, act_id)
        if not row:
            return None

        ast = ActAst.from_dict(row.compiled_ast)
        return CompiledNormativeAct(
            act_id=row.act_id,
            compiled_version_hash=row.compiled_version_hash,
            total_mutations_applied=row.total_mutations_applied,
            last_mutation_effective_date=row.last_mutation_effective_date,
            compiled_ast=ast,
            compiled_html=row.compiled_html,
            compiled_markdown=row.compiled_markdown,
            active_articles_count=row.active_articles_count,
            revoked_articles_count=row.revoked_articles_count,
            last_compiled_at=row.last_compiled_at,
        )

    async def get_compiled_act_by_urn(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        bind = self._session.get_bind()
        is_postgres = bind is not None and bind.dialect.name == "postgresql"

        row = None
        if is_postgres:
            stmt = select(CompiledNormativeActModel).where(
                CompiledNormativeActModel.compiled_ast["canonical_urn"].astext == canonical_urn
            )
            row = self._session.scalars(stmt).first()
        else:
            stmt = select(CompiledNormativeActModel)
            rows = self._session.scalars(stmt).all()
            for r in rows:
                if r.compiled_ast.get("canonical_urn") == canonical_urn:
                    row = r
                    break

        if not row:
            return None

        ast = ActAst.from_dict(row.compiled_ast)
        return CompiledNormativeAct(
            act_id=row.act_id,
            compiled_version_hash=row.compiled_version_hash,
            total_mutations_applied=row.total_mutations_applied,
            last_mutation_effective_date=row.last_mutation_effective_date,
            compiled_ast=ast,
            compiled_html=row.compiled_html,
            compiled_markdown=row.compiled_markdown,
            active_articles_count=row.active_articles_count,
            revoked_articles_count=row.revoked_articles_count,
            last_compiled_at=row.last_compiled_at,
        )

    async def enqueue_backfill_task(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
        try:
            stmt = select(LegislationBackfillQueueModel).where(
                LegislationBackfillQueueModel.canonical_urn == task.canonical_urn.value
            )
            existing = self._session.scalars(stmt).first()
            if existing:
                existing.citation_count += 1
                existing.last_requested_at = datetime.now(UTC)
            else:
                task_id = task.id or uuid.uuid4()
                model = LegislationBackfillQueueModel(
                    id=task_id,
                    canonical_urn=task.canonical_urn.value,
                    territory_id=task.territory_id,
                    act_type=task.act_type,
                    act_number=task.act_number,
                    act_year=task.act_year,
                    citation_count=task.citation_count,
                    status=task.status,
                    last_requested_at=task.last_requested_at,
                )
                self._session.add(model)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

    async def get_backfill_queue(self, limit: int = 20) -> list[LegislationBackfillTask]:
        """Lists highest priority un-resolved backfill tasks."""
        stmt = (
            select(LegislationBackfillQueueModel)
            .where(LegislationBackfillQueueModel.status == "PENDING")
            .order_by(LegislationBackfillQueueModel.citation_count.desc())
            .limit(limit)
        )
        rows = self._session.scalars(stmt).all()
        tasks: list[LegislationBackfillTask] = []
        for r in rows:
            tasks.append(
                LegislationBackfillTask(
                    id=r.id,
                    canonical_urn=CanonicalUrn.from_string(r.canonical_urn),
                    territory_id=r.territory_id,
                    act_type=r.act_type,
                    act_number=r.act_number,
                    act_year=r.act_year,
                    citation_count=r.citation_count,
                    status=r.status,
                    last_requested_at=r.last_requested_at,
                )
            )
        return tasks
