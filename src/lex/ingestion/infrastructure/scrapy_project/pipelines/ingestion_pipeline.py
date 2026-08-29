"""Scrapy Item Pipeline for Gazette and Normative Acts Ingestion and Persistence.

Acts as the Hexagonal boundary integration between Scrapy crawler engines,
the GazetteMapper Anti-Corruption Layer, and the GazetteRepositoryPort adapter.
"""

import logging
import uuid
from typing import Any

from scrapy.crawler import Crawler
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from lex.ingestion.application.ports import GazetteRepositoryPort
from lex.ingestion.domain.value_objects import GazetteDate, TerritoryId
from lex.ingestion.infrastructure.adapters.gazette_mapper import GazetteMapper
from lex.ingestion.infrastructure.adapters.stream_extractor import (
    PdfStreamTextExtractor,
)
from lex.ingestion.infrastructure.dto import (
    RawGazettePayload,
    RawNormativeActPayload,
)
from lex.ingestion.infrastructure.persistence.postgres_repository import (
    PostgresGazetteRepository,
)
from lex.shared_kernel.config import LexSettings

logger = logging.getLogger(__name__)


class GazetteIngestionPipeline:
    """Scrapy pipeline routing RawGazettePayload and RawNormativeActPayload items to DB."""

    def __init__(
        self,
        repository: GazetteRepositoryPort | None = None,
        mapper: GazetteMapper | None = None,
        session: Session | None = None,
    ) -> None:
        self._repository = repository
        self._mapper = mapper
        self._session = session
        # Cache mapped edition UUIDs: key -> edition_id
        self._edition_id_cache: dict[tuple[str, str, str, str, bool], uuid.UUID] = {}

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = LexSettings()
        engine = create_engine(str(settings.database_url), pool_pre_ping=True)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()

        extractor = PdfStreamTextExtractor()
        mapper = GazetteMapper(text_extractor=extractor)
        repository = PostgresGazetteRepository(session=session)

        return cls(repository=repository, mapper=mapper, session=session)

    def process_item(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            try:
                edition = self._mapper.to_domain(item)
                saved_edition = self._repository.save(edition)
                persisted_id = saved_edition.id or uuid.uuid4()

                cache_key = (
                    item.territory_code,
                    str(edition.date.value),
                    str(item.section or ""),
                    str(item.edition_number or ""),
                    item.is_extra_edition,
                )
                self._edition_id_cache[cache_key] = persisted_id
            except Exception as exc:
                logger.error(f"Error persisting edition container {item.source_url}: {exc}")

        elif isinstance(item, RawNormativeActPayload):
            cache_key = (
                item.territory_code,
                str(item.date_obj),
                str(item.section or ""),
                str(item.edition_number or ""),
                item.is_extra_edition,
            )
            cached_id = self._edition_id_cache.get(cache_key)
            final_edition_id: uuid.UUID
            if cached_id is not None:
                final_edition_id = cached_id
            else:
                existing_edition = self._repository.get_by_territory_and_date(
                    territory_id=TerritoryId.from_code(item.territory_code),
                    date=GazetteDate.from_date(item.date_obj),
                    section=item.section,
                )
                if existing_edition is not None and existing_edition.id is not None:
                    final_edition_id = existing_edition.id
                else:
                    # Dynamically create container edition to ensure referential integrity
                    synth_payload = RawGazettePayload(
                        territory_code=item.territory_code,
                        tier="federal",
                        source_url=item.source_url,
                        raw_content=f"Auto-generated container ({item.date_obj})",
                        total_acts=0,
                        date_obj=item.date_obj,
                        section=item.section,
                        edition_number=item.edition_number,
                        is_extra_edition=item.is_extra_edition,
                    )
                    synth_edition = self._mapper.to_domain(synth_payload)
                    saved_synth = self._repository.save(synth_edition)
                    final_edition_id = saved_synth.id or uuid.uuid4()

                self._edition_id_cache[cache_key] = final_edition_id

            try:
                act = self._mapper.to_normative_act(item, edition_id=final_edition_id)
                self._repository.save_normative_act(act)
            except Exception as exc:
                logger.error(f"Error persisting normative act {item.source_url}: {exc}")

        return item

    def close_spider(self, spider: Any = None) -> None:
        """Clean up database session upon spider termination."""
        if self._session is not None:
            self._session.close()
