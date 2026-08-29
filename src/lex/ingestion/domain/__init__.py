"""Ingestion Bounded Context Domain Layer."""

from .entities import GazetteEdition, NormativeAct
from .exceptions import (
    CorruptedGazettePayloadError,
    DomainInvariantViolationError,
    InvalidDocumentHashError,
    InvalidGazetteDateError,
    InvalidTerritoryCodeError,
    LexDomainError,
)
from .value_objects import (
    ActType,
    ClassificationSource,
    DocumentHash,
    FederativeTier,
    GazetteDate,
    IngestionStatus,
    TerritoryId,
)

__all__ = [
    "ActType",
    "ClassificationSource",
    "CorruptedGazettePayloadError",
    "DocumentHash",
    "DomainInvariantViolationError",
    "FederativeTier",
    "GazetteDate",
    "GazetteEdition",
    "IngestionStatus",
    "InvalidDocumentHashError",
    "InvalidGazetteDateError",
    "InvalidTerritoryCodeError",
    "LexDomainError",
    "NormativeAct",
    "TerritoryId",
]
