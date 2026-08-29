"""Application Port Interfaces for the Ingestion and Digestion Bounded Contexts.

Defines structural subtyping Protocols for repository persistence,
in-memory stream extraction, and normative act querying without framework dependencies.
"""

from typing import Protocol, runtime_checkable
from uuid import UUID

from lex.ingestion.domain.entities import GazetteEdition, NormativeAct
from lex.ingestion.domain.value_objects import (
    DocumentHash,
    GazetteDate,
    TerritoryId,
)


@runtime_checkable
class GazetteRepositoryPort(Protocol):
    """Outbound port for persisting and retrieving GazetteEdition aggregates and NormativeActs."""

    def save(self, edition: GazetteEdition) -> GazetteEdition:
        """Persist a gazette edition with idempotent ON CONFLICT semantics, returning entity."""
        ...

    def get_by_territory_and_date(
        self,
        territory_id: TerritoryId,
        date: GazetteDate,
        section: str | None = None,
    ) -> GazetteEdition | None:
        """Retrieve a unique gazette edition if already ingested."""
        ...

    def exists_by_hash(self, summary_hash: DocumentHash) -> bool:
        """Check if a gazette edition with the exact summary hash has already been stored."""
        ...

    def save_normative_act(self, act: NormativeAct) -> None:
        """Persist a discrete normative act with idempotent ON CONFLICT semantics."""
        ...

    def save_normative_acts_bulk(self, acts: list[NormativeAct]) -> None:
        """Persist a batch of discrete normative acts with bulk upsert."""
        ...

    def get_act_by_id(self, act_id: UUID) -> NormativeAct | None:
        """Retrieve a normative act by its unique identifier."""
        ...

    def find_acts_by_edition(self, edition_id: UUID) -> list[NormativeAct]:
        """Retrieve all normative acts associated with a specific gazette edition."""
        ...

    def exists_act_by_hash(self, content_hash: DocumentHash) -> bool:
        """Check if a normative act with the exact content hash has already been stored."""
        ...


@runtime_checkable
class StreamTextExtractorPort(Protocol):
    """Outbound port for streaming binary transformation into clean text."""

    def extract_text(self, stream_bytes: bytes, max_spool_mb: int = 10) -> str:
        """Extract plain text from an in-memory PDF/HTML stream."""
        ...
