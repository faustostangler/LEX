"""Unit tests for Treatment Context Domain Entities and AST models.

Tests DispositivoNode hierarchy, ActAst navigation, and NormativeActMutation invariants.
"""

import uuid
from datetime import date

import pytest

from lex.ingestion.domain.value_objects import DocumentHash, GazetteDate
from lex.treatment.domain.entities import (
    ActAst,
    DispositivoNode,
    NormativeActMutation,
)
from lex.treatment.domain.exceptions import InvalidMutationPayloadError
from lex.treatment.domain.value_objects import (
    CanonicalNodePath,
    DispositivoStatus,
    DispositivoType,
    MutationType,
)


class TestDispositivoNode:
    """Test suite for DispositivoNode AST tree component."""

    def test_node_instantiation_and_defaults(self) -> None:
        """Asserts default status and empty children/history."""
        node = DispositivoNode(
            node_path=CanonicalNodePath.from_string("art_1"),
            node_type=DispositivoType.ARTIGO,
            label="Art. 1º",
            text="Esta Lei estabelece normas gerais de licitação.",
        )
        assert node.status == DispositivoStatus.ORIGINAL_ACTIVE
        assert node.children == []
        assert node.history == []
        assert node.node_path.value == "art_1"

    def test_tree_construction_and_lookup(self) -> None:
        """Asserts recursive child addition and path lookup."""
        art = DispositivoNode(
            node_path=CanonicalNodePath.from_string("art_3"),
            node_type=DispositivoType.ARTIGO,
            label="Art. 3º",
            text="São princípios da licitação:",
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
            text="transparência ativa;",
        )
        inc2.add_child(ali_a)
        art.add_child(inc1)
        art.add_child(inc2)

        assert len(art.children) == 2
        assert len(inc2.children) == 1

        # Recursive lookup
        found_inc = art.find_node("art_3.inc_2")
        assert found_inc is not None
        assert found_inc.label == "II -"

        found_ali = art.find_node("art_3.inc_2.ali_a")
        assert found_ali is not None
        assert found_ali.text == "transparência ativa;"

        assert art.find_node("art_3.inc_3") is None


class TestActAst:
    """Test suite for ActAst aggregate root."""

    def test_act_ast_serialization(self) -> None:
        """Asserts to_dict and from_dict serialization roundtrip."""
        art1 = DispositivoNode(
            node_path=CanonicalNodePath.from_string("art_1"),
            node_type=DispositivoType.ARTIGO,
            label="Art. 1º",
            text="Texto do artigo primeiro.",
        )
        ast = ActAst(
            act_id=uuid.uuid4(),
            canonical_urn="urn:lex:br:federal:lei:2024;1000",
            title="Lei nº 1.000/2024",
            ementa="Dispõe sobre matérias administrativas.",
            nodes=[art1],
        )

        payload = ast.to_dict()
        assert payload["title"] == "Lei nº 1.000/2024"
        assert len(payload["nodes"]) == 1
        assert payload["nodes"][0]["node_path"] == "art_1"

        restored = ActAst.from_dict(payload)
        assert restored.title == ast.title
        assert len(restored.nodes) == 1
        assert restored.nodes[0].text == "Texto do artigo primeiro."


class TestNormativeActMutation:
    """Test suite for NormativeActMutation domain entity."""

    def test_valid_mutation_entity(self) -> None:
        """Asserts valid mutation creation with cryptographic hash."""
        target_id = uuid.uuid4()
        author_id = uuid.uuid4()
        mutation = NormativeActMutation(
            target_act_id=target_id,
            target_node_path=CanonicalNodePath.from_string("art_3.inc_1"),
            author_act_id=author_id,
            author_dispositivo_ref="Art. 1º",
            mutation_type=MutationType.ALTERACAO_NR,
            new_text="legalidade, impessoalidade e eficiência; (NR)",
            publication_date=GazetteDate.from_date(date(2024, 1, 15)),
            effective_date=GazetteDate.from_date(date(2024, 1, 15)),
            extraction_source="lc95_deterministic_regex",
            confidence_score=1.0,
            mutation_sha256=DocumentHash.from_text("legalidade, impessoalidade e eficiência; (NR)"),
        )
        assert mutation.mutation_type == MutationType.ALTERACAO_NR
        assert mutation.target_act_id == target_id

    def test_invalid_mutation_raises(self) -> None:
        """Asserts that ALTERACAO_NR without new_text raises InvalidMutationPayloadError."""
        target_id = uuid.uuid4()
        author_id = uuid.uuid4()
        with pytest.raises(InvalidMutationPayloadError):
            NormativeActMutation(
                target_act_id=target_id,
                target_node_path=CanonicalNodePath.from_string("art_3.inc_1"),
                author_act_id=author_id,
                author_dispositivo_ref="Art. 1º",
                mutation_type=MutationType.ALTERACAO_NR,
                new_text=None,  # Invalid: ALTERACAO_NR requires new_text
                publication_date=GazetteDate.from_date(date(2024, 1, 15)),
                effective_date=GazetteDate.from_date(date(2024, 1, 15)),
                extraction_source="lc95_deterministic_regex",
                confidence_score=1.0,
                mutation_sha256=DocumentHash.from_text("some-hash"),
            )
