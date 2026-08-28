"""Domain Entities for the Ingestion Bounded Context.

Encapsulates Aggregate Roots and Entities that enforce business invariants
at construction time, ensuring illegal states are unrepresentable in memory.
"""

from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, model_validator

from lex.ingestion.domain.exceptions import DomainInvariantViolationError
from lex.ingestion.domain.value_objects import (
    DocumentHash,
    FederativeTier,
    GazetteDate,
    TerritoryId,
)


class GazetteEdition(BaseModel):
    """Aggregate Root representing a distinct published issue of an Official Gazette."""

    model_config = ConfigDict(frozen=True)

    id: UUID | None = None
    territory_id: TerritoryId
    tier: FederativeTier
    date: GazetteDate
    edition_number: str | None = None
    section: str | None = None
    is_extra_edition: bool = False
    power: str = "executive"
    source_url: str
    file_hash: DocumentHash
    char_count: int
    full_text: str
    scraped_at: datetime

    @model_validator(mode="after")
    def _validate_invariants(self) -> Self:
        """Enforces domain invariants at construction time."""
        clean_text = self.full_text.strip()
        if not clean_text:
            raise DomainInvariantViolationError("full_text must contain non-whitespace content.")

        if self.char_count <= 0:
            raise DomainInvariantViolationError("char_count must be strictly greater than zero.")

        if self.char_count != len(clean_text):
            raise DomainInvariantViolationError(
                f"char_count mismatch: expected {len(clean_text)}, got {self.char_count}."
            )

        if not (self.source_url.startswith("http://") or self.source_url.startswith("https://")):
            raise DomainInvariantViolationError(
                f"source_url must start with http:// or https://, got '{self.source_url}'."
            )

        if self.tier == FederativeTier.FEDERAL and self.territory_id.code != "BR":
            raise DomainInvariantViolationError(
                f"Federal tier requires territory code 'BR', got '{self.territory_id.code}'."
            )

        if self.tier == FederativeTier.STATE and len(self.territory_id.code) != 2:
            raise DomainInvariantViolationError(
                f"State tier requires a 2-letter state code, got '{self.territory_id.code}'."
            )

        if self.tier == FederativeTier.MUNICIPAL and len(self.territory_id.code) != 7:
            raise DomainInvariantViolationError(
                f"Municipal tier requires a 7-digit IBGE code, got '{self.territory_id.code}'."
            )

        return self
