"""Unit tests for Trilha A MutationExtractor.

Tests parsing of statutory amendments, (NR) provisions, and express revocations under LC 95/1998.
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

        m2 = mutations[1]
        assert m2.mutation_type == MutationType.ALTERACAO_NR
        assert m2.target_node_path.value == "art_3.inc_3"
        assert "desenvolvimento sustentável" in (m2.new_text or "")

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
