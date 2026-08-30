"""Value Objects for the Consolidation Bounded Context.

Implements CanonicalUrn conforming to the LexML / FRBR Uniform Resource Name standard.
"""

import re
from typing import Self

from pydantic import BaseModel, ConfigDict

from lex.consolidation.domain.exceptions import InvalidCanonicalUrnError

# Canonical LexML URN Regex:
# urn:lex:br:<jurisdiction>:<species>:<date_or_year>;<number>
RE_CANONICAL_URN = re.compile(
    r"^urn:lex:br:(federal|[a-z]{2}):"
    r"(lei|lei\.complementar|decreto|decreto\.lei|medida\.provisoria|portaria|resolucao):"
    r"([0-9]{4}(?:-[0-9]{2}-[0-9]{2})?);"
    r"([0-9a-z\.\-]+)$"
)

VALID_STATE_CODES = {
    "ac",
    "al",
    "ap",
    "am",
    "ba",
    "ce",
    "df",
    "es",
    "go",
    "ma",
    "mt",
    "ms",
    "mg",
    "pa",
    "pb",
    "pr",
    "pe",
    "pi",
    "rj",
    "rn",
    "rs",
    "ro",
    "rr",
    "sc",
    "sp",
    "se",
    "to",
}

TYPE_MAP: dict[str, str] = {
    "lei": "lei",
    "lei ordinária": "lei",
    "lei ordinaria": "lei",
    "lei complementar": "lei.complementar",
    "decreto": "decreto",
    "decreto-lei": "decreto.lei",
    "decreto lei": "decreto.lei",
    "medida provisória": "medida.provisoria",
    "medida provisoria": "medida.provisoria",
    "portaria": "portaria",
    "resolução": "resolucao",
    "resolucao": "resolucao",
}


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁCanonicalUrnǁfrom_string__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCanonicalUrnǁbuild__mutmut: MutantDict = {}  # type: ignore


