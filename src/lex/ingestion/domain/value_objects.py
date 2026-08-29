"""Value Objects for the Ingestion and Digestion Bounded Contexts.

Enforces strict domain invariants at construction time for all legislative metadata
concepts (TerritoryId, GazetteDate, DocumentHash, FederativeTier, ActType, ClassificationSource)
to eradicate Primitive Obsession across the modular monolith.
"""

import hashlib
import re
from datetime import date
from enum import StrEnum
from typing import Final, Self

from pydantic import BaseModel, ConfigDict

from lex.ingestion.domain.exceptions import (
    InvalidDocumentHashError,
    InvalidGazetteDateError,
    InvalidTerritoryCodeError,
)


class FederativeTier(StrEnum):
    """The administrative jurisdiction level of an Official Gazette."""

    FEDERAL = "federal"
    STATE = "state"
    MUNICIPAL = "municipal"


class IngestionStatus(StrEnum):
    """Lifecycle status of a gazette edition ingestion."""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class ClassificationSource(StrEnum):
    """Origin of the normative act classification and boundary segmentation."""

    PRE_SEGMENTED_SOURCE = "pre_segmented_source"
    DETERMINISTIC_REGEX = "deterministic_regex"
    LLM_FALLBACK = "llm_fallback"


class ActType(StrEnum):
    """Standardized legal typology for Brazilian normative acts."""

    LEI = "LEI"
    LEI_COMPLEMENTAR = "LEI COMPLEMENTAR"
    DECRETO = "DECRETO"
    DECRETO_LEI = "DECRETO-LEI"
    PORTARIA = "PORTARIA"
    RESOLUCAO = "RESOLUÇÃO"
    INSTRUCAO_NORMATIVA = "INSTRUÇÃO NORMATIVA"
    ALVARA = "ALVARÁ"
    DECISAO = "DECISÃO"
    DESPACHO = "DESPACHO"
    EDITAL = "EDITAL"
    ACORDAO = "ACÓRDÃO"
    CONTRATO = "CONTRATO"
    CONVENIO = "CONVÊNIO"
    ATO_DECLARATORIO = "ATO DECLARATÓRIO"
    RETIFICACAO = "RETIFICAÇÃO"
    AVISO = "AVISO"
    OUTROS = "OUTROS"


# Set of 27 official Brazilian state codes (26 states + DF)
BRAZILIAN_STATE_CODES: Final[frozenset[str]] = frozenset(
    {
        "AC",
        "AL",
        "AM",
        "AP",
        "BA",
        "CE",
        "DF",
        "ES",
        "GO",
        "MA",
        "MG",
        "MS",
        "MT",
        "PA",
        "PB",
        "PE",
        "PI",
        "PR",
        "RJ",
        "RN",
        "RO",
        "RR",
        "RS",
        "SC",
        "SE",
        "SP",
        "TO",
    }
)

FIRST_BRAZILIAN_GAZETTE_DATE: Final[date] = date(1808, 9, 10)
_HEX_SHA256_REGEX: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{64}$")


class TerritoryId(BaseModel):
    """Immutable Value Object representing an official Brazilian administrative territory."""

    model_config = ConfigDict(frozen=True)

    code: str

    @classmethod
    def from_code(cls, raw_code: str) -> Self:
        """Validate and instantiate a TerritoryId from a raw string code."""
        if not isinstance(raw_code, str):
            raise InvalidTerritoryCodeError(
                f"Territory code must be a string, got {type(raw_code).__name__}"
            )

        stripped = raw_code.strip()
        if not stripped:
            raise InvalidTerritoryCodeError("Territory code cannot be empty or whitespace.")

        if stripped == "BR":
            return cls(code="BR")

        if stripped in BRAZILIAN_STATE_CODES:
            return cls(code=stripped)

        if len(stripped) == 7 and stripped.isdigit():
            return cls(code=stripped)

        raise InvalidTerritoryCodeError(
            f"Invalid Brazilian territory code '{raw_code}'. "
            "Must be 'BR', a 2-letter state code, or a 7-digit IBGE code."
        )


class GazetteDate(BaseModel):
    """Immutable Value Object representing a gazette publication date."""

    model_config = ConfigDict(frozen=True)

    value: date

    @classmethod
    def from_date(cls, target_date: date) -> Self:
        """Validate and instantiate a GazetteDate."""
        if not isinstance(target_date, date):
            raise InvalidGazetteDateError(
                f"Expected datetime.date, got {type(target_date).__name__}"
            )

        if target_date < FIRST_BRAZILIAN_GAZETTE_DATE:
            raise InvalidGazetteDateError(
                f"Publication date {target_date.isoformat()} predates the first "
                f"Brazilian official gazette ({FIRST_BRAZILIAN_GAZETTE_DATE.isoformat()})."
            )

        if target_date > date.today():
            raise InvalidGazetteDateError(
                f"Publication date {target_date.isoformat()} cannot be in the future."
            )

        return cls(value=target_date)


class DocumentHash(BaseModel):
    """Immutable Value Object representing a 64-char SHA-256 content digest."""

    model_config = ConfigDict(frozen=True)

    hex_digest: str

    @classmethod
    def from_hex(cls, raw_hash: str) -> Self:
        """Validate and instantiate a DocumentHash from a hex string."""
        if not isinstance(raw_hash, str) or not _HEX_SHA256_REGEX.match(raw_hash):
            raise InvalidDocumentHashError(
                f"Invalid SHA-256 hash '{raw_hash}'. "
                "Must be exactly 64 lowercase hexadecimal characters."
            )

        return cls(hex_digest=raw_hash)

    @classmethod
    def from_text(cls, text_content: str) -> Self:
        """Compute SHA-256 digest directly from plain text content."""
        digest = hashlib.sha256(text_content.encode("utf-8")).hexdigest()
        return cls.from_hex(digest)
