"""PostgreSQL 16 Implementation of the Gazette and Normative Acts Repository Port.

Uses SQLAlchemy 2.0 ORM and native PostgreSQL dialect features to persist GazetteEdition and
NormativeAct discrete legal entities with idempotent ON CONFLICT resolution and TOAST compression.
"""

import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from lex.ingestion.application.ports import GazetteRepositoryPort
from lex.ingestion.domain.entities import GazetteEdition, NormativeAct
from lex.ingestion.domain.value_objects import (
    ClassificationSource,
    DocumentHash,
    FederativeTier,
    GazetteDate,
    IngestionStatus,
    TerritoryId,
)
from lex.ingestion.infrastructure.persistence.models import (
    GazetteEditionModel,
    NormativeActModel,
)


class PostgresGazetteRepository(GazetteRepositoryPort):
    """Hexagonal Adapter fulfilling GazetteRepositoryPort via PostgreSQL 16."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, edition: GazetteEdition) -> None:
        """Persist a GazetteEdition container record with idempotent upsert."""
        bind = self._session.get_bind()
        is_postgres = bind is not None and bind.dialect.name == "postgresql"

        try:
            if is_postgres:
                stmt = pg_insert(GazetteEditionModel).values(
                    id=edition.id or uuid.uuid4(),
                    territory_id=edition.territory_id.code,
                    tier=edition.tier.value,
                    date=edition.date.value,
                    edition_number=edition.edition_number,
                    section=edition.section,
                    is_extra_edition=edition.is_extra_edition,
                    power=edition.power,
                    source_url=edition.source_url,
                    summary_sha256=edition.summary_hash.hex_digest,
                    total_acts=edition.total_acts,
                    ingestion_status=edition.ingestion_status.value,
                    scraped_at=edition.scraped_at,
                )
                upsert_stmt = stmt.on_conflict_do_update(
                    constraint="uq_gazette_edition_natural_key",
                    set_={
                        "summary_sha256": stmt.excluded.summary_sha256,
                        "total_acts": stmt.excluded.total_acts,
                        "ingestion_status": stmt.excluded.ingestion_status,
                        "source_url": stmt.excluded.source_url,
                        "updated_at": datetime.now(UTC),
                    },
                )
                self._session.execute(upsert_stmt)
            else:
                existing = self._session.execute(
                    select(GazetteEditionModel).where(
                        GazetteEditionModel.territory_id == edition.territory_id.code,
                        GazetteEditionModel.date == edition.date.value,
                        GazetteEditionModel.edition_number == edition.edition_number,
                        GazetteEditionModel.section == edition.section,
                        GazetteEditionModel.is_extra_edition == edition.is_extra_edition,
                    )
                ).scalar_one_or_none()

                if existing is not None:
                    existing.summary_sha256 = edition.summary_hash.hex_digest
                    existing.total_acts = edition.total_acts
                    existing.ingestion_status = edition.ingestion_status.value
                    existing.source_url = edition.source_url
                    existing.updated_at = datetime.now(UTC)
                else:
                    model = GazetteEditionModel(
                        id=edition.id or uuid.uuid4(),
                        territory_id=edition.territory_id.code,
                        tier=edition.tier.value,
                        date=edition.date.value,
                        edition_number=edition.edition_number,
                        section=edition.section,
                        is_extra_edition=edition.is_extra_edition,
                        power=edition.power,
                        source_url=edition.source_url,
                        summary_sha256=edition.summary_hash.hex_digest,
                        total_acts=edition.total_acts,
                        ingestion_status=edition.ingestion_status.value,
                        scraped_at=edition.scraped_at,
                    )
                    self._session.add(model)

            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

    def get_by_territory_and_date(
        self,
        territory_id: TerritoryId,
        date: GazetteDate,
        section: str | None = None,
    ) -> GazetteEdition | None:
        """Retrieve a gazette edition container by territory, date and section."""
        stmt = select(GazetteEditionModel).where(
            GazetteEditionModel.territory_id == territory_id.code,
            GazetteEditionModel.date == date.value,
        )
        if section is not None:
            stmt = stmt.where(GazetteEditionModel.section == section)

        model = self._session.execute(stmt).scalars().first()
        if model is None:
            return None

        return GazetteEdition(
            id=model.id,
            territory_id=TerritoryId.from_code(model.territory_id),
            tier=FederativeTier(model.tier),
            date=GazetteDate.from_date(model.date),
            edition_number=model.edition_number,
            section=model.section,
            is_extra_edition=model.is_extra_edition,
            power=model.power,
            source_url=model.source_url,
            summary_hash=DocumentHash.from_hex(model.summary_sha256),
            total_acts=model.total_acts,
            ingestion_status=IngestionStatus(model.ingestion_status),
            scraped_at=model.scraped_at,
        )

    def exists_by_hash(self, file_hash: DocumentHash) -> bool:
        """Check if an edition container already exists matching summary_hash."""
        stmt = select(GazetteEditionModel.id).where(
            GazetteEditionModel.summary_sha256 == file_hash.hex_digest
        )
        result = self._session.execute(stmt).first()
        return result is not None

    def save_normative_act(self, act: NormativeAct) -> None:
        """Persist a discrete normative act with idempotent ON CONFLICT semantics."""
        self.save_normative_acts_bulk([act])

    def save_normative_acts_bulk(self, acts: list[NormativeAct]) -> None:
        """Persist a batch of discrete normative acts with bulk upsert and rollback safety."""
        if not acts:
            return

        bind = self._session.get_bind()
        is_postgres = bind is not None and bind.dialect.name == "postgresql"

        try:
            if is_postgres:
                for act in acts:
                    stmt = pg_insert(NormativeActModel).values(
                        id=act.id or uuid.uuid4(),
                        edition_id=act.edition_id,
                        territory_id=act.territory_id.code,
                        date=act.date.value,
                        section=act.section,
                        edition_number=act.edition_number,
                        is_extra_edition=act.is_extra_edition,
                        act_type=act.act_type,
                        act_number=act.act_number,
                        act_year=act.act_year,
                        title=act.title,
                        ementa=act.ementa,
                        hierarchy=act.hierarchy,
                        authority_name=act.authority_name,
                        authority_role=act.authority_role,
                        source_url=act.source_url,
                        content_sha256=act.content_hash.hex_digest,
                        char_count=act.char_count,
                        raw_content=act.raw_content,
                        structured_content=act.structured_content,
                        classification_source=act.classification_source.value,
                        classification_confidence=act.classification_confidence,
                        metadata_json=act.metadata_json,
                        scraped_at=act.scraped_at,
                    )
                    upsert_stmt = stmt.on_conflict_do_update(
                        constraint="uq_normative_act_natural_key",
                        set_={
                            "title": stmt.excluded.title,
                            "ementa": stmt.excluded.ementa,
                            "hierarchy": stmt.excluded.hierarchy,
                            "authority_name": stmt.excluded.authority_name,
                            "authority_role": stmt.excluded.authority_role,
                            "raw_content": stmt.excluded.raw_content,
                            "char_count": stmt.excluded.char_count,
                            "updated_at": datetime.now(UTC),
                        },
                    )
                    self._session.execute(upsert_stmt)
            else:
                for act in acts:
                    existing = self._session.execute(
                        select(NormativeActModel).where(
                            NormativeActModel.edition_id == act.edition_id,
                            NormativeActModel.source_url == act.source_url,
                            NormativeActModel.content_sha256 == act.content_hash.hex_digest,
                        )
                    ).scalar_one_or_none()

                    if existing is not None:
                        existing.title = act.title
                        existing.ementa = act.ementa
                        existing.hierarchy = act.hierarchy
                        existing.authority_name = act.authority_name
                        existing.authority_role = act.authority_role
                        existing.raw_content = act.raw_content
                        existing.char_count = act.char_count
                        existing.updated_at = datetime.now(UTC)
                    else:
                        model = NormativeActModel(
                            id=act.id or uuid.uuid4(),
                            edition_id=act.edition_id,
                            territory_id=act.territory_id.code,
                            date=act.date.value,
                            section=act.section,
                            edition_number=act.edition_number,
                            is_extra_edition=act.is_extra_edition,
                            act_type=act.act_type,
                            act_number=act.act_number,
                            act_year=act.act_year,
                            title=act.title,
                            ementa=act.ementa,
                            hierarchy=act.hierarchy,
                            authority_name=act.authority_name,
                            authority_role=act.authority_role,
                            source_url=act.source_url,
                            content_sha256=act.content_hash.hex_digest,
                            char_count=act.char_count,
                            raw_content=act.raw_content,
                            structured_content=act.structured_content,
                            classification_source=act.classification_source.value,
                            classification_confidence=act.classification_confidence,
                            metadata_json=act.metadata_json,
                            scraped_at=act.scraped_at,
                        )
                        self._session.add(model)

            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

    def get_act_by_id(self, act_id: uuid.UUID) -> NormativeAct | None:
        """Retrieve an individual normative act by primary key."""
        model = self._session.execute(
            select(NormativeActModel).where(NormativeActModel.id == act_id)
        ).scalar_one_or_none()
        if model is None:
            return None
        return self._map_act_model_to_domain(model)

    def find_acts_by_edition(self, edition_id: uuid.UUID) -> list[NormativeAct]:
        """Retrieve all normative acts associated with a specific gazette edition."""
        models = (
            self._session.execute(
                select(NormativeActModel).where(NormativeActModel.edition_id == edition_id)
            )
            .scalars()
            .all()
        )
        return [self._map_act_model_to_domain(m) for m in models]

    def exists_act_by_hash(self, content_hash: DocumentHash) -> bool:
        """Check if an act already exists with the given content SHA-256."""
        stmt = select(NormativeActModel.id).where(
            NormativeActModel.content_sha256 == content_hash.hex_digest
        )
        return self._session.execute(stmt).first() is not None

    def _map_act_model_to_domain(self, model: NormativeActModel) -> NormativeAct:
        """Map ORM model to pure domain entity."""
        return NormativeAct(
            id=model.id,
            edition_id=model.edition_id,
            territory_id=TerritoryId.from_code(model.territory_id),
            date=GazetteDate.from_date(model.date),
            section=model.section,
            edition_number=model.edition_number,
            is_extra_edition=model.is_extra_edition,
            act_type=model.act_type,
            act_number=model.act_number,
            act_year=model.act_year,
            title=model.title,
            ementa=model.ementa,
            hierarchy=model.hierarchy,
            authority_name=model.authority_name,
            authority_role=model.authority_role,
            source_url=model.source_url,
            content_hash=DocumentHash.from_hex(model.content_sha256),
            char_count=model.char_count,
            raw_content=model.raw_content,
            structured_content=model.structured_content,
            classification_source=ClassificationSource(model.classification_source),
            classification_confidence=model.classification_confidence,
            metadata_json=model.metadata_json,
            scraped_at=model.scraped_at,
        )
