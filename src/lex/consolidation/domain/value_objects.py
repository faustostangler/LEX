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

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"CanonicalUrn('{self.value}')"
