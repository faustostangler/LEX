"""Application Use Cases for the Consolidation Bounded Context.

Implements statutory compilation, out-of-order catch-up replay, and on-demand time-travel queries.
"""

import uuid
from datetime import date

from lex.consolidation.application.ports import ConsolidationRepositoryPort
from lex.consolidation.domain.entities import CompiledNormativeAct
from lex.consolidation.domain.services.ast_reducer import PureAstReducer
from lex.treatment.domain.entities import ActAst, NormativeActMutation


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁCompileNormativeActUseCaseǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁCompileNormativeActUseCaseǁexecute__mutmut: MutantDict = {}  # type: ignore


class CompileNormativeActUseCase:
    """Use case compiling a base statute AST with all accumulated mutation deltas."""

    @_mutmut_mutated(mutants_xǁCompileNormativeActUseCaseǁ__init____mutmut)
    def __init__(self, repository: ConsolidationRepositoryPort) -> None:
        self._repository = repository

    def xǁCompileNormativeActUseCaseǁ__init____mutmut_orig(self, repository: ConsolidationRepositoryPort) -> None:
        self._repository = repository

    def xǁCompileNormativeActUseCaseǁ__init____mutmut_1(self, repository: ConsolidationRepositoryPort) -> None:
        self._repository = None

    @_mutmut_mutated(mutants_xǁCompileNormativeActUseCaseǁexecute__mutmut)
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

    async def xǁCompileNormativeActUseCaseǁexecute__mutmut_orig(
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

    async def xǁCompileNormativeActUseCaseǁexecute__mutmut_1(
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
        act_id = None
        effective_mutations = mutations
        if effective_mutations is None:
            effective_mutations = await self._repository.get_mutations_for_act(act_id)

        compiled_act = PureAstReducer.reduce(
            base_ast=base_ast,
            mutations=effective_mutations,
        )

        await self._repository.save_compiled_act(compiled_act)
        return compiled_act

    async def xǁCompileNormativeActUseCaseǁexecute__mutmut_2(
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
        act_id = base_ast.act_id and uuid.uuid4()
        effective_mutations = mutations
        if effective_mutations is None:
            effective_mutations = await self._repository.get_mutations_for_act(act_id)

        compiled_act = PureAstReducer.reduce(
            base_ast=base_ast,
            mutations=effective_mutations,
        )

        await self._repository.save_compiled_act(compiled_act)
        return compiled_act

    async def xǁCompileNormativeActUseCaseǁexecute__mutmut_3(
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
        effective_mutations = None
        if effective_mutations is None:
            effective_mutations = await self._repository.get_mutations_for_act(act_id)

        compiled_act = PureAstReducer.reduce(
            base_ast=base_ast,
            mutations=effective_mutations,
        )

        await self._repository.save_compiled_act(compiled_act)
        return compiled_act

    async def xǁCompileNormativeActUseCaseǁexecute__mutmut_4(
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
        if effective_mutations is not None:
            effective_mutations = await self._repository.get_mutations_for_act(act_id)

        compiled_act = PureAstReducer.reduce(
            base_ast=base_ast,
            mutations=effective_mutations,
        )

        await self._repository.save_compiled_act(compiled_act)
        return compiled_act

    async def xǁCompileNormativeActUseCaseǁexecute__mutmut_5(
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
            effective_mutations = None

        compiled_act = PureAstReducer.reduce(
            base_ast=base_ast,
            mutations=effective_mutations,
        )

        await self._repository.save_compiled_act(compiled_act)
        return compiled_act

    async def xǁCompileNormativeActUseCaseǁexecute__mutmut_6(
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
            effective_mutations = await self._repository.get_mutations_for_act(None)

        compiled_act = PureAstReducer.reduce(
            base_ast=base_ast,
            mutations=effective_mutations,
        )

        await self._repository.save_compiled_act(compiled_act)
        return compiled_act

    async def xǁCompileNormativeActUseCaseǁexecute__mutmut_7(
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

        compiled_act = None

        await self._repository.save_compiled_act(compiled_act)
        return compiled_act

    async def xǁCompileNormativeActUseCaseǁexecute__mutmut_8(
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
            base_ast=None,
            mutations=effective_mutations,
        )

        await self._repository.save_compiled_act(compiled_act)
        return compiled_act

    async def xǁCompileNormativeActUseCaseǁexecute__mutmut_9(
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
            mutations=None,
        )

        await self._repository.save_compiled_act(compiled_act)
        return compiled_act

    async def xǁCompileNormativeActUseCaseǁexecute__mutmut_10(
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
            mutations=effective_mutations,
        )

        await self._repository.save_compiled_act(compiled_act)
        return compiled_act

    async def xǁCompileNormativeActUseCaseǁexecute__mutmut_11(
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
            )

        await self._repository.save_compiled_act(compiled_act)
        return compiled_act

    async def xǁCompileNormativeActUseCaseǁexecute__mutmut_12(
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

        await self._repository.save_compiled_act(None)
        return compiled_act

mutants_xǁCompileNormativeActUseCaseǁ__init____mutmut['_mutmut_orig'] = CompileNormativeActUseCase.xǁCompileNormativeActUseCaseǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁCompileNormativeActUseCaseǁ__init____mutmut['xǁCompileNormativeActUseCaseǁ__init____mutmut_1'] = CompileNormativeActUseCase.xǁCompileNormativeActUseCaseǁ__init____mutmut_1 # type: ignore # mutmut generated

mutants_xǁCompileNormativeActUseCaseǁexecute__mutmut['_mutmut_orig'] = CompileNormativeActUseCase.xǁCompileNormativeActUseCaseǁexecute__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCompileNormativeActUseCaseǁexecute__mutmut['xǁCompileNormativeActUseCaseǁexecute__mutmut_1'] = CompileNormativeActUseCase.xǁCompileNormativeActUseCaseǁexecute__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCompileNormativeActUseCaseǁexecute__mutmut['xǁCompileNormativeActUseCaseǁexecute__mutmut_2'] = CompileNormativeActUseCase.xǁCompileNormativeActUseCaseǁexecute__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCompileNormativeActUseCaseǁexecute__mutmut['xǁCompileNormativeActUseCaseǁexecute__mutmut_3'] = CompileNormativeActUseCase.xǁCompileNormativeActUseCaseǁexecute__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCompileNormativeActUseCaseǁexecute__mutmut['xǁCompileNormativeActUseCaseǁexecute__mutmut_4'] = CompileNormativeActUseCase.xǁCompileNormativeActUseCaseǁexecute__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCompileNormativeActUseCaseǁexecute__mutmut['xǁCompileNormativeActUseCaseǁexecute__mutmut_5'] = CompileNormativeActUseCase.xǁCompileNormativeActUseCaseǁexecute__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCompileNormativeActUseCaseǁexecute__mutmut['xǁCompileNormativeActUseCaseǁexecute__mutmut_6'] = CompileNormativeActUseCase.xǁCompileNormativeActUseCaseǁexecute__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCompileNormativeActUseCaseǁexecute__mutmut['xǁCompileNormativeActUseCaseǁexecute__mutmut_7'] = CompileNormativeActUseCase.xǁCompileNormativeActUseCaseǁexecute__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCompileNormativeActUseCaseǁexecute__mutmut['xǁCompileNormativeActUseCaseǁexecute__mutmut_8'] = CompileNormativeActUseCase.xǁCompileNormativeActUseCaseǁexecute__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCompileNormativeActUseCaseǁexecute__mutmut['xǁCompileNormativeActUseCaseǁexecute__mutmut_9'] = CompileNormativeActUseCase.xǁCompileNormativeActUseCaseǁexecute__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCompileNormativeActUseCaseǁexecute__mutmut['xǁCompileNormativeActUseCaseǁexecute__mutmut_10'] = CompileNormativeActUseCase.xǁCompileNormativeActUseCaseǁexecute__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCompileNormativeActUseCaseǁexecute__mutmut['xǁCompileNormativeActUseCaseǁexecute__mutmut_11'] = CompileNormativeActUseCase.xǁCompileNormativeActUseCaseǁexecute__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCompileNormativeActUseCaseǁexecute__mutmut['xǁCompileNormativeActUseCaseǁexecute__mutmut_12'] = CompileNormativeActUseCase.xǁCompileNormativeActUseCaseǁexecute__mutmut_12 # type: ignore # mutmut generated
mutants_xǁTimeTravelCompilationUseCaseǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁTimeTravelCompilationUseCaseǁexecute__mutmut: MutantDict = {}  # type: ignore


class TimeTravelCompilationUseCase:
    """Use case performing on-demand historical consolidation up to a specific date."""

    @_mutmut_mutated(mutants_xǁTimeTravelCompilationUseCaseǁ__init____mutmut)
    def __init__(self, repository: ConsolidationRepositoryPort) -> None:
        self._repository = repository

    def xǁTimeTravelCompilationUseCaseǁ__init____mutmut_orig(self, repository: ConsolidationRepositoryPort) -> None:
        self._repository = repository

    def xǁTimeTravelCompilationUseCaseǁ__init____mutmut_1(self, repository: ConsolidationRepositoryPort) -> None:
        self._repository = None

    @_mutmut_mutated(mutants_xǁTimeTravelCompilationUseCaseǁexecute__mutmut)
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

    async def xǁTimeTravelCompilationUseCaseǁexecute__mutmut_orig(self, base_ast: ActAst, as_of: date) -> CompiledNormativeAct:
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

    async def xǁTimeTravelCompilationUseCaseǁexecute__mutmut_1(self, base_ast: ActAst, as_of: date) -> CompiledNormativeAct:
        """Compiles a statute's text as it stood on a specific historical date.

        Args:
            base_ast: The unmodified base statute AST.
            as_of: Cutoff date for effective mutations.

        Returns:
            A CompiledNormativeAct reflecting the statutory state on the requested date.
        """
        act_id = None
        all_mutations = await self._repository.get_mutations_for_act(act_id)

        # Filter mutations effective on or before the requested date
        historical_mutations = [m for m in all_mutations if m.effective_date.value <= as_of]

        return PureAstReducer.reduce(
            base_ast=base_ast,
            mutations=historical_mutations,
        )

    async def xǁTimeTravelCompilationUseCaseǁexecute__mutmut_2(self, base_ast: ActAst, as_of: date) -> CompiledNormativeAct:
        """Compiles a statute's text as it stood on a specific historical date.

        Args:
            base_ast: The unmodified base statute AST.
            as_of: Cutoff date for effective mutations.

        Returns:
            A CompiledNormativeAct reflecting the statutory state on the requested date.
        """
        act_id = base_ast.act_id and uuid.uuid4()
        all_mutations = await self._repository.get_mutations_for_act(act_id)

        # Filter mutations effective on or before the requested date
        historical_mutations = [m for m in all_mutations if m.effective_date.value <= as_of]

        return PureAstReducer.reduce(
            base_ast=base_ast,
            mutations=historical_mutations,
        )

    async def xǁTimeTravelCompilationUseCaseǁexecute__mutmut_3(self, base_ast: ActAst, as_of: date) -> CompiledNormativeAct:
        """Compiles a statute's text as it stood on a specific historical date.

        Args:
            base_ast: The unmodified base statute AST.
            as_of: Cutoff date for effective mutations.

        Returns:
            A CompiledNormativeAct reflecting the statutory state on the requested date.
        """
        act_id = base_ast.act_id or uuid.uuid4()
        all_mutations = None

        # Filter mutations effective on or before the requested date
        historical_mutations = [m for m in all_mutations if m.effective_date.value <= as_of]

        return PureAstReducer.reduce(
            base_ast=base_ast,
            mutations=historical_mutations,
        )

    async def xǁTimeTravelCompilationUseCaseǁexecute__mutmut_4(self, base_ast: ActAst, as_of: date) -> CompiledNormativeAct:
        """Compiles a statute's text as it stood on a specific historical date.

        Args:
            base_ast: The unmodified base statute AST.
            as_of: Cutoff date for effective mutations.

        Returns:
            A CompiledNormativeAct reflecting the statutory state on the requested date.
        """
        act_id = base_ast.act_id or uuid.uuid4()
        all_mutations = await self._repository.get_mutations_for_act(None)

        # Filter mutations effective on or before the requested date
        historical_mutations = [m for m in all_mutations if m.effective_date.value <= as_of]

        return PureAstReducer.reduce(
            base_ast=base_ast,
            mutations=historical_mutations,
        )

    async def xǁTimeTravelCompilationUseCaseǁexecute__mutmut_5(self, base_ast: ActAst, as_of: date) -> CompiledNormativeAct:
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
        historical_mutations = None

        return PureAstReducer.reduce(
            base_ast=base_ast,
            mutations=historical_mutations,
        )

    async def xǁTimeTravelCompilationUseCaseǁexecute__mutmut_6(self, base_ast: ActAst, as_of: date) -> CompiledNormativeAct:
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
        historical_mutations = [m for m in all_mutations if m.effective_date.value < as_of]

        return PureAstReducer.reduce(
            base_ast=base_ast,
            mutations=historical_mutations,
        )

    async def xǁTimeTravelCompilationUseCaseǁexecute__mutmut_7(self, base_ast: ActAst, as_of: date) -> CompiledNormativeAct:
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
            base_ast=None,
            mutations=historical_mutations,
        )

    async def xǁTimeTravelCompilationUseCaseǁexecute__mutmut_8(self, base_ast: ActAst, as_of: date) -> CompiledNormativeAct:
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
            mutations=None,
        )

    async def xǁTimeTravelCompilationUseCaseǁexecute__mutmut_9(self, base_ast: ActAst, as_of: date) -> CompiledNormativeAct:
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
            mutations=historical_mutations,
        )

    async def xǁTimeTravelCompilationUseCaseǁexecute__mutmut_10(self, base_ast: ActAst, as_of: date) -> CompiledNormativeAct:
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
            )

mutants_xǁTimeTravelCompilationUseCaseǁ__init____mutmut['_mutmut_orig'] = TimeTravelCompilationUseCase.xǁTimeTravelCompilationUseCaseǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁTimeTravelCompilationUseCaseǁ__init____mutmut['xǁTimeTravelCompilationUseCaseǁ__init____mutmut_1'] = TimeTravelCompilationUseCase.xǁTimeTravelCompilationUseCaseǁ__init____mutmut_1 # type: ignore # mutmut generated

mutants_xǁTimeTravelCompilationUseCaseǁexecute__mutmut['_mutmut_orig'] = TimeTravelCompilationUseCase.xǁTimeTravelCompilationUseCaseǁexecute__mutmut_orig # type: ignore # mutmut generated
mutants_xǁTimeTravelCompilationUseCaseǁexecute__mutmut['xǁTimeTravelCompilationUseCaseǁexecute__mutmut_1'] = TimeTravelCompilationUseCase.xǁTimeTravelCompilationUseCaseǁexecute__mutmut_1 # type: ignore # mutmut generated
mutants_xǁTimeTravelCompilationUseCaseǁexecute__mutmut['xǁTimeTravelCompilationUseCaseǁexecute__mutmut_2'] = TimeTravelCompilationUseCase.xǁTimeTravelCompilationUseCaseǁexecute__mutmut_2 # type: ignore # mutmut generated
mutants_xǁTimeTravelCompilationUseCaseǁexecute__mutmut['xǁTimeTravelCompilationUseCaseǁexecute__mutmut_3'] = TimeTravelCompilationUseCase.xǁTimeTravelCompilationUseCaseǁexecute__mutmut_3 # type: ignore # mutmut generated
mutants_xǁTimeTravelCompilationUseCaseǁexecute__mutmut['xǁTimeTravelCompilationUseCaseǁexecute__mutmut_4'] = TimeTravelCompilationUseCase.xǁTimeTravelCompilationUseCaseǁexecute__mutmut_4 # type: ignore # mutmut generated
mutants_xǁTimeTravelCompilationUseCaseǁexecute__mutmut['xǁTimeTravelCompilationUseCaseǁexecute__mutmut_5'] = TimeTravelCompilationUseCase.xǁTimeTravelCompilationUseCaseǁexecute__mutmut_5 # type: ignore # mutmut generated
mutants_xǁTimeTravelCompilationUseCaseǁexecute__mutmut['xǁTimeTravelCompilationUseCaseǁexecute__mutmut_6'] = TimeTravelCompilationUseCase.xǁTimeTravelCompilationUseCaseǁexecute__mutmut_6 # type: ignore # mutmut generated
mutants_xǁTimeTravelCompilationUseCaseǁexecute__mutmut['xǁTimeTravelCompilationUseCaseǁexecute__mutmut_7'] = TimeTravelCompilationUseCase.xǁTimeTravelCompilationUseCaseǁexecute__mutmut_7 # type: ignore # mutmut generated
mutants_xǁTimeTravelCompilationUseCaseǁexecute__mutmut['xǁTimeTravelCompilationUseCaseǁexecute__mutmut_8'] = TimeTravelCompilationUseCase.xǁTimeTravelCompilationUseCaseǁexecute__mutmut_8 # type: ignore # mutmut generated
mutants_xǁTimeTravelCompilationUseCaseǁexecute__mutmut['xǁTimeTravelCompilationUseCaseǁexecute__mutmut_9'] = TimeTravelCompilationUseCase.xǁTimeTravelCompilationUseCaseǁexecute__mutmut_9 # type: ignore # mutmut generated
mutants_xǁTimeTravelCompilationUseCaseǁexecute__mutmut['xǁTimeTravelCompilationUseCaseǁexecute__mutmut_10'] = TimeTravelCompilationUseCase.xǁTimeTravelCompilationUseCaseǁexecute__mutmut_10 # type: ignore # mutmut generated
