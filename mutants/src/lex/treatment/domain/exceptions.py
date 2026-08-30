"""Domain Exceptions for the Treatment and Digestion Bounded Context.

Enforces strongly-typed error handling for AST parsing, canonical addressing,
and constitutional/LINDB hierarchy invariants.
"""

from lex.ingestion.domain.exceptions import LexDomainError


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class InvalidCanonicalNodePathError(LexDomainError):
    """Raised when a provision address violates canonical dot-separated grammar."""


class LexSuperiorViolationError(LexDomainError):
    """Raised when an inferior rank act attempts to modify or revoke a superior rank act."""


class AstParsingError(LexDomainError):
    """Raised when an error occurs while parsing legislative text into an AST."""


class InvalidMutationPayloadError(LexDomainError):
    """Raised when a mutation payload violates domain invariants."""
