"""Data Transfer Objects (DTO) for Ingestion and Digestion Infrastructure.

Defines the unvalidated payload contracts yielded by Scrapy spiders before
passing through the Anti-Corruption Layer (ACL) into pure domain entities.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any


@dataclass(slots=True)
class RawGazettePayload:
    """Transient DTO representing edition metadata emitted by Scrapy spiders."""

    territory_code: str
    tier: str
    source_url: str
    raw_content: bytes | str = field(default="", repr=False)
    total_acts: int = 0
    raw_date_str: str | None = None
    date_obj: date | None = None
    edition_number: str | None = None
    section: str | None = None
    is_extra_edition: bool = False
    power: str = "executive"
    scraped_at: datetime | None = None


@dataclass(slots=True)
class RawNormativeActPayload:
    """Transient DTO representing an individual normative act emitted by Scrapy spiders."""

    territory_code: str
    source_url: str
    raw_content: str = field(repr=False)
    title: str = ""
    act_type: str = "OUTROS"
    date_obj: date = field(default_factory=date.today)
    act_number: str | None = None
    act_year: int | None = None
    ementa: str | None = None
    hierarchy: list[str] = field(default_factory=list)
    authority_name: str | None = None
    authority_role: str | None = None
    edition_number: str | None = None
    section: str | None = None
    is_extra_edition: bool = False
    classification_source: str = "pre_segmented_source"
    classification_confidence: float = 1.0
    metadata_json: dict[str, Any] | None = field(default=None, repr=False)
    scraped_at: datetime | None = None
