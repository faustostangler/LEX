"""Scrapy Item Pipeline for Gazette Ingestion and Persistence.

Acts as the Hexagonal boundary integration between Scrapy crawler engines,
the GazetteMapper Anti-Corruption Layer, and the GazetteRepositoryPort adapter.
"""

from typing import Any

from scrapy.crawler import Crawler
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from lex.ingestion.application.ports import GazetteRepositoryPort
from lex.ingestion.infrastructure.adapters.gazette_mapper import GazetteMapper
from lex.ingestion.infrastructure.adapters.stream_extractor import (
    PdfStreamTextExtractor,
)
from lex.ingestion.infrastructure.dto import RawGazettePayload
from lex.ingestion.infrastructure.persistence.postgres_repository import (
    PostgresGazetteRepository,
)
from lex.shared_kernel.config import LexSettings


class GazetteIngestionPipeline:
    """Scrapy pipeline that routes RawGazettePayload items to the domain repository."""

    def __init__(
        self,
        repository: GazetteRepositoryPort | None = None,
        mapper: GazetteMapper | None = None,
        session: Session | None = None,
    ) -> None:
        self._repository = repository
        self._mapper = mapper
        self._session = session

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
        """Process yielded item through ACL mapper and domain repository."""
        if isinstance(item, RawGazettePayload):
            if self._mapper is not None and self._repository is not None:
                edition = self._mapper.to_domain(item)
                self._repository.save(edition)
        return item

    def close_spider(self, spider: Any = None) -> None:
        """Clean up database session upon spider termination."""
        if self._session is not None:
            self._session.close()
