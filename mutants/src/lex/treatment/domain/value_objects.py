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


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


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
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCanonicalNodePathǁfrom_string__mutmut: MutantDict = {}  # type: ignore


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
    @_mutmut_mutated(mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut, is_classmethod = True)
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_orig(cls, segments: list[str]) -> bool:
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_1(cls, segments: list[str]) -> bool:
        """Validates that segments follow LC 95 hierarchy rules."""
        if segments:
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_2(cls, segments: list[str]) -> bool:
        """Validates that segments follow LC 95 hierarchy rules."""
        if not segments:
            return True

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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_3(cls, segments: list[str]) -> bool:
        """Validates that segments follow LC 95 hierarchy rules."""
        if not segments:
            return False

        # Segment 0 must be an article
        if RE_SEG_ART.fullmatch(segments[0]):
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_4(cls, segments: list[str]) -> bool:
        """Validates that segments follow LC 95 hierarchy rules."""
        if not segments:
            return False

        # Segment 0 must be an article
        if not RE_SEG_ART.fullmatch(None):
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_5(cls, segments: list[str]) -> bool:
        """Validates that segments follow LC 95 hierarchy rules."""
        if not segments:
            return False

        # Segment 0 must be an article
        if not RE_SEG_ART.fullmatch(segments[1]):
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_6(cls, segments: list[str]) -> bool:
        """Validates that segments follow LC 95 hierarchy rules."""
        if not segments:
            return False

        # Segment 0 must be an article
        if not RE_SEG_ART.fullmatch(segments[0]):
            return True

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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_7(cls, segments: list[str]) -> bool:
        """Validates that segments follow LC 95 hierarchy rules."""
        if not segments:
            return False

        # Segment 0 must be an article
        if not RE_SEG_ART.fullmatch(segments[0]):
            return False

        if len(segments) != 1:
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_8(cls, segments: list[str]) -> bool:
        """Validates that segments follow LC 95 hierarchy rules."""
        if not segments:
            return False

        # Segment 0 must be an article
        if not RE_SEG_ART.fullmatch(segments[0]):
            return False

        if len(segments) == 2:
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_9(cls, segments: list[str]) -> bool:
        """Validates that segments follow LC 95 hierarchy rules."""
        if not segments:
            return False

        # Segment 0 must be an article
        if not RE_SEG_ART.fullmatch(segments[0]):
            return False

        if len(segments) == 1:
            return False

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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_10(cls, segments: list[str]) -> bool:
        """Validates that segments follow LC 95 hierarchy rules."""
        if not segments:
            return False

        # Segment 0 must be an article
        if not RE_SEG_ART.fullmatch(segments[0]):
            return False

        if len(segments) == 1:
            return True

        # Classify each segment type
        types: list[str] = None
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_11(cls, segments: list[str]) -> bool:
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
            if RE_SEG_ART.fullmatch(None):
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_12(cls, segments: list[str]) -> bool:
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
                types.append(None)
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_13(cls, segments: list[str]) -> bool:
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
                types.append("XXartXX")
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_14(cls, segments: list[str]) -> bool:
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
                types.append("ART")
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_15(cls, segments: list[str]) -> bool:
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
            elif RE_SEG_PAR.fullmatch(None):
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_16(cls, segments: list[str]) -> bool:
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
                types.append(None)
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_17(cls, segments: list[str]) -> bool:
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
                types.append("XXparXX")
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_18(cls, segments: list[str]) -> bool:
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
                types.append("PAR")
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_19(cls, segments: list[str]) -> bool:
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
            elif RE_SEG_INC.fullmatch(None):
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_20(cls, segments: list[str]) -> bool:
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
                types.append(None)
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_21(cls, segments: list[str]) -> bool:
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
                types.append("XXincXX")
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_22(cls, segments: list[str]) -> bool:
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
                types.append("INC")
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_23(cls, segments: list[str]) -> bool:
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
            elif RE_SEG_ALI.fullmatch(None):
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_24(cls, segments: list[str]) -> bool:
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
                types.append(None)
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_25(cls, segments: list[str]) -> bool:
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
                types.append("XXaliXX")
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_26(cls, segments: list[str]) -> bool:
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
                types.append("ALI")
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_27(cls, segments: list[str]) -> bool:
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
            elif RE_SEG_ITEM.fullmatch(None):
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_28(cls, segments: list[str]) -> bool:
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
                types.append(None)
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_29(cls, segments: list[str]) -> bool:
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
                types.append("XXitemXX")
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_30(cls, segments: list[str]) -> bool:
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
                types.append("ITEM")
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_31(cls, segments: list[str]) -> bool:
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
                return True

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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_32(cls, segments: list[str]) -> bool:
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
        allowed_sequences = None
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_33(cls, segments: list[str]) -> bool:
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
            ("XXartXX",),
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_34(cls, segments: list[str]) -> bool:
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
            ("ART",),
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_35(cls, segments: list[str]) -> bool:
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
            ("XXartXX", "par"),
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_36(cls, segments: list[str]) -> bool:
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
            ("ART", "par"),
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_37(cls, segments: list[str]) -> bool:
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
            ("art", "XXparXX"),
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_38(cls, segments: list[str]) -> bool:
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
            ("art", "PAR"),
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_39(cls, segments: list[str]) -> bool:
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
            ("XXartXX", "par", "inc"),
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_40(cls, segments: list[str]) -> bool:
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
            ("ART", "par", "inc"),
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_41(cls, segments: list[str]) -> bool:
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
            ("art", "XXparXX", "inc"),
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_42(cls, segments: list[str]) -> bool:
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
            ("art", "PAR", "inc"),
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_43(cls, segments: list[str]) -> bool:
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
            ("art", "par", "XXincXX"),
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_44(cls, segments: list[str]) -> bool:
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
            ("art", "par", "INC"),
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
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_45(cls, segments: list[str]) -> bool:
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
            ("XXartXX", "par", "inc", "ali"),
            ("art", "par", "inc", "ali", "item"),
            ("art", "par", "ali"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_46(cls, segments: list[str]) -> bool:
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
            ("ART", "par", "inc", "ali"),
            ("art", "par", "inc", "ali", "item"),
            ("art", "par", "ali"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_47(cls, segments: list[str]) -> bool:
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
            ("art", "XXparXX", "inc", "ali"),
            ("art", "par", "inc", "ali", "item"),
            ("art", "par", "ali"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_48(cls, segments: list[str]) -> bool:
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
            ("art", "PAR", "inc", "ali"),
            ("art", "par", "inc", "ali", "item"),
            ("art", "par", "ali"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_49(cls, segments: list[str]) -> bool:
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
            ("art", "par", "XXincXX", "ali"),
            ("art", "par", "inc", "ali", "item"),
            ("art", "par", "ali"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_50(cls, segments: list[str]) -> bool:
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
            ("art", "par", "INC", "ali"),
            ("art", "par", "inc", "ali", "item"),
            ("art", "par", "ali"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_51(cls, segments: list[str]) -> bool:
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
            ("art", "par", "inc", "XXaliXX"),
            ("art", "par", "inc", "ali", "item"),
            ("art", "par", "ali"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_52(cls, segments: list[str]) -> bool:
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
            ("art", "par", "inc", "ALI"),
            ("art", "par", "inc", "ali", "item"),
            ("art", "par", "ali"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_53(cls, segments: list[str]) -> bool:
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
            ("XXartXX", "par", "inc", "ali", "item"),
            ("art", "par", "ali"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_54(cls, segments: list[str]) -> bool:
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
            ("ART", "par", "inc", "ali", "item"),
            ("art", "par", "ali"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_55(cls, segments: list[str]) -> bool:
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
            ("art", "XXparXX", "inc", "ali", "item"),
            ("art", "par", "ali"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_56(cls, segments: list[str]) -> bool:
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
            ("art", "PAR", "inc", "ali", "item"),
            ("art", "par", "ali"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_57(cls, segments: list[str]) -> bool:
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
            ("art", "par", "XXincXX", "ali", "item"),
            ("art", "par", "ali"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_58(cls, segments: list[str]) -> bool:
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
            ("art", "par", "INC", "ali", "item"),
            ("art", "par", "ali"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_59(cls, segments: list[str]) -> bool:
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
            ("art", "par", "inc", "XXaliXX", "item"),
            ("art", "par", "ali"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_60(cls, segments: list[str]) -> bool:
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
            ("art", "par", "inc", "ALI", "item"),
            ("art", "par", "ali"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_61(cls, segments: list[str]) -> bool:
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
            ("art", "par", "inc", "ali", "XXitemXX"),
            ("art", "par", "ali"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_62(cls, segments: list[str]) -> bool:
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
            ("art", "par", "inc", "ali", "ITEM"),
            ("art", "par", "ali"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_63(cls, segments: list[str]) -> bool:
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
            ("XXartXX", "par", "ali"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_64(cls, segments: list[str]) -> bool:
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
            ("ART", "par", "ali"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_65(cls, segments: list[str]) -> bool:
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
            ("art", "XXparXX", "ali"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_66(cls, segments: list[str]) -> bool:
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
            ("art", "PAR", "ali"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_67(cls, segments: list[str]) -> bool:
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
            ("art", "par", "XXaliXX"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_68(cls, segments: list[str]) -> bool:
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
            ("art", "par", "ALI"),
            ("art", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_69(cls, segments: list[str]) -> bool:
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
            ("XXartXX", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_70(cls, segments: list[str]) -> bool:
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
            ("ART", "par", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_71(cls, segments: list[str]) -> bool:
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
            ("art", "XXparXX", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_72(cls, segments: list[str]) -> bool:
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
            ("art", "PAR", "ali", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_73(cls, segments: list[str]) -> bool:
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
            ("art", "par", "XXaliXX", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_74(cls, segments: list[str]) -> bool:
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
            ("art", "par", "ALI", "item"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_75(cls, segments: list[str]) -> bool:
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
            ("art", "par", "ali", "XXitemXX"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_76(cls, segments: list[str]) -> bool:
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
            ("art", "par", "ali", "ITEM"),
            ("art", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_77(cls, segments: list[str]) -> bool:
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
            ("XXartXX", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_78(cls, segments: list[str]) -> bool:
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
            ("ART", "inc"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_79(cls, segments: list[str]) -> bool:
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
            ("art", "XXincXX"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_80(cls, segments: list[str]) -> bool:
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
            ("art", "INC"),
            ("art", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_81(cls, segments: list[str]) -> bool:
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
            ("XXartXX", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_82(cls, segments: list[str]) -> bool:
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
            ("ART", "inc", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_83(cls, segments: list[str]) -> bool:
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
            ("art", "XXincXX", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_84(cls, segments: list[str]) -> bool:
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
            ("art", "INC", "ali"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_85(cls, segments: list[str]) -> bool:
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
            ("art", "inc", "XXaliXX"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_86(cls, segments: list[str]) -> bool:
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
            ("art", "inc", "ALI"),
            ("art", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_87(cls, segments: list[str]) -> bool:
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
            ("XXartXX", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_88(cls, segments: list[str]) -> bool:
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
            ("ART", "inc", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_89(cls, segments: list[str]) -> bool:
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
            ("art", "XXincXX", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_90(cls, segments: list[str]) -> bool:
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
            ("art", "INC", "ali", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_91(cls, segments: list[str]) -> bool:
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
            ("art", "inc", "XXaliXX", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_92(cls, segments: list[str]) -> bool:
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
            ("art", "inc", "ALI", "item"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_93(cls, segments: list[str]) -> bool:
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
            ("art", "inc", "ali", "XXitemXX"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_94(cls, segments: list[str]) -> bool:
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
            ("art", "inc", "ali", "ITEM"),
        }
        return tuple(types) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_95(cls, segments: list[str]) -> bool:
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
        return tuple(None) in allowed_sequences

    @classmethod
    def xǁCanonicalNodePathǁ_validate_segments__mutmut_96(cls, segments: list[str]) -> bool:
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
        return tuple(types) not in allowed_sequences

    @classmethod
    @_mutmut_mutated(mutants_xǁCanonicalNodePathǁfrom_string__mutmut, is_classmethod = True)
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

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_orig(cls, path_str: str) -> Self:
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

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_1(cls, path_str: str) -> Self:
        """Constructs and validates a CanonicalNodePath from a raw string.

        Args:
            path_str: The dot-separated address (e.g., 'art_3.inc_1').

        Returns:
            A validated CanonicalNodePath instance.

        Raises:
            InvalidCanonicalNodePathError: If path_str does not strictly conform
                to LC 95 hierarchical address grammar.
        """
        if not path_str or not isinstance(path_str, str) and not path_str.strip():
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

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_2(cls, path_str: str) -> Self:
        """Constructs and validates a CanonicalNodePath from a raw string.

        Args:
            path_str: The dot-separated address (e.g., 'art_3.inc_1').

        Returns:
            A validated CanonicalNodePath instance.

        Raises:
            InvalidCanonicalNodePathError: If path_str does not strictly conform
                to LC 95 hierarchical address grammar.
        """
        if not path_str and not isinstance(path_str, str) or not path_str.strip():
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

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_3(cls, path_str: str) -> Self:
        """Constructs and validates a CanonicalNodePath from a raw string.

        Args:
            path_str: The dot-separated address (e.g., 'art_3.inc_1').

        Returns:
            A validated CanonicalNodePath instance.

        Raises:
            InvalidCanonicalNodePathError: If path_str does not strictly conform
                to LC 95 hierarchical address grammar.
        """
        if path_str or not isinstance(path_str, str) or not path_str.strip():
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

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_4(cls, path_str: str) -> Self:
        """Constructs and validates a CanonicalNodePath from a raw string.

        Args:
            path_str: The dot-separated address (e.g., 'art_3.inc_1').

        Returns:
            A validated CanonicalNodePath instance.

        Raises:
            InvalidCanonicalNodePathError: If path_str does not strictly conform
                to LC 95 hierarchical address grammar.
        """
        if not path_str or isinstance(path_str, str) or not path_str.strip():
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

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_5(cls, path_str: str) -> Self:
        """Constructs and validates a CanonicalNodePath from a raw string.

        Args:
            path_str: The dot-separated address (e.g., 'art_3.inc_1').

        Returns:
            A validated CanonicalNodePath instance.

        Raises:
            InvalidCanonicalNodePathError: If path_str does not strictly conform
                to LC 95 hierarchical address grammar.
        """
        if not path_str or not isinstance(path_str, str) or path_str.strip():
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

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_6(cls, path_str: str) -> Self:
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
            raise InvalidCanonicalNodePathError(None)

        cleaned = path_str.strip()
        segments = cleaned.split(".")
        if not cls._validate_segments(segments):
            raise InvalidCanonicalNodePathError(
                f"Invalid canonical node path: '{cleaned}'. "
                "Must follow statutory provision hierarchy: "
                "'art_X[.par_Y|.par_unico][.inc_Z][.ali_W][.item_K]'."
            )

        return cls(value=cleaned)

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_7(cls, path_str: str) -> Self:
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
            raise InvalidCanonicalNodePathError("XXCanonical node path cannot be empty.XX")

        cleaned = path_str.strip()
        segments = cleaned.split(".")
        if not cls._validate_segments(segments):
            raise InvalidCanonicalNodePathError(
                f"Invalid canonical node path: '{cleaned}'. "
                "Must follow statutory provision hierarchy: "
                "'art_X[.par_Y|.par_unico][.inc_Z][.ali_W][.item_K]'."
            )

        return cls(value=cleaned)

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_8(cls, path_str: str) -> Self:
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
            raise InvalidCanonicalNodePathError("canonical node path cannot be empty.")

        cleaned = path_str.strip()
        segments = cleaned.split(".")
        if not cls._validate_segments(segments):
            raise InvalidCanonicalNodePathError(
                f"Invalid canonical node path: '{cleaned}'. "
                "Must follow statutory provision hierarchy: "
                "'art_X[.par_Y|.par_unico][.inc_Z][.ali_W][.item_K]'."
            )

        return cls(value=cleaned)

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_9(cls, path_str: str) -> Self:
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
            raise InvalidCanonicalNodePathError("CANONICAL NODE PATH CANNOT BE EMPTY.")

        cleaned = path_str.strip()
        segments = cleaned.split(".")
        if not cls._validate_segments(segments):
            raise InvalidCanonicalNodePathError(
                f"Invalid canonical node path: '{cleaned}'. "
                "Must follow statutory provision hierarchy: "
                "'art_X[.par_Y|.par_unico][.inc_Z][.ali_W][.item_K]'."
            )

        return cls(value=cleaned)

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_10(cls, path_str: str) -> Self:
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

        cleaned = None
        segments = cleaned.split(".")
        if not cls._validate_segments(segments):
            raise InvalidCanonicalNodePathError(
                f"Invalid canonical node path: '{cleaned}'. "
                "Must follow statutory provision hierarchy: "
                "'art_X[.par_Y|.par_unico][.inc_Z][.ali_W][.item_K]'."
            )

        return cls(value=cleaned)

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_11(cls, path_str: str) -> Self:
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
        segments = None
        if not cls._validate_segments(segments):
            raise InvalidCanonicalNodePathError(
                f"Invalid canonical node path: '{cleaned}'. "
                "Must follow statutory provision hierarchy: "
                "'art_X[.par_Y|.par_unico][.inc_Z][.ali_W][.item_K]'."
            )

        return cls(value=cleaned)

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_12(cls, path_str: str) -> Self:
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
        segments = cleaned.split(None)
        if not cls._validate_segments(segments):
            raise InvalidCanonicalNodePathError(
                f"Invalid canonical node path: '{cleaned}'. "
                "Must follow statutory provision hierarchy: "
                "'art_X[.par_Y|.par_unico][.inc_Z][.ali_W][.item_K]'."
            )

        return cls(value=cleaned)

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_13(cls, path_str: str) -> Self:
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
        segments = cleaned.split("XX.XX")
        if not cls._validate_segments(segments):
            raise InvalidCanonicalNodePathError(
                f"Invalid canonical node path: '{cleaned}'. "
                "Must follow statutory provision hierarchy: "
                "'art_X[.par_Y|.par_unico][.inc_Z][.ali_W][.item_K]'."
            )

        return cls(value=cleaned)

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_14(cls, path_str: str) -> Self:
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
        if cls._validate_segments(segments):
            raise InvalidCanonicalNodePathError(
                f"Invalid canonical node path: '{cleaned}'. "
                "Must follow statutory provision hierarchy: "
                "'art_X[.par_Y|.par_unico][.inc_Z][.ali_W][.item_K]'."
            )

        return cls(value=cleaned)

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_15(cls, path_str: str) -> Self:
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
        if not cls._validate_segments(None):
            raise InvalidCanonicalNodePathError(
                f"Invalid canonical node path: '{cleaned}'. "
                "Must follow statutory provision hierarchy: "
                "'art_X[.par_Y|.par_unico][.inc_Z][.ali_W][.item_K]'."
            )

        return cls(value=cleaned)

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_16(cls, path_str: str) -> Self:
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
                None
            )

        return cls(value=cleaned)

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_17(cls, path_str: str) -> Self:
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
                "XXMust follow statutory provision hierarchy: XX"
                "'art_X[.par_Y|.par_unico][.inc_Z][.ali_W][.item_K]'."
            )

        return cls(value=cleaned)

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_18(cls, path_str: str) -> Self:
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
                "must follow statutory provision hierarchy: "
                "'art_X[.par_Y|.par_unico][.inc_Z][.ali_W][.item_K]'."
            )

        return cls(value=cleaned)

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_19(cls, path_str: str) -> Self:
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
                "MUST FOLLOW STATUTORY PROVISION HIERARCHY: "
                "'art_X[.par_Y|.par_unico][.inc_Z][.ali_W][.item_K]'."
            )

        return cls(value=cleaned)

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_20(cls, path_str: str) -> Self:
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
                "XX'art_X[.par_Y|.par_unico][.inc_Z][.ali_W][.item_K]'.XX"
            )

        return cls(value=cleaned)

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_21(cls, path_str: str) -> Self:
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
                "'art_x[.par_y|.par_unico][.inc_z][.ali_w][.item_k]'."
            )

        return cls(value=cleaned)

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_22(cls, path_str: str) -> Self:
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
                "'ART_X[.PAR_Y|.PAR_UNICO][.INC_Z][.ALI_W][.ITEM_K]'."
            )

        return cls(value=cleaned)

    @classmethod
    def xǁCanonicalNodePathǁfrom_string__mutmut_23(cls, path_str: str) -> Self:
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

        return cls(value=None)

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

mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['_mutmut_orig'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_1'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_2'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_3'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_4'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_5'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_6'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_7'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_8'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_9'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_10'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_11'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_12'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_13'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_14'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_15'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_16'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_17'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_18'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_18 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_19'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_19 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_20'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_20 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_21'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_21 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_22'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_22 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_23'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_23 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_24'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_24 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_25'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_25 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_26'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_26 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_27'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_27 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_28'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_28 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_29'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_29 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_30'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_30 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_31'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_31 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_32'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_32 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_33'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_33 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_34'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_34 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_35'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_35 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_36'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_36 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_37'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_37 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_38'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_38 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_39'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_39 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_40'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_40 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_41'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_41 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_42'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_42 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_43'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_43 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_44'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_44 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_45'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_45 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_46'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_46 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_47'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_47 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_48'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_48 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_49'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_49 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_50'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_50 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_51'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_51 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_52'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_52 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_53'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_53 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_54'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_54 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_55'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_55 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_56'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_56 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_57'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_57 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_58'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_58 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_59'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_59 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_60'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_60 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_61'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_61 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_62'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_62 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_63'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_63 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_64'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_64 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_65'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_65 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_66'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_66 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_67'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_67 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_68'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_68 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_69'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_69 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_70'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_70 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_71'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_71 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_72'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_72 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_73'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_73 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_74'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_74 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_75'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_75 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_76'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_76 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_77'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_77 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_78'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_78 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_79'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_79 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_80'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_80 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_81'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_81 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_82'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_82 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_83'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_83 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_84'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_84 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_85'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_85 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_86'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_86 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_87'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_87 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_88'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_88 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_89'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_89 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_90'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_90 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_91'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_91 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_92'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_92 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_93'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_93 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_94'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_94 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_95'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_95 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁ_validate_segments__mutmut['xǁCanonicalNodePathǁ_validate_segments__mutmut_96'] = CanonicalNodePath.xǁCanonicalNodePathǁ_validate_segments__mutmut_96 # type: ignore # mutmut generated

mutants_xǁCanonicalNodePathǁfrom_string__mutmut['_mutmut_orig'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁfrom_string__mutmut['xǁCanonicalNodePathǁfrom_string__mutmut_1'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁfrom_string__mutmut['xǁCanonicalNodePathǁfrom_string__mutmut_2'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁfrom_string__mutmut['xǁCanonicalNodePathǁfrom_string__mutmut_3'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁfrom_string__mutmut['xǁCanonicalNodePathǁfrom_string__mutmut_4'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁfrom_string__mutmut['xǁCanonicalNodePathǁfrom_string__mutmut_5'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁfrom_string__mutmut['xǁCanonicalNodePathǁfrom_string__mutmut_6'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁfrom_string__mutmut['xǁCanonicalNodePathǁfrom_string__mutmut_7'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁfrom_string__mutmut['xǁCanonicalNodePathǁfrom_string__mutmut_8'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁfrom_string__mutmut['xǁCanonicalNodePathǁfrom_string__mutmut_9'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁfrom_string__mutmut['xǁCanonicalNodePathǁfrom_string__mutmut_10'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁfrom_string__mutmut['xǁCanonicalNodePathǁfrom_string__mutmut_11'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁfrom_string__mutmut['xǁCanonicalNodePathǁfrom_string__mutmut_12'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁfrom_string__mutmut['xǁCanonicalNodePathǁfrom_string__mutmut_13'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁfrom_string__mutmut['xǁCanonicalNodePathǁfrom_string__mutmut_14'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁfrom_string__mutmut['xǁCanonicalNodePathǁfrom_string__mutmut_15'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁfrom_string__mutmut['xǁCanonicalNodePathǁfrom_string__mutmut_16'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁfrom_string__mutmut['xǁCanonicalNodePathǁfrom_string__mutmut_17'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁfrom_string__mutmut['xǁCanonicalNodePathǁfrom_string__mutmut_18'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_18 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁfrom_string__mutmut['xǁCanonicalNodePathǁfrom_string__mutmut_19'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_19 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁfrom_string__mutmut['xǁCanonicalNodePathǁfrom_string__mutmut_20'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_20 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁfrom_string__mutmut['xǁCanonicalNodePathǁfrom_string__mutmut_21'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_21 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁfrom_string__mutmut['xǁCanonicalNodePathǁfrom_string__mutmut_22'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_22 # type: ignore # mutmut generated
mutants_xǁCanonicalNodePathǁfrom_string__mutmut['xǁCanonicalNodePathǁfrom_string__mutmut_23'] = CanonicalNodePath.xǁCanonicalNodePathǁfrom_string__mutmut_23 # type: ignore # mutmut generated
