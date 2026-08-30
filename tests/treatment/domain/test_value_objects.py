"""Unit tests for Treatment Context Value Objects.

Tests CanonicalNodePath validation, MutationType, DispositivoStatus, and DispositivoType.
"""

import pytest

from lex.treatment.domain.exceptions import InvalidCanonicalNodePathError
from lex.treatment.domain.value_objects import (
    CanonicalNodePath,
    DispositivoStatus,
    DispositivoType,
    MutationType,
)


class TestCanonicalNodePath:
    """Test suite for CanonicalNodePath value object."""

    @pytest.mark.parametrize(
        "valid_path",
        [
            "art_1",
            "art_3",
            "art_15_a",
            "art_3.par_1",
            "art_3.par_unico",
            "art_3.par_2.inc_14",
            "art_3.inc_2",
            "art_3.inc_2.ali_a",
            "art_3.inc_2.ali_a.item_1",
            "art_100.par_2.inc_5.ali_b.item_10",
        ],
    )
    def test_valid_canonical_node_paths(self, valid_path: str) -> None:
        """Asserts that standard LC 95 provision paths parse without error."""
        node_path = CanonicalNodePath.from_string(valid_path)
        assert node_path.value == valid_path
        assert str(node_path) == valid_path
        assert repr(node_path) == f"CanonicalNodePath('{valid_path}')"

    @pytest.mark.parametrize(
        "invalid_path",
        [
            "",
            "   ",
            "artigo_1",
            "art_1.invalid_tag",
            "art_1.par_1.extra.inc_1",
            "art_1.inc_1.par_1",  # Paragraph cannot be child of Inciso
            "art_1.item_1",  # Item must be child of Alínea
            "art_1.ali_a",  # Alínea must be child of Inciso or Parágrafo
            "art_",
            "123",
            "ART_1",  # Must be lowercase
        ],
    )
    def test_invalid_canonical_node_paths(self, invalid_path: str) -> None:
        """Asserts that malformed provision paths raise InvalidCanonicalNodePathError."""
        with pytest.raises(InvalidCanonicalNodePathError):
            CanonicalNodePath.from_string(invalid_path)

    def test_node_path_hierarchy_and_depth(self) -> None:
        """Asserts that segments, parent_path, and depth work correctly."""
        path = CanonicalNodePath.from_string("art_3.par_1.inc_14.ali_a.item_1")
        assert path.segments == ["art_3", "par_1", "inc_14", "ali_a", "item_1"]
        assert path.depth == 5
        assert path.leaf_name == "item_1"
        assert path.parent_path == CanonicalNodePath.from_string("art_3.par_1.inc_14.ali_a")

        root = CanonicalNodePath.from_string("art_3")
        assert root.segments == ["art_3"]
        assert root.depth == 1
        assert root.parent_path is None

    def test_immutability_and_equality(self) -> None:
        """Asserts value object hashability and equality."""
        p1 = CanonicalNodePath.from_string("art_3.inc_1")
        p2 = CanonicalNodePath.from_string("art_3.inc_1")
        p3 = CanonicalNodePath.from_string("art_3.inc_2")

        assert p1 == p2
        assert p1 != p3
        assert hash(p1) == hash(p2)
        assert len({p1, p2, p3}) == 2


class TestEnums:
    """Test suite for Treatment Enums."""

    def test_mutation_types(self) -> None:
        """Asserts all LC 95 mutation types exist as strings."""
        assert MutationType.ACRESCIMO == "ACRESCIMO"
        assert MutationType.ALTERACAO_NR == "ALTERACAO_NR"
        assert MutationType.REVOGACAO_EXPRESSA == "REVOGACAO_EXPRESSA"
        assert MutationType.REVOGACAO_TACITA == "REVOGACAO_TACITA"
        assert MutationType.SUSPENSAO_EFICACIA == "SUSPENSAO_EFICACIA"
        assert MutationType.RENUMERACAO == "RENUMERACAO"
        assert MutationType.RETIFICACAO == "RETIFICACAO"

    def test_dispositivo_status(self) -> None:
        """Asserts all legal validity statuses exist."""
        assert DispositivoStatus.ORIGINAL_ACTIVE.value == "original_active"
        assert DispositivoStatus.MODIFIED_ACTIVE.value == "modified_active"
        assert DispositivoStatus.REVOKED.value == "revoked"
        assert DispositivoStatus.SUSPENDED.value == "suspended"

    def test_dispositivo_types(self) -> None:
        """Asserts all statutory structural types exist."""
        assert DispositivoType.ARTIGO.value == "artigo"
        assert DispositivoType.PARAGRAFO.value == "paragrafo"
        assert DispositivoType.PARAGRAFO_UNICO.value == "paragrafo_unico"
        assert DispositivoType.INCISO.value == "inciso"
        assert DispositivoType.ALINEA.value == "alinea"
        assert DispositivoType.ITEM.value == "item"
        assert DispositivoType.CAPUT.value == "caput"
