"""Anti-Corruption Layer (ACL) Mapper for Gazette Ingestion.

Translates untyped RawGazettePayload DTOs emitted by Scrapy spiders into strictly
validated GazetteEdition domain entities, isolating scraping details from core domain rules.
"""

import re
from datetime import UTC, date, datetime

from lex.ingestion.application.ports import StreamTextExtractorPort
from lex.ingestion.domain.entities import GazetteEdition
from lex.ingestion.domain.exceptions import (
    CorruptedGazettePayloadError,
    InvalidGazetteDateError,
)
from lex.ingestion.domain.value_objects import (
    DocumentHash,
    FederativeTier,
    GazetteDate,
    TerritoryId,
)
from lex.ingestion.infrastructure.dto import RawGazettePayload


class GazetteMapper:
    """Anti-Corruption Layer translator from web scraping DTO to Domain Entity."""

    def __init__(self, text_extractor: StreamTextExtractorPort) -> None:
        self._extractor = text_extractor

    def to_domain(self, payload: RawGazettePayload) -> GazetteEdition:
        """Translate a RawGazettePayload DTO into a valid GazetteEdition domain entity."""
        # Step 1: In-Memory Text Extraction
        if isinstance(payload.raw_content, bytes):
            extracted_text = self._extractor.extract_text(payload.raw_content)
        elif isinstance(payload.raw_content, str):
            extracted_text = payload.raw_content
        else:
            raise CorruptedGazettePayloadError(
                f"Unsupported raw_content type '{type(payload.raw_content).__name__}'."
            )

        # Step 2: Date Resolution & Normalization
        resolved_date = self._resolve_date(payload)

        # Step 3: Domain Model Assembly
        territory_id = TerritoryId.from_code(payload.territory_code)
        tier = FederativeTier(payload.tier.lower())
        gazette_date = GazetteDate.from_date(resolved_date)
        file_hash = DocumentHash.from_text(extracted_text)
        char_count = len(extracted_text.strip())

        return GazetteEdition(
            territory_id=territory_id,
            tier=tier,
            date=gazette_date,
            edition_number=payload.edition_number,
            section=payload.section,
            is_extra_edition=payload.is_extra_edition,
            power=payload.power,
            source_url=payload.source_url,
            file_hash=file_hash,
            char_count=char_count,
            full_text=extracted_text,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    @staticmethod
    def _resolve_date(payload: RawGazettePayload) -> date:
        """Resolve date from date_obj or standard Brazilian string representations."""
        if payload.date_obj is not None:
            return payload.date_obj

        if payload.raw_date_str is None:
            raise InvalidGazetteDateError("No publication date provided in payload.")

        raw_str = payload.raw_date_str.strip()

        # Try ISO format YYYY-MM-DD
        if re.match(r"^\d{4}-\d{2}-\d{2}$", raw_str):
            try:
                return datetime.strptime(raw_str, "%Y-%m-%d").replace(tzinfo=UTC).date()
            except ValueError as exc:
                err_msg = f"Unable to parse date string '{raw_str}': {exc}"
                raise InvalidGazetteDateError(err_msg) from exc

        # Try Brazilian formats DD/MM/YYYY or DD-MM-YYYY
        for fmt in ("%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(raw_str, fmt).replace(tzinfo=UTC).date()
            except ValueError:
                continue

        raise InvalidGazetteDateError(
            f"Unable to parse date string '{raw_str}'. Expected ISO or Brazilian format."
        )
