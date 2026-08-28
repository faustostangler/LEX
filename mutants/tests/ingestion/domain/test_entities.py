"""Precision Unit Tests for Ingestion Domain Entities.

Verifies construction-time invariants and business constraints for GazetteEdition
specified in SPEC-001 (Section 2.2 & 4).
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
    source_url: str = (
        "https://pesquisa.in.gov.br/imprensa/jsp/visualiza/index.jsp?data=02/01/2024&jornal=1"
    ),
    full_text: str = (
        "DIÁRIO OFICIAL DA UNIÃO - SEÇÃO 1 - Publicado em 02/01/2024. Atos do Poder Executivo."
    ),
    char_count: int | None = None,
    scraped_at: datetime | None = None,
) -> GazetteEdition:
    """Helper to instantiate a valid GazetteEdition with typed defaults."""
    clean_text = full_text.strip()
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
        file_hash=DocumentHash.from_text(full_text),
        char_count=char_count if char_count is not None else len(clean_text),
        full_text=full_text,
        scraped_at=scraped_at or datetime.now(UTC),
    )


class TestGazetteEdition:
    """Acceptance tests for GazetteEdition Entity."""

    def test_successful_construction(self) -> None:
        """Scenario 1: Valid gazette edition constructs successfully."""
        edition = make_valid_edition()
        assert edition.territory_id.code == "BR"
        assert edition.tier == FederativeTier.FEDERAL
        assert edition.char_count == len(edition.full_text.strip())

    def test_empty_text_raises_invariant(self) -> None:
        """Boundary condition: Empty or whitespace-only full_text is rejected."""
        match_err = "full_text must contain non-whitespace content"
        with pytest.raises(DomainInvariantViolationError, match=match_err):
            make_valid_edition(full_text="   ", char_count=0)

    def test_zero_or_negative_char_count_raises_invariant(self) -> None:
        """Boundary condition: char_count <= 0 is rejected."""
        match_err = "char_count must be strictly greater than zero"
        with pytest.raises(DomainInvariantViolationError, match=match_err):
            make_valid_edition(full_text="valid text", char_count=-5)

    def test_char_count_mismatch_raises_invariant(self) -> None:
        """Boundary condition: char_count must strictly equal len(full_text.strip())."""
        with pytest.raises(DomainInvariantViolationError, match="char_count mismatch"):
            make_valid_edition(char_count=999999)

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
