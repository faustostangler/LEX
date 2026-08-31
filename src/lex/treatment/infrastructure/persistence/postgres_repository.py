"""PostgreSQL Implementation of TreatmentRepositoryPort.

Persists treated AST structures into normative_acts.structured_content,
NER entities into normative_acts.metadata_json, and mutations into normative_act_mutations.
"""

import hashlib
import uuid
from datetime import UTC, date, datetime
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from lex.consolidation.infrastructure.persistence.models import (
    LegislationBackfillQueueModel,
    NormativeActMutationModel,
)
from lex.ingestion.infrastructure.persistence.models import (
    GazetteEditionModel,
    NormativeActModel,
)
from lex.treatment.application.ports import TreatmentRepositoryPort
from lex.treatment.domain.entities import NormativeActMutation

BRAZILIAN_STATES: frozenset[str] = frozenset({
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
    "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
    "RS", "RO", "RR", "SC", "SP", "SE", "TO",
})


def _extract_territory_and_tier(
    urn: str | None, default_territory: str = "BR"
) -> tuple[str, str]:
    """Derives territory code and federative tier from LexML URN or default code (MED-01)."""
    if urn and urn.startswith("urn:lex:br:"):
        parts = urn.split(":")
        if len(parts) >= 4:
            jurisdiction = parts[3].strip().lower()
            if jurisdiction in {s.lower() for s in BRAZILIAN_STATES}:
                return jurisdiction.upper(), "state"
            if jurisdiction == "federal":
                return "BR", "federal"

    code = default_territory.strip().upper()
    if code == "BR":
        return "BR", "federal"
    if code in BRAZILIAN_STATES:
        return code, "state"
    return code, "municipal"


class PostgresTreatmentRepository(TreatmentRepositoryPort):
    """Hexagonal Adapter fulfilling TreatmentRepositoryPort via PostgreSQL 16 / SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    async def save_mutations(
        self, mutations: list[NormativeActMutation], auto_commit: bool = True
    ) -> None:
        """Appends extracted mutation deltas to the write ledger with stub auto-materialization."""
        if not mutations:
            return

        try:
            # 1. Identify distinct target act IDs and ensure they exist in normative_acts
            target_ids = {m.target_act_id for m in mutations}
            for target_id in target_ids:
                existing_act = self._session.get(NormativeActModel, target_id)
                if existing_act is None:
                    # Find mutation carrying metadata for this target
                    sample_mut = next(m for m in mutations if m.target_act_id == target_id)
                    pub_yr = sample_mut.publication_date.value.year
                    urn_val = (
                        sample_mut.target_canonical_urn
                        or f"urn:lex:br:federal:lei:{pub_yr};placeholder"
                    )
                    title_val = sample_mut.target_title or f"Ato Normativo {target_id}"
                    act_type_val = sample_mut.target_act_type or "LEI"
                    act_num_val = sample_mut.target_act_number
                    act_year_val = (
                        sample_mut.target_act_year or sample_mut.publication_date.value.year
                    )
                    target_territory, target_tier = _extract_territory_and_tier(
                        urn_val, default_territory="BR"
                    )

                    # Ensure parent stub edition exists
                    existing_edition = (
                        self._session.query(GazetteEditionModel)
                        .filter_by(
                            territory_id=target_territory,
                            date=date(act_year_val, 1, 1),
                            edition_number="STUB",
                            section="1",
                            is_extra_edition=False,
                        )
                        .first()
                    )
                    if existing_edition is None:
                        stub_edition_id = uuid.uuid5(
                            uuid.NAMESPACE_DNS, f"edition:stub:{target_territory}:{act_year_val}"
                        )
                        existing_edition = GazetteEditionModel(
                            id=stub_edition_id,
                            territory_id=target_territory,
                            tier=target_tier,
                            date=date(act_year_val, 1, 1),
                            edition_number="STUB",
                            section="1",
                            is_extra_edition=False,
                            power="executive",
                            source_url=f"https://stub.lex.internal/edition/{target_territory}/{act_year_val}",
                            summary_sha256=hashlib.sha256(
                                f"stub:edition:{target_territory}:{act_year_val}".encode()
                            ).hexdigest(),
                            total_acts=0,
                            ingestion_status="completed",
                            scraped_at=datetime.now(UTC),
                        )
                        self._session.add(existing_edition)
                        self._session.flush()

                    # Insert Stub NormativeActModel
                    stub_content = "[STUB] Pending base text ingestion"
                    stub_act = NormativeActModel(
                        id=target_id,
                        edition_id=existing_edition.id,
                        territory_id=target_territory,
                        date=date(act_year_val, 1, 1),
                        section="1",
                        edition_number="STUB",
                        is_extra_edition=False,
                        act_type=act_type_val,
                        act_number=act_num_val,
                        act_year=act_year_val,
                        title=title_val,
                        ementa=None,
                        hierarchy=[],
                        source_url=f"https://stub.lex.internal/{urn_val}",
                        content_sha256=hashlib.sha256(
                            f"stub:content:{target_id}".encode()
                        ).hexdigest(),
                        char_count=len(stub_content),
                        raw_content=stub_content,
                        structured_content=None,
                        classification_source="stub_placeholder",
                        classification_confidence=1.0,
                        hierarchical_group=1,
                        hierarchical_rank=70,
                        publication_nature="normativa_abstrata",
                        canonical_urn=urn_val,
                        is_stub=True,
                        metadata_json={"is_stub": True},
                        scraped_at=datetime.now(UTC),
                    )
                    self._session.add(stub_act)
                    self._session.flush()

                    # Enqueue in legislation_backfill_queue if not already there
                    existing_queue = (
                        self._session.query(LegislationBackfillQueueModel)
                        .filter_by(canonical_urn=urn_val)
                        .first()
                    )
                    if existing_queue:
                        existing_queue.citation_count += 1
                        existing_queue.last_requested_at = datetime.now(UTC)
                    else:
                        queue_item = LegislationBackfillQueueModel(
                            id=uuid.uuid4(),
                            canonical_urn=urn_val,
                            territory_id=target_territory,
                            act_type=act_type_val,
                            act_number=act_num_val or "0",
                            act_year=act_year_val,
                            citation_count=1,
                            status="PENDING",
                            last_requested_at=datetime.now(UTC),
                        )
                        self._session.add(queue_item)
                        self._session.flush()

            # 2. Persist mutations
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
            if auto_commit:
                self._session.commit()
            else:
                self._session.flush()
        except Exception:
            self._session.rollback()
            raise

    async def update_normative_act_treatment(
        self,
        act_id: UUID,
        structured_content: dict[str, Any] | None,
        metadata_json: dict[str, Any] | None,
        auto_commit: bool = True,
    ) -> None:
        """Updates a NormativeAct row with parsed AST or extracted NER metadata."""
        try:
            act_model = self._session.get(NormativeActModel, act_id)
            if act_model is not None:
                if structured_content is not None:
                    act_model.structured_content = structured_content
                if metadata_json is not None:
                    act_model.metadata_json = metadata_json
                if auto_commit:
                    self._session.commit()
                else:
                    self._session.flush()
        except Exception:
            self._session.rollback()
            raise
