"""Application Ports for the Treatment Bounded Context.

Defines structural subtyping protocols (@runtime_checkable) for Treatment persistence.
"""

from typing import Any, Protocol, runtime_checkable
from uuid import UUID

from lex.treatment.domain.entities import NormativeActMutation


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


@runtime_checkable
class TreatmentRepositoryPort(Protocol):
    """Port for persisting treated AST structures, NER entities, and mutations."""

    async def save_mutations(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        ...

    async def update_normative_act_treatment(
        self,
        act_id: UUID,
        structured_content: dict[str, Any] | None,
        metadata_json: dict[str, Any] | None,
    ) -> None:
        """Updates a NormativeAct row with its parsed AST or extracted NER metadata."""
        ...
