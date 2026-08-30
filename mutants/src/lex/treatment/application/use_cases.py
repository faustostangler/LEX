"""Application Use Cases for the Treatment Bounded Context.

Orchestrates Dual-Track processing (Trilha A: Deep AST & Mutation Extraction vs.
Trilha B: Fast-Path Regex NER) based on PublicationNature.
"""

import uuid
from typing import NamedTuple

from lex.ingestion.domain.entities import NormativeAct
from lex.shared_kernel.value_objects import PublicationNature
from lex.treatment.application.ports import TreatmentRepositoryPort
from lex.treatment.domain.services.act_segmenter import ActSegmenter
from lex.treatment.domain.services.mutation_extractor import MutationExtractor
from lex.treatment.domain.services.ner_extractor import DeterministicNerExtractor


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class TreatmentResult(NamedTuple):
    """Execution summary for a treated normative act."""

    track: str
    mutations_extracted: int
mutants_xǁProcessNormativeActUseCaseǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut: MutantDict = {}  # type: ignore


class ProcessNormativeActUseCase:
    """Use Case coordinating the Dual-Track treatment pipeline."""

    @_mutmut_mutated(mutants_xǁProcessNormativeActUseCaseǁ__init____mutmut)
    def __init__(self, repository: TreatmentRepositoryPort) -> None:
        self._repository = repository

    def xǁProcessNormativeActUseCaseǁ__init____mutmut_orig(self, repository: TreatmentRepositoryPort) -> None:
        self._repository = repository

    def xǁProcessNormativeActUseCaseǁ__init____mutmut_1(self, repository: TreatmentRepositoryPort) -> None:
        self._repository = None

    @_mutmut_mutated(mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut)
    async def execute(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_orig(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_1(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = None

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_2(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id and uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_3(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature not in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_4(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = None

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_5(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=None,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_6(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=None,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_7(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=None,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_8(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=None,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_9(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=None,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_10(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_11(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_12(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_13(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_14(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_15(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = None

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_16(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=None,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_17(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=None,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_18(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=None,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_19(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=None,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_20(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=None,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_21(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_22(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_23(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_24(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_25(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_26(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(None)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_27(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=None,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_28(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=None,
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_29(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_30(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_31(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_32(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track=None, mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_33(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=None)

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_34(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_35(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", )

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_36(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="XXTRILHA_AXX", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_37(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="trilha_a", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_38(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = None

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_39(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(None)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_40(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=None,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_41(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_42(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_43(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_44(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_45(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track=None, mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_46(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=None)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_47(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_48(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", )

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_49(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="XXTRILHA_BXX", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_50(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="trilha_b", mutations_extracted=0)

    async def xǁProcessNormativeActUseCaseǁexecute__mutmut_51(self, act: NormativeAct) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.

        Returns:
            A TreatmentResult summary indicating track and mutations count.
        """
        act_id = act.id or uuid.uuid4()

        # Trilha A: Deep AST & Mutation extraction for normative/regulatory acts
        if act.publication_nature in (
            PublicationNature.NORMATIVA_ABSTRATA,
            PublicationNature.REGULATORIA_SETORIAL,
        ):
            ast = ActSegmenter.segment_text(
                raw_text=act.raw_content,
                title=act.title,
                ementa=act.ementa,
                act_id=act_id,
                canonical_urn=act.canonical_urn,
            )

            mutations = MutationExtractor.extract_mutations(
                raw_text=act.raw_content,
                author_act_id=act_id,
                publication_date=act.date,
                effective_date=act.date,
                default_territory_id=act.territory_id.code,
            )

            if mutations:
                await self._repository.save_mutations(mutations)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=1)

mutants_xǁProcessNormativeActUseCaseǁ__init____mutmut['_mutmut_orig'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁ__init____mutmut['xǁProcessNormativeActUseCaseǁ__init____mutmut_1'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁ__init____mutmut_1 # type: ignore # mutmut generated

mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['_mutmut_orig'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_orig # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_1'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_1 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_2'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_2 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_3'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_3 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_4'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_4 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_5'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_5 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_6'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_6 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_7'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_7 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_8'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_8 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_9'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_9 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_10'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_10 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_11'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_11 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_12'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_12 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_13'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_13 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_14'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_14 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_15'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_15 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_16'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_16 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_17'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_17 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_18'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_18 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_19'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_19 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_20'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_20 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_21'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_21 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_22'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_22 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_23'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_23 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_24'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_24 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_25'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_25 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_26'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_26 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_27'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_27 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_28'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_28 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_29'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_29 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_30'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_30 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_31'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_31 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_32'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_32 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_33'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_33 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_34'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_34 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_35'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_35 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_36'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_36 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_37'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_37 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_38'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_38 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_39'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_39 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_40'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_40 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_41'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_41 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_42'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_42 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_43'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_43 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_44'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_44 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_45'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_45 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_46'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_46 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_47'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_47 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_48'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_48 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_49'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_49 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_50'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_50 # type: ignore # mutmut generated
mutants_xǁProcessNormativeActUseCaseǁexecute__mutmut['xǁProcessNormativeActUseCaseǁexecute__mutmut_51'] = ProcessNormativeActUseCase.xǁProcessNormativeActUseCaseǁexecute__mutmut_51 # type: ignore # mutmut generated
