"""Unit tests for LINDB and Kelsenian Normative Hierarchy Validation.

Tests that the Lex Superior Derogat Inferiori invariant strictly prevents
inferior legal acts from mutating or revoking superior statutes.
"""

import pytest

from lex.shared_kernel.value_objects import HierarchicalRank
from lex.treatment.domain.exceptions import LexSuperiorViolationError
from lex.treatment.domain.services.kelsen_validator import (
    validate_kelsen_mutation_precedence,
)


class TestKelsenLindbValidator:
    """Test suite for constitutional hierarchy validation."""

    def test_superior_or_equal_rank_mutation_succeeds(self) -> None:
        """Asserts that equal or superior rank mutations pass validation."""
        # EC (100) mutating Lei Ordinária (70)
        validate_kelsen_mutation_precedence(
            author_rank=HierarchicalRank.EMENDA_CONSTITUCIONAL,
            target_rank=HierarchicalRank.LEI_ORDINARIA,
            author_title="Emenda Constitucional nº 132/2023",
            target_title="Lei nº 5.172/1966",
        )

        # Lei Ordinária (70) mutating Lei Ordinária (70)
        validate_kelsen_mutation_precedence(
            author_rank=HierarchicalRank.LEI_ORDINARIA,
            target_rank=HierarchicalRank.LEI_ORDINARIA,
            author_title="Lei nº 14.133/2021",
            target_title="Lei nº 8.666/1993",
        )

        # Lei Complementar (80) mutating Lei Ordinária (70)
        validate_kelsen_mutation_precedence(
            author_rank=HierarchicalRank.LEI_COMPLEMENTAR,
            target_rank=HierarchicalRank.LEI_ORDINARIA,
            author_title="Lei Complementar nº 123/2006",
            target_title="Lei nº 9.317/1996",
        )

    def test_inferior_rank_mutation_raises_lex_superior_violation(self) -> None:
        """Asserts that an inferior act mutating a superior act raises an error."""
        # Portaria (40) attempting to mutate Lei Ordinária (70)
        with pytest.raises(LexSuperiorViolationError) as exc_info:
            validate_kelsen_mutation_precedence(
                author_rank=HierarchicalRank.PORTARIA_NORMATIVA,
                target_rank=HierarchicalRank.LEI_ORDINARIA,
                author_title="Portaria GM/MS nº 100/2024",
                target_title="Lei nº 8.080/1990",
            )
        err_msg = str(exc_info.value)
        assert "Lex Superior" in err_msg or "Constitutional Violation" in err_msg

        # Decreto Executivo (60) attempting to mutate Lei Complementar (80)
        with pytest.raises(LexSuperiorViolationError):
            validate_kelsen_mutation_precedence(
                author_rank=HierarchicalRank.DECRETO_EXECUTIVO,
                target_rank=HierarchicalRank.LEI_COMPLEMENTAR,
                author_title="Decreto nº 10.000/2019",
                target_title="Lei Complementar nº 101/2000",
            )
