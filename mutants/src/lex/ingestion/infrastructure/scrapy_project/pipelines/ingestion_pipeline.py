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
from lex.ingestion.domain.entities import NormativeAct
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

DEFAULT_PIPELINE_BATCH_SIZE: int = 50


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁGazetteIngestionPipelineǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut: MutantDict = {}  # type: ignore
mutants_xǁGazetteIngestionPipelineǁ_flush_acts__mutmut: MutantDict = {}  # type: ignore
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut: MutantDict = {}  # type: ignore
mutants_xǁGazetteIngestionPipelineǁclose_spider__mutmut: MutantDict = {}  # type: ignore


class GazetteIngestionPipeline:
    """Scrapy pipeline routing payloads to DB with micro-batching (ADR-005)."""

    @_mutmut_mutated(mutants_xǁGazetteIngestionPipelineǁ__init____mutmut)
    def __init__(
        self,
        repository: GazetteRepositoryPort | None = None,
        mapper: GazetteMapper | None = None,
        session: Session | None = None,
        batch_size: int = DEFAULT_PIPELINE_BATCH_SIZE,
    ) -> None:
        self._repository = repository
        self._mapper = mapper
        self._session = session
        self._batch_size = batch_size
        self._act_buffer: list[NormativeAct] = []
        # Cache mapped edition UUIDs: key -> edition_id
        self._edition_id_cache: dict[tuple[str, str, str, str, bool], uuid.UUID] = {}

    def xǁGazetteIngestionPipelineǁ__init____mutmut_orig(
        self,
        repository: GazetteRepositoryPort | None = None,
        mapper: GazetteMapper | None = None,
        session: Session | None = None,
        batch_size: int = DEFAULT_PIPELINE_BATCH_SIZE,
    ) -> None:
        self._repository = repository
        self._mapper = mapper
        self._session = session
        self._batch_size = batch_size
        self._act_buffer: list[NormativeAct] = []
        # Cache mapped edition UUIDs: key -> edition_id
        self._edition_id_cache: dict[tuple[str, str, str, str, bool], uuid.UUID] = {}

    def xǁGazetteIngestionPipelineǁ__init____mutmut_1(
        self,
        repository: GazetteRepositoryPort | None = None,
        mapper: GazetteMapper | None = None,
        session: Session | None = None,
        batch_size: int = DEFAULT_PIPELINE_BATCH_SIZE,
    ) -> None:
        self._repository = None
        self._mapper = mapper
        self._session = session
        self._batch_size = batch_size
        self._act_buffer: list[NormativeAct] = []
        # Cache mapped edition UUIDs: key -> edition_id
        self._edition_id_cache: dict[tuple[str, str, str, str, bool], uuid.UUID] = {}

    def xǁGazetteIngestionPipelineǁ__init____mutmut_2(
        self,
        repository: GazetteRepositoryPort | None = None,
        mapper: GazetteMapper | None = None,
        session: Session | None = None,
        batch_size: int = DEFAULT_PIPELINE_BATCH_SIZE,
    ) -> None:
        self._repository = repository
        self._mapper = None
        self._session = session
        self._batch_size = batch_size
        self._act_buffer: list[NormativeAct] = []
        # Cache mapped edition UUIDs: key -> edition_id
        self._edition_id_cache: dict[tuple[str, str, str, str, bool], uuid.UUID] = {}

    def xǁGazetteIngestionPipelineǁ__init____mutmut_3(
        self,
        repository: GazetteRepositoryPort | None = None,
        mapper: GazetteMapper | None = None,
        session: Session | None = None,
        batch_size: int = DEFAULT_PIPELINE_BATCH_SIZE,
    ) -> None:
        self._repository = repository
        self._mapper = mapper
        self._session = None
        self._batch_size = batch_size
        self._act_buffer: list[NormativeAct] = []
        # Cache mapped edition UUIDs: key -> edition_id
        self._edition_id_cache: dict[tuple[str, str, str, str, bool], uuid.UUID] = {}

    def xǁGazetteIngestionPipelineǁ__init____mutmut_4(
        self,
        repository: GazetteRepositoryPort | None = None,
        mapper: GazetteMapper | None = None,
        session: Session | None = None,
        batch_size: int = DEFAULT_PIPELINE_BATCH_SIZE,
    ) -> None:
        self._repository = repository
        self._mapper = mapper
        self._session = session
        self._batch_size = None
        self._act_buffer: list[NormativeAct] = []
        # Cache mapped edition UUIDs: key -> edition_id
        self._edition_id_cache: dict[tuple[str, str, str, str, bool], uuid.UUID] = {}

    def xǁGazetteIngestionPipelineǁ__init____mutmut_5(
        self,
        repository: GazetteRepositoryPort | None = None,
        mapper: GazetteMapper | None = None,
        session: Session | None = None,
        batch_size: int = DEFAULT_PIPELINE_BATCH_SIZE,
    ) -> None:
        self._repository = repository
        self._mapper = mapper
        self._session = session
        self._batch_size = batch_size
        self._act_buffer: list[NormativeAct] = None
        # Cache mapped edition UUIDs: key -> edition_id
        self._edition_id_cache: dict[tuple[str, str, str, str, bool], uuid.UUID] = {}

    def xǁGazetteIngestionPipelineǁ__init____mutmut_6(
        self,
        repository: GazetteRepositoryPort | None = None,
        mapper: GazetteMapper | None = None,
        session: Session | None = None,
        batch_size: int = DEFAULT_PIPELINE_BATCH_SIZE,
    ) -> None:
        self._repository = repository
        self._mapper = mapper
        self._session = session
        self._batch_size = batch_size
        self._act_buffer: list[NormativeAct] = []
        # Cache mapped edition UUIDs: key -> edition_id
        self._edition_id_cache: dict[tuple[str, str, str, str, bool], uuid.UUID] = None

    @classmethod
    @_mutmut_mutated(mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut, is_classmethod = True)
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

    @classmethod
    def xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_orig(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = LexSettings()
        engine = create_engine(str(settings.database_url), pool_pre_ping=True)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()

        extractor = PdfStreamTextExtractor()
        mapper = GazetteMapper(text_extractor=extractor)
        repository = PostgresGazetteRepository(session=session)

        return cls(repository=repository, mapper=mapper, session=session)

    @classmethod
    def xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_1(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = None
        engine = create_engine(str(settings.database_url), pool_pre_ping=True)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()

        extractor = PdfStreamTextExtractor()
        mapper = GazetteMapper(text_extractor=extractor)
        repository = PostgresGazetteRepository(session=session)

        return cls(repository=repository, mapper=mapper, session=session)

    @classmethod
    def xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_2(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = LexSettings()
        engine = None
        session_factory = sessionmaker(bind=engine)
        session = session_factory()

        extractor = PdfStreamTextExtractor()
        mapper = GazetteMapper(text_extractor=extractor)
        repository = PostgresGazetteRepository(session=session)

        return cls(repository=repository, mapper=mapper, session=session)

    @classmethod
    def xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_3(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = LexSettings()
        engine = create_engine(None, pool_pre_ping=True)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()

        extractor = PdfStreamTextExtractor()
        mapper = GazetteMapper(text_extractor=extractor)
        repository = PostgresGazetteRepository(session=session)

        return cls(repository=repository, mapper=mapper, session=session)

    @classmethod
    def xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_4(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = LexSettings()
        engine = create_engine(str(settings.database_url), pool_pre_ping=None)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()

        extractor = PdfStreamTextExtractor()
        mapper = GazetteMapper(text_extractor=extractor)
        repository = PostgresGazetteRepository(session=session)

        return cls(repository=repository, mapper=mapper, session=session)

    @classmethod
    def xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_5(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = LexSettings()
        engine = create_engine(pool_pre_ping=True)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()

        extractor = PdfStreamTextExtractor()
        mapper = GazetteMapper(text_extractor=extractor)
        repository = PostgresGazetteRepository(session=session)

        return cls(repository=repository, mapper=mapper, session=session)

    @classmethod
    def xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_6(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = LexSettings()
        engine = create_engine(str(settings.database_url), )
        session_factory = sessionmaker(bind=engine)
        session = session_factory()

        extractor = PdfStreamTextExtractor()
        mapper = GazetteMapper(text_extractor=extractor)
        repository = PostgresGazetteRepository(session=session)

        return cls(repository=repository, mapper=mapper, session=session)

    @classmethod
    def xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_7(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = LexSettings()
        engine = create_engine(str(None), pool_pre_ping=True)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()

        extractor = PdfStreamTextExtractor()
        mapper = GazetteMapper(text_extractor=extractor)
        repository = PostgresGazetteRepository(session=session)

        return cls(repository=repository, mapper=mapper, session=session)

    @classmethod
    def xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_8(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = LexSettings()
        engine = create_engine(str(settings.database_url), pool_pre_ping=False)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()

        extractor = PdfStreamTextExtractor()
        mapper = GazetteMapper(text_extractor=extractor)
        repository = PostgresGazetteRepository(session=session)

        return cls(repository=repository, mapper=mapper, session=session)

    @classmethod
    def xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_9(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = LexSettings()
        engine = create_engine(str(settings.database_url), pool_pre_ping=True)
        session_factory = None
        session = session_factory()

        extractor = PdfStreamTextExtractor()
        mapper = GazetteMapper(text_extractor=extractor)
        repository = PostgresGazetteRepository(session=session)

        return cls(repository=repository, mapper=mapper, session=session)

    @classmethod
    def xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_10(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = LexSettings()
        engine = create_engine(str(settings.database_url), pool_pre_ping=True)
        session_factory = sessionmaker(bind=None)
        session = session_factory()

        extractor = PdfStreamTextExtractor()
        mapper = GazetteMapper(text_extractor=extractor)
        repository = PostgresGazetteRepository(session=session)

        return cls(repository=repository, mapper=mapper, session=session)

    @classmethod
    def xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_11(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = LexSettings()
        engine = create_engine(str(settings.database_url), pool_pre_ping=True)
        session_factory = sessionmaker(bind=engine)
        session = None

        extractor = PdfStreamTextExtractor()
        mapper = GazetteMapper(text_extractor=extractor)
        repository = PostgresGazetteRepository(session=session)

        return cls(repository=repository, mapper=mapper, session=session)

    @classmethod
    def xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_12(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = LexSettings()
        engine = create_engine(str(settings.database_url), pool_pre_ping=True)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()

        extractor = None
        mapper = GazetteMapper(text_extractor=extractor)
        repository = PostgresGazetteRepository(session=session)

        return cls(repository=repository, mapper=mapper, session=session)

    @classmethod
    def xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_13(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = LexSettings()
        engine = create_engine(str(settings.database_url), pool_pre_ping=True)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()

        extractor = PdfStreamTextExtractor()
        mapper = None
        repository = PostgresGazetteRepository(session=session)

        return cls(repository=repository, mapper=mapper, session=session)

    @classmethod
    def xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_14(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = LexSettings()
        engine = create_engine(str(settings.database_url), pool_pre_ping=True)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()

        extractor = PdfStreamTextExtractor()
        mapper = GazetteMapper(text_extractor=None)
        repository = PostgresGazetteRepository(session=session)

        return cls(repository=repository, mapper=mapper, session=session)

    @classmethod
    def xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_15(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = LexSettings()
        engine = create_engine(str(settings.database_url), pool_pre_ping=True)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()

        extractor = PdfStreamTextExtractor()
        mapper = GazetteMapper(text_extractor=extractor)
        repository = None

        return cls(repository=repository, mapper=mapper, session=session)

    @classmethod
    def xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_16(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = LexSettings()
        engine = create_engine(str(settings.database_url), pool_pre_ping=True)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()

        extractor = PdfStreamTextExtractor()
        mapper = GazetteMapper(text_extractor=extractor)
        repository = PostgresGazetteRepository(session=None)

        return cls(repository=repository, mapper=mapper, session=session)

    @classmethod
    def xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_17(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = LexSettings()
        engine = create_engine(str(settings.database_url), pool_pre_ping=True)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()

        extractor = PdfStreamTextExtractor()
        mapper = GazetteMapper(text_extractor=extractor)
        repository = PostgresGazetteRepository(session=session)

        return cls(repository=None, mapper=mapper, session=session)

    @classmethod
    def xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_18(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = LexSettings()
        engine = create_engine(str(settings.database_url), pool_pre_ping=True)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()

        extractor = PdfStreamTextExtractor()
        mapper = GazetteMapper(text_extractor=extractor)
        repository = PostgresGazetteRepository(session=session)

        return cls(repository=repository, mapper=None, session=session)

    @classmethod
    def xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_19(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = LexSettings()
        engine = create_engine(str(settings.database_url), pool_pre_ping=True)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()

        extractor = PdfStreamTextExtractor()
        mapper = GazetteMapper(text_extractor=extractor)
        repository = PostgresGazetteRepository(session=session)

        return cls(repository=repository, mapper=mapper, session=None)

    @classmethod
    def xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_20(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = LexSettings()
        engine = create_engine(str(settings.database_url), pool_pre_ping=True)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()

        extractor = PdfStreamTextExtractor()
        mapper = GazetteMapper(text_extractor=extractor)
        repository = PostgresGazetteRepository(session=session)

        return cls(mapper=mapper, session=session)

    @classmethod
    def xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_21(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = LexSettings()
        engine = create_engine(str(settings.database_url), pool_pre_ping=True)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()

        extractor = PdfStreamTextExtractor()
        mapper = GazetteMapper(text_extractor=extractor)
        repository = PostgresGazetteRepository(session=session)

        return cls(repository=repository, session=session)

    @classmethod
    def xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_22(cls, crawler: Crawler) -> "GazetteIngestionPipeline":
        """Instantiate pipeline from Scrapy crawler settings."""
        settings = LexSettings()
        engine = create_engine(str(settings.database_url), pool_pre_ping=True)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()

        extractor = PdfStreamTextExtractor()
        mapper = GazetteMapper(text_extractor=extractor)
        repository = PostgresGazetteRepository(session=session)

        return cls(repository=repository, mapper=mapper, )

    @_mutmut_mutated(mutants_xǁGazetteIngestionPipelineǁ_flush_acts__mutmut)
    def _flush_acts(self) -> None:
        """Persist buffered normative acts in a single bulk transaction and clear buffer."""
        if not self._act_buffer or self._repository is None:
            return

        try:
            self._repository.save_normative_acts_bulk(self._act_buffer)
        except Exception as exc:
            logger.error(f"Error bulk persisting {len(self._act_buffer)} normative acts: {exc}")
        finally:
            self._act_buffer.clear()

    def xǁGazetteIngestionPipelineǁ_flush_acts__mutmut_orig(self) -> None:
        """Persist buffered normative acts in a single bulk transaction and clear buffer."""
        if not self._act_buffer or self._repository is None:
            return

        try:
            self._repository.save_normative_acts_bulk(self._act_buffer)
        except Exception as exc:
            logger.error(f"Error bulk persisting {len(self._act_buffer)} normative acts: {exc}")
        finally:
            self._act_buffer.clear()

    def xǁGazetteIngestionPipelineǁ_flush_acts__mutmut_1(self) -> None:
        """Persist buffered normative acts in a single bulk transaction and clear buffer."""
        if not self._act_buffer and self._repository is None:
            return

        try:
            self._repository.save_normative_acts_bulk(self._act_buffer)
        except Exception as exc:
            logger.error(f"Error bulk persisting {len(self._act_buffer)} normative acts: {exc}")
        finally:
            self._act_buffer.clear()

    def xǁGazetteIngestionPipelineǁ_flush_acts__mutmut_2(self) -> None:
        """Persist buffered normative acts in a single bulk transaction and clear buffer."""
        if self._act_buffer or self._repository is None:
            return

        try:
            self._repository.save_normative_acts_bulk(self._act_buffer)
        except Exception as exc:
            logger.error(f"Error bulk persisting {len(self._act_buffer)} normative acts: {exc}")
        finally:
            self._act_buffer.clear()

    def xǁGazetteIngestionPipelineǁ_flush_acts__mutmut_3(self) -> None:
        """Persist buffered normative acts in a single bulk transaction and clear buffer."""
        if not self._act_buffer or self._repository is not None:
            return

        try:
            self._repository.save_normative_acts_bulk(self._act_buffer)
        except Exception as exc:
            logger.error(f"Error bulk persisting {len(self._act_buffer)} normative acts: {exc}")
        finally:
            self._act_buffer.clear()

    def xǁGazetteIngestionPipelineǁ_flush_acts__mutmut_4(self) -> None:
        """Persist buffered normative acts in a single bulk transaction and clear buffer."""
        if not self._act_buffer or self._repository is None:
            return

        try:
            self._repository.save_normative_acts_bulk(None)
        except Exception as exc:
            logger.error(f"Error bulk persisting {len(self._act_buffer)} normative acts: {exc}")
        finally:
            self._act_buffer.clear()

    def xǁGazetteIngestionPipelineǁ_flush_acts__mutmut_5(self) -> None:
        """Persist buffered normative acts in a single bulk transaction and clear buffer."""
        if not self._act_buffer or self._repository is None:
            return

        try:
            self._repository.save_normative_acts_bulk(self._act_buffer)
        except Exception as exc:
            logger.error(None)
        finally:
            self._act_buffer.clear()

    @_mutmut_mutated(mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut)
    def process_item(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_orig(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_1(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None and self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_2(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is not None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_3(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is not None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_4(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
            try:
                edition = None
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_5(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
            try:
                edition = self._mapper.to_domain(None)
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_6(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
            try:
                edition = self._mapper.to_domain(item)
                saved_edition = None
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_7(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
            try:
                edition = self._mapper.to_domain(item)
                saved_edition = self._repository.save(None)
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_8(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
            try:
                edition = self._mapper.to_domain(item)
                saved_edition = self._repository.save(edition)
                persisted_id = None

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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_9(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
            try:
                edition = self._mapper.to_domain(item)
                saved_edition = self._repository.save(edition)
                persisted_id = saved_edition.id and uuid.uuid4()

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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_10(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
            try:
                edition = self._mapper.to_domain(item)
                saved_edition = self._repository.save(edition)
                persisted_id = saved_edition.id or uuid.uuid4()

                cache_key = None
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_11(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
            try:
                edition = self._mapper.to_domain(item)
                saved_edition = self._repository.save(edition)
                persisted_id = saved_edition.id or uuid.uuid4()

                cache_key = (
                    item.territory_code,
                    str(None),
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_12(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
            try:
                edition = self._mapper.to_domain(item)
                saved_edition = self._repository.save(edition)
                persisted_id = saved_edition.id or uuid.uuid4()

                cache_key = (
                    item.territory_code,
                    str(edition.date.value),
                    str(None),
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_13(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
            try:
                edition = self._mapper.to_domain(item)
                saved_edition = self._repository.save(edition)
                persisted_id = saved_edition.id or uuid.uuid4()

                cache_key = (
                    item.territory_code,
                    str(edition.date.value),
                    str(item.section and ""),
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_14(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
            try:
                edition = self._mapper.to_domain(item)
                saved_edition = self._repository.save(edition)
                persisted_id = saved_edition.id or uuid.uuid4()

                cache_key = (
                    item.territory_code,
                    str(edition.date.value),
                    str(item.section or "XXXX"),
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_15(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
            try:
                edition = self._mapper.to_domain(item)
                saved_edition = self._repository.save(edition)
                persisted_id = saved_edition.id or uuid.uuid4()

                cache_key = (
                    item.territory_code,
                    str(edition.date.value),
                    str(item.section or ""),
                    str(None),
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_16(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
            try:
                edition = self._mapper.to_domain(item)
                saved_edition = self._repository.save(edition)
                persisted_id = saved_edition.id or uuid.uuid4()

                cache_key = (
                    item.territory_code,
                    str(edition.date.value),
                    str(item.section or ""),
                    str(item.edition_number and ""),
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_17(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
            try:
                edition = self._mapper.to_domain(item)
                saved_edition = self._repository.save(edition)
                persisted_id = saved_edition.id or uuid.uuid4()

                cache_key = (
                    item.territory_code,
                    str(edition.date.value),
                    str(item.section or ""),
                    str(item.edition_number or "XXXX"),
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_18(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                self._edition_id_cache[cache_key] = None
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_19(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                logger.error(None)

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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_20(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
            cache_key = None
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_21(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                str(None),
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_22(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                str(None),
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_23(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                str(item.section and ""),
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_24(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                str(item.section or "XXXX"),
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_25(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                str(None),
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_26(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                str(item.edition_number and ""),
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_27(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                str(item.edition_number or "XXXX"),
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_28(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
            cached_id = None
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_29(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
            cached_id = self._edition_id_cache.get(None)
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_30(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
            if cached_id is None:
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_31(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                final_edition_id = None
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_32(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                existing_edition = None
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_33(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                    territory_id=None,
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_34(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                    date=None,
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_35(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                    section=None,
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_36(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_37(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_38(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_39(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                    territory_id=TerritoryId.from_code(None),
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_40(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                    date=GazetteDate.from_date(None),
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_41(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                if existing_edition is not None or existing_edition.id is not None:
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_42(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                if existing_edition is None and existing_edition.id is not None:
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_43(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                if existing_edition is not None and existing_edition.id is None:
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_44(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                    final_edition_id = None
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_45(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                    synth_payload = None
                    synth_edition = self._mapper.to_domain(synth_payload)
                    saved_synth = self._repository.save(synth_edition)
                    final_edition_id = saved_synth.id or uuid.uuid4()

                self._edition_id_cache[cache_key] = final_edition_id

            try:
                act = self._mapper.to_normative_act(item, edition_id=final_edition_id)
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_46(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                        territory_code=None,
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_47(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                        tier=None,
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_48(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                        source_url=None,
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_49(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                        raw_content=None,
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_50(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                        total_acts=None,
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_51(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                        date_obj=None,
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_52(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                        section=None,
                        edition_number=item.edition_number,
                        is_extra_edition=item.is_extra_edition,
                    )
                    synth_edition = self._mapper.to_domain(synth_payload)
                    saved_synth = self._repository.save(synth_edition)
                    final_edition_id = saved_synth.id or uuid.uuid4()

                self._edition_id_cache[cache_key] = final_edition_id

            try:
                act = self._mapper.to_normative_act(item, edition_id=final_edition_id)
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_53(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                        edition_number=None,
                        is_extra_edition=item.is_extra_edition,
                    )
                    synth_edition = self._mapper.to_domain(synth_payload)
                    saved_synth = self._repository.save(synth_edition)
                    final_edition_id = saved_synth.id or uuid.uuid4()

                self._edition_id_cache[cache_key] = final_edition_id

            try:
                act = self._mapper.to_normative_act(item, edition_id=final_edition_id)
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_54(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                        is_extra_edition=None,
                    )
                    synth_edition = self._mapper.to_domain(synth_payload)
                    saved_synth = self._repository.save(synth_edition)
                    final_edition_id = saved_synth.id or uuid.uuid4()

                self._edition_id_cache[cache_key] = final_edition_id

            try:
                act = self._mapper.to_normative_act(item, edition_id=final_edition_id)
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_55(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_56(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_57(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_58(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_59(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_60(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_61(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                        edition_number=item.edition_number,
                        is_extra_edition=item.is_extra_edition,
                    )
                    synth_edition = self._mapper.to_domain(synth_payload)
                    saved_synth = self._repository.save(synth_edition)
                    final_edition_id = saved_synth.id or uuid.uuid4()

                self._edition_id_cache[cache_key] = final_edition_id

            try:
                act = self._mapper.to_normative_act(item, edition_id=final_edition_id)
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_62(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                        is_extra_edition=item.is_extra_edition,
                    )
                    synth_edition = self._mapper.to_domain(synth_payload)
                    saved_synth = self._repository.save(synth_edition)
                    final_edition_id = saved_synth.id or uuid.uuid4()

                self._edition_id_cache[cache_key] = final_edition_id

            try:
                act = self._mapper.to_normative_act(item, edition_id=final_edition_id)
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_63(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                        )
                    synth_edition = self._mapper.to_domain(synth_payload)
                    saved_synth = self._repository.save(synth_edition)
                    final_edition_id = saved_synth.id or uuid.uuid4()

                self._edition_id_cache[cache_key] = final_edition_id

            try:
                act = self._mapper.to_normative_act(item, edition_id=final_edition_id)
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_64(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                        tier="XXfederalXX",
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_65(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                        tier="FEDERAL",
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_66(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                        total_acts=1,
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_67(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                    synth_edition = None
                    saved_synth = self._repository.save(synth_edition)
                    final_edition_id = saved_synth.id or uuid.uuid4()

                self._edition_id_cache[cache_key] = final_edition_id

            try:
                act = self._mapper.to_normative_act(item, edition_id=final_edition_id)
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_68(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                    synth_edition = self._mapper.to_domain(None)
                    saved_synth = self._repository.save(synth_edition)
                    final_edition_id = saved_synth.id or uuid.uuid4()

                self._edition_id_cache[cache_key] = final_edition_id

            try:
                act = self._mapper.to_normative_act(item, edition_id=final_edition_id)
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_69(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                    saved_synth = None
                    final_edition_id = saved_synth.id or uuid.uuid4()

                self._edition_id_cache[cache_key] = final_edition_id

            try:
                act = self._mapper.to_normative_act(item, edition_id=final_edition_id)
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_70(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                    saved_synth = self._repository.save(None)
                    final_edition_id = saved_synth.id or uuid.uuid4()

                self._edition_id_cache[cache_key] = final_edition_id

            try:
                act = self._mapper.to_normative_act(item, edition_id=final_edition_id)
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_71(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                    final_edition_id = None

                self._edition_id_cache[cache_key] = final_edition_id

            try:
                act = self._mapper.to_normative_act(item, edition_id=final_edition_id)
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_72(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                    final_edition_id = saved_synth.id and uuid.uuid4()

                self._edition_id_cache[cache_key] = final_edition_id

            try:
                act = self._mapper.to_normative_act(item, edition_id=final_edition_id)
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_73(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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

                self._edition_id_cache[cache_key] = None

            try:
                act = self._mapper.to_normative_act(item, edition_id=final_edition_id)
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_74(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                act = None
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_75(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                act = self._mapper.to_normative_act(None, edition_id=final_edition_id)
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_76(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                act = self._mapper.to_normative_act(item, edition_id=None)
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_77(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                act = self._mapper.to_normative_act(edition_id=final_edition_id)
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_78(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                act = self._mapper.to_normative_act(item, )
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_79(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                self._act_buffer.append(None)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_80(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                self._act_buffer.append(act)
                if len(self._act_buffer) > self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(f"Error preparing normative act {item.source_url}: {exc}")

        return item

    def xǁGazetteIngestionPipelineǁprocess_item__mutmut_81(self, item: Any, spider: Any = None) -> Any:
        """Process yielded items through ACL mapper and domain repository with micro-batching."""
        if self._mapper is None or self._repository is None:
            return item

        if isinstance(item, RawGazettePayload):
            # Flush any pending acts from a previous edition before processing new edition
            self._flush_acts()
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
                self._act_buffer.append(act)
                if len(self._act_buffer) >= self._batch_size:
                    self._flush_acts()
            except Exception as exc:
                logger.error(None)

        return item

    @_mutmut_mutated(mutants_xǁGazetteIngestionPipelineǁclose_spider__mutmut)
    def close_spider(self, spider: Any = None) -> None:
        """Flush any pending buffered acts and clean up database session on spider shutdown."""
        self._flush_acts()
        if self._session is not None:
            self._session.close()

    def xǁGazetteIngestionPipelineǁclose_spider__mutmut_orig(self, spider: Any = None) -> None:
        """Flush any pending buffered acts and clean up database session on spider shutdown."""
        self._flush_acts()
        if self._session is not None:
            self._session.close()

    def xǁGazetteIngestionPipelineǁclose_spider__mutmut_1(self, spider: Any = None) -> None:
        """Flush any pending buffered acts and clean up database session on spider shutdown."""
        self._flush_acts()
        if self._session is None:
            self._session.close()

mutants_xǁGazetteIngestionPipelineǁ__init____mutmut['_mutmut_orig'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁ__init____mutmut['xǁGazetteIngestionPipelineǁ__init____mutmut_1'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁ__init____mutmut['xǁGazetteIngestionPipelineǁ__init____mutmut_2'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁ__init____mutmut['xǁGazetteIngestionPipelineǁ__init____mutmut_3'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁ__init____mutmut_3 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁ__init____mutmut['xǁGazetteIngestionPipelineǁ__init____mutmut_4'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁ__init____mutmut_4 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁ__init____mutmut['xǁGazetteIngestionPipelineǁ__init____mutmut_5'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁ__init____mutmut_5 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁ__init____mutmut['xǁGazetteIngestionPipelineǁ__init____mutmut_6'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁ__init____mutmut_6 # type: ignore # mutmut generated

mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut['_mutmut_orig'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_orig # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut['xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_1'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_1 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut['xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_2'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_2 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut['xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_3'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_3 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut['xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_4'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_4 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut['xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_5'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_5 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut['xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_6'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_6 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut['xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_7'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_7 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut['xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_8'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_8 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut['xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_9'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_9 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut['xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_10'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_10 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut['xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_11'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_11 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut['xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_12'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_12 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut['xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_13'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_13 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut['xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_14'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_14 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut['xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_15'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_15 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut['xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_16'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_16 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut['xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_17'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_17 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut['xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_18'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_18 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut['xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_19'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_19 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut['xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_20'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_20 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut['xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_21'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_21 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁfrom_crawler__mutmut['xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_22'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁfrom_crawler__mutmut_22 # type: ignore # mutmut generated

mutants_xǁGazetteIngestionPipelineǁ_flush_acts__mutmut['_mutmut_orig'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁ_flush_acts__mutmut_orig # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁ_flush_acts__mutmut['xǁGazetteIngestionPipelineǁ_flush_acts__mutmut_1'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁ_flush_acts__mutmut_1 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁ_flush_acts__mutmut['xǁGazetteIngestionPipelineǁ_flush_acts__mutmut_2'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁ_flush_acts__mutmut_2 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁ_flush_acts__mutmut['xǁGazetteIngestionPipelineǁ_flush_acts__mutmut_3'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁ_flush_acts__mutmut_3 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁ_flush_acts__mutmut['xǁGazetteIngestionPipelineǁ_flush_acts__mutmut_4'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁ_flush_acts__mutmut_4 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁ_flush_acts__mutmut['xǁGazetteIngestionPipelineǁ_flush_acts__mutmut_5'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁ_flush_acts__mutmut_5 # type: ignore # mutmut generated

mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['_mutmut_orig'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_orig # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_1'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_1 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_2'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_2 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_3'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_3 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_4'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_4 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_5'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_5 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_6'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_6 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_7'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_7 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_8'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_8 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_9'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_9 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_10'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_10 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_11'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_11 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_12'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_12 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_13'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_13 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_14'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_14 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_15'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_15 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_16'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_16 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_17'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_17 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_18'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_18 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_19'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_19 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_20'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_20 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_21'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_21 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_22'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_22 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_23'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_23 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_24'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_24 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_25'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_25 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_26'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_26 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_27'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_27 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_28'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_28 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_29'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_29 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_30'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_30 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_31'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_31 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_32'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_32 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_33'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_33 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_34'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_34 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_35'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_35 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_36'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_36 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_37'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_37 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_38'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_38 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_39'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_39 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_40'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_40 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_41'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_41 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_42'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_42 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_43'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_43 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_44'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_44 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_45'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_45 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_46'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_46 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_47'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_47 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_48'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_48 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_49'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_49 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_50'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_50 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_51'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_51 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_52'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_52 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_53'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_53 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_54'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_54 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_55'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_55 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_56'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_56 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_57'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_57 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_58'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_58 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_59'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_59 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_60'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_60 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_61'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_61 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_62'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_62 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_63'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_63 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_64'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_64 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_65'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_65 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_66'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_66 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_67'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_67 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_68'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_68 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_69'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_69 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_70'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_70 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_71'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_71 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_72'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_72 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_73'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_73 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_74'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_74 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_75'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_75 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_76'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_76 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_77'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_77 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_78'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_78 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_79'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_79 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_80'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_80 # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁprocess_item__mutmut['xǁGazetteIngestionPipelineǁprocess_item__mutmut_81'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁprocess_item__mutmut_81 # type: ignore # mutmut generated

mutants_xǁGazetteIngestionPipelineǁclose_spider__mutmut['_mutmut_orig'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁclose_spider__mutmut_orig # type: ignore # mutmut generated
mutants_xǁGazetteIngestionPipelineǁclose_spider__mutmut['xǁGazetteIngestionPipelineǁclose_spider__mutmut_1'] = GazetteIngestionPipeline.xǁGazetteIngestionPipelineǁclose_spider__mutmut_1 # type: ignore # mutmut generated
