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


class PostgresTreatmentRepository(TreatmentRepositoryPort):
    """Hexagonal Adapter fulfilling TreatmentRepositoryPort via PostgreSQL 16 / SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    async def save_mutations(self, mutations: list[NormativeActMutation]) -> None:
        """Appends extracted mutation deltas to the write model ledger."""
        try:
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
        except Exception:
            self._session.rollback()
            raise

    async def update_normative_act_treatment(
        self,
        act_id: UUID,
        structured_content: dict[str, Any] | None,
        metadata_json: dict[str, Any] | None,
    ) -> None:
        """Updates a NormativeAct row with parsed AST or extracted NER metadata."""
        try:
            act_model = self._session.get(NormativeActModel, act_id)
            if act_model is not None:
                if structured_content is not None:
                    act_model.structured_content = structured_content
                if metadata_json is not None:
                    act_model.metadata_json = metadata_json
                self._session.commit()
        except Exception:
            self._session.rollback()
            raise
