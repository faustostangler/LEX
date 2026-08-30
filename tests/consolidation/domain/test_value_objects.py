"""Unit tests for Consolidation Context Value Objects.

Tests CanonicalUrn (LexML/FRBR) parsing, building, and validation.
"""

import pytest

from lex.consolidation.domain.exceptions import InvalidCanonicalUrnError
from lex.consolidation.domain.value_objects import CanonicalUrn


class TestCanonicalUrn:
    """Test suite for CanonicalUrn (LexML / FRBR standard)."""

    @pytest.mark.parametrize(
        "valid_urn,expected_jurisdiction,expected_type,expected_number",
        [
            ("urn:lex:br:federal:lei:1993-06-21;8666", "federal", "lei", "8666"),
            ("urn:lex:br:federal:lei:1993;8666", "federal", "lei", "8666"),
            ("urn:lex:br:federal:lei.complementar:2006;123", "federal", "lei.complementar", "123"),
            ("urn:lex:br:federal:decreto.lei:1940;2848", "federal", "decreto.lei", "2848"),
            (
                "urn:lex:br:federal:medida.provisoria:2024;1200",
                "federal",
                "medida.provisoria",
                "1200",
            ),
            ("urn:lex:br:sp:lei:2015;15854", "sp", "lei", "15854"),
            ("urn:lex:br:rj:decreto:2020;47100", "rj", "decreto", "47100"),
        ],
    )
    def test_valid_canonical_urns(
        self,
        valid_urn: str,
        expected_jurisdiction: str,
        expected_type: str,
        expected_number: str,
    ) -> None:
        """Asserts parsing of valid LexML/FRBR URN strings."""
        urn = CanonicalUrn.from_string(valid_urn)
        assert urn.value == valid_urn
        assert urn.jurisdiction == expected_jurisdiction
        assert urn.normative_type == expected_type
        assert urn.number == expected_number
        assert str(urn) == valid_urn
        assert repr(urn) == f"CanonicalUrn('{valid_urn}')"

    @pytest.mark.parametrize(
        "invalid_urn",
        [
            "",
            "   ",
            "urn:lex:us:federal:lei:1993;8666",  # Not br
            "urn:lex:br:invalid_state:lei:1993;8666",  # Invalid state
            "urn:lex:br:federal:custom_species:1993;8666",
            "urn:lex:br:federal:lei:93;8666",  # 2-digit year
            "urn:lex:br:federal:lei:1993",  # Missing number
            "urn:lex:br:federal:lei:1993;",  # Empty number
            "https://leis.gov.br/123",
        ],
    )
    def test_invalid_canonical_urns(self, invalid_urn: str) -> None:
        """Asserts that malformed URNs raise InvalidCanonicalUrnError."""
        with pytest.raises(InvalidCanonicalUrnError):
            CanonicalUrn.from_string(invalid_urn)

    def test_build_canonical_urn(self) -> None:
        """Asserts building a CanonicalUrn from statutory natural metadata."""
        urn = CanonicalUrn.build(
            jurisdiction="BR",
            act_type="Lei Complementar",
            date_or_year=2000,
            number="101",
        )
        assert urn.value == "urn:lex:br:federal:lei.complementar:2000;101"
        assert urn.jurisdiction == "federal"
        assert urn.normative_type == "lei.complementar"

        urn_state = CanonicalUrn.build(
            jurisdiction="SP",
            act_type="Lei Ordinária",
            date_or_year="2015-05-10",
            number="15.854",
        )
        assert urn_state.value == "urn:lex:br:sp:lei:2015-05-10;15854"

    def test_immutability_and_equality(self) -> None:
        """Asserts value object hashability and equality."""
        u1 = CanonicalUrn.from_string("urn:lex:br:federal:lei:1993;8666")
        u2 = CanonicalUrn.from_string("urn:lex:br:federal:lei:1993;8666")
        u3 = CanonicalUrn.from_string("urn:lex:br:federal:lei:2021;14133")

        assert u1 == u2
        assert u1 != u3
        assert hash(u1) == hash(u2)
        assert len({u1, u2, u3}) == 2
