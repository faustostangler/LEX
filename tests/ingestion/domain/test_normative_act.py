"""Precision Unit Tests for NormativeAct Domain Entity.

Verifies construction-time invariants, non-empty text enforcement, hash computation,
and typology validation specified in ADR-002.
"""

import uuid
from datetime import UTC, date, datetime

import pytest

from lex.ingestion.domain.entities import NormativeAct
from lex.ingestion.domain.exceptions import DomainInvariantViolationError
from lex.ingestion.domain.value_objects import (
    ClassificationSource,
    DocumentHash,
    GazetteDate,
    TerritoryId,
)


def make_valid_normative_act(
    *,
    id: uuid.UUID | None = None,
    edition_id: uuid.UUID | None = None,
    territory_code: str = "BR",
    pub_date: date | None = None,
    section: str = "secao_1",
    edition_number: str = "10",
    is_extra: bool = False,
    act_type: str = "ALVARÁ",
    act_number: str = "470",
    act_year: int = 2024,
    title: str = "Alvará nº 470, de 12 de JANEIRO de 2024",
    ementa: str | None = None,
    hierarchy: list[str] | None = None,
    authority_name: str = "WAGNER DA SILVA SIQUEIRA",
    authority_role: str = "Substituto",
    source_url: str = (
        "https://www.in.gov.br/web/dou/-/alvara-n-470-de-12-de-janeiro-de-2024-537307744"
    ),
    raw_content: str = "O SUPERINTENDENTE DE OUTORGA... outorga o seguinte Alvará de Pesquisa.",
    classification_source: ClassificationSource = (ClassificationSource.PRE_SEGMENTED_SOURCE),
    classification_confidence: float = 1.0,
    scraped_at: datetime | None = None,
) -> NormativeAct:
    """Helper to instantiate a valid NormativeAct with typed defaults."""
    clean_text = raw_content.strip()
    return NormativeAct(
        id=id or uuid.uuid4(),
        edition_id=edition_id or uuid.uuid4(),
        territory_id=TerritoryId.from_code(territory_code),
        date=GazetteDate.from_date(pub_date or date(2024, 1, 15)),
        section=section,
        edition_number=edition_number,
        is_extra_edition=is_extra,
        act_type=act_type,
        act_number=act_number,
        act_year=act_year,
        title=title,
        ementa=ementa,
        hierarchy=hierarchy
        or [
            "Ministério de Minas e Energia",
            "Agência Nacional de Mineração",
            "Superintendência de Outorga de Títulos Minerários",
        ],
        authority_name=authority_name,
        authority_role=authority_role,
        source_url=source_url,
        content_hash=DocumentHash.from_text(clean_text),
        char_count=len(clean_text),
        raw_content=raw_content,
        classification_source=classification_source,
        classification_confidence=classification_confidence,
        scraped_at=scraped_at or datetime.now(UTC),
    )


class TestNormativeAct:
    """Acceptance tests for NormativeAct Entity."""

    def test_successful_construction(self) -> None:
        """Scenario 1: Valid normative act constructs successfully."""
        act = make_valid_normative_act()
        assert act.territory_id.code == "BR"
        assert act.act_type == "ALVARÁ"
        assert act.act_number == "470"
        assert act.act_year == 2024
        assert len(act.hierarchy) == 3
        assert act.classification_source == ClassificationSource.PRE_SEGMENTED_SOURCE
        assert act.classification_confidence == 1.0

    def test_empty_raw_content_raises_invariant(self) -> None:
        """Boundary condition: Empty or whitespace-only raw_content is rejected."""
        with pytest.raises(
            DomainInvariantViolationError,
            match="raw_content must contain non-whitespace legislative content",
        ):
            make_valid_normative_act(raw_content="   ")

    def test_empty_title_raises_invariant(self) -> None:
        """Boundary condition: Empty title is rejected."""
        with pytest.raises(DomainInvariantViolationError, match="title cannot be empty"):
            make_valid_normative_act(title="  ")

    def test_empty_act_type_raises_invariant(self) -> None:
        """Boundary condition: Empty act_type is rejected."""
        with pytest.raises(DomainInvariantViolationError, match="act_type cannot be empty"):
            make_valid_normative_act(act_type="  ")

    def test_invalid_source_url_raises_invariant(self) -> None:
        """Boundary condition: source_url must start with http/https."""
        with pytest.raises(DomainInvariantViolationError, match="source_url must start with http"):
            make_valid_normative_act(source_url="ftp://invalid.gov.br/act")
