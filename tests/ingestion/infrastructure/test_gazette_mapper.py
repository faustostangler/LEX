"""Precision Unit Tests for GazetteMapper ACL.

Verifies translation from RawGazettePayload and RawNormativeActPayload DTOs
to GazetteEdition and NormativeAct domain entities, including Kelsenian hierarchy
classification, LexML canonical URN generation, boundary conditions,
and section-based disambiguation.
"""

import uuid
from datetime import UTC, date, datetime

import pytest

from lex.ingestion.domain.entities import GazetteEdition, NormativeAct
from lex.ingestion.domain.exceptions import (
    CorruptedGazettePayloadError,
    InvalidGazetteDateError,
    InvalidTerritoryCodeError,
)
from lex.ingestion.domain.value_objects import (
    ClassificationSource,
    DocumentHash,
    FederativeTier,
    IngestionStatus,
)
from lex.ingestion.infrastructure.adapters.gazette_mapper import (
    GazetteMapper,
    generate_canonical_urn,
    resolve_hierarchy,
)
from lex.ingestion.infrastructure.dto import (
    RawGazettePayload,
    RawNormativeActPayload,
)
from lex.shared_kernel.value_objects import (
    HierarchicalGroup,
    HierarchicalRank,
    PublicationNature,
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
        assert mapper._extractor is extractor

        payload = RawGazettePayload(
            territory_code="BR",
            tier="federal",
            source_url="https://www.in.gov.br/dou/2024-01-02",
            raw_content="DOU secao_1 summary",
            raw_date_str="2024-01-02",
            edition_number="10-A",
            section="secao_1",
            is_extra_edition=True,
            power="legislative",
            total_acts=10,
            scraped_at=datetime(2024, 1, 2, 12, 0, 0, tzinfo=UTC),
        )

        edition = mapper.to_domain(payload)
        assert isinstance(edition, GazetteEdition)
        assert edition.territory_id.code == "BR"
        assert edition.tier == FederativeTier.FEDERAL
        assert edition.date.value == date(2024, 1, 2)
        assert edition.edition_number == "10-A"
        assert edition.section == "secao_1"
        assert edition.is_extra_edition is True
        assert edition.power == "legislative"
        assert edition.total_acts == 10
        assert edition.ingestion_status == IngestionStatus.COMPLETED
        assert edition.summary_hash == DocumentHash.from_text("DOU secao_1 summary")
        assert edition.scraped_at == datetime(2024, 1, 2, 12, 0, 0, tzinfo=UTC)

    def test_map_payload_with_none_raw_content_uses_fallback_summary(self) -> None:
        """Scenario: When raw_content is None, summary is constructed from metadata."""
        extractor = DummyExtractor()
        mapper = GazetteMapper(text_extractor=extractor)

        payload = RawGazettePayload(
            territory_code="BR",
            tier="federal",
            source_url="https://www.in.gov.br/dou/2024-01-02",
            raw_content=None,
            date_obj=date(2024, 1, 2),
            edition_number="5",
            section="secao_2",
            total_acts=15,
        )

        edition = mapper.to_domain(payload)
        expected_summary = "https://www.in.gov.br/dou/2024-01-02-15-5"
        assert edition.summary_hash == DocumentHash.from_text(expected_summary)
        assert edition.scraped_at is not None

    def test_map_valid_normative_act_payload(self) -> None:
        """Scenario: Map RawNormativeActPayload into a valid NormativeAct with hierarchy & URN."""
        extractor = DummyExtractor()
        mapper = GazetteMapper(text_extractor=extractor)
        edition_id = uuid.uuid4()

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
            edition_number="123",
            is_extra_edition=True,
            hierarchy=["Ministério da Fazenda", "Gabinete"],
            authority_name="Ministro",
            authority_role="Chefe",
            classification_source="pre_segmented_source",
            classification_confidence=0.99,
            metadata_json={"source": "scrapy"},
            scraped_at=datetime(2024, 1, 15, 12, 0, 0, tzinfo=UTC),
        )

        act = mapper.to_normative_act(payload, edition_id=edition_id)
        assert isinstance(act, NormativeAct)
        assert act.edition_id == edition_id
        assert act.territory_id.code == "BR"
        assert act.section == "secao_1"
        assert act.edition_number == "123"
        assert act.is_extra_edition is True
        assert act.act_type == "PORTARIA"
        assert act.act_number == "1"
        assert act.act_year == 2024
        assert act.title == "PORTARIA Nº 1, DE 15 DE JANEIRO DE 2024"
        assert act.hierarchy == ["Ministério da Fazenda", "Gabinete"]
        assert act.authority_name == "Ministro"
        assert act.authority_role == "Chefe"
        assert act.char_count == len("Art. 1º Fica instituído o comitê.")
        assert act.hierarchical_group == HierarchicalGroup.GRUPO_4_ORDINATORIO_MINISTERIAL
        assert act.hierarchical_rank == int(HierarchicalRank.PORTARIA_NORMATIVA)
        assert act.publication_nature == PublicationNature.NORMATIVA_ABSTRATA
        assert act.canonical_urn == "urn:lex:br:federal:portaria:2024;1"
        assert act.is_stub is False
        assert act.classification_source == ClassificationSource.PRE_SEGMENTED_SOURCE
        assert act.classification_confidence == 0.99
        assert act.metadata_json == {"source": "scrapy"}
        assert act.scraped_at == datetime(2024, 1, 15, 12, 0, 0, tzinfo=UTC)

    def test_map_normative_act_empty_raw_content_raises_corrupted(self) -> None:
        """Boundary condition: Empty or whitespace raw content in act payload raises error."""
        extractor = DummyExtractor()
        mapper = GazetteMapper(text_extractor=extractor)

        payload = RawNormativeActPayload(
            territory_code="BR",
            source_url="https://www.in.gov.br/web/dou/-/portaria-1",
            raw_content="   \n\t ",
            title="PORTARIA Nº 1",
            act_type="PORTARIA",
            act_number="1",
            act_year=2024,
            date_obj=date(2024, 1, 15),
        )

        with pytest.raises(
            CorruptedGazettePayloadError, match="Normative act raw_content cannot be empty."
        ):
            mapper.to_normative_act(payload)

    @pytest.mark.parametrize(
        ("act_type", "section", "expected_group", "expected_rank", "expected_nature"),
        [
            (
                "LEI COMPLEMENTAR",
                "secao_1",
                HierarchicalGroup.GRUPO_1_PRIMARIO,
                80,
                PublicationNature.NORMATIVA_ABSTRATA,
            ),
            (
                "LEI",
                "secao_1",
                HierarchicalGroup.GRUPO_1_PRIMARIO,
                70,
                PublicationNature.NORMATIVA_ABSTRATA,
            ),
            (
                "MEDIDA PROVISÓRIA",
                "secao_1",
                HierarchicalGroup.GRUPO_1_PRIMARIO,
                70,
                PublicationNature.NORMATIVA_ABSTRATA,
            ),
            (
                "DECRETO LEGISLATIVO",
                "secao_1",
                HierarchicalGroup.GRUPO_1_PRIMARIO,
                70,
                PublicationNature.NORMATIVA_ABSTRATA,
            ),
            (
                "DECRETO",
                "secao_1",
                HierarchicalGroup.GRUPO_2_EXECUTIVO,
                60,
                PublicationNature.NORMATIVA_ABSTRATA,
            ),
            (
                "RESOLUÇÃO",
                "secao_1",
                HierarchicalGroup.GRUPO_3_COLEGIADO_REGULATORIO,
                50,
                PublicationNature.REGULATORIA_SETORIAL,
            ),
            (
                "INSTRUÇÃO NORMATIVA",
                "secao_1",
                HierarchicalGroup.GRUPO_3_COLEGIADO_REGULATORIO,
                50,
                PublicationNature.REGULATORIA_SETORIAL,
            ),
            (
                "PORTARIA",
                "secao_1",
                HierarchicalGroup.GRUPO_4_ORDINATORIO_MINISTERIAL,
                40,
                PublicationNature.NORMATIVA_ABSTRATA,
            ),
            (
                "PORTARIA",
                "secao_2",
                HierarchicalGroup.GRUPO_4_ORDINATORIO_MINISTERIAL,
                40,
                PublicationNature.CONCRETA_INDIVIDUAL,
            ),
            (
                "DESPACHO DECISÓRIO",
                "secao_1",
                HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
                20,
                PublicationNature.CONCRETA_INDIVIDUAL,
            ),
            (
                "ALVARÁ",
                "secao_1",
                HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
                20,
                PublicationNature.CONCRETA_INDIVIDUAL,
            ),
            (
                "EDITAL DE LICITAÇÃO",
                "secao_3",
                HierarchicalGroup.GRUPO_6_EDITALICIO,
                10,
                PublicationNature.PUBLICIDADE_OPERACIONAL,
            ),
            (
                "CONTRATO",
                "secao_3",
                HierarchicalGroup.GRUPO_7_CONTRATUAL,
                10,
                PublicationNature.PUBLICIDADE_OPERACIONAL,
            ),
            (
                "EXTRATO DE CONTRATO",
                "secao_3",
                HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
                10,
                PublicationNature.PUBLICIDADE_OPERACIONAL,
            ),
            (
                "EXTRATO DE TERMO ADITIVO",
                "secao_3",
                HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
                10,
                PublicationNature.PUBLICIDADE_OPERACIONAL,
            ),
            (
                "AVISO DE LICITAÇÃO PREGÃO ELETRÔNICO",
                "secao_3",
                HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
                10,
                PublicationNature.PUBLICIDADE_OPERACIONAL,
            ),
            (
                "RESULTADO DE JULGAMENTO",
                "secao_3",
                HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
                10,
                PublicationNature.PUBLICIDADE_OPERACIONAL,
            ),
            (
                "RETIFICAÇÃO",
                "secao_1",
                HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
                10,
                PublicationNature.PUBLICIDADE_OPERACIONAL,
            ),
            (
                "DOCUMENTO_DESCONHECIDO_XYZ",
                "secao_1",
                HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
                10,
                PublicationNature.PUBLICIDADE_OPERACIONAL,
            ),
        ],
    )
    def test_resolve_hierarchy_precedence(
        self,
        act_type: str,
        section: str,
        expected_group: HierarchicalGroup,
        expected_rank: int,
        expected_nature: PublicationNature,
    ) -> None:
        """Scenario: Resolve hierarchy verifies top-down precedence and fallback to Group 8."""
        group, rank, nature = resolve_hierarchy(act_type, section)
        assert group == expected_group
        assert rank == expected_rank
        assert nature == expected_nature

    def test_generate_canonical_urn_standard(self) -> None:
        """Scenario: Standard act number and year produces structured URN."""
        urn = generate_canonical_urn("BR", "LEI COMPLEMENTAR", "195", 2022, date(2022, 7, 8))
        assert urn == "urn:lex:br:federal:lei.complementar:2022;195"

    def test_generate_canonical_urn_with_symbols_and_slashes(self) -> None:
        """Scenario: Act type and number with symbols and surrounding dots are cleanly slugified."""
        urn = generate_canonical_urn(
            "BR",
            "...PORTARIA CONJUNTA...",
            "100/2024-A",
            2024,
            date(2024, 1, 15),
        )
        assert urn == "urn:lex:br:federal:portaria.conjunta:2024;1002024-A"

    def test_generate_canonical_urn_empty_or_symbol_type_defaults_to_ato(self) -> None:
        """Scenario: When act_type has no alphanumeric chars, defaults to 'ato'."""
        urn = generate_canonical_urn("BR", "---", "50", 2024, date(2024, 1, 15))
        assert urn == "urn:lex:br:federal:ato:2024;50"

    def test_generate_canonical_urn_missing_number_or_invalid_year_uses_content_hash(self) -> None:
        """Scenario: Missing act_number or historical year <= 1800 falls back to date + hash."""
        urn_no_num = generate_canonical_urn(
            "BR",
            "EXTRATO DE CONTRATO",
            None,
            2024,
            date(2024, 1, 15),
            content_hash="0123456789abcdef0123456789abcdef",
        )
        assert urn_no_num == "urn:lex:br:federal:extrato.de.contrato:2024-01-15;0123456789abcdef"

        urn_old_year = generate_canonical_urn(
            "BR",
            "DECRETO",
            "1",
            1700,
            date(1700, 1, 1),
            content_hash="fedcba9876543210fedcba9876543210",
        )
        assert urn_old_year == "urn:lex:br:federal:decreto:1700-01-01;fedcba9876543210"

    def test_generate_canonical_urn_missing_hash_uses_uuid_slice(self) -> None:
        """Scenario: When content_hash is None, uses 8-char random UUID fallback."""
        urn = generate_canonical_urn(
            "BR", "AVISO", None, None, date(2024, 1, 15), content_hash=None
        )
        prefix = "urn:lex:br:federal:aviso:2024-01-15;"
        assert urn.startswith(prefix)
        suffix = urn.removeprefix(prefix)
        assert len(suffix) == 8

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
            raw_date_str="2024-02-30",
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
