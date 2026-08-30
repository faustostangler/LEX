"""Out-of-Order Stub Entity Handler and JIT Backfill Task Manager.

Implements the Stub/Skeleton Entity pattern (ADR-006) to preserve relational
integrity when modern gazettes amend un-ingested historical base statutes.
"""

import uuid
from datetime import UTC, date, datetime
from uuid import UUID

from lex.consolidation.domain.entities import LegislationBackfillTask
from lex.consolidation.domain.events import NormativeActHydrated
from lex.consolidation.domain.value_objects import CanonicalUrn
from lex.ingestion.domain.entities import NormativeAct
from lex.ingestion.domain.value_objects import (
    ClassificationSource,
    DocumentHash,
    GazetteDate,
    TerritoryId,
)
from lex.shared_kernel.value_objects import (
    HierarchicalGroup,
    PublicationNature,
)


class StubHandler:
    """Service managing the creation, lookup, and hydration of Out-of-Order Stub entities."""

    @classmethod
    def create_stub_and_task(
        cls,
        canonical_urn: CanonicalUrn,
        territory_id: str,
        act_type: str,
        act_number: str,
        act_year: int,
        parent_edition_id: UUID | None = None,
    ) -> tuple[NormativeAct, LegislationBackfillTask]:
        """Creates a placeholder Stub entity in normative_acts and enqueues a JIT backfill task.

        Args:
            canonical_urn: Deterministic LexML URN for the missing base statute.
            territory_id: Territory code ('BR', 'SP', etc.).
            act_type: Type of the act ('Lei', 'Lei Complementar', etc.).
            act_number: Number of the statute.
            act_year: Year of the statute.
            parent_edition_id: Optional edition container UUID.

        Returns:
            Tuple containing (Stub NormativeAct, LegislationBackfillTask).
        """
        stub_id = uuid.uuid5(uuid.NAMESPACE_DNS, canonical_urn.value)
        edition_id = parent_edition_id or uuid.uuid5(
            uuid.NAMESPACE_DNS, f"stub_edition:{territory_id}:{act_year}"
        )
        now = datetime.now(UTC)
        approx_date = date(act_year, 1, 1)

        # 1. Instantiate Stub NormativeAct
        stub_act = NormativeAct(
            id=stub_id,
            edition_id=edition_id,
            territory_id=TerritoryId.from_code(territory_id),
            date=GazetteDate.from_date(approx_date),
            act_type=act_type,
            act_number=act_number,
            act_year=act_year,
            title=f"{act_type} nº {act_number}/{act_year}",
            source_url=f"urn:stub:{canonical_urn.value}",
            content_hash=DocumentHash.from_text(f"STUB:{canonical_urn.value}"),
            char_count=0,
            raw_content="",
            is_stub=True,
            canonical_urn=canonical_urn.value,
            hierarchical_group=HierarchicalGroup.GRUPO_1_PRIMARIO,
            hierarchical_rank=70,
            publication_nature=PublicationNature.NORMATIVA_ABSTRATA,
            classification_source=ClassificationSource.PRE_SEGMENTED_SOURCE,
            scraped_at=now,
        )

        # 2. Instantiate JIT Backfill Task
        backfill_task = LegislationBackfillTask(
            id=uuid.uuid4(),
            canonical_urn=canonical_urn,
            territory_id=territory_id,
            act_type=act_type,
            act_number=act_number,
            act_year=act_year,
            citation_count=1,
            status="PENDING",
            last_requested_at=now,
        )

        return stub_act, backfill_task

    @classmethod
    def hydrate_stub(
        cls,
        stub_act: NormativeAct,
        raw_content: str,
        source_url: str,
        exact_date: date | None = None,
    ) -> tuple[NormativeAct, NormativeActHydrated]:
        """Hydrates a Stub entity with authentic legislative text and emits NormativeActHydrated.

        Args:
            stub_act: The existing placeholder entity.
            raw_content: Genuine statutory full text scraped by a backfill crawler.
            source_url: Canonical SSOT URL of the base publication.
            exact_date: Optional authentic enactment date.

        Returns:
            Tuple of (Hydrated NormativeAct, NormativeActHydrated Domain Event).
        """
        now = datetime.now(UTC)
        clean_text = raw_content.strip()
        pub_date = GazetteDate.from_date(exact_date) if exact_date else stub_act.date

        hydrated = NormativeAct(
            id=stub_act.id,
            edition_id=stub_act.edition_id,
            territory_id=stub_act.territory_id,
            date=pub_date,
            section=stub_act.section,
            edition_number=stub_act.edition_number,
            is_extra_edition=stub_act.is_extra_edition,
            act_type=stub_act.act_type,
            act_number=stub_act.act_number,
            act_year=stub_act.act_year,
            title=stub_act.title,
            ementa=stub_act.ementa,
            hierarchy=stub_act.hierarchy,
            authority_name=stub_act.authority_name,
            authority_role=stub_act.authority_role,
            source_url=source_url,
            content_hash=DocumentHash.from_text(clean_text),
            char_count=len(clean_text),
            raw_content=clean_text,
            structured_content=stub_act.structured_content,
            classification_source=stub_act.classification_source,
            classification_confidence=stub_act.classification_confidence,
            hierarchical_group=stub_act.hierarchical_group,
            hierarchical_rank=stub_act.hierarchical_rank,
            publication_nature=stub_act.publication_nature,
            canonical_urn=stub_act.canonical_urn,
            is_stub=False,
            metadata_json=stub_act.metadata_json,
            scraped_at=now,
        )

        assert stub_act.canonical_urn is not None
        urn = CanonicalUrn.from_string(stub_act.canonical_urn)
        assert stub_act.id is not None
        event = NormativeActHydrated(
            act_id=stub_act.id,
            canonical_urn=urn,
            hydrated_at=now,
        )

        return hydrated, event
