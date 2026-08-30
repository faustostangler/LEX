"""Unit tests for PureAstReducer.

Tests deterministic reduction of base AST trees with chronological mutation streams,
recursive subtree revocations, and pre-rendered LZ4 HTML/Markdown compilation.
"""

import uuid
from datetime import date

from lex.consolidation.domain.services.ast_reducer import PureAstReducer
from lex.ingestion.domain.value_objects import DocumentHash, GazetteDate
from lex.treatment.domain.entities import (
    ActAst,
    DispositivoNode,
    NormativeActMutation,
)
from lex.treatment.domain.value_objects import (
    CanonicalNodePath,
    DispositivoStatus,
    DispositivoType,
    MutationType,
)


class TestPureAstReducer:
    """Test suite for Pure AST Reducer."""

    def test_reduce_alteration_and_revocation(self) -> None:
        """Asserts reduction of (NR) alteration and express revocation with cascade."""
        # 1. Base Act (Lei nº 10.000/2010)
        art1 = DispositivoNode(
            node_path=CanonicalNodePath.from_string("art_1"),
            node_type=DispositivoType.ARTIGO,
            label="Art. 1º",
            text="Esta Lei disciplina os contratos administrativos.",
        )
        art3 = DispositivoNode(
            node_path=CanonicalNodePath.from_string("art_3"),
            node_type=DispositivoType.ARTIGO,
            label="Art. 3º",
            text="São princípios fundamentais da contratação:",
        )
        inc1 = DispositivoNode(
            node_path=CanonicalNodePath.from_string("art_3.inc_1"),
            node_type=DispositivoType.INCISO,
            label="I -",
            text="legalidade e impessoalidade;",
        )
        inc2 = DispositivoNode(
            node_path=CanonicalNodePath.from_string("art_3.inc_2"),
            node_type=DispositivoType.INCISO,
            label="II -",
            text="moralidade e publicidade.",
        )
        ali_a = DispositivoNode(
            node_path=CanonicalNodePath.from_string("art_3.inc_2.ali_a"),
            node_type=DispositivoType.ALINEA,
            label="a)",
            text="transparência ampla;",
        )
        inc2.add_child(ali_a)
        art3.add_child(inc1)
        art3.add_child(inc2)

        base_ast = ActAst(
            act_id=uuid.uuid4(),
            canonical_urn="urn:lex:br:federal:lei:2010;10000",
            title="Lei nº 10.000/2010",
            ementa="Disciplina os contratos administrativos.",
            nodes=[art1, art3],
        )

        # 2. Mutations from Lei nº 12.000/2015
        author_id = uuid.uuid4()
        m_alt = NormativeActMutation(
            target_act_id=base_ast.act_id or uuid.uuid4(),
            target_node_path=CanonicalNodePath.from_string("art_3.inc_1"),
            author_act_id=author_id,
            author_dispositivo_ref="Art. 1º",
            mutation_type=MutationType.ALTERACAO_NR,
            new_text="legalidade, impessoalidade e eficiência; (NR)",
            publication_date=GazetteDate.from_date(date(2015, 6, 1)),
            effective_date=GazetteDate.from_date(date(2015, 6, 1)),
            extraction_source="lc95_regex",
            confidence_score=1.0,
            mutation_sha256=DocumentHash.from_text("mutation-1"),
        )
        m_rev = NormativeActMutation(
            target_act_id=base_ast.act_id or uuid.uuid4(),
            target_node_path=CanonicalNodePath.from_string("art_3.inc_2"),
            author_act_id=author_id,
            author_dispositivo_ref="Art. 2º",
            mutation_type=MutationType.REVOGACAO_EXPRESSA,
            new_text=None,
            publication_date=GazetteDate.from_date(date(2015, 6, 1)),
            effective_date=GazetteDate.from_date(date(2015, 6, 1)),
            extraction_source="lc95_regex",
            confidence_score=1.0,
            mutation_sha256=DocumentHash.from_text("mutation-2"),
        )

        # 3. Execute Pure Reduction
        compiled = PureAstReducer.reduce(
            base_ast=base_ast,
            mutations=[m_alt, m_rev],
        )

        # 4. Verify AST state
        assert compiled.total_mutations_applied == 2
        assert compiled.active_articles_count == 2
        assert compiled.last_mutation_effective_date == date(2015, 6, 1)

        # Verify Inciso I modified active
        reduced_inc1 = compiled.compiled_ast.find_node("art_3.inc_1")
        assert reduced_inc1 is not None
        assert reduced_inc1.status == DispositivoStatus.MODIFIED_ACTIVE
        assert "eficiência" in reduced_inc1.text
        assert len(reduced_inc1.history) == 1
        assert "legalidade e impessoalidade;" in reduced_inc1.history[0]["old_text"]

        # Verify Inciso II revoked and child alínea cascaded to revoked
        reduced_inc2 = compiled.compiled_ast.find_node("art_3.inc_2")
        assert reduced_inc2 is not None
        assert reduced_inc2.status == DispositivoStatus.REVOKED

        reduced_ali_a = compiled.compiled_ast.find_node("art_3.inc_2.ali_a")
        assert reduced_ali_a is not None
        assert reduced_ali_a.status == DispositivoStatus.REVOKED

        # Verify Pre-rendered HTML and Markdown
        assert "<strike>II - moralidade e publicidade.</strike>" in compiled.compiled_html
        assert "eficiência" in compiled.compiled_html
        assert compiled.compiled_version_hash is not None
        assert len(compiled.compiled_version_hash) == 64
