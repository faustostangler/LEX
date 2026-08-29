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


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


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
mutants_xǁTerritoryIdǁfrom_code__mutmut: MutantDict = {}  # type: ignore


class TerritoryId(BaseModel):
    """Immutable Value Object representing an official Brazilian administrative territory."""

    model_config = ConfigDict(frozen=True)

    code: str

    @classmethod
    @_mutmut_mutated(mutants_xǁTerritoryIdǁfrom_code__mutmut, is_classmethod = True)
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

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_orig(cls, raw_code: str) -> Self:
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

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_1(cls, raw_code: str) -> Self:
        """Validate and instantiate a TerritoryId from a raw string code."""
        if isinstance(raw_code, str):
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

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_2(cls, raw_code: str) -> Self:
        """Validate and instantiate a TerritoryId from a raw string code."""
        if not isinstance(raw_code, str):
            raise InvalidTerritoryCodeError(
                None
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

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_3(cls, raw_code: str) -> Self:
        """Validate and instantiate a TerritoryId from a raw string code."""
        if not isinstance(raw_code, str):
            raise InvalidTerritoryCodeError(
                f"Territory code must be a string, got {type(None).__name__}"
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

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_4(cls, raw_code: str) -> Self:
        """Validate and instantiate a TerritoryId from a raw string code."""
        if not isinstance(raw_code, str):
            raise InvalidTerritoryCodeError(
                f"Territory code must be a string, got {type(raw_code).__name__}"
            )

        stripped = None
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

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_5(cls, raw_code: str) -> Self:
        """Validate and instantiate a TerritoryId from a raw string code."""
        if not isinstance(raw_code, str):
            raise InvalidTerritoryCodeError(
                f"Territory code must be a string, got {type(raw_code).__name__}"
            )

        stripped = raw_code.strip()
        if stripped:
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

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_6(cls, raw_code: str) -> Self:
        """Validate and instantiate a TerritoryId from a raw string code."""
        if not isinstance(raw_code, str):
            raise InvalidTerritoryCodeError(
                f"Territory code must be a string, got {type(raw_code).__name__}"
            )

        stripped = raw_code.strip()
        if not stripped:
            raise InvalidTerritoryCodeError(None)

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

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_7(cls, raw_code: str) -> Self:
        """Validate and instantiate a TerritoryId from a raw string code."""
        if not isinstance(raw_code, str):
            raise InvalidTerritoryCodeError(
                f"Territory code must be a string, got {type(raw_code).__name__}"
            )

        stripped = raw_code.strip()
        if not stripped:
            raise InvalidTerritoryCodeError("XXTerritory code cannot be empty or whitespace.XX")

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

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_8(cls, raw_code: str) -> Self:
        """Validate and instantiate a TerritoryId from a raw string code."""
        if not isinstance(raw_code, str):
            raise InvalidTerritoryCodeError(
                f"Territory code must be a string, got {type(raw_code).__name__}"
            )

        stripped = raw_code.strip()
        if not stripped:
            raise InvalidTerritoryCodeError("territory code cannot be empty or whitespace.")

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

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_9(cls, raw_code: str) -> Self:
        """Validate and instantiate a TerritoryId from a raw string code."""
        if not isinstance(raw_code, str):
            raise InvalidTerritoryCodeError(
                f"Territory code must be a string, got {type(raw_code).__name__}"
            )

        stripped = raw_code.strip()
        if not stripped:
            raise InvalidTerritoryCodeError("TERRITORY CODE CANNOT BE EMPTY OR WHITESPACE.")

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

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_10(cls, raw_code: str) -> Self:
        """Validate and instantiate a TerritoryId from a raw string code."""
        if not isinstance(raw_code, str):
            raise InvalidTerritoryCodeError(
                f"Territory code must be a string, got {type(raw_code).__name__}"
            )

        stripped = raw_code.strip()
        if not stripped:
            raise InvalidTerritoryCodeError("Territory code cannot be empty or whitespace.")

        if stripped != "BR":
            return cls(code="BR")

        if stripped in BRAZILIAN_STATE_CODES:
            return cls(code=stripped)

        if len(stripped) == 7 and stripped.isdigit():
            return cls(code=stripped)

        raise InvalidTerritoryCodeError(
            f"Invalid Brazilian territory code '{raw_code}'. "
            "Must be 'BR', a 2-letter state code, or a 7-digit IBGE code."
        )

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_11(cls, raw_code: str) -> Self:
        """Validate and instantiate a TerritoryId from a raw string code."""
        if not isinstance(raw_code, str):
            raise InvalidTerritoryCodeError(
                f"Territory code must be a string, got {type(raw_code).__name__}"
            )

        stripped = raw_code.strip()
        if not stripped:
            raise InvalidTerritoryCodeError("Territory code cannot be empty or whitespace.")

        if stripped == "XXBRXX":
            return cls(code="BR")

        if stripped in BRAZILIAN_STATE_CODES:
            return cls(code=stripped)

        if len(stripped) == 7 and stripped.isdigit():
            return cls(code=stripped)

        raise InvalidTerritoryCodeError(
            f"Invalid Brazilian territory code '{raw_code}'. "
            "Must be 'BR', a 2-letter state code, or a 7-digit IBGE code."
        )

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_12(cls, raw_code: str) -> Self:
        """Validate and instantiate a TerritoryId from a raw string code."""
        if not isinstance(raw_code, str):
            raise InvalidTerritoryCodeError(
                f"Territory code must be a string, got {type(raw_code).__name__}"
            )

        stripped = raw_code.strip()
        if not stripped:
            raise InvalidTerritoryCodeError("Territory code cannot be empty or whitespace.")

        if stripped == "br":
            return cls(code="BR")

        if stripped in BRAZILIAN_STATE_CODES:
            return cls(code=stripped)

        if len(stripped) == 7 and stripped.isdigit():
            return cls(code=stripped)

        raise InvalidTerritoryCodeError(
            f"Invalid Brazilian territory code '{raw_code}'. "
            "Must be 'BR', a 2-letter state code, or a 7-digit IBGE code."
        )

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_13(cls, raw_code: str) -> Self:
        """Validate and instantiate a TerritoryId from a raw string code."""
        if not isinstance(raw_code, str):
            raise InvalidTerritoryCodeError(
                f"Territory code must be a string, got {type(raw_code).__name__}"
            )

        stripped = raw_code.strip()
        if not stripped:
            raise InvalidTerritoryCodeError("Territory code cannot be empty or whitespace.")

        if stripped == "BR":
            return cls(code=None)

        if stripped in BRAZILIAN_STATE_CODES:
            return cls(code=stripped)

        if len(stripped) == 7 and stripped.isdigit():
            return cls(code=stripped)

        raise InvalidTerritoryCodeError(
            f"Invalid Brazilian territory code '{raw_code}'. "
            "Must be 'BR', a 2-letter state code, or a 7-digit IBGE code."
        )

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_14(cls, raw_code: str) -> Self:
        """Validate and instantiate a TerritoryId from a raw string code."""
        if not isinstance(raw_code, str):
            raise InvalidTerritoryCodeError(
                f"Territory code must be a string, got {type(raw_code).__name__}"
            )

        stripped = raw_code.strip()
        if not stripped:
            raise InvalidTerritoryCodeError("Territory code cannot be empty or whitespace.")

        if stripped == "BR":
            return cls(code="XXBRXX")

        if stripped in BRAZILIAN_STATE_CODES:
            return cls(code=stripped)

        if len(stripped) == 7 and stripped.isdigit():
            return cls(code=stripped)

        raise InvalidTerritoryCodeError(
            f"Invalid Brazilian territory code '{raw_code}'. "
            "Must be 'BR', a 2-letter state code, or a 7-digit IBGE code."
        )

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_15(cls, raw_code: str) -> Self:
        """Validate and instantiate a TerritoryId from a raw string code."""
        if not isinstance(raw_code, str):
            raise InvalidTerritoryCodeError(
                f"Territory code must be a string, got {type(raw_code).__name__}"
            )

        stripped = raw_code.strip()
        if not stripped:
            raise InvalidTerritoryCodeError("Territory code cannot be empty or whitespace.")

        if stripped == "BR":
            return cls(code="br")

        if stripped in BRAZILIAN_STATE_CODES:
            return cls(code=stripped)

        if len(stripped) == 7 and stripped.isdigit():
            return cls(code=stripped)

        raise InvalidTerritoryCodeError(
            f"Invalid Brazilian territory code '{raw_code}'. "
            "Must be 'BR', a 2-letter state code, or a 7-digit IBGE code."
        )

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_16(cls, raw_code: str) -> Self:
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

        if stripped not in BRAZILIAN_STATE_CODES:
            return cls(code=stripped)

        if len(stripped) == 7 and stripped.isdigit():
            return cls(code=stripped)

        raise InvalidTerritoryCodeError(
            f"Invalid Brazilian territory code '{raw_code}'. "
            "Must be 'BR', a 2-letter state code, or a 7-digit IBGE code."
        )

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_17(cls, raw_code: str) -> Self:
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
            return cls(code=None)

        if len(stripped) == 7 and stripped.isdigit():
            return cls(code=stripped)

        raise InvalidTerritoryCodeError(
            f"Invalid Brazilian territory code '{raw_code}'. "
            "Must be 'BR', a 2-letter state code, or a 7-digit IBGE code."
        )

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_18(cls, raw_code: str) -> Self:
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

        if len(stripped) == 7 or stripped.isdigit():
            return cls(code=stripped)

        raise InvalidTerritoryCodeError(
            f"Invalid Brazilian territory code '{raw_code}'. "
            "Must be 'BR', a 2-letter state code, or a 7-digit IBGE code."
        )

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_19(cls, raw_code: str) -> Self:
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

        if len(stripped) != 7 and stripped.isdigit():
            return cls(code=stripped)

        raise InvalidTerritoryCodeError(
            f"Invalid Brazilian territory code '{raw_code}'. "
            "Must be 'BR', a 2-letter state code, or a 7-digit IBGE code."
        )

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_20(cls, raw_code: str) -> Self:
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

        if len(stripped) == 8 and stripped.isdigit():
            return cls(code=stripped)

        raise InvalidTerritoryCodeError(
            f"Invalid Brazilian territory code '{raw_code}'. "
            "Must be 'BR', a 2-letter state code, or a 7-digit IBGE code."
        )

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_21(cls, raw_code: str) -> Self:
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
            return cls(code=None)

        raise InvalidTerritoryCodeError(
            f"Invalid Brazilian territory code '{raw_code}'. "
            "Must be 'BR', a 2-letter state code, or a 7-digit IBGE code."
        )

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_22(cls, raw_code: str) -> Self:
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
            None
        )

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_23(cls, raw_code: str) -> Self:
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
            "XXMust be 'BR', a 2-letter state code, or a 7-digit IBGE code.XX"
        )

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_24(cls, raw_code: str) -> Self:
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
            "must be 'br', a 2-letter state code, or a 7-digit ibge code."
        )

    @classmethod
    def xǁTerritoryIdǁfrom_code__mutmut_25(cls, raw_code: str) -> Self:
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
            "MUST BE 'BR', A 2-LETTER STATE CODE, OR A 7-DIGIT IBGE CODE."
        )