class CanonicalUrn(BaseModel):
    """Immutable Value Object representing a LexML / FRBR Canonical Uniform Resource Name.

    Examples:
        - `urn:lex:br:federal:lei:1993-06-21;8666`
        - `urn:lex:br:federal:lei:1993;8666`
        - `urn:lex:br:sp:lei:2015;15854`
    """

    model_config = ConfigDict(frozen=True)

    value: str
    jurisdiction: str
    normative_type: str
    date_or_year: str
    number: str

    @classmethod
    @_mutmut_mutated(mutants_xǁCanonicalUrnǁfrom_string__mutmut, is_classmethod = True)
    def from_string(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_orig(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_1(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) and not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_2(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str and not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_3(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_4(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_5(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_6(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError(None)

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_7(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("XXCanonical URN cannot be empty.XX")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_8(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("canonical urn cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_9(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("CANONICAL URN CANNOT BE EMPTY.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_10(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = None
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_11(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = None
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_12(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(None)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_13(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_14(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                None
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_15(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "XXMust follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'.XX"
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_16(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "must follow 'urn:lex:br:<federal|uf>:<species>:<yyyy[-mm-dd]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_17(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "MUST FOLLOW 'URN:LEX:BR:<FEDERAL|UF>:<SPECIES>:<YYYY[-MM-DD]>;<NUMBER>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_18(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = None
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_19(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).upper()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_20(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(None).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_21(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(2).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_22(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" or jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_23(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction == "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_24(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "XXfederalXX" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_25(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "FEDERAL" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_26(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_27(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                None
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_28(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "XXMust be 'federal' or a valid 2-letter state code.XX"
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_29(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_30(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "MUST BE 'FEDERAL' OR A VALID 2-LETTER STATE CODE."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_31(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = None
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_32(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).upper()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_33(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(None).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_34(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(3).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_35(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = None
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_36(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(None)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_37(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(4)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_38(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = None

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_39(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(None)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_40(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(5)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_41(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=None,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_42(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=None,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_43(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=None,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_44(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=None,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_45(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=None,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_46(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_47(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            normative_type=normative_type,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_48(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            date_or_year=date_or_year,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_49(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            number=number,
        )

    @classmethod
    def xǁCanonicalUrnǁfrom_string__mutmut_50(cls, urn_str: str) -> Self:
        """Parses and validates a canonical LexML URN string.

        Args:
            urn_str: The raw URN string.

        Returns:
            A validated CanonicalUrn instance.

        Raises:
            InvalidCanonicalUrnError: If the URN does not strictly adhere to
                LexML/FRBR Brazilian legal standards.
        """
        if not urn_str or not isinstance(urn_str, str) or not urn_str.strip():
            raise InvalidCanonicalUrnError("Canonical URN cannot be empty.")

        cleaned = urn_str.strip()
        m = RE_CANONICAL_URN.match(cleaned)
        if not m:
            raise InvalidCanonicalUrnError(
                f"Invalid Canonical URN: '{cleaned}'. "
                "Must follow 'urn:lex:br:<federal|uf>:<species>:<YYYY[-MM-DD]>;<number>'."
            )

        jurisdiction = m.group(1).lower()
        if jurisdiction != "federal" and jurisdiction not in VALID_STATE_CODES:
            raise InvalidCanonicalUrnError(
                f"Invalid jurisdiction '{jurisdiction}' in URN. "
                "Must be 'federal' or a valid 2-letter state code."
            )

        normative_type = m.group(2).lower()
        date_or_year = m.group(3)
        number = m.group(4)

        return cls(
            value=cleaned,
            jurisdiction=jurisdiction,
            normative_type=normative_type,
            date_or_year=date_or_year,
            )

    @classmethod
    @_mutmut_mutated(mutants_xǁCanonicalUrnǁbuild__mutmut, is_classmethod = True)
    def build(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_orig(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_1(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = None
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_2(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "XXfederalXX" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_3(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "FEDERAL" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_4(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.lower() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_5(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() != "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_6(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "XXBRXX" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_7(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "br" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_8(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.upper().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_9(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = None
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_10(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            None,
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_11(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            None,
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_12(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_13(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_14(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.upper().strip(),
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_15(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(None, ".").strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_16(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", None).strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_17(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(".").strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_18(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", ).strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_19(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.upper().replace(" ", ".").strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_20(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace("XX XX", ".").strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_21(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", "XX.XX").strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_22(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = None
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_23(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = number.replace(None, "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_24(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = number.replace(".", None).strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_25(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = number.replace("").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_26(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = number.replace(".", ).strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_27(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = number.replace("XX.XX", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_28(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = number.replace(".", "XXXX").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_29(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = None

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_30(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(None).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_31(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = None
        return cls.from_string(urn_string)

    @classmethod
    def xǁCanonicalUrnǁbuild__mutmut_32(
        cls,
        jurisdiction: str,
        act_type: str,
        date_or_year: str | int,
        number: str,
    ) -> Self:
        """Constructs a CanonicalUrn from natural metadata components.

        Args:
            jurisdiction: 'BR', 'federal', or 2-letter state code (e.g. 'SP').
            act_type: Natural type string (e.g. 'Lei Complementar').
            date_or_year: Year integer or ISO date string (YYYY or YYYY-MM-DD).
            number: Act number (e.g. '8666' or '15.854').

        Returns:
            A validated CanonicalUrn.
        """
        jur = "federal" if jurisdiction.upper() == "BR" else jurisdiction.lower().strip()
        norm_type = TYPE_MAP.get(
            act_type.lower().strip(),
            act_type.lower().replace(" ", ".").strip(),
        )
        clean_num = number.replace(".", "").strip()
        clean_date = str(date_or_year).strip()

        urn_string = f"urn:lex:br:{jur}:{norm_type}:{clean_date};{clean_num}"
        return cls.from_string(None)

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"CanonicalUrn('{self.value}')"

mutants_xǁCanonicalUrnǁfrom_string__mutmut['_mutmut_orig'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_1'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_2'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_3'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_4'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_5'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_6'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_7'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_8'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_9'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_10'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_11'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_12'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_13'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_14'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_15'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_16'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_17'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_18'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_18 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_19'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_19 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_20'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_20 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_21'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_21 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_22'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_22 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_23'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_23 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_24'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_24 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_25'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_25 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_26'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_26 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_27'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_27 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_28'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_28 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_29'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_29 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_30'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_30 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_31'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_31 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_32'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_32 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_33'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_33 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_34'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_34 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_35'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_35 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_36'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_36 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_37'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_37 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_38'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_38 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_39'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_39 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_40'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_40 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_41'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_41 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_42'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_42 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_43'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_43 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_44'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_44 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_45'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_45 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_46'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_46 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_47'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_47 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_48'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_48 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_49'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_49 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁfrom_string__mutmut['xǁCanonicalUrnǁfrom_string__mutmut_50'] = CanonicalUrn.xǁCanonicalUrnǁfrom_string__mutmut_50 # type: ignore # mutmut generated

mutants_xǁCanonicalUrnǁbuild__mutmut['_mutmut_orig'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_1'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_2'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_3'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_4'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_5'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_6'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_7'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_8'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_9'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_10'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_11'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_12'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_13'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_14'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_15'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_16'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_17'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_18'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_18 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_19'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_19 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_20'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_20 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_21'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_21 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_22'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_22 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_23'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_23 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_24'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_24 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_25'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_25 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_26'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_26 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_27'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_27 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_28'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_28 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_29'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_29 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_30'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_30 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_31'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_31 # type: ignore # mutmut generated
mutants_xǁCanonicalUrnǁbuild__mutmut['xǁCanonicalUrnǁbuild__mutmut_32'] = CanonicalUrn.xǁCanonicalUrnǁbuild__mutmut_32 # type: ignore # mutmut generated
