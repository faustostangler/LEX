"""Precision Unit Tests for GazetteMapper ACL.

Verifies translation from RawGazettePayload and RawNormativeActPayload DTOs
to GazetteEdition and NormativeAct domain entities.
"""

from datetime import UTC, date, datetime

import pytest

from lex.ingestion.domain.entities import GazetteEdition, NormativeAct
from lex.ingestion.domain.exceptions import (
    CorruptedGazettePayloadError,
    InvalidGazetteDateError,
    InvalidTerritoryCodeError,
)
from lex.ingestion.domain.value_objects import FederativeTier
from lex.ingestion.infrastructure.adapters.gazette_mapper import GazetteMapper
from lex.ingestion.infrastructure.dto import (
    RawGazettePayload,
    RawNormativeActPayload,
)


class DummyExtractor:
    """In-memory test double for StreamTextExtractorPort."""

    def __init__(self, return_text: str = "EXTRACTED GAZETTE TEXT") -> None:
        self.return_text = return_text
        self.called_with: bytes | None = None

    def extract_text(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        self.called_with = stream_bytes
        if not stream_bytes:
            raise CorruptedGazettePayloadError("Empty byte stream")
        return self.return_text


class TestGazetteMapper:
    """Acceptance tests for GazetteMapper Anti-Corruption Layer."""

    def test_map_valid_payload_with_raw_text(self) -> None:
        """Scenario: Map raw text payload into a valid GazetteEdition."""
        extractor = DummyExtractor()
        mapper = GazetteMapper(text_extractor=extractor)

        payload = RawGazettePayload(
            territory_code="BR",
            tier="federal",
            source_url="https://www.in.gov.br/dou/2024-01-02",
            raw_content="DOU secao_1 summary",
            raw_date_str="2024-01-02",
            edition_number="1",
            section="secao_1",
            is_extra_edition=False,
            power="executive",
            total_acts=10,
            scraped_at=datetime(2024, 1, 2, 12, 0, 0, tzinfo=UTC),
        )

        edition = mapper.to_domain(payload)
        assert isinstance(edition, GazetteEdition)
        assert edition.territory_id.code == "BR"
        assert edition.tier == FederativeTier.FEDERAL
        assert edition.date.value == date(2024, 1, 2)
        assert edition.total_acts == 10

    def test_map_valid_normative_act_payload(self) -> None:
        """Scenario: Map RawNormativeActPayload into a valid NormativeAct domain entity."""
        extractor = DummyExtractor()
        mapper = GazetteMapper(text_extractor=extractor)

        payload = RawNormativeActPayload(
            territory_code="BR",
            source_url="https://www.in.gov.br/web/dou/-/portaria-1",
            raw_content="Art. 1º Fica instituído o comitê.",
            title="PORTARIA Nº 1, DE 15 DE JANEIRO DE 2024",
            act_type="PORTARIA",
            act_number="1",
            act_year=2024,
            date_obj=date(2024, 1, 15),
            section="secao_1",
            hierarchy=["Ministério da Fazenda", "Gabinete"],
        )

        act = mapper.to_normative_act(payload)
        assert isinstance(act, NormativeAct)
        assert act.territory_id.code == "BR"
        assert act.act_type == "PORTARIA"
        assert act.act_number == "1"
        assert act.act_year == 2024
        assert act.hierarchy == ["Ministério da Fazenda", "Gabinete"]
        assert act.char_count == len("Art. 1º Fica instituído o comitê.")

    @pytest.mark.parametrize(
        ("date_str", "expected_date"),
        [
            ("2024-01-15", date(2024, 1, 15)),
            ("15/01/2024", date(2024, 1, 15)),
            ("15-01-2024", date(2024, 1, 15)),
        ],
    )
    def test_map_parses_various_date_formats(self, date_str: str, expected_date: date) -> None:
        """Scenario: Common Brazilian date formats are parsed successfully."""
        extractor = DummyExtractor(return_text="GAZETTE BODY")
        mapper = GazetteMapper(text_extractor=extractor)

        payload = RawGazettePayload(
            territory_code="MG",
            tier="state",
            source_url="https://doe.mg.gov.br",
            raw_content="GAZETTE BODY",
            raw_date_str=date_str,
        )

        edition = mapper.to_domain(payload)
        assert edition.date.value == expected_date

    def test_map_iso_regex_with_invalid_calendar_date_raises(self) -> None:
        """Boundary condition: ISO matching date that is chronologically invalid raises error."""
        extractor = DummyExtractor(return_text="GAZETTE BODY")
        mapper = GazetteMapper(text_extractor=extractor)

        payload = RawGazettePayload(
            territory_code="BR",
            tier="federal",
            source_url="https://www.in.gov.br",
            raw_content="GAZETTE BODY",
            raw_date_str="2024-02-30",  # Feb 30 does not exist
        )

        with pytest.raises(InvalidGazetteDateError, match="Unable to parse date string"):
            mapper.to_domain(payload)

    def test_map_missing_both_date_fields_raises_exception(self) -> None:
        """Boundary condition: Missing date_obj and raw_date_str raises InvalidGazetteDateError."""
        extractor = DummyExtractor()
        mapper = GazetteMapper(text_extractor=extractor)

        payload = RawGazettePayload(
            territory_code="BR",
            tier="federal",
            source_url="https://www.in.gov.br",
            raw_content="SOME CONTENT",
            raw_date_str=None,
            date_obj=None,
        )

        with pytest.raises(InvalidGazetteDateError, match="No publication date provided"):
            mapper.to_domain(payload)

    def test_map_unparseable_date_str_raises_exception(self) -> None:
        """Boundary condition: Unparseable date string raises InvalidGazetteDateError."""
        extractor = DummyExtractor()
        mapper = GazetteMapper(text_extractor=extractor)

        payload = RawGazettePayload(
            territory_code="BR",
            tier="federal",
            source_url="https://www.in.gov.br",
            raw_content="SOME CONTENT",
            raw_date_str="invalid-date-string",
        )

        with pytest.raises(InvalidGazetteDateError, match="Unable to parse date string"):
            mapper.to_domain(payload)

    def test_map_invalid_territory_code_raises_exception(self) -> None:
        """Boundary condition: Invalid territory code in DTO raises InvalidTerritoryCodeError."""
        extractor = DummyExtractor()
        mapper = GazetteMapper(text_extractor=extractor)

        payload = RawGazettePayload(
            territory_code="INVALID_UF",
            tier="state",
            source_url="https://doe.invalid.gov.br",
            raw_content="SOME CONTENT",
            date_obj=date(2024, 1, 1),
        )

        with pytest.raises(InvalidTerritoryCodeError):
            mapper.to_domain(payload)
