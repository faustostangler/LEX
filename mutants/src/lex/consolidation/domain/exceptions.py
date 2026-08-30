"""Domain Exceptions for the Consolidation Bounded Context.

Enforces typed errors for LexML URN parsing, out-of-order resolution, and reduction.
"""

from lex.ingestion.domain.exceptions import LexDomainError


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class InvalidCanonicalUrnError(LexDomainError):
    """Raised when a LexML/FRBR URN violates canonical statutory syntax."""


class ConsolidationReductionError(LexDomainError):
    """Raised when an error occurs during pure AST mutation reduction."""


class StubResolutionError(LexDomainError):
    """Raised when an error occurs resolving or hydrating a Stub entity."""
