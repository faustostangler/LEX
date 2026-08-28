"""PostgreSQL Repository Adapter for Gazette Ingestion Persistence.

Implements GazetteRepositoryPort to store GazetteEdition aggregates with
idempotent ON CONFLICT resolution and TOAST compression support.
"""

import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from lex.ingestion.application.ports import GazetteRepositoryPort
from lex.ingestion.domain.entities import GazetteEdition
from lex.ingestion.domain.value_objects import (
    DocumentHash,
    FederativeTier,
    GazetteDate,
    TerritoryId,
)
from lex.ingestion.infrastructure.persistence.models import GazetteEditionModel


class PostgresGazetteRepository(GazetteRepositoryPort):
    """PostgreSQL implementation of the GazetteRepositoryPort."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, edition: GazetteEdition) -> None:
        """Persist a gazette edition with idempotent ON CONFLICT semantics."""
        bind = self._session.get_bind()
        is_postgres = bind is not None and bind.dialect.name == "postgresql"

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
                content_sha256=edition.file_hash.hex_digest,
                char_count=edition.char_count,
                full_text=edition.full_text,
                scraped_at=edition.scraped_at,
            )
            upsert_stmt = stmt.on_conflict_do_update(
                constraint="uq_gazette_edition_natural_key",
                set_={
                    "scraped_at": stmt.excluded.scraped_at,
                    "updated_at": datetime.now(UTC),
                    "content_sha256": stmt.excluded.content_sha256,
                    "char_count": stmt.excluded.char_count,
                    "full_text": stmt.excluded.full_text,
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
                existing.scraped_at = edition.scraped_at
                existing.updated_at = datetime.now(UTC)
                existing.content_sha256 = edition.file_hash.hex_digest
                existing.char_count = edition.char_count
                existing.full_text = edition.full_text
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
                    content_sha256=edition.file_hash.hex_digest,
                    char_count=edition.char_count,
                    full_text=edition.full_text,
                    scraped_at=edition.scraped_at,
                )
                self._session.add(model)

        self._session.commit()

    def get_by_territory_and_date(
        self,
        territory_id: TerritoryId,
        date: GazetteDate,
        section: str | None = None,
    ) -> GazetteEdition | None:
        """Retrieve a unique gazette edition if already ingested."""
        query = select(GazetteEditionModel).where(
            GazetteEditionModel.territory_id == territory_id.code,
            GazetteEditionModel.date == date.value,
        )
        if section is not None:
            query = query.where(GazetteEditionModel.section == section)

        model = self._session.execute(query).scalars().first()
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
            file_hash=DocumentHash.from_hex(model.content_sha256),
            char_count=model.char_count,
            full_text=model.full_text,
            scraped_at=model.scraped_at,
        )

    def exists_by_hash(self, file_hash: DocumentHash) -> bool:
        """Check if a gazette with the exact content hash has already been stored."""
        stmt = select(GazetteEditionModel.id).where(
            GazetteEditionModel.content_sha256 == file_hash.hex_digest
        )
        result = self._session.execute(stmt).first()
        return result is not None
