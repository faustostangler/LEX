"""Data Transfer Objects (DTO) for Ingestion Infrastructure.

Defines the unvalidated payload contract yielded by Scrapy spiders before
passing through the Anti-Corruption Layer (ACL) into pure domain entities.
"""

from dataclasses import dataclass
from datetime import date, datetime


@dataclass(slots=True)
class RawGazettePayload:
    """Transient DTO emitted by Scrapy spiders before domain validation."""

    territory_code: str
    tier: str
    source_url: str
    raw_content: bytes | str
    raw_date_str: str | None = None
    date_obj: date | None = None
    edition_number: str | None = None
    section: str | None = None
    is_extra_edition: bool = False
    power: str = "executive"
    scraped_at: datetime | None = None
