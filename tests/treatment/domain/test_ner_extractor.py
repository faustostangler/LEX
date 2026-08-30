"""Unit tests for Trilha B DeterministicNerExtractor.

Tests high-speed regex entity extraction for contracts, bidding notices, and procurement acts.
"""

from lex.treatment.domain.services.ner_extractor import DeterministicNerExtractor


class TestDeterministicNerExtractor:
    """Test suite for Fast-Path NER Extractor."""

    def test_extract_extrato_de_contrato_entities(self) -> None:
        """Asserts extraction of CNPJ, Process, Value, and Modality from contract notice."""
        extrato_text = """
        EXTRATO DE CONTRATO Nº 15/2024 - UASG 153010

        Nº Processo: 23067.012345/2024-89.
        Pregão Eletrônico Nº 04/2024.
        Contratante: UNIVERSIDADE FEDERAL DO RIO DE JANEIRO.
        CNPJ Contratado: 00.394.460/0058-87 - EMPRESA BRASILEIRA DE TECNOLOGIA LTDA.
        Objeto: Aquisição de equipamentos de rede e servidores de alto desempenho.
        Fundamento Legal: Lei 14.133/2021.
        Vigência: 01/06/2024 a 01/06/2025.
        Valor Total: R$ 1.450.000,00.
        Data de Assinatura: 28/05/2024.
        """

        entities = DeterministicNerExtractor.extract_entities(extrato_text)

        assert entities["cnpjs"] == ["00.394.460/0058-87"]
        assert entities["processos"] == ["23067.012345/2024-89"]
        assert entities["licitacao_modalidade"] == "Pregão Eletrônico"
        assert entities["licitacao_numero"] == "04/2024"
        assert entities["valor_total"] == 1450000.00
        assert entities["valor_formatado"] == "R$ 1.450.000,00"
        assert "Aquisição de equipamentos" in (entities.get("objeto") or "")
        assert entities["vigencia_inicio"] == "2024-06-01"
        assert entities["vigencia_fim"] == "2025-06-01"

    def test_extract_cpf_with_lgpd_masking(self) -> None:
        """Asserts that CPFs are identified and sanitized under LGPD requirements."""
        portaria_text = """
        PORTARIA Nº 120, DE 15 DE MARÇO DE 2024

        O SECRETÁRIO DE GESTÃO resolve:
        Nomear o servidor JOÃO DA SILVA, CPF nº 123.456.789-00, para exercer o cargo em comissão.
        """
        entities = DeterministicNerExtractor.extract_entities(portaria_text)
        assert entities["cpfs_masked"] == ["***.456.789-**"]
        assert entities["total_cpfs_found"] == 1

    def test_extract_dispensa_licitacao(self) -> None:
        """Asserts extraction of Dispensa de Licitação notice."""
        dispensa_text = """
        AVISO DE DISPENSA DE LICITAÇÃO Nº 10/2024

        Processo: 19995.001234/2024-11.
        Objeto: Contratação emergencial de serviços de manutenção predial.
        Valor Total: R$ 45.320,50.
        CNPJ: 11.222.333/0001-44.
        """
        entities = DeterministicNerExtractor.extract_entities(dispensa_text)
        assert entities["licitacao_modalidade"] == "Dispensa de Licitação"
        assert entities["licitacao_numero"] == "10/2024"
        assert entities["valor_total"] == 45320.50
        assert entities["cnpjs"] == ["11.222.333/0001-44"]
