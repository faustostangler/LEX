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


class TreatmentResult(NamedTuple):
    """Execution summary for a treated normative act."""

    track: str
    mutations_extracted: int


class ProcessNormativeActUseCase:
    """Use Case coordinating the Dual-Track treatment pipeline."""

    def __init__(self, repository: TreatmentRepositoryPort) -> None:
        self._repository = repository

    async def execute(self, act: NormativeAct, auto_commit: bool = True) -> TreatmentResult:
        """Executes the appropriate processing track based on the act's nature.

        Args:
            act: The raw NormativeAct entity to treat.
            auto_commit: Whether to commit changes immediately (True)
                or stage in session buffer (False).

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
                await self._repository.save_mutations(mutations, auto_commit=auto_commit)

            await self._repository.update_normative_act_treatment(
                act_id=act_id,
                structured_content=ast.to_dict(),
                metadata_json=None,
                auto_commit=auto_commit,
            )

            return TreatmentResult(track="TRILHA_A", mutations_extracted=len(mutations))

        # Trilha B: Fast-Path NER entity extraction for notices, contracts, procurement, personnel
        entities = DeterministicNerExtractor.extract_entities(act.raw_content)

        await self._repository.update_normative_act_treatment(
            act_id=act_id,
            structured_content=None,
            metadata_json=entities if entities else None,
            auto_commit=auto_commit,
        )

        return TreatmentResult(track="TRILHA_B", mutations_extracted=0)
