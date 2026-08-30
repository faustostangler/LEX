"""LEX Shared Kernel Package."""

from lex.shared_kernel.config import LexSettings
from lex.shared_kernel.value_objects import (
    HierarchicalGroup,
    HierarchicalRank,
    PublicationNature,
)

__all__ = [
    "HierarchicalGroup",
    "HierarchicalRank",
    "LexSettings",
    "PublicationNature",
]


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
