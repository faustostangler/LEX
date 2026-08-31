"""Unit tests for Treatment Application Use Cases and Dual-Track Routing.

Tests ProcessNormativeActUseCase with pure in-memory test double repository.
"""

import uuid
from datetime import date, datetime
from typing import Any
from uuid import UUID

import pytest

from lex.ingestion.domain.entities import NormativeAct
from lex.ingestion.domain.value_objects import (
    DocumentHash,
    GazetteDate,
    TerritoryId,
)
from lex.shared_kernel.value_objects import (
    HierarchicalGroup,
    PublicationNature,
)
from lex.treatment.application.ports import TreatmentRepositoryPort
from lex.treatment.application.use_cases import ProcessNormativeActUseCase
from lex.treatment.domain.entities import NormativeActMutation


class InMemoryTreatmentRepository(TreatmentRepositoryPort):
    """Pure in-memory test double implementing TreatmentRepositoryPort."""

    def __init__(self) -> None:
        self.saved_mutations: list[NormativeActMutation] = []
        self.treatment_updates: dict[UUID, dict[str, Any]] = {}

    async def save_mutations(
        self, mutations: list[NormativeActMutation], auto_commit: bool = True
    ) -> None:
        self.saved_mutations.extend(mutations)

    async def update_normative_act_treatment(
        self,
        act_id: UUID,
        structured_content: dict[str, Any] | None,
        metadata_json: dict[str, Any] | None,
        auto_commit: bool = True,
    ) -> None:
        self.treatment_updates[act_id] = {
            "structured_content": structured_content,
            "metadata_json": metadata_json,
        }


class TestProcessNormativeActUseCase:
    """Test suite for Dual-Track ProcessNormativeActUseCase."""

    @pytest.mark.anyio
    async def test_route_trilha_a_normative_act(self) -> None:
        """Asserts that general normative acts route to AST segmentation and mutation extraction."""
        repo = InMemoryTreatmentRepository()
        use_case = ProcessNormativeActUseCase(repository=repo)

        act_id = uuid.uuid4()
        edition_id = uuid.uuid4()
        raw_text = """
        Art. 1º A Lei nº 10.000, de 2010, passa a vigorar com as seguintes alterações:
        "Art. 3º ............................................................................
        I - legalidade e eficiência; (NR)"
        """
        act = NormativeAct(
            id=act_id,
            edition_id=edition_id,
            territory_id=TerritoryId.from_code("BR"),
            date=GazetteDate.from_date(date(2024, 1, 15)),
            act_type="LEI",
            act_number="12000",
            act_year=2024,
            title="Lei nº 12.000/2024",
            source_url="https://www.in.gov.br/dou/-/lei-12000",
            content_hash=DocumentHash.from_text(raw_text),
            char_count=len(raw_text.strip()),
            raw_content=raw_text,
            hierarchical_group=HierarchicalGroup.GRUPO_1_PRIMARIO,
            hierarchical_rank=70,
            publication_nature=PublicationNature.NORMATIVA_ABSTRATA,
            scraped_at=datetime(2024, 1, 15, 12, 0, 0),
        )

        result = await use_case.execute(act)

        assert result.track == "TRILHA_A"
        assert result.mutations_extracted == 1
        assert act_id in repo.treatment_updates
        assert repo.treatment_updates[act_id]["structured_content"] is not None
        assert len(repo.saved_mutations) == 1

    @pytest.mark.anyio
    async def test_route_trilha_b_operational_act(self) -> None:
        """Asserts that operational notices route to Fast-Path NER without AST overhead."""
        repo = InMemoryTreatmentRepository()
        use_case = ProcessNormativeActUseCase(repository=repo)

        act_id = uuid.uuid4()
        edition_id = uuid.uuid4()
        raw_text = """
        EXTRATO DE CONTRATO Nº 50/2024
        Processo: 12345.001/2024-99.
        CNPJ: 00.111.222/0001-33.
        Valor Total: R$ 500.000,00.
        """
        act = NormativeAct(
            id=act_id,
            edition_id=edition_id,
            territory_id=TerritoryId.from_code("BR"),
            date=GazetteDate.from_date(date(2024, 1, 15)),
            act_type="EXTRATO DE CONTRATO",
            title="Extrato de Contrato nº 50/2024",
            source_url="https://www.in.gov.br/dou/-/extrato-50",
            content_hash=DocumentHash.from_text(raw_text),
            char_count=len(raw_text.strip()),
            raw_content=raw_text,
            hierarchical_group=HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
            hierarchical_rank=10,
            publication_nature=PublicationNature.PUBLICIDADE_OPERACIONAL,
            scraped_at=datetime(2024, 1, 15, 12, 0, 0),
        )

        result = await use_case.execute(act)

        assert result.track == "TRILHA_B"
        assert result.mutations_extracted == 0
        assert act_id in repo.treatment_updates
        assert repo.treatment_updates[act_id]["structured_content"] is None
        meta = repo.treatment_updates[act_id]["metadata_json"]
        assert meta["cnpjs"] == ["00.111.222/0001-33"]
        assert meta["valor_total"] == 500000.00
        assert meta["triage_status"] == "EXTRACTED"
        assert meta["needs_manual_review"] is False

    @pytest.mark.anyio
    async def test_route_trilha_b_personnel_act(self) -> None:
        """Asserts that concrete individual personnel acts route to Trilha B."""
        repo = InMemoryTreatmentRepository()
        use_case = ProcessNormativeActUseCase(repository=repo)

        act_id = uuid.uuid4()
        edition_id = uuid.uuid4()
        raw_text = """
        PORTARIA Nº 994/2026
        DESIGNAR o servidor RICARDO ANDRE HOLLAS (88781)
        para exercer o cargo em comissão de ASSESSOR-CHEFE-CJ3.
        """
        act = NormativeAct(
            id=act_id,
            edition_id=edition_id,
            territory_id=TerritoryId.from_code("BR"),
            date=GazetteDate.from_date(date(2026, 5, 13)),
            act_type="PORTARIA",
            title="Portaria nº 994/2026",
            source_url="https://www.in.gov.br/dou/-/portaria-994",
            content_hash=DocumentHash.from_text(raw_text),
            char_count=len(raw_text.strip()),
            raw_content=raw_text,
            hierarchical_group=HierarchicalGroup.GRUPO_4_ORDINATORIO_MINISTERIAL,
            hierarchical_rank=40,
            publication_nature=PublicationNature.CONCRETA_INDIVIDUAL,
            scraped_at=datetime(2026, 5, 13, 12, 0, 0),
        )

        result = await use_case.execute(act)

        assert result.track == "TRILHA_B"
        assert result.mutations_extracted == 0
        assert act_id in repo.treatment_updates
        meta = repo.treatment_updates[act_id]["metadata_json"]
        assert meta is not None
        assert meta["tipo_ato_pessoal"] == "DESIGNACAO"
        assert meta["servidor_nome"] == "RICARDO ANDRE HOLLAS"
        assert meta["servidor_matricula"] == "88781"
        assert meta["triage_status"] == "EXTRACTED"
        assert meta["needs_manual_review"] is False
