"""Comprehensive Unit Tests for Trilha B DeterministicNerExtractor.

Exercises high-speed regex entity extraction for contracts, bidding notices,
personnel acts, monetary parsing, LGPD masking, and triage classification.
Guarantees 100% branch coverage and mutant elimination.
"""

from lex.treatment.domain.services.ner_extractor import (
    DeterministicNerExtractor,
    _mask_cpf,
    _parse_currency,
    _parse_date,
)


class TestDeterministicNerExtractor:
    """Test suite for Fast-Path NER Extractor."""

    def test_mask_cpf_variations(self) -> None:
        """Verifies LGPD masking on standard and non-standard CPF strings."""
        assert _mask_cpf("123.456.789-00") == "***.456.789-**"
        assert _mask_cpf("123456789-00") == "***.***.***-**"
        assert _mask_cpf("invalid-cpf") == "***.***.***-**"
        assert _mask_cpf("123.456.789.00") == "***.***.***-**"

    def test_parse_currency_variations(self) -> None:
        """Verifies monetary string parsing and error handling."""
        assert _parse_currency("R$ 1.450.000,50") == 1450000.50
        assert _parse_currency("R$ 100,00") == 100.00
        assert _parse_currency(" 500,25 ") == 500.25
        assert _parse_currency("0,00") == 0.0
        assert _parse_currency("invalid") is None
        assert _parse_currency("") is None

    def test_parse_date_variations(self) -> None:
        """Verifies DD/MM/YYYY to ISO conversion."""
        assert _parse_date("15/03/2024") == "2024-03-15"
        assert _parse_date("01/01/2025") == "2025-01-01"
        assert _parse_date("31/12/2023") == "2023-12-31"
        assert _parse_date("32/01/2024") is None
        assert _parse_date("invalid") is None
        assert _parse_date("") is None

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
        assert (
            entities["objeto"]
            == "Aquisição de equipamentos de rede e servidores de alto desempenho"
        )
        assert entities["vigencia_inicio"] == "2024-06-01"
        assert entities["vigencia_fim"] == "2025-06-01"
        assert entities["triage_status"] == "EXTRACTED"
        assert entities["needs_manual_review"] is False

    def test_extract_processo_filtering_by_length(self) -> None:
        """Verifies processes under 5 characters are filtered out and deduplication works."""
        text = "Processo: 1234. Processo: 12345. Processo: 12345. PA nº 98765/2024."
        entities = DeterministicNerExtractor.extract_entities(text)
        assert entities["processos"] == ["12345", "98765/2024"]

    def test_extract_bidding_modalities_coverage(self) -> None:
        """Tests all bidding modality regex branches with and without accents."""
        cases = [
            ("PREGÃO ELETRÔNICO Nº 1/2024", "Pregão Eletrônico", "1/2024"),
            ("pregao eletronico 2/2024", "Pregão Eletrônico", "2/2024"),
            ("Pregão Presencial Nº 3/2024", "Pregão Presencial", "3/2024"),
            ("pregao presencial 4/2024", "Pregão Presencial", "4/2024"),
            ("Dispensa de Licitação Nº 5/2024", "Dispensa de Licitação", "5/2024"),
            ("Inexigibilidade de Licitação Nº 6/2024", "Inexigibilidade de Licitação", "6/2024"),
            ("Concorrência Nº 7/2024", "Concorrência", "7/2024"),
            ("concorrencia 8/2024", "Concorrência", "8/2024"),
            ("Tomada de Preços Nº 9/2024", "Tomada de Preços", "9/2024"),
            ("tomada de precos 10/2024", "Tomada de Preços", "10/2024"),
            ("Leilão Nº 11/2024", "Leilão", "11/2024"),
            ("leilao 12/2024", "Leilão", "12/2024"),
            ("Convite Nº 13/2024", "Convite", "13/2024"),
        ]
        for snippet, expected_mod, expected_num in cases:
            entities = DeterministicNerExtractor.extract_entities(snippet)
            assert entities["licitacao_modalidade"] == expected_mod
            assert entities["licitacao_numero"] == expected_num

    def test_extract_vigencia_invalid_dates_are_ignored(self) -> None:
        """Verifies that invalid dates in vigência string do not populate ISO fields."""
        text = "Vigência: 99/99/9999 até 88/88/8888"
        entities = DeterministicNerExtractor.extract_entities(text)
        assert "vigencia_inicio" not in entities
        assert "vigencia_fim" not in entities

    def test_extract_personnel_actions_coverage(self) -> None:
        """Tests all personnel action normalization branches."""
        actions = [
            ("CONCEDER APOSENTADORIA ao servidor JOAO SILVA, Siape 12345", "APOSENTADORIA"),
            ("DECLARAR APOSENTADA a servidora MARIA SOUZA, matrícula 54321", "APOSENTADORIA"),
            ("CONCEDER PENSÃO vitalícia para a servidora ANA LIMA (99999)", "PENSAO"),
            ("CONCEDER PENSAO temporária para o servidor PAULO COSTA (88888)", "PENSAO"),
            ("DECLARAR VACÂNCIA do cargo ocupado pelo servidor JOSE ALVES (77777)", "VACANCIA"),
            ("DECLARAR VACANCIA do cargo ocupado pela servidora CARLA DIAS (66666)", "VACANCIA"),
            ("DESIGNAR o servidor PEDRO RAMOS (11111) para exercer", "DESIGNACAO"),
            ("NOMEAR a servidora LUCIA FERREIRA (22222) para exercer", "NOMEACAO"),
            ("EXONERAR o servidor MARCOS ROCHA (33333)", "EXONERACAO"),
            ("DISPENSAR a servidora RITA GOMES (44444)", "DISPENSA"),
            ("REMOVER o servidor LUCAS MARTINS (55555)", "REMOCAO"),
            ("SUBSTITUIR o servidor TIAGO NUNES (66666)", "SUBSTITUICAO"),
        ]
        for text, expected_action in actions:
            entities = DeterministicNerExtractor.extract_entities(text)
            assert entities["tipo_ato_pessoal"] == expected_action

    def test_extract_personnel_cargos_and_matricula(self) -> None:
        """Verifies extraction of cargo de origem, destino, and matricula."""
        text = """
        PORTARIA Nº 50/2024
        DESIGNAR a servidora BEATRIZ SANTOS, titular do cargo de Analista Judiciário,
        registro funcional 98765, para exercer o cargo em comissão de CHEFE DE GABINETE,
        do GABINETE DA PRESIDÊNCIA.
        """
        entities = DeterministicNerExtractor.extract_entities(text)
        assert entities["tipo_ato_pessoal"] == "DESIGNACAO"
        assert entities["servidor_nome"] == "BEATRIZ SANTOS"
        assert entities["servidor_matricula"] == "98765"
        assert entities["cargo_origem"] == "Analista Judiciário"
        assert entities["cargo_destino"] == "CHEFE DE GABINETE"
        assert entities["triage_status"] == "EXTRACTED"
        assert entities["needs_manual_review"] is False

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
        assert entities["triage_status"] == "EXTRACTED"
        assert entities["needs_manual_review"] is False

    def test_extract_unclassified_act_flags_manual_review(self) -> None:
        """Asserts that unmatched acts are flagged for batch discovery and manual triage."""
        unclassified_text = """
        COMUNICADO Nº 12/2026
        Informamos a todos os colaboradores que o expediente da próxima sexta-feira
        será reduzido em virtude de manutenção predial no edifício-sede.
        """
        entities = DeterministicNerExtractor.extract_entities(unclassified_text)
        assert entities["triage_status"] == "UNCLASSIFIED_TRILHA_B"
        assert entities["needs_manual_review"] is True
        assert "Informamos a todos" in entities.get("triage_sample", "")

    def test_extract_unclassified_act_triage_sample_long_paragraph(self) -> None:
        """Asserts that triage_sample preserves the entire first paragraph if >= 300 chars."""
        long_para = "A" * 350
        text = f"{long_para}\n\nSegundo paragrafo que nao deve entrar no sample."
        entities = DeterministicNerExtractor.extract_entities(text)
        assert entities["triage_status"] == "UNCLASSIFIED_TRILHA_B"
        assert entities["triage_sample"] == long_para
        assert "Segundo paragrafo" not in entities["triage_sample"]

    def test_extract_unclassified_act_triage_sample_short_paragraph_picks_300_chars(self) -> None:
        """Asserts that triage_sample selects 300 chars if substantive text is short."""
        first_substantive_para = "Texto substantivo inicial que possui tamanho intermediario."
        second_para = "B" * 400
        text = f"{first_substantive_para}\n\n{second_para}"
        entities = DeterministicNerExtractor.extract_entities(text)
        assert entities["triage_status"] == "UNCLASSIFIED_TRILHA_B"
        assert len(entities["triage_sample"]) == 300
        assert entities["triage_sample"].startswith("Texto substantivo inicial")

    def test_extract_triage_sample_skips_retificacao_header(self) -> None:
        """Asserts that isolated title headers like RETIFICACAO are skipped."""
        text = (
            "RETIFICAÇÃO\n\n"
            "Na Portaria Inmetro nº 11, de 2 de janeiro de 2025, que aprova o Regulamento Técnico\n"
            "da Qualidade e os Requisitos de Avaliação da Conformidade para Carrinhos,\n"
            "publicada no Diário Oficial da União de 10 de fevereiro de 2025, seção 1:\n\n"
            "Onde se lê: no Anexo I...\nLeia-se: no Anexo II..."
        )
        entities = DeterministicNerExtractor.extract_entities(text)
        assert entities["triage_status"] == "UNCLASSIFIED_TRILHA_B"
        assert not entities["triage_sample"].startswith("RETIFICAÇÃO")
        assert entities["triage_sample"].startswith("Na Portaria Inmetro nº 11")
