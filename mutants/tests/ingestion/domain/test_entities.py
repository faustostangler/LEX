"""Precision Unit Tests for Ingestion Domain Entities.

Verifies construction-time invariants and business constraints for GazetteEdition
and NormativeAct specified in ADR-002, ADR-006, and ADR-007.
"""

import uuid
from datetime import UTC, date, datetime

import pytest

from lex.ingestion.domain.entities import GazetteEdition, NormativeAct
from lex.ingestion.domain.exceptions import DomainInvariantViolationError
from lex.ingestion.domain.value_objects import (
    ClassificationSource,
    DocumentHash,
    FederativeTier,
    GazetteDate,
    IngestionStatus,
    TerritoryId,
)
from lex.shared_kernel.value_objects import (
    HierarchicalGroup,
    PublicationNature,
)


def make_valid_edition(
    *,
    id: uuid.UUID | None = None,
    territory_code: str = "BR",
    tier: FederativeTier = FederativeTier.FEDERAL,
    pub_date: date | None = None,
    edition_number: str | None = "1",
    section: str | None = "secao_1",
    is_extra_edition: bool = False,
    power: str = "executive",
    source_url: str = "https://www.in.gov.br/leiturajornal?data=02-01-2024&secao=do1",
    summary_hash: DocumentHash | None = None,
    total_acts: int = 25,
    ingestion_status: IngestionStatus = IngestionStatus.COMPLETED,
    scraped_at: datetime | None = None,
) -> GazetteEdition:
    """Helper to instantiate a valid GazetteEdition with typed defaults."""
    return GazetteEdition(
        id=id or uuid.uuid4(),
        territory_id=TerritoryId.from_code(territory_code),
        tier=tier,
        date=GazetteDate.from_date(pub_date or date(2024, 1, 2)),
        edition_number=edition_number,
        section=section,
        is_extra_edition=is_extra_edition,
        power=power,
        source_url=source_url,
        summary_hash=summary_hash or DocumentHash.from_text("edition-summary-mock"),
        total_acts=total_acts,
        ingestion_status=ingestion_status,
        scraped_at=scraped_at or datetime.now(UTC),
    )


def make_valid_act(
    *,
    id: uuid.UUID | None = None,
    edition_id: uuid.UUID | None = None,
    territory_code: str = "BR",
    pub_date: date | None = None,
    act_type: str = "PORTARIA",
    act_number: str | None = "100",
    act_year: int | None = 2024,
    title: str = "PORTARIA Nº 100, DE 2024",
    raw_content: str = "Art. 1º Disposições normativas.",
    source_url: str = "https://www.in.gov.br/web/dou/-/portaria-100",
    char_count: int | None = None,
    hierarchical_group: HierarchicalGroup = HierarchicalGroup.GRUPO_4_ORDINATORIO_MINISTERIAL,
    hierarchical_rank: int = 40,
    publication_nature: PublicationNature = PublicationNature.NORMATIVA_ABSTRATA,
    canonical_urn: str | None = "urn:lex:br:federal:portaria:2024;100",
    is_stub: bool = False,
) -> NormativeAct:
    """Helper to instantiate a valid NormativeAct with typed defaults."""
    content = raw_content.strip()
    return NormativeAct(
        id=id or uuid.uuid4(),
        edition_id=edition_id or uuid.uuid4(),
        territory_id=TerritoryId.from_code(territory_code),
        date=GazetteDate.from_date(pub_date or date(2024, 1, 2)),
        act_type=act_type,
        act_number=act_number,
        act_year=act_year,
        title=title,
        source_url=source_url,
        content_hash=DocumentHash.from_text(content or "fallback"),
        char_count=char_count if char_count is not None else len(content),
        raw_content=raw_content,
        classification_source=ClassificationSource.PRE_SEGMENTED_SOURCE,
        classification_confidence=1.0,
        hierarchical_group=hierarchical_group,
        hierarchical_rank=hierarchical_rank,
        publication_nature=publication_nature,
        canonical_urn=canonical_urn,
        is_stub=is_stub,
        scraped_at=datetime.now(UTC),
    )


