"""Comprehensive Unit tests for Trilha A ActSegmenter.

Tests parsing of Brazilian legislation into structured AST trees under LC 95/1998,
including roman numeral conversions, parágrafos únicos, alphanumeric articles,
nested incisos, alíneas, items, and edge cases.
"""

from lex.treatment.domain.services.act_segmenter import ActSegmenter, _roman_to_int
from lex.treatment.domain.value_objects import DispositivoType


class TestActSegmenter:
    """Test suite for LC 95/1998 AST Segmenter."""

    def test_roman_to_int_conversion(self) -> None:
        """Verifies roman numeral parsing across various values."""
        assert _roman_to_int("I") == 1
        assert _roman_to_int("IV") == 4
        assert _roman_to_int("IX") == 9
        assert _roman_to_int("XIV") == 14
        assert _roman_to_int("XIX") == 19
        assert _roman_to_int("XXVIII") == 28
        assert _roman_to_int("XL") == 40
        assert _roman_to_int("L") == 50
        assert _roman_to_int("XC") == 90
        assert _roman_to_int("C") == 100

    def test_segment_simple_law(self) -> None:
        """Asserts segmentation of basic articles with paragraphs and clauses."""
        raw_text = """
        LEI Nº 14.000, DE 10 DE JANEIRO DE 2024

        Dispõe sobre a transparência em licitações públicas.

        O PRESIDENTE DA REPÚBLICA Faço saber que o Congresso Nacional decreta e eu sanciono:

        Art. 1º Esta Lei estabelece normas de transparência nas compras governamentais.

        Art. 2º Para os efeitos desta Lei, considera-se:
        I - órgão: a unidade de atuação integrante da estrutura da administração;
        II - entidade: a unidade de atuação dotada de personalidade jurídica.

        Art. 3º Os órgãos deverão publicar seus editais na internet.
        § 1º A publicação deverá ocorrer no prazo de 5 (cinco) dias.
        § 2º O descumprimento do caput sujeita o infrator a penalidades:
        I - advertência formal;
        II - suspensão temporária:
        a) por 30 dias na primeira infração;
        b) por 90 dias em caso de reincidência:
        1. com cancelamento do registro;
        2. com aplicação de multa.

        Art. 4º Esta Lei entra em vigor na data de sua publicação.
        """

        ast = ActSegmenter.segment_text(
            raw_text=raw_text,
            title="Lei nº 14.000/2024",
            ementa="Dispõe sobre a transparência em licitações públicas.",
        )

        assert ast.title == "Lei nº 14.000/2024"
        assert len(ast.nodes) == 4

        # Verify Art. 1
        art1 = ast.find_node("art_1")
        assert art1 is not None
        assert art1.node_type == DispositivoType.ARTIGO
        assert "estabelece normas" in art1.text

        # Verify Art. 2 incisos
        art2 = ast.find_node("art_2")
        assert art2 is not None
        assert len(art2.children) == 2
        inc1 = ast.find_node("art_2.inc_1")
        assert inc1 is not None
        assert "órgão:" in inc1.text
        inc2 = ast.find_node("art_2.inc_2")
        assert inc2 is not None
        assert "entidade:" in inc2.text

        # Verify Art. 3 paragraphs, incisos, alíneas, items
        par1 = ast.find_node("art_3.par_1")
        assert par1 is not None
        assert "prazo de 5" in par1.text

        par2 = ast.find_node("art_3.par_2")
        assert par2 is not None
        assert len(par2.children) == 2

        ali_a = ast.find_node("art_3.par_2.inc_2.ali_a")
        assert ali_a is not None
        assert "30 dias" in ali_a.text

        item1 = ast.find_node("art_3.par_2.inc_2.ali_b.item_1")
        assert item1 is not None
        assert "cancelamento" in item1.text

    def test_segment_paragrafo_unico(self) -> None:
        """Asserts handling of 'Parágrafo único.' provision label."""
        raw_text = """
        Art. 15. O processo será sigiloso até a decisão final.
        Parágrafo único. A publicidade dos atos será garantida após o julgamento.
        """
        ast = ActSegmenter.segment_text(raw_text=raw_text, title="Lei Teste")
        par_unico = ast.find_node("art_15.par_unico")
        assert par_unico is not None
        assert par_unico.node_type == DispositivoType.PARAGRAFO_UNICO
        assert "A publicidade" in par_unico.text

    def test_segment_alphanumeric_articles(self) -> None:
        """Asserts handling of added articles like 'Art. 15-A' or 'Art. 15-B'."""
        raw_text = """
        Art. 15-A. Fica instituído o comitê de governança digital.
        § 1º O comitê reunir-se-á mensalmente.
        """
        ast = ActSegmenter.segment_text(raw_text=raw_text, title="Lei Alfanumérica")
        art15a = ast.find_node("art_15_a")
        assert art15a is not None
        assert "comitê de governança" in art15a.text

        par1 = ast.find_node("art_15_a.par_1")
        assert par1 is not None
        assert "mensalmente" in par1.text
