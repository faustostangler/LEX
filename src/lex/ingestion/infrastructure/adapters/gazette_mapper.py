"""Anti-Corruption Layer (ACL) Mapper for Gazette and Normative Acts Ingestion.

Translates untyped RawGazettePayload and RawNormativeActPayload DTOs emitted by Scrapy
spiders into strictly validated GazetteEdition and NormativeAct domain entities with
O(1) deterministic Kelsenian hierarchy classification and LexML canonical URN formatting.
"""

import re
import uuid
from collections.abc import Sequence
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
from lex.shared_kernel.value_objects import (
    HierarchicalGroup,
    HierarchicalRank,
    PublicationNature,
)

# -----------------------------------------------------------------------------
# Module Constants & Date Patterns (ADR-003)
# -----------------------------------------------------------------------------
ISO_DATE_PATTERN: re.Pattern[str] = re.compile(r"^\d{4}-\d{2}-\d{2}$")
BRAZILIAN_DATE_FORMATS: Sequence[str] = ("%d/%m/%Y", "%d-%m-%Y")

# -----------------------------------------------------------------------------
# Hierarchy Classification Rules (SPEC-003 & ADR-007)
# Ordered by specificity: Composite prefixes MUST precede generic terms.
# -----------------------------------------------------------------------------
HIERARCHY_MATCHING_TABLE: list[
    tuple[str, HierarchicalGroup, HierarchicalRank, PublicationNature]
] = [
    # 1. Composite & Specific Prefixes
    (
        "EMENDA CONSTITUCIONAL",
        HierarchicalGroup.GRUPO_1_PRIMARIO,
        HierarchicalRank.EMENDA_CONSTITUCIONAL,
        PublicationNature.NORMATIVA_ABSTRATA,
    ),
    (
        "LEI COMPLEMENTAR",
        HierarchicalGroup.GRUPO_1_PRIMARIO,
        HierarchicalRank.LEI_COMPLEMENTAR,
        PublicationNature.NORMATIVA_ABSTRATA,
    ),
    (
        "MEDIDA PROVISÓRIA",
        HierarchicalGroup.GRUPO_1_PRIMARIO,
        HierarchicalRank.MEDIDA_PROVISORIA,
        PublicationNature.NORMATIVA_ABSTRATA,
    ),
    (
        "MEDIDA PROVISORIA",
        HierarchicalGroup.GRUPO_1_PRIMARIO,
        HierarchicalRank.MEDIDA_PROVISORIA,
        PublicationNature.NORMATIVA_ABSTRATA,
    ),
    (
        "DECRETO LEGISLATIVO",
        HierarchicalGroup.GRUPO_1_PRIMARIO,
        HierarchicalRank.DECRETO_LEGISLATIVO,
        PublicationNature.NORMATIVA_ABSTRATA,
    ),
    (
        "LEI DELEGADA",
        HierarchicalGroup.GRUPO_1_PRIMARIO,
        HierarchicalRank.LEI_DELEGADA,
        PublicationNature.NORMATIVA_ABSTRATA,
    ),
    (
        "INSTRUÇÃO NORMATIVA",
        HierarchicalGroup.GRUPO_3_COLEGIADO_REGULATORIO,
        HierarchicalRank.INSTRUCAO_NORMATIVA,
        PublicationNature.REGULATORIA_SETORIAL,
    ),
    (
        "INSTRUCAO NORMATIVA",
        HierarchicalGroup.GRUPO_3_COLEGIADO_REGULATORIO,
        HierarchicalRank.INSTRUCAO_NORMATIVA,
        PublicationNature.REGULATORIA_SETORIAL,
    ),
    (
        "ATO DECLARATÓRIO",
        HierarchicalGroup.GRUPO_4_ORDINATORIO_MINISTERIAL,
        HierarchicalRank.PORTARIA_NORMATIVA,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "ATO DECLARATORIO",
        HierarchicalGroup.GRUPO_4_ORDINATORIO_MINISTERIAL,
        HierarchicalRank.PORTARIA_NORMATIVA,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "ATO CONVOCATÓRIO",
        HierarchicalGroup.GRUPO_6_EDITALICIO,
        HierarchicalRank.PUBLICIDADE_OPERACIONAL,
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    ),
    (
        "ATO CONVOCATORIO",
        HierarchicalGroup.GRUPO_6_EDITALICIO,
        HierarchicalRank.PUBLICIDADE_OPERACIONAL,
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    ),
    (
        "SOLUÇÃO DE CONSULTA",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "SOLUCAO DE CONSULTA",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    # 2. Extratos, Avisos e Publicidade (Must precede CONTRATO/CONVÊNIO)
    (
        "EXTRATO",
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        HierarchicalRank.PUBLICIDADE_OPERACIONAL,
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    ),
    (
        "AVISO",
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        HierarchicalRank.PUBLICIDADE_OPERACIONAL,
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    ),
    (
        "RESULTADO",
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        HierarchicalRank.PUBLICIDADE_OPERACIONAL,
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    ),
    (
        "RETIFICAÇÃO",
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        HierarchicalRank.PUBLICIDADE_OPERACIONAL,
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    ),
    (
        "RETIFICACAO",
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        HierarchicalRank.PUBLICIDADE_OPERACIONAL,
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    ),
    (
        "EDITAL",
        HierarchicalGroup.GRUPO_6_EDITALICIO,
        HierarchicalRank.PUBLICIDADE_OPERACIONAL,
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    ),
    (
        "PAUTA",
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        HierarchicalRank.PUBLICIDADE_OPERACIONAL,
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    ),
    (
        "COMUNICADO",
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        HierarchicalRank.PUBLICIDADE_OPERACIONAL,
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    ),
    (
        "SÚMULA",
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        HierarchicalRank.PUBLICIDADE_OPERACIONAL,
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    ),
    (
        "SUMULA",
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        HierarchicalRank.PUBLICIDADE_OPERACIONAL,
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    ),
    # 3. Generic Typologies
    (
        "LEI",
        HierarchicalGroup.GRUPO_1_PRIMARIO,
        HierarchicalRank.LEI_ORDINARIA,
        PublicationNature.NORMATIVA_ABSTRATA,
    ),
    (
        "DECRETO",
        HierarchicalGroup.GRUPO_2_EXECUTIVO,
        HierarchicalRank.DECRETO_EXECUTIVO,
        PublicationNature.NORMATIVA_ABSTRATA,
    ),
    (
        "RESOLUÇÃO-RE",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "RESOLUCAO-RE",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "RESOLUÇÃO RE",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "RESOLUCAO RE",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "RESOLUÇÃO ESPECÍFICA",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "RESOLUCAO ESPECIFICA",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "RESOLUÇÃO AUTORIZATIVA",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "RESOLUCAO AUTORIZATIVA",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "RESOLUÇÃO HOMOLOGATÓRIA",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "RESOLUCAO HOMOLOGATORIA",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "RESOLUÇÃO OPERACIONAL",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "RESOLUCAO OPERACIONAL",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "RESOLUÇÃO",
        HierarchicalGroup.GRUPO_3_COLEGIADO_REGULATORIO,
        HierarchicalRank.RESOLUCAO_REGULATORIA,
        PublicationNature.REGULATORIA_SETORIAL,
    ),
    (
        "RESOLUCAO",
        HierarchicalGroup.GRUPO_3_COLEGIADO_REGULATORIO,
        HierarchicalRank.RESOLUCAO_REGULATORIA,
        PublicationNature.REGULATORIA_SETORIAL,
    ),
    (
        "DELIBERAÇÃO",
        HierarchicalGroup.GRUPO_3_COLEGIADO_REGULATORIO,
        HierarchicalRank.RESOLUCAO_REGULATORIA,
        PublicationNature.REGULATORIA_SETORIAL,
    ),
    (
        "DELIBERACAO",
        HierarchicalGroup.GRUPO_3_COLEGIADO_REGULATORIO,
        HierarchicalRank.RESOLUCAO_REGULATORIA,
        PublicationNature.REGULATORIA_SETORIAL,
    ),
    (
        "PORTARIA",
        HierarchicalGroup.GRUPO_4_ORDINATORIO_MINISTERIAL,
        HierarchicalRank.PORTARIA_NORMATIVA,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "DESPACHO",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "DECISÃO",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "DECISAO",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "ACÓRDÃO",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "ACORDAO",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "ALVARÁ",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "ALVARA",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "AUTORIZAÇÃO",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "AUTORIZACAO",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "LICENÇA",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "LICENCA",
        HierarchicalGroup.GRUPO_5_DECISORIO_CONCRETO,
        HierarchicalRank.ATO_ADMINISTRATIVO_CONCRETO,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
    (
        "CONTRATO",
        HierarchicalGroup.GRUPO_7_CONTRATUAL,
        HierarchicalRank.PUBLICIDADE_OPERACIONAL,
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    ),
    (
        "CONVÊNIO",
        HierarchicalGroup.GRUPO_7_CONTRATUAL,
        HierarchicalRank.PUBLICIDADE_OPERACIONAL,
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    ),
    (
        "CONVENIO",
        HierarchicalGroup.GRUPO_7_CONTRATUAL,
        HierarchicalRank.PUBLICIDADE_OPERACIONAL,
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    ),
    (
        "TERMO",
        HierarchicalGroup.GRUPO_7_CONTRATUAL,
        HierarchicalRank.PUBLICIDADE_OPERACIONAL,
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    ),
    (
        "ACORDO",
        HierarchicalGroup.GRUPO_7_CONTRATUAL,
        HierarchicalRank.PUBLICIDADE_OPERACIONAL,
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    ),
    (
        "ATA",
        HierarchicalGroup.GRUPO_6_EDITALICIO,
        HierarchicalRank.PUBLICIDADE_OPERACIONAL,
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    ),
    (
        "ATO",
        HierarchicalGroup.GRUPO_4_ORDINATORIO_MINISTERIAL,
        HierarchicalRank.PORTARIA_NORMATIVA,
        PublicationNature.CONCRETA_INDIVIDUAL,
    ),
]


def resolve_hierarchy(
    act_type: str, section: str | None = None
) -> tuple[HierarchicalGroup, int, PublicationNature]:
    """Deterministically classify an act based on act_type and official gazette section."""
    clean_type = act_type.strip().upper()
    clean_sec = (section or "").strip().lower()

    # Invariant: Section 2 of official gazettes is strictly dedicated to Personnel Acts (Trilha B)
    if clean_sec == "secao_2":
        for prefix, group, rank, _ in HIERARCHY_MATCHING_TABLE:
            if clean_type.startswith(prefix):
                return (group, int(rank), PublicationNature.CONCRETA_INDIVIDUAL)
        return (
            HierarchicalGroup.GRUPO_4_ORDINATORIO_MINISTERIAL,
            int(HierarchicalRank.PORTARIA_NORMATIVA),
            PublicationNature.CONCRETA_INDIVIDUAL,
        )

    # Invariant: Section 3 is strictly dedicated to Procurement, Contracts, Notices (Trilha B)
    if clean_sec == "secao_3":
        for prefix, group, rank, _ in HIERARCHY_MATCHING_TABLE:
            if clean_type.startswith(prefix):
                return (group, int(rank), PublicationNature.PUBLICIDADE_OPERACIONAL)
        return (
            HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
            int(HierarchicalRank.PUBLICIDADE_OPERACIONAL),
            PublicationNature.PUBLICIDADE_OPERACIONAL,
        )

    # Section 1 or unspecified: Standard Normative Rules (Trilha A where applicable)
    for prefix, group, rank, nature in HIERARCHY_MATCHING_TABLE:
        if clean_type.startswith(prefix):
            # Portaria published in Section 1 is normative regulation (Trilha A)
            if prefix == "PORTARIA" and clean_sec == "secao_1":
                return (group, int(rank), PublicationNature.NORMATIVA_ABSTRATA)
            return (group, int(rank), nature)

    # Fallback to Group 8
    return (
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        int(HierarchicalRank.PUBLICIDADE_OPERACIONAL),
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    )


def generate_canonical_urn(
    territory_code: str,
    act_type: str,
    act_number: str | None,
    act_year: int | None,
    act_date: date,
    content_hash: str | None = None,
) -> str:
    """Generate a standardized LexML/FRBR Canonical URN for a normative act."""
    clean_territory = territory_code.strip().lower()
    clean_type = re.sub(r"[^a-zA-Z0-9]+", ".", act_type.strip().lower())[:80].strip(".")
    if not clean_type:
        clean_type = "ato"

    if act_number and act_year and act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


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

        group, rank, nature = resolve_hierarchy(payload.act_type, payload.section)
        canonical_urn = generate_canonical_urn(
            territory_code=payload.territory_code,
            act_type=payload.act_type,
            act_number=payload.act_number,
            act_year=payload.act_year,
            act_date=payload.date_obj,
            content_hash=content_hash.hex_digest,
        )

        return NormativeAct(
            id=None,
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
            structured_content=None,
            classification_source=ClassificationSource(payload.classification_source),
            classification_confidence=payload.classification_confidence,
            hierarchical_group=group,
            hierarchical_rank=rank,
            publication_nature=nature,
            canonical_urn=canonical_urn,
            is_stub=False,
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
        if ISO_DATE_PATTERN.match(raw_str):
            try:
                return datetime.strptime(raw_str, "%Y-%m-%d").replace(tzinfo=UTC).date()
            except ValueError as exc:
                err_msg = f"Unable to parse date string '{raw_str}': {exc}"
                raise InvalidGazetteDateError(err_msg) from exc

        # Try Brazilian formats DD/MM/YYYY or DD-MM-YYYY
        for fmt in BRAZILIAN_DATE_FORMATS:
            try:
                return datetime.strptime(raw_str, fmt).replace(tzinfo=UTC).date()
            except ValueError:
                continue

        raise InvalidGazetteDateError(
            f"Unable to parse date string '{raw_str}'. Expected ISO or Brazilian format."
        )