class TestGazetteEdition:
    """Acceptance tests for GazetteEdition Entity."""

    def test_successful_construction(self) -> None:
        """Scenario 1: Valid gazette edition constructs successfully."""
        edition = make_valid_edition()
        assert edition.territory_id.code == "BR"
        assert edition.tier == FederativeTier.FEDERAL
        assert edition.total_acts == 25
        assert edition.ingestion_status == IngestionStatus.COMPLETED

    def test_invalid_source_url_raises_invariant(self) -> None:
        """Boundary condition: source_url must be an HTTP/HTTPS URL."""
        with pytest.raises(DomainInvariantViolationError, match="source_url must start with http"):
            make_valid_edition(source_url="ftp://invalid-source.com/gazette.pdf")

    def test_federal_tier_with_non_br_territory_raises_invariant(self) -> None:
        """Boundary condition: Federal tier must have territory code 'BR'."""
        match_err = "Federal tier requires territory code 'BR'"
        with pytest.raises(DomainInvariantViolationError, match=match_err):
            make_valid_edition(tier=FederativeTier.FEDERAL, territory_code="SP")

    def test_state_tier_with_municipal_territory_raises_invariant(self) -> None:
        """Boundary condition: State tier requires a 2-letter state code."""
        match_err = "State tier requires a 2-letter state code"
        with pytest.raises(DomainInvariantViolationError, match=match_err):
            make_valid_edition(tier=FederativeTier.STATE, territory_code="3550308")

    def test_municipal_tier_with_state_territory_raises_invariant(self) -> None:
        """Boundary condition: Municipal tier requires a 7-digit IBGE code."""
        match_err = "Municipal tier requires a 7-digit IBGE code"
        with pytest.raises(DomainInvariantViolationError, match=match_err):
            make_valid_edition(tier=FederativeTier.MUNICIPAL, territory_code="SP")


class TestNormativeAct:
    """Acceptance tests for NormativeAct Entity."""

    def test_successful_construction(self) -> None:
        """Scenario 1: Valid normative act constructs with all fields."""
        act = make_valid_act()
        assert act.territory_id.code == "BR"
        assert act.act_type == "PORTARIA"
        assert act.act_number == "100"
        assert act.act_year == 2024
        assert act.hierarchical_group == HierarchicalGroup.GRUPO_4_ORDINATORIO_MINISTERIAL
        assert act.hierarchical_rank == 40
        assert act.publication_nature == PublicationNature.NORMATIVA_ABSTRATA
        assert act.canonical_urn == "urn:lex:br:federal:portaria:2024;100"
        assert act.is_stub is False

    def test_empty_raw_content_raises_invariant(self) -> None:
        """Boundary condition: Empty or whitespace raw content is rejected."""
        with pytest.raises(DomainInvariantViolationError, match="raw_content must contain"):
            make_valid_act(raw_content="   \n\t  ")

    def test_empty_title_raises_invariant(self) -> None:
        """Boundary condition: Empty or whitespace title is rejected."""
        with pytest.raises(DomainInvariantViolationError, match="title cannot be empty"):
            make_valid_act(title="   ")

    def test_empty_act_type_raises_invariant(self) -> None:
        """Boundary condition: Empty or whitespace act_type is rejected."""
        with pytest.raises(DomainInvariantViolationError, match="act_type cannot be empty"):
            make_valid_act(act_type="   ")

    def test_zero_or_negative_char_count_raises_invariant(self) -> None:
        """Boundary condition: char_count must be strictly positive."""
        with pytest.raises(
            DomainInvariantViolationError, match="char_count must be strictly positive"
        ):
            make_valid_act(char_count=0)

        with pytest.raises(
            DomainInvariantViolationError, match="char_count must be strictly positive"
        ):
            make_valid_act(char_count=-5)

    def test_invalid_source_url_raises_invariant(self) -> None:
        """Boundary condition: source_url must start with http:// or https://."""
        with pytest.raises(DomainInvariantViolationError, match="source_url must start with http"):
            make_valid_act(source_url="ftp://invalid-server.com/act.html")