mutants_xǁTerritoryIdǁfrom_code__mutmut['_mutmut_orig'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_orig # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_1'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_1 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_2'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_2 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_3'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_3 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_4'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_4 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_5'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_5 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_6'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_6 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_7'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_7 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_8'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_8 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_9'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_9 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_10'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_10 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_11'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_11 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_12'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_12 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_13'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_13 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_14'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_14 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_15'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_15 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_16'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_16 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_17'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_17 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_18'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_18 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_19'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_19 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_20'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_20 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_21'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_21 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_22'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_22 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_23'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_23 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_24'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_24 # type: ignore # mutmut generated
mutants_xǁTerritoryIdǁfrom_code__mutmut['xǁTerritoryIdǁfrom_code__mutmut_25'] = TerritoryId.xǁTerritoryIdǁfrom_code__mutmut_25 # type: ignore # mutmut generated
mutants_xǁGazetteDateǁfrom_date__mutmut: MutantDict = {}  # type: ignore


class GazetteDate(BaseModel):
    """Immutable Value Object representing a gazette publication date."""

    model_config = ConfigDict(frozen=True)

    value: date

    @classmethod
    @_mutmut_mutated(mutants_xǁGazetteDateǁfrom_date__mutmut, is_classmethod = True)
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

    @classmethod
    def xǁGazetteDateǁfrom_date__mutmut_orig(cls, target_date: date) -> Self:
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

    @classmethod
    def xǁGazetteDateǁfrom_date__mutmut_1(cls, target_date: date) -> Self:
        """Validate and instantiate a GazetteDate."""
        if isinstance(target_date, date):
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

    @classmethod
    def xǁGazetteDateǁfrom_date__mutmut_2(cls, target_date: date) -> Self:
        """Validate and instantiate a GazetteDate."""
        if not isinstance(target_date, date):
            raise InvalidGazetteDateError(
                None
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

    @classmethod
    def xǁGazetteDateǁfrom_date__mutmut_3(cls, target_date: date) -> Self:
        """Validate and instantiate a GazetteDate."""
        if not isinstance(target_date, date):
            raise InvalidGazetteDateError(
                f"Expected datetime.date, got {type(None).__name__}"
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

    @classmethod
    def xǁGazetteDateǁfrom_date__mutmut_4(cls, target_date: date) -> Self:
        """Validate and instantiate a GazetteDate."""
        if not isinstance(target_date, date):
            raise InvalidGazetteDateError(
                f"Expected datetime.date, got {type(target_date).__name__}"
            )

        if target_date <= FIRST_BRAZILIAN_GAZETTE_DATE:
            raise InvalidGazetteDateError(
                f"Publication date {target_date.isoformat()} predates the first "
                f"Brazilian official gazette ({FIRST_BRAZILIAN_GAZETTE_DATE.isoformat()})."
            )

        if target_date > date.today():
            raise InvalidGazetteDateError(
                f"Publication date {target_date.isoformat()} cannot be in the future."
            )

        return cls(value=target_date)

    @classmethod
    def xǁGazetteDateǁfrom_date__mutmut_5(cls, target_date: date) -> Self:
        """Validate and instantiate a GazetteDate."""
        if not isinstance(target_date, date):
            raise InvalidGazetteDateError(
                f"Expected datetime.date, got {type(target_date).__name__}"
            )

        if target_date < FIRST_BRAZILIAN_GAZETTE_DATE:
            raise InvalidGazetteDateError(
                None
            )

        if target_date > date.today():
            raise InvalidGazetteDateError(
                f"Publication date {target_date.isoformat()} cannot be in the future."
            )

        return cls(value=target_date)

    @classmethod
    def xǁGazetteDateǁfrom_date__mutmut_6(cls, target_date: date) -> Self:
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

        if target_date >= date.today():
            raise InvalidGazetteDateError(
                f"Publication date {target_date.isoformat()} cannot be in the future."
            )

        return cls(value=target_date)

    @classmethod
    def xǁGazetteDateǁfrom_date__mutmut_7(cls, target_date: date) -> Self:
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
                None
            )

        return cls(value=target_date)

    @classmethod
    def xǁGazetteDateǁfrom_date__mutmut_8(cls, target_date: date) -> Self:
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

        return cls(value=None)

mutants_xǁGazetteDateǁfrom_date__mutmut['_mutmut_orig'] = GazetteDate.xǁGazetteDateǁfrom_date__mutmut_orig # type: ignore # mutmut generated
mutants_xǁGazetteDateǁfrom_date__mutmut['xǁGazetteDateǁfrom_date__mutmut_1'] = GazetteDate.xǁGazetteDateǁfrom_date__mutmut_1 # type: ignore # mutmut generated
mutants_xǁGazetteDateǁfrom_date__mutmut['xǁGazetteDateǁfrom_date__mutmut_2'] = GazetteDate.xǁGazetteDateǁfrom_date__mutmut_2 # type: ignore # mutmut generated
mutants_xǁGazetteDateǁfrom_date__mutmut['xǁGazetteDateǁfrom_date__mutmut_3'] = GazetteDate.xǁGazetteDateǁfrom_date__mutmut_3 # type: ignore # mutmut generated
mutants_xǁGazetteDateǁfrom_date__mutmut['xǁGazetteDateǁfrom_date__mutmut_4'] = GazetteDate.xǁGazetteDateǁfrom_date__mutmut_4 # type: ignore # mutmut generated
mutants_xǁGazetteDateǁfrom_date__mutmut['xǁGazetteDateǁfrom_date__mutmut_5'] = GazetteDate.xǁGazetteDateǁfrom_date__mutmut_5 # type: ignore # mutmut generated
mutants_xǁGazetteDateǁfrom_date__mutmut['xǁGazetteDateǁfrom_date__mutmut_6'] = GazetteDate.xǁGazetteDateǁfrom_date__mutmut_6 # type: ignore # mutmut generated
mutants_xǁGazetteDateǁfrom_date__mutmut['xǁGazetteDateǁfrom_date__mutmut_7'] = GazetteDate.xǁGazetteDateǁfrom_date__mutmut_7 # type: ignore # mutmut generated
mutants_xǁGazetteDateǁfrom_date__mutmut['xǁGazetteDateǁfrom_date__mutmut_8'] = GazetteDate.xǁGazetteDateǁfrom_date__mutmut_8 # type: ignore # mutmut generated
mutants_xǁDocumentHashǁfrom_hex__mutmut: MutantDict = {}  # type: ignore
mutants_xǁDocumentHashǁfrom_text__mutmut: MutantDict = {}  # type: ignore


class DocumentHash(BaseModel):
    """Immutable Value Object representing a 64-char SHA-256 content digest."""

    model_config = ConfigDict(frozen=True)

    hex_digest: str

    @classmethod
    @_mutmut_mutated(mutants_xǁDocumentHashǁfrom_hex__mutmut, is_classmethod = True)
    def from_hex(cls, raw_hash: str) -> Self:
        """Validate and instantiate a DocumentHash from a hex string."""
        if not isinstance(raw_hash, str) or not _HEX_SHA256_REGEX.match(raw_hash):
            raise InvalidDocumentHashError(
                f"Invalid SHA-256 hash '{raw_hash}'. "
                "Must be exactly 64 lowercase hexadecimal characters."
            )

        return cls(hex_digest=raw_hash)

    @classmethod
    def xǁDocumentHashǁfrom_hex__mutmut_orig(cls, raw_hash: str) -> Self:
        """Validate and instantiate a DocumentHash from a hex string."""
        if not isinstance(raw_hash, str) or not _HEX_SHA256_REGEX.match(raw_hash):
            raise InvalidDocumentHashError(
                f"Invalid SHA-256 hash '{raw_hash}'. "
                "Must be exactly 64 lowercase hexadecimal characters."
            )

        return cls(hex_digest=raw_hash)

    @classmethod
    def xǁDocumentHashǁfrom_hex__mutmut_1(cls, raw_hash: str) -> Self:
        """Validate and instantiate a DocumentHash from a hex string."""
        if not isinstance(raw_hash, str) and not _HEX_SHA256_REGEX.match(raw_hash):
            raise InvalidDocumentHashError(
                f"Invalid SHA-256 hash '{raw_hash}'. "
                "Must be exactly 64 lowercase hexadecimal characters."
            )

        return cls(hex_digest=raw_hash)

    @classmethod
    def xǁDocumentHashǁfrom_hex__mutmut_2(cls, raw_hash: str) -> Self:
        """Validate and instantiate a DocumentHash from a hex string."""
        if isinstance(raw_hash, str) or not _HEX_SHA256_REGEX.match(raw_hash):
            raise InvalidDocumentHashError(
                f"Invalid SHA-256 hash '{raw_hash}'. "
                "Must be exactly 64 lowercase hexadecimal characters."
            )

        return cls(hex_digest=raw_hash)

    @classmethod
    def xǁDocumentHashǁfrom_hex__mutmut_3(cls, raw_hash: str) -> Self:
        """Validate and instantiate a DocumentHash from a hex string."""
        if not isinstance(raw_hash, str) or _HEX_SHA256_REGEX.match(raw_hash):
            raise InvalidDocumentHashError(
                f"Invalid SHA-256 hash '{raw_hash}'. "
                "Must be exactly 64 lowercase hexadecimal characters."
            )

        return cls(hex_digest=raw_hash)

    @classmethod
    def xǁDocumentHashǁfrom_hex__mutmut_4(cls, raw_hash: str) -> Self:
        """Validate and instantiate a DocumentHash from a hex string."""
        if not isinstance(raw_hash, str) or not _HEX_SHA256_REGEX.match(None):
            raise InvalidDocumentHashError(
                f"Invalid SHA-256 hash '{raw_hash}'. "
                "Must be exactly 64 lowercase hexadecimal characters."
            )

        return cls(hex_digest=raw_hash)

    @classmethod
    def xǁDocumentHashǁfrom_hex__mutmut_5(cls, raw_hash: str) -> Self:
        """Validate and instantiate a DocumentHash from a hex string."""
        if not isinstance(raw_hash, str) or not _HEX_SHA256_REGEX.match(raw_hash):
            raise InvalidDocumentHashError(
                None
            )

        return cls(hex_digest=raw_hash)

    @classmethod
    def xǁDocumentHashǁfrom_hex__mutmut_6(cls, raw_hash: str) -> Self:
        """Validate and instantiate a DocumentHash from a hex string."""
        if not isinstance(raw_hash, str) or not _HEX_SHA256_REGEX.match(raw_hash):
            raise InvalidDocumentHashError(
                f"Invalid SHA-256 hash '{raw_hash}'. "
                "XXMust be exactly 64 lowercase hexadecimal characters.XX"
            )

        return cls(hex_digest=raw_hash)

    @classmethod
    def xǁDocumentHashǁfrom_hex__mutmut_7(cls, raw_hash: str) -> Self:
        """Validate and instantiate a DocumentHash from a hex string."""
        if not isinstance(raw_hash, str) or not _HEX_SHA256_REGEX.match(raw_hash):
            raise InvalidDocumentHashError(
                f"Invalid SHA-256 hash '{raw_hash}'. "
                "must be exactly 64 lowercase hexadecimal characters."
            )

        return cls(hex_digest=raw_hash)

    @classmethod
    def xǁDocumentHashǁfrom_hex__mutmut_8(cls, raw_hash: str) -> Self:
        """Validate and instantiate a DocumentHash from a hex string."""
        if not isinstance(raw_hash, str) or not _HEX_SHA256_REGEX.match(raw_hash):
            raise InvalidDocumentHashError(
                f"Invalid SHA-256 hash '{raw_hash}'. "
                "MUST BE EXACTLY 64 LOWERCASE HEXADECIMAL CHARACTERS."
            )

        return cls(hex_digest=raw_hash)

    @classmethod
    def xǁDocumentHashǁfrom_hex__mutmut_9(cls, raw_hash: str) -> Self:
        """Validate and instantiate a DocumentHash from a hex string."""
        if not isinstance(raw_hash, str) or not _HEX_SHA256_REGEX.match(raw_hash):
            raise InvalidDocumentHashError(
                f"Invalid SHA-256 hash '{raw_hash}'. "
                "Must be exactly 64 lowercase hexadecimal characters."
            )

        return cls(hex_digest=None)

    @classmethod
    @_mutmut_mutated(mutants_xǁDocumentHashǁfrom_text__mutmut, is_classmethod = True)
    def from_text(cls, text_content: str) -> Self:
        """Compute SHA-256 digest directly from plain text content."""
        digest = hashlib.sha256(text_content.encode("utf-8")).hexdigest()
        return cls.from_hex(digest)

    @classmethod
    def xǁDocumentHashǁfrom_text__mutmut_orig(cls, text_content: str) -> Self:
        """Compute SHA-256 digest directly from plain text content."""
        digest = hashlib.sha256(text_content.encode("utf-8")).hexdigest()
        return cls.from_hex(digest)

    @classmethod
    def xǁDocumentHashǁfrom_text__mutmut_1(cls, text_content: str) -> Self:
        """Compute SHA-256 digest directly from plain text content."""
        digest = None
        return cls.from_hex(digest)

    @classmethod
    def xǁDocumentHashǁfrom_text__mutmut_2(cls, text_content: str) -> Self:
        """Compute SHA-256 digest directly from plain text content."""
        digest = hashlib.sha256(None).hexdigest()
        return cls.from_hex(digest)

    @classmethod
    def xǁDocumentHashǁfrom_text__mutmut_3(cls, text_content: str) -> Self:
        """Compute SHA-256 digest directly from plain text content."""
        digest = hashlib.sha256(text_content.encode(None)).hexdigest()
        return cls.from_hex(digest)

    @classmethod
    def xǁDocumentHashǁfrom_text__mutmut_4(cls, text_content: str) -> Self:
        """Compute SHA-256 digest directly from plain text content."""
        digest = hashlib.sha256(text_content.encode("XXutf-8XX")).hexdigest()
        return cls.from_hex(digest)

    @classmethod
    def xǁDocumentHashǁfrom_text__mutmut_5(cls, text_content: str) -> Self:
        """Compute SHA-256 digest directly from plain text content."""
        digest = hashlib.sha256(text_content.encode("UTF-8")).hexdigest()
        return cls.from_hex(digest)

    @classmethod
    def xǁDocumentHashǁfrom_text__mutmut_6(cls, text_content: str) -> Self:
        """Compute SHA-256 digest directly from plain text content."""
        digest = hashlib.sha256(text_content.encode("utf-8")).hexdigest()
        return cls.from_hex(None)

mutants_xǁDocumentHashǁfrom_hex__mutmut['_mutmut_orig'] = DocumentHash.xǁDocumentHashǁfrom_hex__mutmut_orig # type: ignore # mutmut generated
mutants_xǁDocumentHashǁfrom_hex__mutmut['xǁDocumentHashǁfrom_hex__mutmut_1'] = DocumentHash.xǁDocumentHashǁfrom_hex__mutmut_1 # type: ignore # mutmut generated
mutants_xǁDocumentHashǁfrom_hex__mutmut['xǁDocumentHashǁfrom_hex__mutmut_2'] = DocumentHash.xǁDocumentHashǁfrom_hex__mutmut_2 # type: ignore # mutmut generated
mutants_xǁDocumentHashǁfrom_hex__mutmut['xǁDocumentHashǁfrom_hex__mutmut_3'] = DocumentHash.xǁDocumentHashǁfrom_hex__mutmut_3 # type: ignore # mutmut generated
mutants_xǁDocumentHashǁfrom_hex__mutmut['xǁDocumentHashǁfrom_hex__mutmut_4'] = DocumentHash.xǁDocumentHashǁfrom_hex__mutmut_4 # type: ignore # mutmut generated
mutants_xǁDocumentHashǁfrom_hex__mutmut['xǁDocumentHashǁfrom_hex__mutmut_5'] = DocumentHash.xǁDocumentHashǁfrom_hex__mutmut_5 # type: ignore # mutmut generated
mutants_xǁDocumentHashǁfrom_hex__mutmut['xǁDocumentHashǁfrom_hex__mutmut_6'] = DocumentHash.xǁDocumentHashǁfrom_hex__mutmut_6 # type: ignore # mutmut generated
mutants_xǁDocumentHashǁfrom_hex__mutmut['xǁDocumentHashǁfrom_hex__mutmut_7'] = DocumentHash.xǁDocumentHashǁfrom_hex__mutmut_7 # type: ignore # mutmut generated
mutants_xǁDocumentHashǁfrom_hex__mutmut['xǁDocumentHashǁfrom_hex__mutmut_8'] = DocumentHash.xǁDocumentHashǁfrom_hex__mutmut_8 # type: ignore # mutmut generated
mutants_xǁDocumentHashǁfrom_hex__mutmut['xǁDocumentHashǁfrom_hex__mutmut_9'] = DocumentHash.xǁDocumentHashǁfrom_hex__mutmut_9 # type: ignore # mutmut generated

mutants_xǁDocumentHashǁfrom_text__mutmut['_mutmut_orig'] = DocumentHash.xǁDocumentHashǁfrom_text__mutmut_orig # type: ignore # mutmut generated
mutants_xǁDocumentHashǁfrom_text__mutmut['xǁDocumentHashǁfrom_text__mutmut_1'] = DocumentHash.xǁDocumentHashǁfrom_text__mutmut_1 # type: ignore # mutmut generated
mutants_xǁDocumentHashǁfrom_text__mutmut['xǁDocumentHashǁfrom_text__mutmut_2'] = DocumentHash.xǁDocumentHashǁfrom_text__mutmut_2 # type: ignore # mutmut generated
mutants_xǁDocumentHashǁfrom_text__mutmut['xǁDocumentHashǁfrom_text__mutmut_3'] = DocumentHash.xǁDocumentHashǁfrom_text__mutmut_3 # type: ignore # mutmut generated
mutants_xǁDocumentHashǁfrom_text__mutmut['xǁDocumentHashǁfrom_text__mutmut_4'] = DocumentHash.xǁDocumentHashǁfrom_text__mutmut_4 # type: ignore # mutmut generated
mutants_xǁDocumentHashǁfrom_text__mutmut['xǁDocumentHashǁfrom_text__mutmut_5'] = DocumentHash.xǁDocumentHashǁfrom_text__mutmut_5 # type: ignore # mutmut generated
mutants_xǁDocumentHashǁfrom_text__mutmut['xǁDocumentHashǁfrom_text__mutmut_6'] = DocumentHash.xǁDocumentHashǁfrom_text__mutmut_6 # type: ignore # mutmut generated
