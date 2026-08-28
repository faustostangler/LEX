"""Application Port Interfaces for the Ingestion Bounded Context.

Defines structural subtyping Protocols for repository persistence,
in-memory stream extraction, and event notification without framework dependencies.
"""

from typing import Protocol, runtime_checkable

from lex.ingestion.domain.entities import GazetteEdition
from lex.ingestion.domain.value_objects import (
    DocumentHash,
    GazetteDate,
    TerritoryId,
)


@runtime_checkable
class GazetteRepositoryPort(Protocol):
    """Outbound port for persisting and retrieving GazetteEdition aggregates."""

    def save(self, edition: GazetteEdition) -> None:
        """Persist a gazette edition with idempotent ON CONFLICT semantics."""
        ...

    def get_by_territory_and_date(
        self,
        territory_id: TerritoryId,
        date: GazetteDate,
        section: str | None = None,
    ) -> GazetteEdition | None:
        """Retrieve a unique gazette edition if already ingested."""
        ...

    def exists_by_hash(self, file_hash: DocumentHash) -> bool:
        """Check if a gazette with the exact content hash has already been stored."""
        ...


@runtime_checkable
class StreamTextExtractorPort(Protocol):
    """Outbound port for streaming binary transformation into clean text."""

    def extract_text(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        """Extract plain text from an in-memory PDF/HTML stream."""
        ...
