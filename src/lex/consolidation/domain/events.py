"""Domain Events for the Consolidation Bounded Context."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from lex.consolidation.domain.value_objects import CanonicalUrn


class NormativeActHydrated(BaseModel):
    """Domain Event published when an un-ingested base statute is scraped and hydrated.

    Triggers the PureAstReducer to recompile all accumulated historical mutations.
    """

    model_config = ConfigDict(frozen=True)

    act_id: UUID
    canonical_urn: CanonicalUrn
    hydrated_at: datetime
