"""Domain Entities for the Ingestion and Digestion Bounded Contexts.

Encapsulates Aggregate Roots and Entities that enforce business invariants
at construction time, ensuring illegal states are unrepresentable in memory.
"""

from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from lex.ingestion.domain.exceptions import DomainInvariantViolationError
from lex.ingestion.domain.value_objects import (
    ClassificationSource,
    DocumentHash,
    FederativeTier,
    GazetteDate,
    IngestionStatus,
    TerritoryId,
)
from lex.shared_kernel.value_objects import (
    HierarchicalGroup,
    PublicationNature,
)


class GazetteEdition(BaseModel):
    """Aggregate Root for publication container and audit metadata of an Official Gazette."""

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
    summary_hash: DocumentHash
    total_acts: int = Field(default=0, ge=0)
    ingestion_status: IngestionStatus = IngestionStatus.COMPLETED
    scraped_at: datetime

    @model_validator(mode="after")
    def _validate_invariants(self) -> Self:
        """Enforces domain invariants at construction time."""
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


class NormativeAct(BaseModel):
    """Entity representing a discrete normative act (SSOT for legislative content)."""

    model_config = ConfigDict(frozen=True)

    id: UUID | None = None
    edition_id: UUID | None = None
    territory_id: TerritoryId
    date: GazetteDate
    section: str | None = None
    edition_number: str | None = None
    is_extra_edition: bool = False
    act_type: str
    act_number: str | None = None
    act_year: int | None = None
    title: str
    ementa: str | None = None
    hierarchy: list[str] = Field(default_factory=list)
    authority_name: str | None = None
    authority_role: str | None = None
    source_url: str
    content_hash: DocumentHash
    char_count: int
    raw_content: str
    structured_content: dict[str, object] | None = None
    classification_source: ClassificationSource = ClassificationSource.PRE_SEGMENTED_SOURCE
    classification_confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    hierarchical_group: HierarchicalGroup = HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS
    hierarchical_rank: int = 10
    publication_nature: PublicationNature = PublicationNature.PUBLICIDADE_OPERACIONAL
    canonical_urn: str | None = None
    is_stub: bool = False
    metadata_json: dict[str, object] | None = None
    scraped_at: datetime

    @model_validator(mode="after")
    def _validate_invariants(self) -> Self:
        """Enforces domain invariants on the discrete normative act."""
        if not self.title.strip():
            raise DomainInvariantViolationError("title cannot be empty.")

        if not self.act_type.strip():
            raise DomainInvariantViolationError("act_type cannot be empty.")

        if self.is_stub:
            # Stubs are placeholders for out-of-order reference resolution
            return self

        clean_content = self.raw_content.strip()
        if not clean_content:
            raise DomainInvariantViolationError(
                "raw_content must contain non-whitespace legislative content."
            )

        if self.char_count <= 0:
            raise DomainInvariantViolationError("char_count must be strictly positive.")

        if not (self.source_url.startswith("http://") or self.source_url.startswith("https://")):
            raise DomainInvariantViolationError(
                f"source_url must start with http:// or https://, got '{self.source_url}'."
            )

        return self
