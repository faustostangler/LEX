"""Value Objects and Enums for the Treatment Bounded Context.

Codifies canonical provision paths, mutation types, and statutory status indicators.
"""

import re
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict

from lex.treatment.domain.exceptions import InvalidCanonicalNodePathError

# Canonical segment patterns
RE_SEG_ART = re.compile(r"^art_\d+(?:_[a-z]+)?$")
RE_SEG_PAR = re.compile(r"^(?:par_\d+(?:_[a-z]+)?|par_unico)$")
RE_SEG_INC = re.compile(r"^inc_\d+(?:_[a-z]+)?$")
RE_SEG_ALI = re.compile(r"^ali_[a-z]+$")
RE_SEG_ITEM = re.compile(r"^item_\d+$")


class MutationType(StrEnum):
    """Enumeration of all statutory amendment modalities under LC 95/1998."""

    ACRESCIMO = "ACRESCIMO"
    ALTERACAO_NR = "ALTERACAO_NR"
    REVOGACAO_EXPRESSA = "REVOGACAO_EXPRESSA"
    REVOGACAO_TACITA = "REVOGACAO_TACITA"
    SUSPENSAO_EFICACIA = "SUSPENSAO_EFICACIA"
    RENUMERACAO = "RENUMERACAO"
    RETIFICACAO = "RETIFICACAO"


class DispositivoStatus(StrEnum):
    """Operational legal validity state of a statutory provision."""

    ORIGINAL_ACTIVE = "original_active"  # Unaltered since base enactment
    MODIFIED_ACTIVE = "modified_active"  # Altered by subsequent statute (NR)
    REVOKED = "revoked"  # Revoked (rendered with <strike>)
    SUSPENDED = "suspended"  # Efficacy suspended (e.g. STF ADI)


class DispositivoType(StrEnum):
    """Structural typology of legislative provisions under LC 95/1998."""

    ARTIGO = "artigo"
    PARAGRAFO = "paragrafo"
    PARAGRAFO_UNICO = "paragrafo_unico"
    INCISO = "inciso"
    ALINEA = "alinea"
    ITEM = "item"
    CAPUT = "caput"


class CanonicalNodePath(BaseModel):
    """Immutable Value Object for a dot-separated hierarchical provision address.

    Examples:
        - `art_3`
        - `art_3.par_1`
        - `art_3.par_unico`
        - `art_3.par_2.inc_14`
        - `art_3.inc_2.ali_a.item_1`
    """

    model_config = ConfigDict(frozen=True)

    value: str

    @classmethod
    def _validate_segments(cls, segments: list[str]) -> bool:
        """Validates that segments follow LC 95 hierarchy rules."""
        if not segments:
            return False

        # Segment 0 must be an article
        if not RE_SEG_ART.fullmatch(segments[0]):
            return False

        if len(segments) == 1:
            return True

        # Classify each segment type
        types: list[str] = []
        for seg in segments:
            if RE_SEG_ART.fullmatch(seg):
                types.append("art")
            elif RE_SEG_PAR.fullmatch(seg):
                types.append("par")
            elif RE_SEG_INC.fullmatch(seg):
                types.append("inc")
            elif RE_SEG_ALI.fullmatch(seg):
                types.append("ali")
            elif RE_SEG_ITEM.fullmatch(seg):
                types.append("item")
            else:
                return False

        # Allowed sequences of types under LC 95:
        # art
        # art.par
        # art.par.inc
        # art.par.inc.ali
        # art.par.inc.ali.item
        # art.par.ali
        # art.par.ali.item
        # art.inc
        # art.inc.ali
        # art.inc.ali.item
        allowed_sequences = {
            ("art",),
            ("art", "par"),
            ("art", "par", "inc"),
            ("art", "par", "inc", "ali"),
            ("art", "par", "inc", "ali", "item"),
            ("art", "par", "ali"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def from_string(cls, path_str: str) -> Self:
        """Constructs and validates a CanonicalNodePath from a raw string.

        Args:
            path_str: The dot-separated address (e.g., 'art_3.inc_1').

        Returns:
            A validated CanonicalNodePath instance.

        Raises:
            InvalidCanonicalNodePathError: If path_str does not strictly conform
                to LC 95 hierarchical address grammar.
        """
        if not path_str or not isinstance(path_str, str) or not path_str.strip():
            raise InvalidCanonicalNodePathError("Canonical node path cannot be empty.")

        cleaned = path_str.strip()
        segments = cleaned.split(".")
        if not cls._validate_segments(segments):
            raise InvalidCanonicalNodePathError(
                f"Invalid canonical node path: '{cleaned}'. "
                "Must follow statutory provision hierarchy: "
                "'art_X[.par_Y|.par_unico][.inc_Z][.ali_W][.item_K]'."
            )

        return cls(value=cleaned)

    @property
    def segments(self) -> list[str]:
        """Returns the individual path segments."""
        return self.value.split(".")

    @property
    def depth(self) -> int:
        """Returns the hierarchical nesting depth (1 for art_X, 2 for par_Y/inc_Z, etc.)."""
        return len(self.segments)

    @property
    def leaf_name(self) -> str:
        """Returns the terminal segment of the path."""
        return self.segments[-1]

    @property
    def parent_path(self) -> "CanonicalNodePath | None":
        """Returns the parent node path, or None if this is an article root."""
        segs = self.segments
        if len(segs) <= 1:
            return None
        return CanonicalNodePath(value=".".join(segs[:-1]))

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"CanonicalNodePath('{self.value}')"
