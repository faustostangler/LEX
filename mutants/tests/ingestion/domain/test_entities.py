"""Precision Unit Tests for Ingestion Domain Entities.

Verifies construction-time invariants and business constraints for GazetteEdition
specified in ADR-002 and SPEC-001.
"""

import uuid
from datetime import UTC, date, datetime

import pytest

from lex.ingestion.domain.entities import GazetteEdition
from lex.ingestion.domain.exceptions import DomainInvariantViolationError
from lex.ingestion.domain.value_objects import (
    DocumentHash,
    FederativeTier,
    GazetteDate,
    IngestionStatus,
    TerritoryId,
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
    source_url: str = ("https://www.in.gov.br/leiturajornal?data=02-01-2024&secao=do1"),
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
