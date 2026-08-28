"""Precision Unit Tests for Ingestion Value Objects.

Verifies construction-time invariants, validation boundaries, and exception mappings
specified in SPEC-001 (Section 2.1 & 5).
"""

import hashlib
from datetime import date, timedelta

import pytest

from lex.ingestion.domain.exceptions import (
    InvalidDocumentHashError,
    InvalidGazetteDateError,
    InvalidTerritoryCodeError,
)
from lex.ingestion.domain.value_objects import (
    DocumentHash,
    GazetteDate,
    TerritoryId,
)


class TestTerritoryId:
    """Acceptance tests for TerritoryId Value Object."""

    def test_valid_federal_code(self) -> None:
        """Scenario: Federal territory 'BR' is accepted."""
        territory = TerritoryId.from_code("BR")
        assert territory.code == "BR"

    @pytest.mark.parametrize("state_code", ["SP", "RJ", "MG", "RS", "BA", "DF", "AC", "TO"])
    def test_valid_state_codes(self, state_code: str) -> None:
        """Scenario: All 27 Brazilian state codes (uppercase) are accepted."""
        territory = TerritoryId.from_code(state_code)
        assert territory.code == state_code

    @pytest.mark.parametrize("ibge_code", ["3550308", "3304557", "3106200", "4314902", "5200050"])
    def test_valid_municipal_ibge_codes(self, ibge_code: str) -> None:
        """Scenario: Valid 7-digit numeric IBGE municipal codes are accepted."""
        territory = TerritoryId.from_code(ibge_code)
        assert territory.code == ibge_code

    def test_strip_whitespace(self) -> None:
        """Scenario: Leading/trailing whitespace is sanitized."""
        territory = TerritoryId.from_code("  SP  ")
        assert territory.code == "SP"

    def test_non_string_code_raises_exception(self) -> None:
        """Boundary condition: Non-string input raises InvalidTerritoryCodeError."""
        with pytest.raises(InvalidTerritoryCodeError, match="Territory code must be a string"):
            TerritoryId.from_code(123)  # type: ignore[arg-type]

    def test_empty_or_whitespace_code_raises_exception(self) -> None:
        """Boundary condition: Empty code raises specific error message."""
        with pytest.raises(InvalidTerritoryCodeError, match="cannot be empty or whitespace"):
            TerritoryId.from_code("   ")

    @pytest.mark.parametrize(
        "invalid_code",
        [
            "sp",  # Lowercase state code rejected
            "São Paulo",  # Full name rejected
            "XX",  # Non-existent state code rejected
            "123",  # 3 digits rejected
            "355030",  # 6 digits rejected (must be 7)
            "35503081",  # 8 digits rejected
            "BR12345",  # Alphanumeric rejected
            "None",
        ],
    )
    def test_invalid_codes_raise_exception(self, invalid_code: str) -> None:
        """Boundary condition: Invalid codes raise InvalidTerritoryCodeError."""
        with pytest.raises(InvalidTerritoryCodeError, match="Invalid Brazilian territory code"):
            TerritoryId.from_code(invalid_code)


class TestGazetteDate:
    """Acceptance tests for GazetteDate Value Object."""

    def test_non_date_raises_exception(self) -> None:
        """Boundary condition: Non-date input raises InvalidGazetteDateError."""
        with pytest.raises(InvalidGazetteDateError, match="Expected datetime.date"):
            GazetteDate.from_date("2024-01-01")  # type: ignore[arg-type]

    def test_valid_historical_and_modern_dates(self) -> None:
        """Scenario: Dates between 1808-09-10 and today are accepted."""
        first_date = GazetteDate.from_date(date(1808, 9, 10))
        assert first_date.value == date(1808, 9, 10)

        modern_date = GazetteDate.from_date(date(2024, 1, 2))
        assert modern_date.value == date(2024, 1, 2)

        today_date = GazetteDate.from_date(date.today())
        assert today_date.value == date.today()

    def test_pre_1808_date_raises_exception(self) -> None:
        """Boundary condition: Dates before first Brazilian gazette are rejected."""
        err_msg = "predates the first Brazilian official gazette"
        with pytest.raises(InvalidGazetteDateError, match=err_msg):
            GazetteDate.from_date(date(1808, 9, 9))

        with pytest.raises(InvalidGazetteDateError, match=err_msg):
            GazetteDate.from_date(date(1500, 4, 22))

    def test_future_date_raises_exception(self) -> None:
        """Boundary condition: Future dates strictly raise InvalidGazetteDateError."""
        tomorrow = date.today() + timedelta(days=1)
        with pytest.raises(InvalidGazetteDateError, match="cannot be in the future"):
            GazetteDate.from_date(tomorrow)


class TestDocumentHash:
    """Acceptance tests for DocumentHash Value Object."""

    def test_valid_hex_hash(self) -> None:
        """Scenario: Valid 64-character lowercase hexadecimal hash is accepted."""
        valid_hex = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        doc_hash = DocumentHash.from_hex(valid_hex)
        assert doc_hash.hex_digest == valid_hex

    def test_hash_computed_from_text(self) -> None:
        """Scenario: SHA-256 is correctly computed from UTF-8 text."""
        raw_text = "Hello LEX Brazilian Legislation Engine"
        expected = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()
        doc_hash = DocumentHash.from_text(raw_text)
        assert doc_hash.hex_digest == expected

    @pytest.mark.parametrize(
        "invalid_hash",
        [
            "",
            "12345",
            "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855",  # Uppercase
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b85z",  # 'z' non-hex
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b85",  # 63 chars
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b8555",  # 65 chars
            12345,  # Non-string
        ],
    )
    def test_invalid_hash_raises_exception(self, invalid_hash: object) -> None:
        """Boundary condition: Malformed hashes raise InvalidDocumentHashError."""
        with pytest.raises(InvalidDocumentHashError, match="Invalid SHA-256 hash"):
            DocumentHash.from_hex(invalid_hash)  # type: ignore[arg-type]
