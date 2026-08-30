"""Application Ports for the Consolidation Bounded Context.

Defines structural subtyping protocols (@runtime_checkable) for CQRS Write and Read operations.
"""

from typing import Protocol, runtime_checkable
from uuid import UUID

from lex.consolidation.domain.entities import (
    CompiledNormativeAct,
    LegislationBackfillTask,
)
from lex.treatment.domain.entities import NormativeActMutation


@runtime_checkable
class ConsolidationRepositoryPort(Protocol):
    """Port for CQRS Mutation Ledger, JIT Backfill, and Compiled Read Models."""

    async def save_mutation(self, mutation: NormativeActMutation) -> None:
        """Appends a single mutation delta to the write model ledger."""
        ...

    async def get_mutations_for_act(self, target_act_id: UUID) -> list[NormativeActMutation]:
        """Fetches all mutation deltas targeting a given statute, ordered chronologically."""
        ...

    async def save_compiled_act(self, compiled_act: CompiledNormativeAct) -> None:
        """Saves or updates a materialized compiled act projection in the read model."""
        ...

    async def get_compiled_act(self, act_id: UUID) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by statute UUID."""
        ...

    async def get_compiled_act_by_urn(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        ...

    async def enqueue_backfill_task(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing base statute in the JIT queue."""
        ...

    async def get_backfill_queue(self, limit: int = 20) -> list[LegislationBackfillTask]:
        """Lists highest priority un-resolved backfill tasks."""
        ...
