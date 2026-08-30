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


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁPostgresConsolidationRepositoryǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut: MutantDict = {}  # type: ignore
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut: MutantDict = {}  # type: ignore
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut: MutantDict = {}  # type: ignore
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut: MutantDict = {}  # type: ignore
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut: MutantDict = {}  # type: ignore
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut: MutantDict = {}  # type: ignore
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut: MutantDict = {}  # type: ignore


class PostgresConsolidationRepository(ConsolidationRepositoryPort):
    """PostgreSQL 16 persistence adapter for the Consolidation Bounded Context."""

    @_mutmut_mutated(mutants_xǁPostgresConsolidationRepositoryǁ__init____mutmut)
    def __init__(self, session: Session) -> None:
        self._session = session

    def xǁPostgresConsolidationRepositoryǁ__init____mutmut_orig(self, session: Session) -> None:
        self._session = session

    def xǁPostgresConsolidationRepositoryǁ__init____mutmut_1(self, session: Session) -> None:
        self._session = None

    @_mutmut_mutated(mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut)
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
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_orig(self, mutation: NormativeActMutation) -> None:
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
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_1(self, mutation: NormativeActMutation) -> None:
        """Appends a mutation delta to the Write Model ledger."""
        mut_id = None
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
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_2(self, mutation: NormativeActMutation) -> None:
        """Appends a mutation delta to the Write Model ledger."""
        mut_id = mutation.id and uuid.uuid4()
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
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_3(self, mutation: NormativeActMutation) -> None:
        """Appends a mutation delta to the Write Model ledger."""
        mut_id = mutation.id or uuid.uuid4()
        model = None
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_4(self, mutation: NormativeActMutation) -> None:
        """Appends a mutation delta to the Write Model ledger."""
        mut_id = mutation.id or uuid.uuid4()
        model = NormativeActMutationModel(
            id=None,
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
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_5(self, mutation: NormativeActMutation) -> None:
        """Appends a mutation delta to the Write Model ledger."""
        mut_id = mutation.id or uuid.uuid4()
        model = NormativeActMutationModel(
            id=mut_id,
            target_act_id=None,
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
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_6(self, mutation: NormativeActMutation) -> None:
        """Appends a mutation delta to the Write Model ledger."""
        mut_id = mutation.id or uuid.uuid4()
        model = NormativeActMutationModel(
            id=mut_id,
            target_act_id=mutation.target_act_id,
            target_node_path=None,
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
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_7(self, mutation: NormativeActMutation) -> None:
        """Appends a mutation delta to the Write Model ledger."""
        mut_id = mutation.id or uuid.uuid4()
        model = NormativeActMutationModel(
            id=mut_id,
            target_act_id=mutation.target_act_id,
            target_node_path=mutation.target_node_path.value,
            author_act_id=None,
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
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_8(self, mutation: NormativeActMutation) -> None:
        """Appends a mutation delta to the Write Model ledger."""
        mut_id = mutation.id or uuid.uuid4()
        model = NormativeActMutationModel(
            id=mut_id,
            target_act_id=mutation.target_act_id,
            target_node_path=mutation.target_node_path.value,
            author_act_id=mutation.author_act_id,
            author_dispositivo_ref=None,
            mutation_type=mutation.mutation_type.value,
            new_text=mutation.new_text,
            new_structured_payload=mutation.new_structured_payload,
            publication_date=mutation.publication_date.value,
            effective_date=mutation.effective_date.value,
            extraction_source=mutation.extraction_source,
            confidence_score=mutation.confidence_score,
            mutation_sha256=mutation.mutation_sha256.hex_digest,
        )
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_9(self, mutation: NormativeActMutation) -> None:
        """Appends a mutation delta to the Write Model ledger."""
        mut_id = mutation.id or uuid.uuid4()
        model = NormativeActMutationModel(
            id=mut_id,
            target_act_id=mutation.target_act_id,
            target_node_path=mutation.target_node_path.value,
            author_act_id=mutation.author_act_id,
            author_dispositivo_ref=mutation.author_dispositivo_ref,
            mutation_type=None,
            new_text=mutation.new_text,
            new_structured_payload=mutation.new_structured_payload,
            publication_date=mutation.publication_date.value,
            effective_date=mutation.effective_date.value,
            extraction_source=mutation.extraction_source,
            confidence_score=mutation.confidence_score,
            mutation_sha256=mutation.mutation_sha256.hex_digest,
        )
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_10(self, mutation: NormativeActMutation) -> None:
        """Appends a mutation delta to the Write Model ledger."""
        mut_id = mutation.id or uuid.uuid4()
        model = NormativeActMutationModel(
            id=mut_id,
            target_act_id=mutation.target_act_id,
            target_node_path=mutation.target_node_path.value,
            author_act_id=mutation.author_act_id,
            author_dispositivo_ref=mutation.author_dispositivo_ref,
            mutation_type=mutation.mutation_type.value,
            new_text=None,
            new_structured_payload=mutation.new_structured_payload,
            publication_date=mutation.publication_date.value,
            effective_date=mutation.effective_date.value,
            extraction_source=mutation.extraction_source,
            confidence_score=mutation.confidence_score,
            mutation_sha256=mutation.mutation_sha256.hex_digest,
        )
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_11(self, mutation: NormativeActMutation) -> None:
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
            new_structured_payload=None,
            publication_date=mutation.publication_date.value,
            effective_date=mutation.effective_date.value,
            extraction_source=mutation.extraction_source,
            confidence_score=mutation.confidence_score,
            mutation_sha256=mutation.mutation_sha256.hex_digest,
        )
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_12(self, mutation: NormativeActMutation) -> None:
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
            publication_date=None,
            effective_date=mutation.effective_date.value,
            extraction_source=mutation.extraction_source,
            confidence_score=mutation.confidence_score,
            mutation_sha256=mutation.mutation_sha256.hex_digest,
        )
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_13(self, mutation: NormativeActMutation) -> None:
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
            effective_date=None,
            extraction_source=mutation.extraction_source,
            confidence_score=mutation.confidence_score,
            mutation_sha256=mutation.mutation_sha256.hex_digest,
        )
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_14(self, mutation: NormativeActMutation) -> None:
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
            extraction_source=None,
            confidence_score=mutation.confidence_score,
            mutation_sha256=mutation.mutation_sha256.hex_digest,
        )
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_15(self, mutation: NormativeActMutation) -> None:
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
            confidence_score=None,
            mutation_sha256=mutation.mutation_sha256.hex_digest,
        )
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_16(self, mutation: NormativeActMutation) -> None:
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
            mutation_sha256=None,
        )
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_17(self, mutation: NormativeActMutation) -> None:
        """Appends a mutation delta to the Write Model ledger."""
        mut_id = mutation.id or uuid.uuid4()
        model = NormativeActMutationModel(
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
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_18(self, mutation: NormativeActMutation) -> None:
        """Appends a mutation delta to the Write Model ledger."""
        mut_id = mutation.id or uuid.uuid4()
        model = NormativeActMutationModel(
            id=mut_id,
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
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_19(self, mutation: NormativeActMutation) -> None:
        """Appends a mutation delta to the Write Model ledger."""
        mut_id = mutation.id or uuid.uuid4()
        model = NormativeActMutationModel(
            id=mut_id,
            target_act_id=mutation.target_act_id,
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
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_20(self, mutation: NormativeActMutation) -> None:
        """Appends a mutation delta to the Write Model ledger."""
        mut_id = mutation.id or uuid.uuid4()
        model = NormativeActMutationModel(
            id=mut_id,
            target_act_id=mutation.target_act_id,
            target_node_path=mutation.target_node_path.value,
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
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_21(self, mutation: NormativeActMutation) -> None:
        """Appends a mutation delta to the Write Model ledger."""
        mut_id = mutation.id or uuid.uuid4()
        model = NormativeActMutationModel(
            id=mut_id,
            target_act_id=mutation.target_act_id,
            target_node_path=mutation.target_node_path.value,
            author_act_id=mutation.author_act_id,
            mutation_type=mutation.mutation_type.value,
            new_text=mutation.new_text,
            new_structured_payload=mutation.new_structured_payload,
            publication_date=mutation.publication_date.value,
            effective_date=mutation.effective_date.value,
            extraction_source=mutation.extraction_source,
            confidence_score=mutation.confidence_score,
            mutation_sha256=mutation.mutation_sha256.hex_digest,
        )
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_22(self, mutation: NormativeActMutation) -> None:
        """Appends a mutation delta to the Write Model ledger."""
        mut_id = mutation.id or uuid.uuid4()
        model = NormativeActMutationModel(
            id=mut_id,
            target_act_id=mutation.target_act_id,
            target_node_path=mutation.target_node_path.value,
            author_act_id=mutation.author_act_id,
            author_dispositivo_ref=mutation.author_dispositivo_ref,
            new_text=mutation.new_text,
            new_structured_payload=mutation.new_structured_payload,
            publication_date=mutation.publication_date.value,
            effective_date=mutation.effective_date.value,
            extraction_source=mutation.extraction_source,
            confidence_score=mutation.confidence_score,
            mutation_sha256=mutation.mutation_sha256.hex_digest,
        )
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_23(self, mutation: NormativeActMutation) -> None:
        """Appends a mutation delta to the Write Model ledger."""
        mut_id = mutation.id or uuid.uuid4()
        model = NormativeActMutationModel(
            id=mut_id,
            target_act_id=mutation.target_act_id,
            target_node_path=mutation.target_node_path.value,
            author_act_id=mutation.author_act_id,
            author_dispositivo_ref=mutation.author_dispositivo_ref,
            mutation_type=mutation.mutation_type.value,
            new_structured_payload=mutation.new_structured_payload,
            publication_date=mutation.publication_date.value,
            effective_date=mutation.effective_date.value,
            extraction_source=mutation.extraction_source,
            confidence_score=mutation.confidence_score,
            mutation_sha256=mutation.mutation_sha256.hex_digest,
        )
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_24(self, mutation: NormativeActMutation) -> None:
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
            publication_date=mutation.publication_date.value,
            effective_date=mutation.effective_date.value,
            extraction_source=mutation.extraction_source,
            confidence_score=mutation.confidence_score,
            mutation_sha256=mutation.mutation_sha256.hex_digest,
        )
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_25(self, mutation: NormativeActMutation) -> None:
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
            effective_date=mutation.effective_date.value,
            extraction_source=mutation.extraction_source,
            confidence_score=mutation.confidence_score,
            mutation_sha256=mutation.mutation_sha256.hex_digest,
        )
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_26(self, mutation: NormativeActMutation) -> None:
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
            extraction_source=mutation.extraction_source,
            confidence_score=mutation.confidence_score,
            mutation_sha256=mutation.mutation_sha256.hex_digest,
        )
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_27(self, mutation: NormativeActMutation) -> None:
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
            confidence_score=mutation.confidence_score,
            mutation_sha256=mutation.mutation_sha256.hex_digest,
        )
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_28(self, mutation: NormativeActMutation) -> None:
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
            mutation_sha256=mutation.mutation_sha256.hex_digest,
        )
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_29(self, mutation: NormativeActMutation) -> None:
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
            )
        self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_30(self, mutation: NormativeActMutation) -> None:
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
        self._session.add(None)
        self._session.commit()

    @_mutmut_mutated(mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut)
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_orig(self, target_act_id: UUID) -> list[NormativeActMutation]:
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_1(self, target_act_id: UUID) -> list[NormativeActMutation]:
        """Fetches all mutations targeting a given statute, ordered chronologically."""
        stmt = None
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_2(self, target_act_id: UUID) -> list[NormativeActMutation]:
        """Fetches all mutations targeting a given statute, ordered chronologically."""
        stmt = (
            select(NormativeActMutationModel)
            .where(NormativeActMutationModel.target_act_id == target_act_id)
            .order_by(
                None,
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_3(self, target_act_id: UUID) -> list[NormativeActMutation]:
        """Fetches all mutations targeting a given statute, ordered chronologically."""
        stmt = (
            select(NormativeActMutationModel)
            .where(NormativeActMutationModel.target_act_id == target_act_id)
            .order_by(
                NormativeActMutationModel.effective_date.asc(),
                None,
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_4(self, target_act_id: UUID) -> list[NormativeActMutation]:
        """Fetches all mutations targeting a given statute, ordered chronologically."""
        stmt = (
            select(NormativeActMutationModel)
            .where(NormativeActMutationModel.target_act_id == target_act_id)
            .order_by(
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_5(self, target_act_id: UUID) -> list[NormativeActMutation]:
        """Fetches all mutations targeting a given statute, ordered chronologically."""
        stmt = (
            select(NormativeActMutationModel)
            .where(NormativeActMutationModel.target_act_id == target_act_id)
            .order_by(
                NormativeActMutationModel.effective_date.asc(),
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_6(self, target_act_id: UUID) -> list[NormativeActMutation]:
        """Fetches all mutations targeting a given statute, ordered chronologically."""
        stmt = (
            select(NormativeActMutationModel)
            .where(None)
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_7(self, target_act_id: UUID) -> list[NormativeActMutation]:
        """Fetches all mutations targeting a given statute, ordered chronologically."""
        stmt = (
            select(None)
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_8(self, target_act_id: UUID) -> list[NormativeActMutation]:
        """Fetches all mutations targeting a given statute, ordered chronologically."""
        stmt = (
            select(NormativeActMutationModel)
            .where(NormativeActMutationModel.target_act_id != target_act_id)
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_9(self, target_act_id: UUID) -> list[NormativeActMutation]:
        """Fetches all mutations targeting a given statute, ordered chronologically."""
        stmt = (
            select(NormativeActMutationModel)
            .where(NormativeActMutationModel.target_act_id == target_act_id)
            .order_by(
                NormativeActMutationModel.effective_date.asc(),
                NormativeActMutationModel.created_at.asc(),
            )
        )
        rows = None
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_10(self, target_act_id: UUID) -> list[NormativeActMutation]:
        """Fetches all mutations targeting a given statute, ordered chronologically."""
        stmt = (
            select(NormativeActMutationModel)
            .where(NormativeActMutationModel.target_act_id == target_act_id)
            .order_by(
                NormativeActMutationModel.effective_date.asc(),
                NormativeActMutationModel.created_at.asc(),
            )
        )
        rows = self._session.scalars(None).all()
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_11(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
        mutations: list[NormativeActMutation] = None
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_12(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                None
            )
        return mutations

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_13(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    id=None,
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_14(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    target_act_id=None,
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_15(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    target_node_path=None,
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_16(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    author_act_id=None,
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_17(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    author_dispositivo_ref=None,
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_18(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    mutation_type=None,
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_19(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    new_text=None,
                    new_structured_payload=r.new_structured_payload,
                    publication_date=GazetteDate.from_date(r.publication_date),
                    effective_date=GazetteDate.from_date(r.effective_date),
                    extraction_source=r.extraction_source,
                    confidence_score=r.confidence_score,
                    mutation_sha256=DocumentHash.from_text(r.mutation_sha256),
                )
            )
        return mutations

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_20(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    new_structured_payload=None,
                    publication_date=GazetteDate.from_date(r.publication_date),
                    effective_date=GazetteDate.from_date(r.effective_date),
                    extraction_source=r.extraction_source,
                    confidence_score=r.confidence_score,
                    mutation_sha256=DocumentHash.from_text(r.mutation_sha256),
                )
            )
        return mutations

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_21(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    publication_date=None,
                    effective_date=GazetteDate.from_date(r.effective_date),
                    extraction_source=r.extraction_source,
                    confidence_score=r.confidence_score,
                    mutation_sha256=DocumentHash.from_text(r.mutation_sha256),
                )
            )
        return mutations

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_22(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    effective_date=None,
                    extraction_source=r.extraction_source,
                    confidence_score=r.confidence_score,
                    mutation_sha256=DocumentHash.from_text(r.mutation_sha256),
                )
            )
        return mutations

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_23(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    extraction_source=None,
                    confidence_score=r.confidence_score,
                    mutation_sha256=DocumentHash.from_text(r.mutation_sha256),
                )
            )
        return mutations

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_24(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    confidence_score=None,
                    mutation_sha256=DocumentHash.from_text(r.mutation_sha256),
                )
            )
        return mutations

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_25(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    mutation_sha256=None,
                )
            )
        return mutations

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_26(self, target_act_id: UUID) -> list[NormativeActMutation]:
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_27(self, target_act_id: UUID) -> list[NormativeActMutation]:
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_28(self, target_act_id: UUID) -> list[NormativeActMutation]:
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_29(self, target_act_id: UUID) -> list[NormativeActMutation]:
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_30(self, target_act_id: UUID) -> list[NormativeActMutation]:
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_31(self, target_act_id: UUID) -> list[NormativeActMutation]:
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_32(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    new_structured_payload=r.new_structured_payload,
                    publication_date=GazetteDate.from_date(r.publication_date),
                    effective_date=GazetteDate.from_date(r.effective_date),
                    extraction_source=r.extraction_source,
                    confidence_score=r.confidence_score,
                    mutation_sha256=DocumentHash.from_text(r.mutation_sha256),
                )
            )
        return mutations

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_33(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    publication_date=GazetteDate.from_date(r.publication_date),
                    effective_date=GazetteDate.from_date(r.effective_date),
                    extraction_source=r.extraction_source,
                    confidence_score=r.confidence_score,
                    mutation_sha256=DocumentHash.from_text(r.mutation_sha256),
                )
            )
        return mutations

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_34(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    effective_date=GazetteDate.from_date(r.effective_date),
                    extraction_source=r.extraction_source,
                    confidence_score=r.confidence_score,
                    mutation_sha256=DocumentHash.from_text(r.mutation_sha256),
                )
            )
        return mutations

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_35(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    extraction_source=r.extraction_source,
                    confidence_score=r.confidence_score,
                    mutation_sha256=DocumentHash.from_text(r.mutation_sha256),
                )
            )
        return mutations

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_36(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    confidence_score=r.confidence_score,
                    mutation_sha256=DocumentHash.from_text(r.mutation_sha256),
                )
            )
        return mutations

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_37(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    mutation_sha256=DocumentHash.from_text(r.mutation_sha256),
                )
            )
        return mutations

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_38(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    )
            )
        return mutations

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_39(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    target_node_path=CanonicalNodePath.from_string(None),
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_40(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    mutation_type=MutationType(None),
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

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_41(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    publication_date=GazetteDate.from_date(None),
                    effective_date=GazetteDate.from_date(r.effective_date),
                    extraction_source=r.extraction_source,
                    confidence_score=r.confidence_score,
                    mutation_sha256=DocumentHash.from_text(r.mutation_sha256),
                )
            )
        return mutations

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_42(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    effective_date=GazetteDate.from_date(None),
                    extraction_source=r.extraction_source,
                    confidence_score=r.confidence_score,
                    mutation_sha256=DocumentHash.from_text(r.mutation_sha256),
                )
            )
        return mutations

    async def xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_43(self, target_act_id: UUID) -> list[NormativeActMutation]:
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
                    mutation_sha256=DocumentHash.from_text(None),
                )
            )
        return mutations

    @_mutmut_mutated(mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut)
    async def save_compiled_act(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_orig(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_1(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
        existing = None
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_2(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
        existing = self._session.get(None, compiled_act.act_id)
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_3(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
        existing = self._session.get(CompiledNormativeActModel, None)
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_4(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
        existing = self._session.get(compiled_act.act_id)
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_5(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
        existing = self._session.get(CompiledNormativeActModel, )
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_6(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
        existing = self._session.get(CompiledNormativeActModel, compiled_act.act_id)
        if existing:
            existing.compiled_version_hash = None
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_7(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
        existing = self._session.get(CompiledNormativeActModel, compiled_act.act_id)
        if existing:
            existing.compiled_version_hash = compiled_act.compiled_version_hash
            existing.total_mutations_applied = None
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_8(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
        existing = self._session.get(CompiledNormativeActModel, compiled_act.act_id)
        if existing:
            existing.compiled_version_hash = compiled_act.compiled_version_hash
            existing.total_mutations_applied = compiled_act.total_mutations_applied
            existing.last_mutation_effective_date = None
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_9(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
        existing = self._session.get(CompiledNormativeActModel, compiled_act.act_id)
        if existing:
            existing.compiled_version_hash = compiled_act.compiled_version_hash
            existing.total_mutations_applied = compiled_act.total_mutations_applied
            existing.last_mutation_effective_date = compiled_act.last_mutation_effective_date
            existing.compiled_ast = None
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_10(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
        existing = self._session.get(CompiledNormativeActModel, compiled_act.act_id)
        if existing:
            existing.compiled_version_hash = compiled_act.compiled_version_hash
            existing.total_mutations_applied = compiled_act.total_mutations_applied
            existing.last_mutation_effective_date = compiled_act.last_mutation_effective_date
            existing.compiled_ast = compiled_act.compiled_ast.to_dict()
            existing.compiled_html = None
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_11(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
        existing = self._session.get(CompiledNormativeActModel, compiled_act.act_id)
        if existing:
            existing.compiled_version_hash = compiled_act.compiled_version_hash
            existing.total_mutations_applied = compiled_act.total_mutations_applied
            existing.last_mutation_effective_date = compiled_act.last_mutation_effective_date
            existing.compiled_ast = compiled_act.compiled_ast.to_dict()
            existing.compiled_html = compiled_act.compiled_html
            existing.compiled_markdown = None
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_12(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
        existing = self._session.get(CompiledNormativeActModel, compiled_act.act_id)
        if existing:
            existing.compiled_version_hash = compiled_act.compiled_version_hash
            existing.total_mutations_applied = compiled_act.total_mutations_applied
            existing.last_mutation_effective_date = compiled_act.last_mutation_effective_date
            existing.compiled_ast = compiled_act.compiled_ast.to_dict()
            existing.compiled_html = compiled_act.compiled_html
            existing.compiled_markdown = compiled_act.compiled_markdown
            existing.active_articles_count = None
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_13(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
        existing = self._session.get(CompiledNormativeActModel, compiled_act.act_id)
        if existing:
            existing.compiled_version_hash = compiled_act.compiled_version_hash
            existing.total_mutations_applied = compiled_act.total_mutations_applied
            existing.last_mutation_effective_date = compiled_act.last_mutation_effective_date
            existing.compiled_ast = compiled_act.compiled_ast.to_dict()
            existing.compiled_html = compiled_act.compiled_html
            existing.compiled_markdown = compiled_act.compiled_markdown
            existing.active_articles_count = compiled_act.active_articles_count
            existing.revoked_articles_count = None
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_14(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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
            existing.last_compiled_at = None
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_15(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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
            existing.updated_at = None
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_16(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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
            existing.updated_at = datetime.now(None)
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_17(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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
            model = None
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_18(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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
                act_id=None,
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_19(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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
                compiled_version_hash=None,
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_20(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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
                total_mutations_applied=None,
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_21(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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
                last_mutation_effective_date=None,
                compiled_ast=compiled_act.compiled_ast.to_dict(),
                compiled_html=compiled_act.compiled_html,
                compiled_markdown=compiled_act.compiled_markdown,
                active_articles_count=compiled_act.active_articles_count,
                revoked_articles_count=compiled_act.revoked_articles_count,
                last_compiled_at=compiled_act.last_compiled_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_22(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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
                compiled_ast=None,
                compiled_html=compiled_act.compiled_html,
                compiled_markdown=compiled_act.compiled_markdown,
                active_articles_count=compiled_act.active_articles_count,
                revoked_articles_count=compiled_act.revoked_articles_count,
                last_compiled_at=compiled_act.last_compiled_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_23(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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
                compiled_html=None,
                compiled_markdown=compiled_act.compiled_markdown,
                active_articles_count=compiled_act.active_articles_count,
                revoked_articles_count=compiled_act.revoked_articles_count,
                last_compiled_at=compiled_act.last_compiled_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_24(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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
                compiled_markdown=None,
                active_articles_count=compiled_act.active_articles_count,
                revoked_articles_count=compiled_act.revoked_articles_count,
                last_compiled_at=compiled_act.last_compiled_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_25(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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
                active_articles_count=None,
                revoked_articles_count=compiled_act.revoked_articles_count,
                last_compiled_at=compiled_act.last_compiled_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_26(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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
                revoked_articles_count=None,
                last_compiled_at=compiled_act.last_compiled_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_27(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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
                last_compiled_at=None,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_28(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_29(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_30(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_31(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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
                compiled_ast=compiled_act.compiled_ast.to_dict(),
                compiled_html=compiled_act.compiled_html,
                compiled_markdown=compiled_act.compiled_markdown,
                active_articles_count=compiled_act.active_articles_count,
                revoked_articles_count=compiled_act.revoked_articles_count,
                last_compiled_at=compiled_act.last_compiled_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_32(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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
                compiled_html=compiled_act.compiled_html,
                compiled_markdown=compiled_act.compiled_markdown,
                active_articles_count=compiled_act.active_articles_count,
                revoked_articles_count=compiled_act.revoked_articles_count,
                last_compiled_at=compiled_act.last_compiled_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_33(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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
                compiled_markdown=compiled_act.compiled_markdown,
                active_articles_count=compiled_act.active_articles_count,
                revoked_articles_count=compiled_act.revoked_articles_count,
                last_compiled_at=compiled_act.last_compiled_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_34(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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
                active_articles_count=compiled_act.active_articles_count,
                revoked_articles_count=compiled_act.revoked_articles_count,
                last_compiled_at=compiled_act.last_compiled_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_35(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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
                revoked_articles_count=compiled_act.revoked_articles_count,
                last_compiled_at=compiled_act.last_compiled_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_36(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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
                last_compiled_at=compiled_act.last_compiled_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_37(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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
                )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_38(self, compiled_act: CompiledNormativeAct) -> None:
        """Upserts a materialized compiled act projection in the read model."""
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
            self._session.add(None)
        self._session.commit()

    @_mutmut_mutated(mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut)
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

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_orig(self, act_id: UUID) -> CompiledNormativeAct | None:
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

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_1(self, act_id: UUID) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by statute UUID."""
        row = None
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

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_2(self, act_id: UUID) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by statute UUID."""
        row = self._session.get(None, act_id)
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

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_3(self, act_id: UUID) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by statute UUID."""
        row = self._session.get(CompiledNormativeActModel, None)
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

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_4(self, act_id: UUID) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by statute UUID."""
        row = self._session.get(act_id)
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

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_5(self, act_id: UUID) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by statute UUID."""
        row = self._session.get(CompiledNormativeActModel, )
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

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_6(self, act_id: UUID) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by statute UUID."""
        row = self._session.get(CompiledNormativeActModel, act_id)
        if row:
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

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_7(self, act_id: UUID) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by statute UUID."""
        row = self._session.get(CompiledNormativeActModel, act_id)
        if not row:
            return None

        ast = None
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

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_8(self, act_id: UUID) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by statute UUID."""
        row = self._session.get(CompiledNormativeActModel, act_id)
        if not row:
            return None

        ast = ActAst.from_dict(None)
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

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_9(self, act_id: UUID) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by statute UUID."""
        row = self._session.get(CompiledNormativeActModel, act_id)
        if not row:
            return None

        ast = ActAst.from_dict(row.compiled_ast)
        return CompiledNormativeAct(
            act_id=None,
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

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_10(self, act_id: UUID) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by statute UUID."""
        row = self._session.get(CompiledNormativeActModel, act_id)
        if not row:
            return None

        ast = ActAst.from_dict(row.compiled_ast)
        return CompiledNormativeAct(
            act_id=row.act_id,
            compiled_version_hash=None,
            total_mutations_applied=row.total_mutations_applied,
            last_mutation_effective_date=row.last_mutation_effective_date,
            compiled_ast=ast,
            compiled_html=row.compiled_html,
            compiled_markdown=row.compiled_markdown,
            active_articles_count=row.active_articles_count,
            revoked_articles_count=row.revoked_articles_count,
            last_compiled_at=row.last_compiled_at,
        )

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_11(self, act_id: UUID) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by statute UUID."""
        row = self._session.get(CompiledNormativeActModel, act_id)
        if not row:
            return None

        ast = ActAst.from_dict(row.compiled_ast)
        return CompiledNormativeAct(
            act_id=row.act_id,
            compiled_version_hash=row.compiled_version_hash,
            total_mutations_applied=None,
            last_mutation_effective_date=row.last_mutation_effective_date,
            compiled_ast=ast,
            compiled_html=row.compiled_html,
            compiled_markdown=row.compiled_markdown,
            active_articles_count=row.active_articles_count,
            revoked_articles_count=row.revoked_articles_count,
            last_compiled_at=row.last_compiled_at,
        )

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_12(self, act_id: UUID) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by statute UUID."""
        row = self._session.get(CompiledNormativeActModel, act_id)
        if not row:
            return None

        ast = ActAst.from_dict(row.compiled_ast)
        return CompiledNormativeAct(
            act_id=row.act_id,
            compiled_version_hash=row.compiled_version_hash,
            total_mutations_applied=row.total_mutations_applied,
            last_mutation_effective_date=None,
            compiled_ast=ast,
            compiled_html=row.compiled_html,
            compiled_markdown=row.compiled_markdown,
            active_articles_count=row.active_articles_count,
            revoked_articles_count=row.revoked_articles_count,
            last_compiled_at=row.last_compiled_at,
        )

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_13(self, act_id: UUID) -> CompiledNormativeAct | None:
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
            compiled_ast=None,
            compiled_html=row.compiled_html,
            compiled_markdown=row.compiled_markdown,
            active_articles_count=row.active_articles_count,
            revoked_articles_count=row.revoked_articles_count,
            last_compiled_at=row.last_compiled_at,
        )

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_14(self, act_id: UUID) -> CompiledNormativeAct | None:
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
            compiled_html=None,
            compiled_markdown=row.compiled_markdown,
            active_articles_count=row.active_articles_count,
            revoked_articles_count=row.revoked_articles_count,
            last_compiled_at=row.last_compiled_at,
        )

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_15(self, act_id: UUID) -> CompiledNormativeAct | None:
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
            compiled_markdown=None,
            active_articles_count=row.active_articles_count,
            revoked_articles_count=row.revoked_articles_count,
            last_compiled_at=row.last_compiled_at,
        )

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_16(self, act_id: UUID) -> CompiledNormativeAct | None:
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
            active_articles_count=None,
            revoked_articles_count=row.revoked_articles_count,
            last_compiled_at=row.last_compiled_at,
        )

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_17(self, act_id: UUID) -> CompiledNormativeAct | None:
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
            revoked_articles_count=None,
            last_compiled_at=row.last_compiled_at,
        )

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_18(self, act_id: UUID) -> CompiledNormativeAct | None:
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
            last_compiled_at=None,
        )

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_19(self, act_id: UUID) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by statute UUID."""
        row = self._session.get(CompiledNormativeActModel, act_id)
        if not row:
            return None

        ast = ActAst.from_dict(row.compiled_ast)
        return CompiledNormativeAct(
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

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_20(self, act_id: UUID) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by statute UUID."""
        row = self._session.get(CompiledNormativeActModel, act_id)
        if not row:
            return None

        ast = ActAst.from_dict(row.compiled_ast)
        return CompiledNormativeAct(
            act_id=row.act_id,
            total_mutations_applied=row.total_mutations_applied,
            last_mutation_effective_date=row.last_mutation_effective_date,
            compiled_ast=ast,
            compiled_html=row.compiled_html,
            compiled_markdown=row.compiled_markdown,
            active_articles_count=row.active_articles_count,
            revoked_articles_count=row.revoked_articles_count,
            last_compiled_at=row.last_compiled_at,
        )

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_21(self, act_id: UUID) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by statute UUID."""
        row = self._session.get(CompiledNormativeActModel, act_id)
        if not row:
            return None

        ast = ActAst.from_dict(row.compiled_ast)
        return CompiledNormativeAct(
            act_id=row.act_id,
            compiled_version_hash=row.compiled_version_hash,
            last_mutation_effective_date=row.last_mutation_effective_date,
            compiled_ast=ast,
            compiled_html=row.compiled_html,
            compiled_markdown=row.compiled_markdown,
            active_articles_count=row.active_articles_count,
            revoked_articles_count=row.revoked_articles_count,
            last_compiled_at=row.last_compiled_at,
        )

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_22(self, act_id: UUID) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by statute UUID."""
        row = self._session.get(CompiledNormativeActModel, act_id)
        if not row:
            return None

        ast = ActAst.from_dict(row.compiled_ast)
        return CompiledNormativeAct(
            act_id=row.act_id,
            compiled_version_hash=row.compiled_version_hash,
            total_mutations_applied=row.total_mutations_applied,
            compiled_ast=ast,
            compiled_html=row.compiled_html,
            compiled_markdown=row.compiled_markdown,
            active_articles_count=row.active_articles_count,
            revoked_articles_count=row.revoked_articles_count,
            last_compiled_at=row.last_compiled_at,
        )

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_23(self, act_id: UUID) -> CompiledNormativeAct | None:
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
            compiled_html=row.compiled_html,
            compiled_markdown=row.compiled_markdown,
            active_articles_count=row.active_articles_count,
            revoked_articles_count=row.revoked_articles_count,
            last_compiled_at=row.last_compiled_at,
        )

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_24(self, act_id: UUID) -> CompiledNormativeAct | None:
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
            compiled_markdown=row.compiled_markdown,
            active_articles_count=row.active_articles_count,
            revoked_articles_count=row.revoked_articles_count,
            last_compiled_at=row.last_compiled_at,
        )

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_25(self, act_id: UUID) -> CompiledNormativeAct | None:
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
            active_articles_count=row.active_articles_count,
            revoked_articles_count=row.revoked_articles_count,
            last_compiled_at=row.last_compiled_at,
        )

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_26(self, act_id: UUID) -> CompiledNormativeAct | None:
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
            revoked_articles_count=row.revoked_articles_count,
            last_compiled_at=row.last_compiled_at,
        )

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_27(self, act_id: UUID) -> CompiledNormativeAct | None:
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
            last_compiled_at=row.last_compiled_at,
        )

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_28(self, act_id: UUID) -> CompiledNormativeAct | None:
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
            )

    @_mutmut_mutated(mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut)
    async def get_compiled_act_by_urn(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_orig(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_1(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = None
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_2(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(None)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_3(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = None
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_4(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(None).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_5(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get(None) == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_6(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("XXcanonical_urnXX") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_7(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("CANONICAL_URN") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_8(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") != canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_9(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = None
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_10(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(None)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_11(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=None,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_12(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=None,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_13(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=None,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_14(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=None,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_15(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=None,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_16(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=None,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_17(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=None,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_18(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=None,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_19(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=None,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_20(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=None,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_21(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_22(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_23(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_24(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_25(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_26(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_27(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_28(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    revoked_articles_count=r.revoked_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_29(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    last_compiled_at=r.last_compiled_at,
                )
        return None

    async def xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_30(self, canonical_urn: str) -> CompiledNormativeAct | None:
        """Retrieves the current compiled act projection by LexML URN."""
        stmt = select(CompiledNormativeActModel)
        rows = self._session.scalars(stmt).all()
        for r in rows:
            if r.compiled_ast.get("canonical_urn") == canonical_urn:
                ast = ActAst.from_dict(r.compiled_ast)
                return CompiledNormativeAct(
                    act_id=r.act_id,
                    compiled_version_hash=r.compiled_version_hash,
                    total_mutations_applied=r.total_mutations_applied,
                    last_mutation_effective_date=r.last_mutation_effective_date,
                    compiled_ast=ast,
                    compiled_html=r.compiled_html,
                    compiled_markdown=r.compiled_markdown,
                    active_articles_count=r.active_articles_count,
                    revoked_articles_count=r.revoked_articles_count,
                    )
        return None

    @_mutmut_mutated(mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut)
    async def enqueue_backfill_task(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
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

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_orig(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
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

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_1(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
        stmt = None
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

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_2(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
        stmt = select(LegislationBackfillQueueModel).where(
            None
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

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_3(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
        stmt = select(None).where(
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

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_4(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
        stmt = select(LegislationBackfillQueueModel).where(
            LegislationBackfillQueueModel.canonical_urn != task.canonical_urn.value
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

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_5(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
        stmt = select(LegislationBackfillQueueModel).where(
            LegislationBackfillQueueModel.canonical_urn == task.canonical_urn.value
        )
        existing = None
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

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_6(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
        stmt = select(LegislationBackfillQueueModel).where(
            LegislationBackfillQueueModel.canonical_urn == task.canonical_urn.value
        )
        existing = self._session.scalars(None).first()
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

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_7(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
        stmt = select(LegislationBackfillQueueModel).where(
            LegislationBackfillQueueModel.canonical_urn == task.canonical_urn.value
        )
        existing = self._session.scalars(stmt).first()
        if existing:
            existing.citation_count = 1
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

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_8(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
        stmt = select(LegislationBackfillQueueModel).where(
            LegislationBackfillQueueModel.canonical_urn == task.canonical_urn.value
        )
        existing = self._session.scalars(stmt).first()
        if existing:
            existing.citation_count -= 1
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

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_9(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
        stmt = select(LegislationBackfillQueueModel).where(
            LegislationBackfillQueueModel.canonical_urn == task.canonical_urn.value
        )
        existing = self._session.scalars(stmt).first()
        if existing:
            existing.citation_count += 2
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

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_10(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
        stmt = select(LegislationBackfillQueueModel).where(
            LegislationBackfillQueueModel.canonical_urn == task.canonical_urn.value
        )
        existing = self._session.scalars(stmt).first()
        if existing:
            existing.citation_count += 1
            existing.last_requested_at = None
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

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_11(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
        stmt = select(LegislationBackfillQueueModel).where(
            LegislationBackfillQueueModel.canonical_urn == task.canonical_urn.value
        )
        existing = self._session.scalars(stmt).first()
        if existing:
            existing.citation_count += 1
            existing.last_requested_at = datetime.now(None)
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

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_12(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
        stmt = select(LegislationBackfillQueueModel).where(
            LegislationBackfillQueueModel.canonical_urn == task.canonical_urn.value
        )
        existing = self._session.scalars(stmt).first()
        if existing:
            existing.citation_count += 1
            existing.last_requested_at = datetime.now(UTC)
        else:
            task_id = None
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

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_13(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
        stmt = select(LegislationBackfillQueueModel).where(
            LegislationBackfillQueueModel.canonical_urn == task.canonical_urn.value
        )
        existing = self._session.scalars(stmt).first()
        if existing:
            existing.citation_count += 1
            existing.last_requested_at = datetime.now(UTC)
        else:
            task_id = task.id and uuid.uuid4()
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

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_14(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
        stmt = select(LegislationBackfillQueueModel).where(
            LegislationBackfillQueueModel.canonical_urn == task.canonical_urn.value
        )
        existing = self._session.scalars(stmt).first()
        if existing:
            existing.citation_count += 1
            existing.last_requested_at = datetime.now(UTC)
        else:
            task_id = task.id or uuid.uuid4()
            model = None
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_15(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
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
                id=None,
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

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_16(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
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
                canonical_urn=None,
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

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_17(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
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
                territory_id=None,
                act_type=task.act_type,
                act_number=task.act_number,
                act_year=task.act_year,
                citation_count=task.citation_count,
                status=task.status,
                last_requested_at=task.last_requested_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_18(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
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
                act_type=None,
                act_number=task.act_number,
                act_year=task.act_year,
                citation_count=task.citation_count,
                status=task.status,
                last_requested_at=task.last_requested_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_19(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
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
                act_number=None,
                act_year=task.act_year,
                citation_count=task.citation_count,
                status=task.status,
                last_requested_at=task.last_requested_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_20(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
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
                act_year=None,
                citation_count=task.citation_count,
                status=task.status,
                last_requested_at=task.last_requested_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_21(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
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
                citation_count=None,
                status=task.status,
                last_requested_at=task.last_requested_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_22(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
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
                status=None,
                last_requested_at=task.last_requested_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_23(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
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
                last_requested_at=None,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_24(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
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

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_25(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
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

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_26(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
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
                act_type=task.act_type,
                act_number=task.act_number,
                act_year=task.act_year,
                citation_count=task.citation_count,
                status=task.status,
                last_requested_at=task.last_requested_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_27(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
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
                act_number=task.act_number,
                act_year=task.act_year,
                citation_count=task.citation_count,
                status=task.status,
                last_requested_at=task.last_requested_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_28(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
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
                act_year=task.act_year,
                citation_count=task.citation_count,
                status=task.status,
                last_requested_at=task.last_requested_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_29(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
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
                citation_count=task.citation_count,
                status=task.status,
                last_requested_at=task.last_requested_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_30(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
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
                status=task.status,
                last_requested_at=task.last_requested_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_31(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
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
                last_requested_at=task.last_requested_at,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_32(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
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
                )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_33(self, task: LegislationBackfillTask) -> None:
        """Enqueues or increments citation count of a missing statute in the JIT queue."""
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
            self._session.add(None)
        self._session.commit()

    @_mutmut_mutated(mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut)
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

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_orig(self, limit: int = 20) -> list[LegislationBackfillTask]:
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

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_1(self, limit: int = 21) -> list[LegislationBackfillTask]:
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

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_2(self, limit: int = 20) -> list[LegislationBackfillTask]:
        """Lists highest priority un-resolved backfill tasks."""
        stmt = None
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

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_3(self, limit: int = 20) -> list[LegislationBackfillTask]:
        """Lists highest priority un-resolved backfill tasks."""
        stmt = (
            select(LegislationBackfillQueueModel)
            .where(LegislationBackfillQueueModel.status == "PENDING")
            .order_by(LegislationBackfillQueueModel.citation_count.desc())
            .limit(None)
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

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_4(self, limit: int = 20) -> list[LegislationBackfillTask]:
        """Lists highest priority un-resolved backfill tasks."""
        stmt = (
            select(LegislationBackfillQueueModel)
            .where(LegislationBackfillQueueModel.status == "PENDING")
            .order_by(None)
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

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_5(self, limit: int = 20) -> list[LegislationBackfillTask]:
        """Lists highest priority un-resolved backfill tasks."""
        stmt = (
            select(LegislationBackfillQueueModel)
            .where(None)
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

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_6(self, limit: int = 20) -> list[LegislationBackfillTask]:
        """Lists highest priority un-resolved backfill tasks."""
        stmt = (
            select(None)
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

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_7(self, limit: int = 20) -> list[LegislationBackfillTask]:
        """Lists highest priority un-resolved backfill tasks."""
        stmt = (
            select(LegislationBackfillQueueModel)
            .where(LegislationBackfillQueueModel.status != "PENDING")
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

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_8(self, limit: int = 20) -> list[LegislationBackfillTask]:
        """Lists highest priority un-resolved backfill tasks."""
        stmt = (
            select(LegislationBackfillQueueModel)
            .where(LegislationBackfillQueueModel.status == "XXPENDINGXX")
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

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_9(self, limit: int = 20) -> list[LegislationBackfillTask]:
        """Lists highest priority un-resolved backfill tasks."""
        stmt = (
            select(LegislationBackfillQueueModel)
            .where(LegislationBackfillQueueModel.status == "pending")
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

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_10(self, limit: int = 20) -> list[LegislationBackfillTask]:
        """Lists highest priority un-resolved backfill tasks."""
        stmt = (
            select(LegislationBackfillQueueModel)
            .where(LegislationBackfillQueueModel.status == "PENDING")
            .order_by(LegislationBackfillQueueModel.citation_count.desc())
            .limit(limit)
        )
        rows = None
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

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_11(self, limit: int = 20) -> list[LegislationBackfillTask]:
        """Lists highest priority un-resolved backfill tasks."""
        stmt = (
            select(LegislationBackfillQueueModel)
            .where(LegislationBackfillQueueModel.status == "PENDING")
            .order_by(LegislationBackfillQueueModel.citation_count.desc())
            .limit(limit)
        )
        rows = self._session.scalars(None).all()
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

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_12(self, limit: int = 20) -> list[LegislationBackfillTask]:
        """Lists highest priority un-resolved backfill tasks."""
        stmt = (
            select(LegislationBackfillQueueModel)
            .where(LegislationBackfillQueueModel.status == "PENDING")
            .order_by(LegislationBackfillQueueModel.citation_count.desc())
            .limit(limit)
        )
        rows = self._session.scalars(stmt).all()
        tasks: list[LegislationBackfillTask] = None
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

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_13(self, limit: int = 20) -> list[LegislationBackfillTask]:
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
                None
            )
        return tasks

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_14(self, limit: int = 20) -> list[LegislationBackfillTask]:
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
                    id=None,
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

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_15(self, limit: int = 20) -> list[LegislationBackfillTask]:
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
                    canonical_urn=None,
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

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_16(self, limit: int = 20) -> list[LegislationBackfillTask]:
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
                    territory_id=None,
                    act_type=r.act_type,
                    act_number=r.act_number,
                    act_year=r.act_year,
                    citation_count=r.citation_count,
                    status=r.status,
                    last_requested_at=r.last_requested_at,
                )
            )
        return tasks

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_17(self, limit: int = 20) -> list[LegislationBackfillTask]:
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
                    act_type=None,
                    act_number=r.act_number,
                    act_year=r.act_year,
                    citation_count=r.citation_count,
                    status=r.status,
                    last_requested_at=r.last_requested_at,
                )
            )
        return tasks

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_18(self, limit: int = 20) -> list[LegislationBackfillTask]:
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
                    act_number=None,
                    act_year=r.act_year,
                    citation_count=r.citation_count,
                    status=r.status,
                    last_requested_at=r.last_requested_at,
                )
            )
        return tasks

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_19(self, limit: int = 20) -> list[LegislationBackfillTask]:
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
                    act_year=None,
                    citation_count=r.citation_count,
                    status=r.status,
                    last_requested_at=r.last_requested_at,
                )
            )
        return tasks

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_20(self, limit: int = 20) -> list[LegislationBackfillTask]:
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
                    citation_count=None,
                    status=r.status,
                    last_requested_at=r.last_requested_at,
                )
            )
        return tasks

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_21(self, limit: int = 20) -> list[LegislationBackfillTask]:
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
                    status=None,
                    last_requested_at=r.last_requested_at,
                )
            )
        return tasks

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_22(self, limit: int = 20) -> list[LegislationBackfillTask]:
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
                    last_requested_at=None,
                )
            )
        return tasks

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_23(self, limit: int = 20) -> list[LegislationBackfillTask]:
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

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_24(self, limit: int = 20) -> list[LegislationBackfillTask]:
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

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_25(self, limit: int = 20) -> list[LegislationBackfillTask]:
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
                    act_type=r.act_type,
                    act_number=r.act_number,
                    act_year=r.act_year,
                    citation_count=r.citation_count,
                    status=r.status,
                    last_requested_at=r.last_requested_at,
                )
            )
        return tasks

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_26(self, limit: int = 20) -> list[LegislationBackfillTask]:
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
                    act_number=r.act_number,
                    act_year=r.act_year,
                    citation_count=r.citation_count,
                    status=r.status,
                    last_requested_at=r.last_requested_at,
                )
            )
        return tasks

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_27(self, limit: int = 20) -> list[LegislationBackfillTask]:
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
                    act_year=r.act_year,
                    citation_count=r.citation_count,
                    status=r.status,
                    last_requested_at=r.last_requested_at,
                )
            )
        return tasks

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_28(self, limit: int = 20) -> list[LegislationBackfillTask]:
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
                    citation_count=r.citation_count,
                    status=r.status,
                    last_requested_at=r.last_requested_at,
                )
            )
        return tasks

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_29(self, limit: int = 20) -> list[LegislationBackfillTask]:
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
                    status=r.status,
                    last_requested_at=r.last_requested_at,
                )
            )
        return tasks

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_30(self, limit: int = 20) -> list[LegislationBackfillTask]:
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
                    last_requested_at=r.last_requested_at,
                )
            )
        return tasks

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_31(self, limit: int = 20) -> list[LegislationBackfillTask]:
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
                    )
            )
        return tasks

    async def xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_32(self, limit: int = 20) -> list[LegislationBackfillTask]:
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
                    canonical_urn=CanonicalUrn.from_string(None),
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

mutants_xǁPostgresConsolidationRepositoryǁ__init____mutmut['_mutmut_orig'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁ__init____mutmut['xǁPostgresConsolidationRepositoryǁ__init____mutmut_1'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁ__init____mutmut_1 # type: ignore # mutmut generated

mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['_mutmut_orig'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_1'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_2'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_3'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_4'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_5'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_5 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_6'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_6 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_7'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_7 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_8'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_8 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_9'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_9 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_10'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_10 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_11'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_11 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_12'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_12 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_13'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_13 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_14'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_14 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_15'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_15 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_16'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_16 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_17'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_17 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_18'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_18 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_19'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_19 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_20'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_20 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_21'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_21 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_22'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_22 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_23'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_23 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_24'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_24 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_25'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_25 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_26'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_26 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_27'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_27 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_28'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_28 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_29'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_29 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut['xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_30'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_mutation__mutmut_30 # type: ignore # mutmut generated

mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['_mutmut_orig'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_1'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_2'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_3'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_4'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_5'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_5 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_6'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_6 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_7'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_7 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_8'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_8 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_9'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_9 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_10'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_10 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_11'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_11 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_12'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_12 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_13'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_13 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_14'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_14 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_15'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_15 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_16'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_16 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_17'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_17 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_18'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_18 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_19'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_19 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_20'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_20 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_21'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_21 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_22'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_22 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_23'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_23 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_24'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_24 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_25'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_25 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_26'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_26 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_27'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_27 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_28'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_28 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_29'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_29 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_30'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_30 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_31'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_31 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_32'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_32 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_33'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_33 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_34'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_34 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_35'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_35 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_36'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_36 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_37'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_37 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_38'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_38 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_39'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_39 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_40'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_40 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_41'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_41 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_42'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_42 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut['xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_43'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_mutations_for_act__mutmut_43 # type: ignore # mutmut generated

mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['_mutmut_orig'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_1'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_2'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_3'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_4'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_5'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_5 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_6'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_6 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_7'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_7 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_8'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_8 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_9'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_9 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_10'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_10 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_11'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_11 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_12'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_12 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_13'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_13 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_14'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_14 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_15'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_15 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_16'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_16 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_17'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_17 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_18'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_18 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_19'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_19 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_20'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_20 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_21'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_21 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_22'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_22 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_23'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_23 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_24'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_24 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_25'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_25 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_26'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_26 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_27'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_27 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_28'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_28 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_29'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_29 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_30'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_30 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_31'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_31 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_32'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_32 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_33'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_33 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_34'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_34 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_35'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_35 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_36'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_36 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_37'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_37 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_38'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁsave_compiled_act__mutmut_38 # type: ignore # mutmut generated

mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['_mutmut_orig'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_1'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_2'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_3'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_4'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_5'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_5 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_6'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_6 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_7'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_7 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_8'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_8 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_9'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_9 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_10'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_10 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_11'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_11 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_12'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_12 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_13'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_13 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_14'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_14 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_15'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_15 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_16'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_16 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_17'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_17 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_18'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_18 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_19'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_19 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_20'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_20 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_21'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_21 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_22'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_22 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_23'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_23 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_24'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_24 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_25'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_25 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_26'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_26 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_27'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_27 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_28'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act__mutmut_28 # type: ignore # mutmut generated

mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['_mutmut_orig'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_1'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_2'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_3'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_4'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_5'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_5 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_6'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_6 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_7'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_7 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_8'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_8 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_9'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_9 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_10'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_10 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_11'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_11 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_12'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_12 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_13'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_13 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_14'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_14 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_15'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_15 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_16'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_16 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_17'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_17 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_18'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_18 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_19'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_19 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_20'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_20 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_21'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_21 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_22'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_22 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_23'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_23 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_24'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_24 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_25'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_25 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_26'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_26 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_27'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_27 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_28'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_28 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_29'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_29 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut['xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_30'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_compiled_act_by_urn__mutmut_30 # type: ignore # mutmut generated

mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['_mutmut_orig'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_1'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_2'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_3'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_4'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_5'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_5 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_6'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_6 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_7'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_7 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_8'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_8 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_9'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_9 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_10'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_10 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_11'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_11 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_12'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_12 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_13'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_13 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_14'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_14 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_15'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_15 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_16'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_16 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_17'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_17 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_18'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_18 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_19'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_19 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_20'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_20 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_21'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_21 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_22'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_22 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_23'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_23 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_24'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_24 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_25'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_25 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_26'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_26 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_27'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_27 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_28'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_28 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_29'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_29 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_30'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_30 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_31'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_31 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_32'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_32 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut['xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_33'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁenqueue_backfill_task__mutmut_33 # type: ignore # mutmut generated

mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['_mutmut_orig'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_1'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_2'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_3'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_4'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_5'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_5 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_6'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_6 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_7'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_7 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_8'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_8 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_9'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_9 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_10'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_10 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_11'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_11 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_12'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_12 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_13'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_13 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_14'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_14 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_15'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_15 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_16'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_16 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_17'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_17 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_18'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_18 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_19'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_19 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_20'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_20 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_21'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_21 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_22'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_22 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_23'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_23 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_24'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_24 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_25'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_25 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_26'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_26 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_27'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_27 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_28'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_28 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_29'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_29 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_30'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_30 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_31'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_31 # type: ignore # mutmut generated
mutants_xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut['xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_32'] = PostgresConsolidationRepository.xǁPostgresConsolidationRepositoryǁget_backfill_queue__mutmut_32 # type: ignore # mutmut generated
