"""PostgreSQL Implementation of TreatmentRepositoryPort.

Persists treated AST structures into normative_acts.structured_content,
NER entities into normative_acts.metadata_json, and mutations into normative_act_mutations.
"""

import uuid
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from lex.consolidation.infrastructure.persistence.models import NormativeActMutationModel
from lex.ingestion.infrastructure.persistence.models import NormativeActModel
from lex.treatment.application.ports import TreatmentRepositoryPort
from lex.treatment.domain.entities import NormativeActMutation


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁPostgresTreatmentRepositoryǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut: MutantDict = {}  # type: ignore
mutants_xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut: MutantDict = {}  # type: ignore


class PostgresTreatmentRepository(TreatmentRepositoryPort):
    """Hexagonal Adapter fulfilling TreatmentRepositoryPort via PostgreSQL 16 / SQLAlchemy."""

    @_mutmut_mutated(mutants_xǁPostgresTreatmentRepositoryǁ__init____mutmut)
    def __init__(self, session: Session) -> None:
        self._session = session

    def xǁPostgresTreatmentRepositoryǁ__init____mutmut_orig(self, session: Session) -> None:
        self._session = session

    def xǁPostgresTreatmentRepositoryǁ__init____mutmut_1(self, session: Session) -> None:
        self._session = None

    @_mutmut_mutated(mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut)
    async def save_mutations(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_orig(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_1(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = None
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_2(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id and uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_3(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = None
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_4(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=None,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_5(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=None,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_6(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=None,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_7(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=None,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_8(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=None,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_9(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=None,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_10(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=None,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_11(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=None,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_12(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=None,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_13(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=None,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_14(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=None,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_15(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=None,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_16(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=None,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_17(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_18(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_19(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_20(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_21(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_22(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_23(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_24(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_25(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_26(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_27(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_28(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_29(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                )
            self._session.add(model)
        self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_30(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        for m in mutations:
            mut_id = m.id or uuid.uuid4()
            model = NormativeActMutationModel(
                id=mut_id,
                target_act_id=m.target_act_id,
                target_node_path=m.target_node_path.value,
                author_act_id=m.author_act_id,
                author_dispositivo_ref=m.author_dispositivo_ref,
                mutation_type=m.mutation_type.value,
                new_text=m.new_text,
                new_structured_payload=m.new_structured_payload,
                publication_date=m.publication_date.value,
                effective_date=m.effective_date.value,
                extraction_source=m.extraction_source,
                confidence_score=m.confidence_score,
                mutation_sha256=m.mutation_sha256.hex_digest,
            )
            self._session.add(None)
        self._session.commit()

    @_mutmut_mutated(mutants_xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut)
    async def update_normative_act_treatment(
        self,
        act_id: UUID,
        structured_content: dict[str, Any] | None,
        metadata_json: dict[str, Any] | None,
    ) -> None:
        """Updates a NormativeAct row with parsed AST or extracted NER metadata."""
        act_model = self._session.get(NormativeActModel, act_id)
        if act_model is not None:
            if structured_content is not None:
                act_model.structured_content = structured_content
            if metadata_json is not None:
                act_model.metadata_json = metadata_json
            self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_orig(
        self,
        act_id: UUID,
        structured_content: dict[str, Any] | None,
        metadata_json: dict[str, Any] | None,
    ) -> None:
        """Updates a NormativeAct row with parsed AST or extracted NER metadata."""
        act_model = self._session.get(NormativeActModel, act_id)
        if act_model is not None:
            if structured_content is not None:
                act_model.structured_content = structured_content
            if metadata_json is not None:
                act_model.metadata_json = metadata_json
            self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_1(
        self,
        act_id: UUID,
        structured_content: dict[str, Any] | None,
        metadata_json: dict[str, Any] | None,
    ) -> None:
        """Updates a NormativeAct row with parsed AST or extracted NER metadata."""
        act_model = None
        if act_model is not None:
            if structured_content is not None:
                act_model.structured_content = structured_content
            if metadata_json is not None:
                act_model.metadata_json = metadata_json
            self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_2(
        self,
        act_id: UUID,
        structured_content: dict[str, Any] | None,
        metadata_json: dict[str, Any] | None,
    ) -> None:
        """Updates a NormativeAct row with parsed AST or extracted NER metadata."""
        act_model = self._session.get(None, act_id)
        if act_model is not None:
            if structured_content is not None:
                act_model.structured_content = structured_content
            if metadata_json is not None:
                act_model.metadata_json = metadata_json
            self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_3(
        self,
        act_id: UUID,
        structured_content: dict[str, Any] | None,
        metadata_json: dict[str, Any] | None,
    ) -> None:
        """Updates a NormativeAct row with parsed AST or extracted NER metadata."""
        act_model = self._session.get(NormativeActModel, None)
        if act_model is not None:
            if structured_content is not None:
                act_model.structured_content = structured_content
            if metadata_json is not None:
                act_model.metadata_json = metadata_json
            self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_4(
        self,
        act_id: UUID,
        structured_content: dict[str, Any] | None,
        metadata_json: dict[str, Any] | None,
    ) -> None:
        """Updates a NormativeAct row with parsed AST or extracted NER metadata."""
        act_model = self._session.get(act_id)
        if act_model is not None:
            if structured_content is not None:
                act_model.structured_content = structured_content
            if metadata_json is not None:
                act_model.metadata_json = metadata_json
            self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_5(
        self,
        act_id: UUID,
        structured_content: dict[str, Any] | None,
        metadata_json: dict[str, Any] | None,
    ) -> None:
        """Updates a NormativeAct row with parsed AST or extracted NER metadata."""
        act_model = self._session.get(NormativeActModel, )
        if act_model is not None:
            if structured_content is not None:
                act_model.structured_content = structured_content
            if metadata_json is not None:
                act_model.metadata_json = metadata_json
            self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_6(
        self,
        act_id: UUID,
        structured_content: dict[str, Any] | None,
        metadata_json: dict[str, Any] | None,
    ) -> None:
        """Updates a NormativeAct row with parsed AST or extracted NER metadata."""
        act_model = self._session.get(NormativeActModel, act_id)
        if act_model is None:
            if structured_content is not None:
                act_model.structured_content = structured_content
            if metadata_json is not None:
                act_model.metadata_json = metadata_json
            self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_7(
        self,
        act_id: UUID,
        structured_content: dict[str, Any] | None,
        metadata_json: dict[str, Any] | None,
    ) -> None:
        """Updates a NormativeAct row with parsed AST or extracted NER metadata."""
        act_model = self._session.get(NormativeActModel, act_id)
        if act_model is not None:
            if structured_content is None:
                act_model.structured_content = structured_content
            if metadata_json is not None:
                act_model.metadata_json = metadata_json
            self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_8(
        self,
        act_id: UUID,
        structured_content: dict[str, Any] | None,
        metadata_json: dict[str, Any] | None,
    ) -> None:
        """Updates a NormativeAct row with parsed AST or extracted NER metadata."""
        act_model = self._session.get(NormativeActModel, act_id)
        if act_model is not None:
            if structured_content is not None:
                act_model.structured_content = None
            if metadata_json is not None:
                act_model.metadata_json = metadata_json
            self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_9(
        self,
        act_id: UUID,
        structured_content: dict[str, Any] | None,
        metadata_json: dict[str, Any] | None,
    ) -> None:
        """Updates a NormativeAct row with parsed AST or extracted NER metadata."""
        act_model = self._session.get(NormativeActModel, act_id)
        if act_model is not None:
            if structured_content is not None:
                act_model.structured_content = structured_content
            if metadata_json is None:
                act_model.metadata_json = metadata_json
            self._session.commit()

    async def xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_10(
        self,
        act_id: UUID,
        structured_content: dict[str, Any] | None,
        metadata_json: dict[str, Any] | None,
    ) -> None:
        """Updates a NormativeAct row with parsed AST or extracted NER metadata."""
        act_model = self._session.get(NormativeActModel, act_id)
        if act_model is not None:
            if structured_content is not None:
                act_model.structured_content = structured_content
            if metadata_json is not None:
                act_model.metadata_json = None
            self._session.commit()

mutants_xǁPostgresTreatmentRepositoryǁ__init____mutmut['_mutmut_orig'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁ__init____mutmut['xǁPostgresTreatmentRepositoryǁ__init____mutmut_1'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁ__init____mutmut_1 # type: ignore # mutmut generated

mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['_mutmut_orig'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_1'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_2'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_3'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_4'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_5'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_5 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_6'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_6 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_7'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_7 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_8'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_8 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_9'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_9 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_10'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_10 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_11'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_11 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_12'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_12 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_13'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_13 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_14'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_14 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_15'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_15 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_16'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_16 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_17'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_17 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_18'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_18 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_19'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_19 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_20'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_20 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_21'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_21 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_22'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_22 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_23'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_23 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_24'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_24 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_25'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_25 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_26'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_26 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_27'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_27 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_28'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_28 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_29'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_29 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut['xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_30'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁsave_mutations__mutmut_30 # type: ignore # mutmut generated

mutants_xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut['_mutmut_orig'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut['xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_1'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut['xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_2'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut['xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_3'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut['xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_4'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut['xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_5'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_5 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut['xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_6'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_6 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut['xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_7'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_7 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut['xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_8'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_8 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut['xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_9'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_9 # type: ignore # mutmut generated
mutants_xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut['xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_10'] = PostgresTreatmentRepository.xǁPostgresTreatmentRepositoryǁupdate_normative_act_treatment__mutmut_10 # type: ignore # mutmut generated
