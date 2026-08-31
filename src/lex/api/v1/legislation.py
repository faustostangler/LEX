"""FastAPI Router for Legislation Read Model Endpoints.

Provides O(1) instantaneous access to compiled legislation, Stub handling,
and on-demand time-travel queries.
"""

from collections.abc import Generator
from datetime import date
from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from lex.consolidation.application.use_cases import (
    CompileNormativeActUseCase,
    TimeTravelCompilationUseCase,
)
from lex.consolidation.infrastructure.persistence.postgres_repository import (
    PostgresConsolidationRepository,
)
from lex.ingestion.infrastructure.persistence.models import NormativeActModel
from lex.treatment.domain.entities import ActAst

router = APIRouter(prefix="/legislation", tags=["Legislation"])


def get_db_session() -> Generator[Session, None, None]:
    """Dependency placeholder replaced during application startup or testing."""
    raise NotImplementedError("Database session dependency must be overridden.")


@router.get("/{identifier}")
async def get_compiled_legislation(
    identifier: str,
    as_of: Annotated[
        date | None,
        Query(description="Time-travel historical cutoff date (YYYY-MM-DD)"),
    ] = None,
    session: Annotated[Session, Depends(get_db_session)] = None,  # type: ignore[assignment]
) -> dict[str, Any]:
    """Retrieves the consolidated normative act in O(1) time or performs time-travel compilation."""
    repo = PostgresConsolidationRepository(session=session)
    act_uuid: UUID | None = None

    try:
        act_uuid = UUID(identifier)
    except ValueError:
        # Search by Canonical URN
        stmt = select(NormativeActModel).where(NormativeActModel.canonical_urn == identifier)
        act_model = session.scalars(stmt).first()
        if act_model:
            act_uuid = act_model.id

    if act_uuid is None:
        raise HTTPException(status_code=404, detail=f"Statute '{identifier}' not found.")

    # 1. Check if the target is a Stub entity
    raw_act = session.get(NormativeActModel, act_uuid)
    if raw_act and raw_act.is_stub:
        mutations = await repo.get_mutations_for_act(act_uuid)
        return {
            "status": "PENDING_BASE_INGESTION",
            "act_id": str(raw_act.id),
            "canonical_urn": raw_act.canonical_urn,
            "title": raw_act.title,
            "act_type": raw_act.act_type,
            "act_number": raw_act.act_number,
            "act_year": raw_act.act_year,
            "mutations": [
                {
                    "id": str(m.id),
                    "target_node_path": m.target_node_path.value,
                    "mutation_type": m.mutation_type.value,
                    "new_text": m.new_text,
                    "effective_date": str(m.effective_date.value),
                }
                for m in mutations
            ],
        }

    # 2. Time-Travel compilation requested
    if as_of is not None and raw_act and raw_act.structured_content:
        base_ast = ActAst.from_dict(raw_act.structured_content)
        time_travel_case = TimeTravelCompilationUseCase(repository=repo)
        compiled = await time_travel_case.execute(base_ast, as_of=as_of)
        return {
            "act_id": str(compiled.act_id),
            "canonical_urn": compiled.compiled_ast.canonical_urn,
            "title": compiled.compiled_ast.title,
            "as_of": str(as_of),
            "total_mutations_applied": compiled.total_mutations_applied,
            "compiled_html": compiled.compiled_html,
            "compiled_markdown": compiled.compiled_markdown,
            "active_articles_count": compiled.active_articles_count,
            "revoked_articles_count": compiled.revoked_articles_count,
        }

    # 3. Retrieve pre-rendered compiled projection
    compiled_act = await repo.get_compiled_act(act_uuid)
    if compiled_act:
        return {
            "act_id": str(compiled_act.act_id),
            "canonical_urn": compiled_act.compiled_ast.canonical_urn,
            "title": compiled_act.compiled_ast.title,
            "compiled_version_hash": compiled_act.compiled_version_hash,
            "total_mutations_applied": compiled_act.total_mutations_applied,
            "last_mutation_effective_date": (
                str(compiled_act.last_mutation_effective_date)
                if compiled_act.last_mutation_effective_date
                else None
            ),
            "compiled_html": compiled_act.compiled_html,
            "compiled_markdown": compiled_act.compiled_markdown,
            "active_articles_count": compiled_act.active_articles_count,
            "revoked_articles_count": compiled_act.revoked_articles_count,
            "last_compiled_at": compiled_act.last_compiled_at.isoformat(),
        }

    # 4. Fallback: on-the-fly compilation if raw_act exists with structured content
    if raw_act and raw_act.structured_content:
        base_ast = ActAst.from_dict(raw_act.structured_content)
        compile_case = CompileNormativeActUseCase(repository=repo)
        compiled_act = await compile_case.execute(base_ast)
        return {
            "act_id": str(compiled_act.act_id),
            "canonical_urn": compiled_act.compiled_ast.canonical_urn,
            "title": compiled_act.compiled_ast.title,
            "compiled_version_hash": compiled_act.compiled_version_hash,
            "total_mutations_applied": compiled_act.total_mutations_applied,
            "compiled_html": compiled_act.compiled_html,
            "compiled_markdown": compiled_act.compiled_markdown,
            "active_articles_count": compiled_act.active_articles_count,
            "revoked_articles_count": compiled_act.revoked_articles_count,
            "last_compiled_at": compiled_act.last_compiled_at.isoformat(),
        }

    raise HTTPException(status_code=404, detail=f"Legislation for '{identifier}' is not compiled.")
