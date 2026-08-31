"""Comprehensive Unit Tests for Trilha A MutationExtractor.

Tests parsing of statutory amendments, (NR) provisions, express revocations,
acréscimos, paragraph modifications, and exact metadata generation under LC 95/1998.
"""

import uuid
from datetime import date

from lex.ingestion.domain.value_objects import GazetteDate
from lex.treatment.domain.services.mutation_extractor import MutationExtractor
from lex.treatment.domain.value_objects import MutationType


class TestMutationExtractor:
    """Test suite for LC 95/1998 Mutation Extractor."""

    def test_extract_alterations_with_nr(self) -> None:
        """Asserts extraction of altered provisions marked with (NR)."""
        amending_text = """
        LEI Nº 12.000, DE 1º DE JUNHO DE 2015

        Altera a Lei nº 10.000, de 10 de janeiro de 2010.

        O PRESIDENTE DA REPÚBLICA Faço saber que o Congresso Nacional decreta e eu sanciono:

        Art. 1º A Lei nº 10.000/2010 passa a vigorar com as seguintes alterações:
        "Art. 3º ............................................................................
        I - legalidade, impessoalidade e eficiência; (NR)
        ......................................................................................
        III - desenvolvimento sustentável." (NR)
        """

        author_id = uuid.uuid4()
        pub_date = GazetteDate.from_date(date(2015, 6, 1))

        mutations = MutationExtractor.extract_mutations(
            raw_text=amending_text,
            author_act_id=author_id,
            publication_date=pub_date,
            effective_date=pub_date,
            default_territory_id="BR",
        )

        assert len(mutations) == 2

        m1 = mutations[0]
        assert m1.mutation_type == MutationType.ALTERACAO_NR
        assert m1.target_node_path.value == "art_3.inc_1"
        assert "eficiência" in (m1.new_text or "")
        assert m1.author_act_id == author_id
        assert m1.publication_date == pub_date
        assert m1.effective_date == pub_date
        assert m1.confidence_score == 1.0
        assert m1.extraction_source == "lc95_deterministic_regex"
        assert m1.target_act_type == "Lei"
        assert m1.target_act_number == "10.000"
        assert m1.target_act_year == 2010
        assert m1.target_canonical_urn == "urn:lex:br:federal:lei:2010;10000"
        expected_target_id = uuid.uuid5(uuid.NAMESPACE_DNS, "urn:lex:br:federal:lei:2010;10000")
        assert m1.target_act_id == expected_target_id

        m2 = mutations[1]
        assert m2.mutation_type == MutationType.ALTERACAO_NR
        assert m2.target_node_path.value == "art_3.inc_3"
        assert "desenvolvimento sustentável" in (m2.new_text or "")
        assert m2.confidence_score == 1.0
        assert m2.extraction_source == "lc95_deterministic_regex"
        assert m2.target_act_id == expected_target_id

    def test_extract_express_revocations(self) -> None:
        """Asserts extraction of express revocation clauses."""
        revocation_text = """
        LEI Nº 14.500, DE 5 DE MAIO DE 2023

        Art. 1º Fica alterada a regulamentação anterior.
        Art. 2º Revogam-se os incisos I e II do art. 5º da Lei nº 10.000, de 2010.
        Art. 3º Revoga-se o art. 12 da Lei nº 10.000, de 2010.
        """

        author_id = uuid.uuid4()
        pub_date = GazetteDate.from_date(date(2023, 5, 5))

        mutations = MutationExtractor.extract_mutations(
            raw_text=revocation_text,
            author_act_id=author_id,
            publication_date=pub_date,
            effective_date=pub_date,
            default_territory_id="BR",
        )

        # Expect 3 revocations: art_5.inc_1, art_5.inc_2, art_12
        assert len(mutations) == 3
        revoked_paths = [m.target_node_path.value for m in mutations]
        assert "art_5.inc_1" in revoked_paths
        assert "art_5.inc_2" in revoked_paths
        assert "art_12" in revoked_paths

        for m in mutations:
            assert m.mutation_type == MutationType.REVOGACAO_EXPRESSA
            assert m.new_text is None
            assert m.confidence_score == 1.0
            assert m.extraction_source == "lc95_deterministic_regex"

    def test_alteration_headers_date_variations(self) -> None:
        """Scenario: Alteration headers with various date formats and phrasing are parsed."""
        headers = [
            (
                "Art. 1º A Lei nº 10.000, de 10 de janeiro de 2010, passa a vigorar com as "
                'seguintes alterações:\n"Art. 1º Teste (NR)"'
            ),
            'Art. 1º O Decreto nº 5.000, de 2021, passa a vigorar:\n"Art. 1º Teste (NR)"',
            (
                "Art. 1º A Medida Provisória nº 1.200/2024 passa a vigorar com as seguintes "
                'alterações:\n"Art. 1º Teste (NR)"'
            ),
            (
                "Art. 1º A Portaria nº 100 passa a vigorar com a seguinte alteração:\n"
                '"Art. 1º Teste (NR)"'
            ),
            (
                "Art. 1º A Lei Complementar nº 101, de 4 de maio de 2000, passa a vigorar:\n"
                '"Art. 1º Teste (NR)"'
            ),
        ]
        author_id = uuid.uuid4()
        pub_date = GazetteDate.from_date(date(2024, 1, 1))

        for header_text in headers:
            mutations = MutationExtractor.extract_mutations(
                raw_text=header_text,
                author_act_id=author_id,
                publication_date=pub_date,
                effective_date=pub_date,
                default_territory_id="BR",
            )
            assert len(mutations) == 1
            assert mutations[0].mutation_type == MutationType.ALTERACAO_NR

    def test_alteration_header_redos_resilience(self) -> None:
        """Scenario: Malformed repetitive inputs do not cause ReDoS (CWE-1333)."""
        import time

        # Adversarial payload with nested repetitive words designed to trigger backtracking
        adversarial_line = (
            "Art. 1º A Lei nº 12.345 " + ("de janeiro de algo " * 40) + "passa a nao vigorar"
        )
        adversarial_text = f'{adversarial_line}\n"Art. 1º Conteudo (NR)"'

        author_id = uuid.uuid4()
        pub_date = GazetteDate.from_date(date(2024, 1, 1))

        start_time = time.perf_counter()
        mutations = MutationExtractor.extract_mutations(
            raw_text=adversarial_text,
            author_act_id=author_id,
            publication_date=pub_date,
            effective_date=pub_date,
            default_territory_id="BR",
        )
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        # Execution must complete in linear time (< 50ms)
        assert elapsed_ms < 50.0
        assert len(mutations) == 0  # Header didn't match cleanly, skipped without ReDoS hang
