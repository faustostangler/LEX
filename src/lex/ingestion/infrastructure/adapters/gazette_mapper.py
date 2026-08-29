"""Anti-Corruption Layer (ACL) Mapper for Gazette and Normative Acts Ingestion.

Translates untyped RawGazettePayload and RawNormativeActPayload DTOs emitted by Scrapy
spiders into strictly validated GazetteEdition and NormativeAct domain entities.
"""

import re
import uuid
from datetime import UTC, date, datetime

from lex.ingestion.application.ports import StreamTextExtractorPort
from lex.ingestion.domain.entities import GazetteEdition, NormativeAct
from lex.ingestion.domain.exceptions import (
    CorruptedGazettePayloadError,
    InvalidGazetteDateError,
)
from lex.ingestion.domain.value_objects import (
    ClassificationSource,
    DocumentHash,
    FederativeTier,
    GazetteDate,
    IngestionStatus,
    TerritoryId,
)
from lex.ingestion.infrastructure.dto import (
    RawGazettePayload,
    RawNormativeActPayload,
)


class GazetteMapper:
    """Anti-Corruption Layer translator from web scraping DTOs to Domain Entities."""

    def __init__(self, text_extractor: StreamTextExtractorPort) -> None:
        self._extractor = text_extractor

    def to_domain(self, payload: RawGazettePayload) -> GazetteEdition:
        """Translate a RawGazettePayload DTO into a valid GazetteEdition domain entity."""
        summary_text = (
            payload.raw_content
            if isinstance(payload.raw_content, str)
            else (payload.source_url + f"-{payload.total_acts}-{payload.edition_number}")
        )
        resolved_date = self._resolve_date(payload)

        territory_id = TerritoryId.from_code(payload.territory_code)
        tier = FederativeTier(payload.tier.lower())
        gazette_date = GazetteDate.from_date(resolved_date)
        summary_hash = DocumentHash.from_text(summary_text or payload.source_url)

        return GazetteEdition(
            territory_id=territory_id,
            tier=tier,
            date=gazette_date,
            edition_number=payload.edition_number,
            section=payload.section,
            is_extra_edition=payload.is_extra_edition,
            power=payload.power,
            source_url=payload.source_url,
            summary_hash=summary_hash,
            total_acts=payload.total_acts,
            ingestion_status=IngestionStatus.COMPLETED,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def to_normative_act(
        self,
        payload: RawNormativeActPayload,
        edition_id: uuid.UUID | None = None,
    ) -> NormativeAct:
        """Translate a RawNormativeActPayload DTO into a valid NormativeAct domain entity."""
        raw_text = payload.raw_content.strip()
        if not raw_text:
            raise CorruptedGazettePayloadError("Normative act raw_content cannot be empty.")

        content_hash = DocumentHash.from_text(raw_text)
        char_count = len(raw_text)
        territory_id = TerritoryId.from_code(payload.territory_code)
        gazette_date = GazetteDate.from_date(payload.date_obj)

        return NormativeAct(
            edition_id=edition_id,
            territory_id=territory_id,
            date=gazette_date,
            section=payload.section,
            edition_number=payload.edition_number,
            is_extra_edition=payload.is_extra_edition,
            act_type=payload.act_type,
            act_number=payload.act_number,
            act_year=payload.act_year,
            title=payload.title,
            ementa=payload.ementa,
            hierarchy=payload.hierarchy,
            authority_name=payload.authority_name,
            authority_role=payload.authority_role,
            source_url=payload.source_url,
            content_hash=content_hash,
            char_count=char_count,
            raw_content=raw_text,
            classification_source=ClassificationSource(payload.classification_source),
            classification_confidence=payload.classification_confidence,
            metadata_json=payload.metadata_json,
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
