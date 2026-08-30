"""LINDB and Kelsenian Normative Hierarchy Precedence Validator.

Enforces the 'Lex Superior Derogat Inferiori' constitutional invariant across
legislative amendments and consolidations.
"""

from lex.treatment.domain.exceptions import LexSuperiorViolationError


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_validate_kelsen_mutation_precedence__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_validate_kelsen_mutation_precedence__mutmut)
def validate_kelsen_mutation_precedence(
    author_rank: int, target_rank: int, author_title: str, target_title: str
) -> None:
    """Enforces the 'Lex Superior Derogat Inferiori' constitutional invariant.

    Args:
        author_rank: Hierarchical rank score of the amending act.
        target_rank: Hierarchical rank score of the target statute.
        author_title: Human-readable title of the author act.
        target_title: Human-readable title of the target statute.

    Raises:
        LexSuperiorViolationError: If an inferior rank act attempts to mutate or
            revoke a superior rank act.
    """
    if author_rank < target_rank:
        raise LexSuperiorViolationError(
            f"Constitutional Violation (LINDB / Kelsen / Lex Superior): Act '{author_title}' "
            f"(Rank {author_rank}) cannot alter or revoke superior statute '{target_title}' "
            f"(Rank {target_rank})."
        )


def x_validate_kelsen_mutation_precedence__mutmut_orig(
    author_rank: int, target_rank: int, author_title: str, target_title: str
) -> None:
    """Enforces the 'Lex Superior Derogat Inferiori' constitutional invariant.

    Args:
        author_rank: Hierarchical rank score of the amending act.
        target_rank: Hierarchical rank score of the target statute.
        author_title: Human-readable title of the author act.
        target_title: Human-readable title of the target statute.

    Raises:
        LexSuperiorViolationError: If an inferior rank act attempts to mutate or
            revoke a superior rank act.
    """
    if author_rank < target_rank:
        raise LexSuperiorViolationError(
            f"Constitutional Violation (LINDB / Kelsen / Lex Superior): Act '{author_title}' "
            f"(Rank {author_rank}) cannot alter or revoke superior statute '{target_title}' "
            f"(Rank {target_rank})."
        )


def x_validate_kelsen_mutation_precedence__mutmut_1(
    author_rank: int, target_rank: int, author_title: str, target_title: str
) -> None:
    """Enforces the 'Lex Superior Derogat Inferiori' constitutional invariant.

    Args:
        author_rank: Hierarchical rank score of the amending act.
        target_rank: Hierarchical rank score of the target statute.
        author_title: Human-readable title of the author act.
        target_title: Human-readable title of the target statute.

    Raises:
        LexSuperiorViolationError: If an inferior rank act attempts to mutate or
            revoke a superior rank act.
    """
    if author_rank <= target_rank:
        raise LexSuperiorViolationError(
            f"Constitutional Violation (LINDB / Kelsen / Lex Superior): Act '{author_title}' "
            f"(Rank {author_rank}) cannot alter or revoke superior statute '{target_title}' "
            f"(Rank {target_rank})."
        )


def x_validate_kelsen_mutation_precedence__mutmut_2(
    author_rank: int, target_rank: int, author_title: str, target_title: str
) -> None:
    """Enforces the 'Lex Superior Derogat Inferiori' constitutional invariant.

    Args:
        author_rank: Hierarchical rank score of the amending act.
        target_rank: Hierarchical rank score of the target statute.
        author_title: Human-readable title of the author act.
        target_title: Human-readable title of the target statute.

    Raises:
        LexSuperiorViolationError: If an inferior rank act attempts to mutate or
            revoke a superior rank act.
    """
    if author_rank < target_rank:
        raise LexSuperiorViolationError(
            None
        )

mutants_x_validate_kelsen_mutation_precedence__mutmut['_mutmut_orig'] = x_validate_kelsen_mutation_precedence__mutmut_orig # type: ignore # mutmut generated
mutants_x_validate_kelsen_mutation_precedence__mutmut['x_validate_kelsen_mutation_precedence__mutmut_1'] = x_validate_kelsen_mutation_precedence__mutmut_1 # type: ignore # mutmut generated
mutants_x_validate_kelsen_mutation_precedence__mutmut['x_validate_kelsen_mutation_precedence__mutmut_2'] = x_validate_kelsen_mutation_precedence__mutmut_2 # type: ignore # mutmut generated
