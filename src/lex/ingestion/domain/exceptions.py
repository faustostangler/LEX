"""Ingestion Domain Exceptions.

Provides strongly typed exceptions representing domain invariant violations
and processing failures within the Ingestion Bounded Context.
"""


class LexDomainError(Exception):
    """Base exception for all LEX domain errors."""


class InvalidTerritoryCodeError(LexDomainError):
    """Raised when a territory code does not match federal, state, or municipal standards."""


class InvalidGazetteDateError(LexDomainError):
    """Raised when a gazette publication date is outside valid historical boundaries."""


class InvalidDocumentHashError(LexDomainError):
    """Raised when a content hash string is not a valid 64-character lowercase SHA-256."""


class DomainInvariantViolationError(LexDomainError):
    """Raised when a domain entity constructor or method violates business invariants."""


class CorruptedGazettePayloadError(LexDomainError):
    """Raised when an incoming raw byte stream cannot be decoded or parsed as a valid gazette."""
