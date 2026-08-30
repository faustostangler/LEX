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


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut: MutantDict = {}  # type: ignore
mutants_xǁStubHandlerǁhydrate_stub__mutmut: MutantDict = {}  # type: ignore


class StubHandler:
    """Service managing the creation, lookup, and hydration of Out-of-Order Stub entities."""

    @classmethod
    @_mutmut_mutated(mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut, is_classmethod = True)
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_orig(
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_1(
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
        stub_id = None
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_2(
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
        stub_id = uuid.uuid5(None, canonical_urn.value)
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_3(
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
        stub_id = uuid.uuid5(uuid.NAMESPACE_DNS, None)
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_4(
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
        stub_id = uuid.uuid5(canonical_urn.value)
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_5(
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
        stub_id = uuid.uuid5(uuid.NAMESPACE_DNS, )
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_6(
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
        edition_id = None
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_7(
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
        edition_id = parent_edition_id and uuid.uuid5(
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_8(
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
            None, f"stub_edition:{territory_id}:{act_year}"
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_9(
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
            uuid.NAMESPACE_DNS, None
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_10(
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
            f"stub_edition:{territory_id}:{act_year}"
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_11(
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
            uuid.NAMESPACE_DNS, )
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_12(
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
        now = None
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_13(
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
        now = datetime.now(None)
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_14(
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
        approx_date = None

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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_15(
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
        approx_date = date(None, 1, 1)

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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_16(
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
        approx_date = date(act_year, None, 1)

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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_17(
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
        approx_date = date(act_year, 1, None)

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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_18(
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
        approx_date = date(1, 1)

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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_19(
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
        approx_date = date(act_year, 1)

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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_20(
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
        approx_date = date(act_year, 1, )

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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_21(
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
        approx_date = date(act_year, 2, 1)

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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_22(
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
        approx_date = date(act_year, 1, 2)

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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_23(
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
        stub_act = None

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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_24(
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
            id=None,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_25(
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
            edition_id=None,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_26(
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
            territory_id=None,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_27(
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
            date=None,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_28(
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
            act_type=None,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_29(
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
            act_number=None,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_30(
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
            act_year=None,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_31(
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
            title=None,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_32(
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
            source_url=None,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_33(
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
            content_hash=None,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_34(
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
            char_count=None,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_35(
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
            raw_content=None,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_36(
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
            is_stub=None,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_37(
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
            canonical_urn=None,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_38(
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
            hierarchical_group=None,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_39(
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
            hierarchical_rank=None,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_40(
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
            publication_nature=None,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_41(
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
            classification_source=None,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_42(
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
            scraped_at=None,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_43(
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_44(
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_45(
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_46(
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_47(
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_48(
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_49(
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_50(
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_51(
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_52(
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_53(
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_54(
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_55(
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_56(
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_57(
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_58(
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_59(
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_60(
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_61(
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_62(
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
            territory_id=TerritoryId.from_code(None),
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_63(
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
            date=GazetteDate.from_date(None),
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_64(
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
            content_hash=DocumentHash.from_text(None),
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_65(
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
            char_count=1,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_66(
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
            raw_content="XXXX",
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_67(
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
            is_stub=False,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_68(
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
            hierarchical_rank=71,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_69(
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
        backfill_task = None

        return stub_act, backfill_task

    @classmethod
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_70(
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
            id=None,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_71(
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
            canonical_urn=None,
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_72(
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
            territory_id=None,
            act_type=act_type,
            act_number=act_number,
            act_year=act_year,
            citation_count=1,
            status="PENDING",
            last_requested_at=now,
        )

        return stub_act, backfill_task

    @classmethod
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_73(
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
            act_type=None,
            act_number=act_number,
            act_year=act_year,
            citation_count=1,
            status="PENDING",
            last_requested_at=now,
        )

        return stub_act, backfill_task

    @classmethod
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_74(
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
            act_number=None,
            act_year=act_year,
            citation_count=1,
            status="PENDING",
            last_requested_at=now,
        )

        return stub_act, backfill_task

    @classmethod
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_75(
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
            act_year=None,
            citation_count=1,
            status="PENDING",
            last_requested_at=now,
        )

        return stub_act, backfill_task

    @classmethod
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_76(
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
            citation_count=None,
            status="PENDING",
            last_requested_at=now,
        )

        return stub_act, backfill_task

    @classmethod
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_77(
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
            status=None,
            last_requested_at=now,
        )

        return stub_act, backfill_task

    @classmethod
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_78(
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
            last_requested_at=None,
        )

        return stub_act, backfill_task

    @classmethod
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_79(
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_80(
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
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_81(
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
            act_type=act_type,
            act_number=act_number,
            act_year=act_year,
            citation_count=1,
            status="PENDING",
            last_requested_at=now,
        )

        return stub_act, backfill_task

    @classmethod
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_82(
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
            act_number=act_number,
            act_year=act_year,
            citation_count=1,
            status="PENDING",
            last_requested_at=now,
        )

        return stub_act, backfill_task

    @classmethod
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_83(
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
            act_year=act_year,
            citation_count=1,
            status="PENDING",
            last_requested_at=now,
        )

        return stub_act, backfill_task

    @classmethod
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_84(
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
            citation_count=1,
            status="PENDING",
            last_requested_at=now,
        )

        return stub_act, backfill_task

    @classmethod
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_85(
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
            status="PENDING",
            last_requested_at=now,
        )

        return stub_act, backfill_task

    @classmethod
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_86(
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
            last_requested_at=now,
        )

        return stub_act, backfill_task

    @classmethod
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_87(
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
            )

        return stub_act, backfill_task

    @classmethod
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_88(
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
            citation_count=2,
            status="PENDING",
            last_requested_at=now,
        )

        return stub_act, backfill_task

    @classmethod
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_89(
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
            status="XXPENDINGXX",
            last_requested_at=now,
        )

        return stub_act, backfill_task

    @classmethod
    def xǁStubHandlerǁcreate_stub_and_task__mutmut_90(
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
            status="pending",
            last_requested_at=now,
        )

        return stub_act, backfill_task

    @classmethod
    @_mutmut_mutated(mutants_xǁStubHandlerǁhydrate_stub__mutmut, is_classmethod = True)
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_orig(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_1(
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
        now = None
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_2(
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
        now = datetime.now(None)
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_3(
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
        clean_text = None
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_4(
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
        pub_date = None

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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_5(
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
        pub_date = GazetteDate.from_date(None) if exact_date else stub_act.date

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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_6(
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

        hydrated = None

        assert stub_act.canonical_urn is not None
        urn = CanonicalUrn.from_string(stub_act.canonical_urn)
        assert stub_act.id is not None
        event = NormativeActHydrated(
            act_id=stub_act.id,
            canonical_urn=urn,
            hydrated_at=now,
        )

        return hydrated, event

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_7(
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
            id=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_8(
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
            edition_id=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_9(
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
            territory_id=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_10(
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
            date=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_11(
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
            section=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_12(
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
            edition_number=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_13(
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
            is_extra_edition=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_14(
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
            act_type=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_15(
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
            act_number=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_16(
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
            act_year=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_17(
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
            title=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_18(
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
            ementa=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_19(
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
            hierarchy=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_20(
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
            authority_name=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_21(
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
            authority_role=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_22(
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
            source_url=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_23(
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
            content_hash=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_24(
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
            char_count=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_25(
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
            raw_content=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_26(
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
            structured_content=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_27(
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
            classification_source=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_28(
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
            classification_confidence=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_29(
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
            hierarchical_group=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_30(
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
            hierarchical_rank=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_31(
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
            publication_nature=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_32(
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
            canonical_urn=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_33(
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
            is_stub=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_34(
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
            metadata_json=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_35(
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
            scraped_at=None,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_36(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_37(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_38(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_39(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_40(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_41(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_42(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_43(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_44(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_45(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_46(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_47(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_48(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_49(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_50(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_51(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_52(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_53(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_54(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_55(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_56(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_57(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_58(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_59(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_60(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_61(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_62(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_63(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_64(
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_65(
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
            content_hash=DocumentHash.from_text(None),
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_66(
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
            is_stub=True,
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

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_67(
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

        assert stub_act.canonical_urn is None
        urn = CanonicalUrn.from_string(stub_act.canonical_urn)
        assert stub_act.id is not None
        event = NormativeActHydrated(
            act_id=stub_act.id,
            canonical_urn=urn,
            hydrated_at=now,
        )

        return hydrated, event

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_68(
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
        urn = None
        assert stub_act.id is not None
        event = NormativeActHydrated(
            act_id=stub_act.id,
            canonical_urn=urn,
            hydrated_at=now,
        )

        return hydrated, event

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_69(
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
        urn = CanonicalUrn.from_string(None)
        assert stub_act.id is not None
        event = NormativeActHydrated(
            act_id=stub_act.id,
            canonical_urn=urn,
            hydrated_at=now,
        )

        return hydrated, event

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_70(
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
        assert stub_act.id is None
        event = NormativeActHydrated(
            act_id=stub_act.id,
            canonical_urn=urn,
            hydrated_at=now,
        )

        return hydrated, event

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_71(
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
        event = None

        return hydrated, event

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_72(
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
            act_id=None,
            canonical_urn=urn,
            hydrated_at=now,
        )

        return hydrated, event

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_73(
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
            canonical_urn=None,
            hydrated_at=now,
        )

        return hydrated, event

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_74(
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
            hydrated_at=None,
        )

        return hydrated, event

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_75(
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
            canonical_urn=urn,
            hydrated_at=now,
        )

        return hydrated, event

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_76(
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
            hydrated_at=now,
        )

        return hydrated, event

    @classmethod
    def xǁStubHandlerǁhydrate_stub__mutmut_77(
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
            )

        return hydrated, event

mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['_mutmut_orig'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_orig # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_1'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_1 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_2'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_2 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_3'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_3 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_4'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_4 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_5'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_5 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_6'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_6 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_7'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_7 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_8'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_8 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_9'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_9 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_10'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_10 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_11'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_11 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_12'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_12 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_13'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_13 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_14'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_14 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_15'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_15 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_16'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_16 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_17'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_17 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_18'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_18 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_19'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_19 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_20'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_20 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_21'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_21 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_22'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_22 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_23'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_23 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_24'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_24 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_25'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_25 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_26'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_26 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_27'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_27 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_28'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_28 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_29'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_29 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_30'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_30 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_31'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_31 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_32'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_32 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_33'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_33 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_34'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_34 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_35'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_35 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_36'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_36 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_37'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_37 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_38'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_38 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_39'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_39 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_40'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_40 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_41'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_41 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_42'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_42 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_43'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_43 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_44'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_44 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_45'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_45 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_46'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_46 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_47'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_47 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_48'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_48 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_49'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_49 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_50'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_50 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_51'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_51 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_52'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_52 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_53'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_53 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_54'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_54 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_55'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_55 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_56'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_56 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_57'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_57 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_58'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_58 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_59'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_59 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_60'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_60 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_61'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_61 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_62'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_62 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_63'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_63 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_64'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_64 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_65'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_65 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_66'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_66 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_67'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_67 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_68'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_68 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_69'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_69 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_70'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_70 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_71'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_71 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_72'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_72 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_73'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_73 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_74'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_74 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_75'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_75 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_76'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_76 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_77'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_77 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_78'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_78 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_79'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_79 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_80'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_80 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_81'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_81 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_82'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_82 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_83'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_83 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_84'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_84 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_85'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_85 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_86'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_86 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_87'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_87 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_88'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_88 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_89'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_89 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁcreate_stub_and_task__mutmut['xǁStubHandlerǁcreate_stub_and_task__mutmut_90'] = StubHandler.xǁStubHandlerǁcreate_stub_and_task__mutmut_90 # type: ignore # mutmut generated

mutants_xǁStubHandlerǁhydrate_stub__mutmut['_mutmut_orig'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_orig # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_1'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_1 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_2'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_2 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_3'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_3 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_4'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_4 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_5'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_5 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_6'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_6 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_7'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_7 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_8'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_8 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_9'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_9 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_10'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_10 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_11'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_11 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_12'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_12 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_13'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_13 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_14'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_14 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_15'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_15 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_16'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_16 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_17'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_17 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_18'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_18 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_19'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_19 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_20'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_20 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_21'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_21 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_22'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_22 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_23'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_23 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_24'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_24 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_25'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_25 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_26'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_26 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_27'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_27 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_28'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_28 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_29'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_29 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_30'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_30 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_31'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_31 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_32'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_32 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_33'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_33 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_34'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_34 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_35'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_35 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_36'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_36 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_37'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_37 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_38'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_38 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_39'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_39 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_40'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_40 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_41'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_41 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_42'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_42 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_43'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_43 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_44'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_44 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_45'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_45 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_46'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_46 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_47'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_47 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_48'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_48 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_49'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_49 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_50'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_50 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_51'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_51 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_52'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_52 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_53'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_53 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_54'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_54 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_55'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_55 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_56'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_56 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_57'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_57 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_58'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_58 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_59'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_59 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_60'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_60 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_61'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_61 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_62'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_62 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_63'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_63 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_64'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_64 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_65'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_65 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_66'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_66 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_67'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_67 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_68'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_68 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_69'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_69 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_70'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_70 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_71'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_71 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_72'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_72 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_73'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_73 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_74'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_74 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_75'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_75 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_76'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_76 # type: ignore # mutmut generated
mutants_xǁStubHandlerǁhydrate_stub__mutmut['xǁStubHandlerǁhydrate_stub__mutmut_77'] = StubHandler.xǁStubHandlerǁhydrate_stub__mutmut_77 # type: ignore # mutmut generated
