"""Unit tests for Consolidation Application Use Cases.

Tests CompileNormativeActUseCase and TimeTravelCompilationUseCase with in-memory test doubles.
"""

import uuid
from datetime import date
from uuid import UUID

import pytest

from lex.consolidation.application.ports import ConsolidationRepositoryPort
from lex.consolidation.application.use_cases import (
    CompileNormativeActUseCase,
    TimeTravelCompilationUseCase,
)
from lex.consolidation.domain.entities import (
    CompiledNormativeAct,
    LegislationBackfillTask,
)
from lex.ingestion.domain.value_objects import DocumentHash, GazetteDate
from lex.treatment.domain.entities import (
    ActAst,
    DispositivoNode,
    NormativeActMutation,
)
from lex.treatment.domain.value_objects import (
    CanonicalNodePath,
    DispositivoType,
    MutationType,
)


class InMemoryConsolidationRepository(ConsolidationRepositoryPort):
    """Pure in-memory test double implementing ConsolidationRepositoryPort."""

    def __init__(self) -> None:
        self.mutations: dict[UUID, list[NormativeActMutation]] = {}
        self.compiled_acts: dict[UUID, CompiledNormativeAct] = {}
        self.backfill_tasks: dict[str, LegislationBackfillTask] = {}

    async def save_mutation(self, mutation: NormativeActMutation) -> None:
        self.mutations.setdefault(mutation.target_act_id, []).append(mutation)

    async def get_mutations_for_act(self, target_act_id: UUID) -> list[NormativeActMutation]:
        return self.mutations.get(target_act_id, [])

    async def save_compiled_act(self, compiled_act: CompiledNormativeAct) -> None:
        self.compiled_acts[compiled_act.act_id] = compiled_act

    async def get_compiled_act(self, act_id: UUID) -> CompiledNormativeAct | None:
        return self.compiled_acts.get(act_id)

    async def get_compiled_act_by_urn(self, canonical_urn: str) -> CompiledNormativeAct | None:
        for act in self.compiled_acts.values():
            if act.compiled_ast.canonical_urn == canonical_urn:
                return act
        return None

    async def enqueue_backfill_task(self, task: LegislationBackfillTask) -> None:
        urn_key = task.canonical_urn.value
        if urn_key in self.backfill_tasks:
            existing = self.backfill_tasks[urn_key]
            self.backfill_tasks[urn_key] = LegislationBackfillTask(
                id=existing.id,
                canonical_urn=existing.canonical_urn,
                territory_id=existing.territory_id,
                act_type=existing.act_type,
                act_number=existing.act_number,
                act_year=existing.act_year,
                citation_count=existing.citation_count + 1,
                status=existing.status,
                last_requested_at=task.last_requested_at,
            )
        else:
            self.backfill_tasks[urn_key] = task

    async def get_backfill_queue(self, limit: int = 20) -> list[LegislationBackfillTask]:
        tasks = list(self.backfill_tasks.values())
        tasks.sort(key=lambda t: t.citation_count, reverse=True)
        return tasks[:limit]


class TestConsolidationUseCases:
    """Test suite for Consolidation Use Cases."""

    @pytest.mark.anyio
    async def test_compile_normative_act_use_case(self) -> None:
        """Asserts end-to-end compilation through CompileNormativeActUseCase."""
        repo = InMemoryConsolidationRepository()
        use_case = CompileNormativeActUseCase(repository=repo)

        act_id = uuid.uuid4()
        art1 = DispositivoNode(
            node_path=CanonicalNodePath.from_string("art_1"),
            node_type=DispositivoType.ARTIGO,
            label="Art. 1º",
            text="Texto base original.",
        )
        base_ast = ActAst(
            act_id=act_id,
            canonical_urn="urn:lex:br:federal:lei:2010;1000",
            title="Lei nº 1.000/2010",
            nodes=[art1],
        )

        m = NormativeActMutation(
            target_act_id=act_id,
            target_node_path=CanonicalNodePath.from_string("art_1"),
            author_act_id=uuid.uuid4(),
            mutation_type=MutationType.ALTERACAO_NR,
            new_text="Texto alterado e consolidado. (NR)",
            publication_date=GazetteDate.from_date(date(2020, 5, 10)),
            effective_date=GazetteDate.from_date(date(2020, 5, 10)),
            extraction_source="lc95_regex",
            confidence_score=1.0,
            mutation_sha256=DocumentHash.from_text("mutation-hash-1"),
        )
        await repo.save_mutation(m)

        compiled = await use_case.execute(base_ast)

        assert compiled.act_id == act_id
        assert compiled.total_mutations_applied == 1
        assert "Texto alterado e consolidado" in compiled.compiled_html
        assert act_id in repo.compiled_acts

    @pytest.mark.anyio
    async def test_time_travel_compilation_use_case(self) -> None:
        """Asserts on-demand time travel compilation for historical dates."""
        repo = InMemoryConsolidationRepository()
        time_travel_case = TimeTravelCompilationUseCase(repository=repo)

        act_id = uuid.uuid4()
        art1 = DispositivoNode(
            node_path=CanonicalNodePath.from_string("art_1"),
            node_type=DispositivoType.ARTIGO,
            label="Art. 1º",
            text="Texto original 2010.",
        )
        base_ast = ActAst(
            act_id=act_id,
            canonical_urn="urn:lex:br:federal:lei:2010;1000",
            title="Lei nº 1.000/2010",
            nodes=[art1],
        )

        # Mutation 1 in 2015
        m1 = NormativeActMutation(
            target_act_id=act_id,
            target_node_path=CanonicalNodePath.from_string("art_1"),
            author_act_id=uuid.uuid4(),
            mutation_type=MutationType.ALTERACAO_NR,
            new_text="Texto redação 2015. (NR)",
            publication_date=GazetteDate.from_date(date(2015, 1, 1)),
            effective_date=GazetteDate.from_date(date(2015, 1, 1)),
            extraction_source="lc95_regex",
            confidence_score=1.0,
            mutation_sha256=DocumentHash.from_text("hash-2015"),
        )
        # Mutation 2 in 2022
        m2 = NormativeActMutation(
            target_act_id=act_id,
            target_node_path=CanonicalNodePath.from_string("art_1"),
            author_act_id=uuid.uuid4(),
            mutation_type=MutationType.ALTERACAO_NR,
            new_text="Texto redação 2022. (NR)",
            publication_date=GazetteDate.from_date(date(2022, 1, 1)),
            effective_date=GazetteDate.from_date(date(2022, 1, 1)),
            extraction_source="lc95_regex",
            confidence_score=1.0,
            mutation_sha256=DocumentHash.from_text("hash-2022"),
        )
        await repo.save_mutation(m1)
        await repo.save_mutation(m2)

        # Query as of 2018 (should have m1 applied, but NOT m2)
        compiled_2018 = await time_travel_case.execute(base_ast, as_of=date(2018, 6, 1))
        assert compiled_2018.total_mutations_applied == 1
        assert "Texto redação 2015" in compiled_2018.compiled_html
        assert "Texto redação 2022" not in compiled_2018.compiled_html

        # Query as of 2012 (before any mutation, should be original)
        compiled_2012 = await time_travel_case.execute(base_ast, as_of=date(2012, 1, 1))
        assert compiled_2012.total_mutations_applied == 0
        assert "Texto original 2010" in compiled_2012.compiled_html
