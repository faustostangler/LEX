"""Application Ports for the Treatment Bounded Context.

Defines structural subtyping protocols (@runtime_checkable) for Treatment persistence.
"""

from typing import Any, Protocol, runtime_checkable
from uuid import UUID

from lex.treatment.domain.entities import NormativeActMutation


@runtime_checkable
class TreatmentRepositoryPort(Protocol):
    """Port for persisting treated AST structures, NER entities, and mutations."""

    async def save_mutations(
        self, mutations: list[NormativeActMutation], auto_commit: bool = True
    ) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        ...

    async def update_normative_act_treatment(
        self,
        act_id: UUID,
        structured_content: dict[str, Any] | None,
        metadata_json: dict[str, Any] | None,
        auto_commit: bool = True,
    ) -> None:
        """Updates a NormativeAct row with its parsed AST or extracted NER metadata."""
        ...
