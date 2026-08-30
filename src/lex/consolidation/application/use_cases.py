"""Application Use Cases for the Consolidation Bounded Context.

Implements statutory compilation, out-of-order catch-up replay, and on-demand time-travel queries.
"""

import uuid
from datetime import date

from lex.consolidation.application.ports import ConsolidationRepositoryPort
from lex.consolidation.domain.entities import CompiledNormativeAct
from lex.consolidation.domain.services.ast_reducer import PureAstReducer
from lex.treatment.domain.entities import ActAst, NormativeActMutation


class CompileNormativeActUseCase:
    """Use case compiling a base statute AST with all accumulated mutation deltas."""

    def __init__(self, repository: ConsolidationRepositoryPort) -> None:
        self._repository = repository

    async def execute(
        self,
        base_ast: ActAst,
        mutations: list[NormativeActMutation] | None = None,
    ) -> CompiledNormativeAct:
        """Executes the pure AST reduction and persists the read model projection.

        Args:
            base_ast: The authentic unmodified AST of the statute.
            mutations: Optional explicit list of mutations; fetched from repository if None.

        Returns:
            The compiled, pre-rendered CompiledNormativeAct.
        """
        act_id = base_ast.act_id or uuid.uuid4()
        effective_mutations = mutations
        if effective_mutations is None:
            effective_mutations = await self._repository.get_mutations_for_act(act_id)

        compiled_act = PureAstReducer.reduce(
            base_ast=base_ast,
            mutations=effective_mutations,
        )

        await self._repository.save_compiled_act(compiled_act)
        return compiled_act


class TimeTravelCompilationUseCase:
    """Use case performing on-demand historical consolidation up to a specific date."""

    def __init__(self, repository: ConsolidationRepositoryPort) -> None:
        self._repository = repository

    async def execute(self, base_ast: ActAst, as_of: date) -> CompiledNormativeAct:
        """Compiles a statute's text as it stood on a specific historical date.

        Args:
            base_ast: The unmodified base statute AST.
            as_of: Cutoff date for effective mutations.

        Returns:
            A CompiledNormativeAct reflecting the statutory state on the requested date.
        """
        act_id = base_ast.act_id or uuid.uuid4()
        all_mutations = await self._repository.get_mutations_for_act(act_id)

        # Filter mutations effective on or before the requested date
        historical_mutations = [m for m in all_mutations if m.effective_date.value <= as_of]

        return PureAstReducer.reduce(
            base_ast=base_ast,
            mutations=historical_mutations,
        )
