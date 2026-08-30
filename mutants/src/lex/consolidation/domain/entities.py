"""Domain Entities for the Consolidation Bounded Context.

Encapsulates the JIT Backfill Task and the Materialized Read Model Projection
for Compiled Normative Legislation.
"""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from lex.consolidation.domain.value_objects import CanonicalUrn
from lex.treatment.domain.entities import ActAst


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class LegislationBackfillTask(BaseModel):
    """Entity representing a missing base statute in the JIT discovery queue."""

    model_config = ConfigDict(frozen=True)

    id: UUID | None = None
    canonical_urn: CanonicalUrn
    territory_id: str
    act_type: str
    act_number: str
    act_year: int
    citation_count: int = Field(default=1, ge=1)
    status: str = "PENDING"  # 'PENDING', 'IN_PROGRESS', 'RESOLVED'
    last_requested_at: datetime


class CompiledNormativeAct(BaseModel):
    """Materialized Read Model projection for consolidated legislation (ADR-006)."""

    model_config = ConfigDict(frozen=True)

    act_id: UUID
    compiled_version_hash: str
    total_mutations_applied: int = Field(default=0, ge=0)
    last_mutation_effective_date: date | None = None
    compiled_ast: ActAst
    compiled_html: str
    compiled_markdown: str
    active_articles_count: int = Field(default=0, ge=0)
    revoked_articles_count: int = Field(default=0, ge=0)
    last_compiled_at: datetime
