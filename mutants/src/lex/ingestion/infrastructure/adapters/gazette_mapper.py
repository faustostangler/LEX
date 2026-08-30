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


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_resolve_hierarchy__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_resolve_hierarchy__mutmut)
def resolve_hierarchy(
    act_type: str, section: str | None = None
) -> tuple[HierarchicalGroup, int, PublicationNature]:
    """Deterministically classify an act based on act_type and official gazette section."""
    clean_type = act_type.strip().upper()

    for prefix, group, rank, nature in HIERARCHY_MATCHING_TABLE:
        if clean_type.startswith(prefix):
            # Portaria published in Section 1 is normative regulation (Trilha A)
            if prefix == "PORTARIA" and section == "secao_1":
                return (group, int(rank), PublicationNature.NORMATIVA_ABSTRATA)
            return (group, int(rank), nature)

    # Fallback to Group 8
    return (
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        int(HierarchicalRank.PUBLICIDADE_OPERACIONAL),
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    )


def x_resolve_hierarchy__mutmut_orig(
    act_type: str, section: str | None = None
) -> tuple[HierarchicalGroup, int, PublicationNature]:
    """Deterministically classify an act based on act_type and official gazette section."""
    clean_type = act_type.strip().upper()

    for prefix, group, rank, nature in HIERARCHY_MATCHING_TABLE:
        if clean_type.startswith(prefix):
            # Portaria published in Section 1 is normative regulation (Trilha A)
            if prefix == "PORTARIA" and section == "secao_1":
                return (group, int(rank), PublicationNature.NORMATIVA_ABSTRATA)
            return (group, int(rank), nature)

    # Fallback to Group 8
    return (
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        int(HierarchicalRank.PUBLICIDADE_OPERACIONAL),
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    )


def x_resolve_hierarchy__mutmut_1(
    act_type: str, section: str | None = None
) -> tuple[HierarchicalGroup, int, PublicationNature]:
    """Deterministically classify an act based on act_type and official gazette section."""
    clean_type = None

    for prefix, group, rank, nature in HIERARCHY_MATCHING_TABLE:
        if clean_type.startswith(prefix):
            # Portaria published in Section 1 is normative regulation (Trilha A)
            if prefix == "PORTARIA" and section == "secao_1":
                return (group, int(rank), PublicationNature.NORMATIVA_ABSTRATA)
            return (group, int(rank), nature)

    # Fallback to Group 8
    return (
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        int(HierarchicalRank.PUBLICIDADE_OPERACIONAL),
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    )


def x_resolve_hierarchy__mutmut_2(
    act_type: str, section: str | None = None
) -> tuple[HierarchicalGroup, int, PublicationNature]:
    """Deterministically classify an act based on act_type and official gazette section."""
    clean_type = act_type.strip().lower()

    for prefix, group, rank, nature in HIERARCHY_MATCHING_TABLE:
        if clean_type.startswith(prefix):
            # Portaria published in Section 1 is normative regulation (Trilha A)
            if prefix == "PORTARIA" and section == "secao_1":
                return (group, int(rank), PublicationNature.NORMATIVA_ABSTRATA)
            return (group, int(rank), nature)

    # Fallback to Group 8
    return (
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        int(HierarchicalRank.PUBLICIDADE_OPERACIONAL),
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    )


def x_resolve_hierarchy__mutmut_3(
    act_type: str, section: str | None = None
) -> tuple[HierarchicalGroup, int, PublicationNature]:
    """Deterministically classify an act based on act_type and official gazette section."""
    clean_type = act_type.strip().upper()

    for prefix, group, rank, nature in HIERARCHY_MATCHING_TABLE:
        if clean_type.startswith(None):
            # Portaria published in Section 1 is normative regulation (Trilha A)
            if prefix == "PORTARIA" and section == "secao_1":
                return (group, int(rank), PublicationNature.NORMATIVA_ABSTRATA)
            return (group, int(rank), nature)

    # Fallback to Group 8
    return (
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        int(HierarchicalRank.PUBLICIDADE_OPERACIONAL),
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    )


def x_resolve_hierarchy__mutmut_4(
    act_type: str, section: str | None = None
) -> tuple[HierarchicalGroup, int, PublicationNature]:
    """Deterministically classify an act based on act_type and official gazette section."""
    clean_type = act_type.strip().upper()

    for prefix, group, rank, nature in HIERARCHY_MATCHING_TABLE:
        if clean_type.startswith(prefix):
            # Portaria published in Section 1 is normative regulation (Trilha A)
            if prefix == "PORTARIA" or section == "secao_1":
                return (group, int(rank), PublicationNature.NORMATIVA_ABSTRATA)
            return (group, int(rank), nature)

    # Fallback to Group 8
    return (
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        int(HierarchicalRank.PUBLICIDADE_OPERACIONAL),
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    )


def x_resolve_hierarchy__mutmut_5(
    act_type: str, section: str | None = None
) -> tuple[HierarchicalGroup, int, PublicationNature]:
    """Deterministically classify an act based on act_type and official gazette section."""
    clean_type = act_type.strip().upper()

    for prefix, group, rank, nature in HIERARCHY_MATCHING_TABLE:
        if clean_type.startswith(prefix):
            # Portaria published in Section 1 is normative regulation (Trilha A)
            if prefix != "PORTARIA" and section == "secao_1":
                return (group, int(rank), PublicationNature.NORMATIVA_ABSTRATA)
            return (group, int(rank), nature)

    # Fallback to Group 8
    return (
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        int(HierarchicalRank.PUBLICIDADE_OPERACIONAL),
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    )


def x_resolve_hierarchy__mutmut_6(
    act_type: str, section: str | None = None
) -> tuple[HierarchicalGroup, int, PublicationNature]:
    """Deterministically classify an act based on act_type and official gazette section."""
    clean_type = act_type.strip().upper()

    for prefix, group, rank, nature in HIERARCHY_MATCHING_TABLE:
        if clean_type.startswith(prefix):
            # Portaria published in Section 1 is normative regulation (Trilha A)
            if prefix == "XXPORTARIAXX" and section == "secao_1":
                return (group, int(rank), PublicationNature.NORMATIVA_ABSTRATA)
            return (group, int(rank), nature)

    # Fallback to Group 8
    return (
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        int(HierarchicalRank.PUBLICIDADE_OPERACIONAL),
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    )


def x_resolve_hierarchy__mutmut_7(
    act_type: str, section: str | None = None
) -> tuple[HierarchicalGroup, int, PublicationNature]:
    """Deterministically classify an act based on act_type and official gazette section."""
    clean_type = act_type.strip().upper()

    for prefix, group, rank, nature in HIERARCHY_MATCHING_TABLE:
        if clean_type.startswith(prefix):
            # Portaria published in Section 1 is normative regulation (Trilha A)
            if prefix == "portaria" and section == "secao_1":
                return (group, int(rank), PublicationNature.NORMATIVA_ABSTRATA)
            return (group, int(rank), nature)

    # Fallback to Group 8
    return (
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        int(HierarchicalRank.PUBLICIDADE_OPERACIONAL),
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    )


def x_resolve_hierarchy__mutmut_8(
    act_type: str, section: str | None = None
) -> tuple[HierarchicalGroup, int, PublicationNature]:
    """Deterministically classify an act based on act_type and official gazette section."""
    clean_type = act_type.strip().upper()

    for prefix, group, rank, nature in HIERARCHY_MATCHING_TABLE:
        if clean_type.startswith(prefix):
            # Portaria published in Section 1 is normative regulation (Trilha A)
            if prefix == "PORTARIA" and section != "secao_1":
                return (group, int(rank), PublicationNature.NORMATIVA_ABSTRATA)
            return (group, int(rank), nature)

    # Fallback to Group 8
    return (
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        int(HierarchicalRank.PUBLICIDADE_OPERACIONAL),
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    )


def x_resolve_hierarchy__mutmut_9(
    act_type: str, section: str | None = None
) -> tuple[HierarchicalGroup, int, PublicationNature]:
    """Deterministically classify an act based on act_type and official gazette section."""
    clean_type = act_type.strip().upper()

    for prefix, group, rank, nature in HIERARCHY_MATCHING_TABLE:
        if clean_type.startswith(prefix):
            # Portaria published in Section 1 is normative regulation (Trilha A)
            if prefix == "PORTARIA" and section == "XXsecao_1XX":
                return (group, int(rank), PublicationNature.NORMATIVA_ABSTRATA)
            return (group, int(rank), nature)

    # Fallback to Group 8
    return (
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        int(HierarchicalRank.PUBLICIDADE_OPERACIONAL),
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    )


def x_resolve_hierarchy__mutmut_10(
    act_type: str, section: str | None = None
) -> tuple[HierarchicalGroup, int, PublicationNature]:
    """Deterministically classify an act based on act_type and official gazette section."""
    clean_type = act_type.strip().upper()

    for prefix, group, rank, nature in HIERARCHY_MATCHING_TABLE:
        if clean_type.startswith(prefix):
            # Portaria published in Section 1 is normative regulation (Trilha A)
            if prefix == "PORTARIA" and section == "SECAO_1":
                return (group, int(rank), PublicationNature.NORMATIVA_ABSTRATA)
            return (group, int(rank), nature)

    # Fallback to Group 8
    return (
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        int(HierarchicalRank.PUBLICIDADE_OPERACIONAL),
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    )


def x_resolve_hierarchy__mutmut_11(
    act_type: str, section: str | None = None
) -> tuple[HierarchicalGroup, int, PublicationNature]:
    """Deterministically classify an act based on act_type and official gazette section."""
    clean_type = act_type.strip().upper()

    for prefix, group, rank, nature in HIERARCHY_MATCHING_TABLE:
        if clean_type.startswith(prefix):
            # Portaria published in Section 1 is normative regulation (Trilha A)
            if prefix == "PORTARIA" and section == "secao_1":
                return (group, int(None), PublicationNature.NORMATIVA_ABSTRATA)
            return (group, int(rank), nature)

    # Fallback to Group 8
    return (
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        int(HierarchicalRank.PUBLICIDADE_OPERACIONAL),
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    )


def x_resolve_hierarchy__mutmut_12(
    act_type: str, section: str | None = None
) -> tuple[HierarchicalGroup, int, PublicationNature]:
    """Deterministically classify an act based on act_type and official gazette section."""
    clean_type = act_type.strip().upper()

    for prefix, group, rank, nature in HIERARCHY_MATCHING_TABLE:
        if clean_type.startswith(prefix):
            # Portaria published in Section 1 is normative regulation (Trilha A)
            if prefix == "PORTARIA" and section == "secao_1":
                return (group, int(rank), PublicationNature.NORMATIVA_ABSTRATA)
            return (group, int(None), nature)

    # Fallback to Group 8
    return (
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        int(HierarchicalRank.PUBLICIDADE_OPERACIONAL),
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    )


def x_resolve_hierarchy__mutmut_13(
    act_type: str, section: str | None = None
) -> tuple[HierarchicalGroup, int, PublicationNature]:
    """Deterministically classify an act based on act_type and official gazette section."""
    clean_type = act_type.strip().upper()

    for prefix, group, rank, nature in HIERARCHY_MATCHING_TABLE:
        if clean_type.startswith(prefix):
            # Portaria published in Section 1 is normative regulation (Trilha A)
            if prefix == "PORTARIA" and section == "secao_1":
                return (group, int(rank), PublicationNature.NORMATIVA_ABSTRATA)
            return (group, int(rank), nature)

    # Fallback to Group 8
    return (
        HierarchicalGroup.GRUPO_8_PUBLICIDADE_EXTRATOS,
        int(None),
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    )

mutants_x_resolve_hierarchy__mutmut['_mutmut_orig'] = x_resolve_hierarchy__mutmut_orig # type: ignore # mutmut generated
mutants_x_resolve_hierarchy__mutmut['x_resolve_hierarchy__mutmut_1'] = x_resolve_hierarchy__mutmut_1 # type: ignore # mutmut generated
mutants_x_resolve_hierarchy__mutmut['x_resolve_hierarchy__mutmut_2'] = x_resolve_hierarchy__mutmut_2 # type: ignore # mutmut generated
mutants_x_resolve_hierarchy__mutmut['x_resolve_hierarchy__mutmut_3'] = x_resolve_hierarchy__mutmut_3 # type: ignore # mutmut generated
mutants_x_resolve_hierarchy__mutmut['x_resolve_hierarchy__mutmut_4'] = x_resolve_hierarchy__mutmut_4 # type: ignore # mutmut generated
mutants_x_resolve_hierarchy__mutmut['x_resolve_hierarchy__mutmut_5'] = x_resolve_hierarchy__mutmut_5 # type: ignore # mutmut generated
mutants_x_resolve_hierarchy__mutmut['x_resolve_hierarchy__mutmut_6'] = x_resolve_hierarchy__mutmut_6 # type: ignore # mutmut generated
mutants_x_resolve_hierarchy__mutmut['x_resolve_hierarchy__mutmut_7'] = x_resolve_hierarchy__mutmut_7 # type: ignore # mutmut generated
mutants_x_resolve_hierarchy__mutmut['x_resolve_hierarchy__mutmut_8'] = x_resolve_hierarchy__mutmut_8 # type: ignore # mutmut generated
mutants_x_resolve_hierarchy__mutmut['x_resolve_hierarchy__mutmut_9'] = x_resolve_hierarchy__mutmut_9 # type: ignore # mutmut generated
mutants_x_resolve_hierarchy__mutmut['x_resolve_hierarchy__mutmut_10'] = x_resolve_hierarchy__mutmut_10 # type: ignore # mutmut generated
mutants_x_resolve_hierarchy__mutmut['x_resolve_hierarchy__mutmut_11'] = x_resolve_hierarchy__mutmut_11 # type: ignore # mutmut generated
mutants_x_resolve_hierarchy__mutmut['x_resolve_hierarchy__mutmut_12'] = x_resolve_hierarchy__mutmut_12 # type: ignore # mutmut generated
mutants_x_resolve_hierarchy__mutmut['x_resolve_hierarchy__mutmut_13'] = x_resolve_hierarchy__mutmut_13 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_generate_canonical_urn__mutmut)
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


def x_generate_canonical_urn__mutmut_orig(
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


def x_generate_canonical_urn__mutmut_1(
    territory_code: str,
    act_type: str,
    act_number: str | None,
    act_year: int | None,
    act_date: date,
    content_hash: str | None = None,
) -> str:
    """Generate a standardized LexML/FRBR Canonical URN for a normative act."""
    clean_territory = None
    clean_type = re.sub(r"[^a-zA-Z0-9]+", ".", act_type.strip().lower())[:80].strip(".")
    if not clean_type:
        clean_type = "ato"

    if act_number and act_year and act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_2(
    territory_code: str,
    act_type: str,
    act_number: str | None,
    act_year: int | None,
    act_date: date,
    content_hash: str | None = None,
) -> str:
    """Generate a standardized LexML/FRBR Canonical URN for a normative act."""
    clean_territory = territory_code.strip().upper()
    clean_type = re.sub(r"[^a-zA-Z0-9]+", ".", act_type.strip().lower())[:80].strip(".")
    if not clean_type:
        clean_type = "ato"

    if act_number and act_year and act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_3(
    territory_code: str,
    act_type: str,
    act_number: str | None,
    act_year: int | None,
    act_date: date,
    content_hash: str | None = None,
) -> str:
    """Generate a standardized LexML/FRBR Canonical URN for a normative act."""
    clean_territory = territory_code.strip().lower()
    clean_type = None
    if not clean_type:
        clean_type = "ato"

    if act_number and act_year and act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_4(
    territory_code: str,
    act_type: str,
    act_number: str | None,
    act_year: int | None,
    act_date: date,
    content_hash: str | None = None,
) -> str:
    """Generate a standardized LexML/FRBR Canonical URN for a normative act."""
    clean_territory = territory_code.strip().lower()
    clean_type = re.sub(r"[^a-zA-Z0-9]+", ".", act_type.strip().lower())[:80].strip(None)
    if not clean_type:
        clean_type = "ato"

    if act_number and act_year and act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_5(
    territory_code: str,
    act_type: str,
    act_number: str | None,
    act_year: int | None,
    act_date: date,
    content_hash: str | None = None,
) -> str:
    """Generate a standardized LexML/FRBR Canonical URN for a normative act."""
    clean_territory = territory_code.strip().lower()
    clean_type = re.sub(None, ".", act_type.strip().lower())[:80].strip(".")
    if not clean_type:
        clean_type = "ato"

    if act_number and act_year and act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_6(
    territory_code: str,
    act_type: str,
    act_number: str | None,
    act_year: int | None,
    act_date: date,
    content_hash: str | None = None,
) -> str:
    """Generate a standardized LexML/FRBR Canonical URN for a normative act."""
    clean_territory = territory_code.strip().lower()
    clean_type = re.sub(r"[^a-zA-Z0-9]+", None, act_type.strip().lower())[:80].strip(".")
    if not clean_type:
        clean_type = "ato"

    if act_number and act_year and act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_7(
    territory_code: str,
    act_type: str,
    act_number: str | None,
    act_year: int | None,
    act_date: date,
    content_hash: str | None = None,
) -> str:
    """Generate a standardized LexML/FRBR Canonical URN for a normative act."""
    clean_territory = territory_code.strip().lower()
    clean_type = re.sub(r"[^a-zA-Z0-9]+", ".", None)[:80].strip(".")
    if not clean_type:
        clean_type = "ato"

    if act_number and act_year and act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_8(
    territory_code: str,
    act_type: str,
    act_number: str | None,
    act_year: int | None,
    act_date: date,
    content_hash: str | None = None,
) -> str:
    """Generate a standardized LexML/FRBR Canonical URN for a normative act."""
    clean_territory = territory_code.strip().lower()
    clean_type = re.sub(".", act_type.strip().lower())[:80].strip(".")
    if not clean_type:
        clean_type = "ato"

    if act_number and act_year and act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_9(
    territory_code: str,
    act_type: str,
    act_number: str | None,
    act_year: int | None,
    act_date: date,
    content_hash: str | None = None,
) -> str:
    """Generate a standardized LexML/FRBR Canonical URN for a normative act."""
    clean_territory = territory_code.strip().lower()
    clean_type = re.sub(r"[^a-zA-Z0-9]+", act_type.strip().lower())[:80].strip(".")
    if not clean_type:
        clean_type = "ato"

    if act_number and act_year and act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_10(
    territory_code: str,
    act_type: str,
    act_number: str | None,
    act_year: int | None,
    act_date: date,
    content_hash: str | None = None,
) -> str:
    """Generate a standardized LexML/FRBR Canonical URN for a normative act."""
    clean_territory = territory_code.strip().lower()
    clean_type = re.sub(r"[^a-zA-Z0-9]+", ".", )[:80].strip(".")
    if not clean_type:
        clean_type = "ato"

    if act_number and act_year and act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_11(
    territory_code: str,
    act_type: str,
    act_number: str | None,
    act_year: int | None,
    act_date: date,
    content_hash: str | None = None,
) -> str:
    """Generate a standardized LexML/FRBR Canonical URN for a normative act."""
    clean_territory = territory_code.strip().lower()
    clean_type = re.sub(r"XX[^a-zA-Z0-9]+XX", ".", act_type.strip().lower())[:80].strip(".")
    if not clean_type:
        clean_type = "ato"

    if act_number and act_year and act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_12(
    territory_code: str,
    act_type: str,
    act_number: str | None,
    act_year: int | None,
    act_date: date,
    content_hash: str | None = None,
) -> str:
    """Generate a standardized LexML/FRBR Canonical URN for a normative act."""
    clean_territory = territory_code.strip().lower()
    clean_type = re.sub(r"[^a-za-z0-9]+", ".", act_type.strip().lower())[:80].strip(".")
    if not clean_type:
        clean_type = "ato"

    if act_number and act_year and act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_13(
    territory_code: str,
    act_type: str,
    act_number: str | None,
    act_year: int | None,
    act_date: date,
    content_hash: str | None = None,
) -> str:
    """Generate a standardized LexML/FRBR Canonical URN for a normative act."""
    clean_territory = territory_code.strip().lower()
    clean_type = re.sub(r"[^A-ZA-Z0-9]+", ".", act_type.strip().lower())[:80].strip(".")
    if not clean_type:
        clean_type = "ato"

    if act_number and act_year and act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_14(
    territory_code: str,
    act_type: str,
    act_number: str | None,
    act_year: int | None,
    act_date: date,
    content_hash: str | None = None,
) -> str:
    """Generate a standardized LexML/FRBR Canonical URN for a normative act."""
    clean_territory = territory_code.strip().lower()
    clean_type = re.sub(r"[^a-zA-Z0-9]+", "XX.XX", act_type.strip().lower())[:80].strip(".")
    if not clean_type:
        clean_type = "ato"

    if act_number and act_year and act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_15(
    territory_code: str,
    act_type: str,
    act_number: str | None,
    act_year: int | None,
    act_date: date,
    content_hash: str | None = None,
) -> str:
    """Generate a standardized LexML/FRBR Canonical URN for a normative act."""
    clean_territory = territory_code.strip().lower()
    clean_type = re.sub(r"[^a-zA-Z0-9]+", ".", act_type.strip().upper())[:80].strip(".")
    if not clean_type:
        clean_type = "ato"

    if act_number and act_year and act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_16(
    territory_code: str,
    act_type: str,
    act_number: str | None,
    act_year: int | None,
    act_date: date,
    content_hash: str | None = None,
) -> str:
    """Generate a standardized LexML/FRBR Canonical URN for a normative act."""
    clean_territory = territory_code.strip().lower()
    clean_type = re.sub(r"[^a-zA-Z0-9]+", ".", act_type.strip().lower())[:81].strip(".")
    if not clean_type:
        clean_type = "ato"

    if act_number and act_year and act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_17(
    territory_code: str,
    act_type: str,
    act_number: str | None,
    act_year: int | None,
    act_date: date,
    content_hash: str | None = None,
) -> str:
    """Generate a standardized LexML/FRBR Canonical URN for a normative act."""
    clean_territory = territory_code.strip().lower()
    clean_type = re.sub(r"[^a-zA-Z0-9]+", ".", act_type.strip().lower())[:80].strip("XX.XX")
    if not clean_type:
        clean_type = "ato"

    if act_number and act_year and act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_18(
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
    if clean_type:
        clean_type = "ato"

    if act_number and act_year and act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_19(
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
        clean_type = None

    if act_number and act_year and act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_20(
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
        clean_type = "XXatoXX"

    if act_number and act_year and act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_21(
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
        clean_type = "ATO"

    if act_number and act_year and act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_22(
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

    if act_number and act_year and act_number.strip() or act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_23(
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

    if act_number and act_year or act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_24(
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

    if act_number or act_year and act_number.strip() and act_year > 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_25(
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

    if act_number and act_year and act_number.strip() and act_year >= 1800:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_26(
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

    if act_number and act_year and act_number.strip() and act_year > 1801:
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_27(
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
        clean_num = None
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_28(
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
        clean_num = re.sub(None, "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_29(
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
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", None, act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_30(
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
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", None)[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_31(
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
        clean_num = re.sub("", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_32(
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
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_33(
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
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", )[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_34(
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
        clean_num = re.sub(r"XX[^a-zA-Z0-9.\-]+XX", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_35(
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
        clean_num = re.sub(r"[^a-za-z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_36(
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
        clean_num = re.sub(r"[^A-ZA-Z0-9.\-]+", "", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_37(
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
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "XXXX", act_number.strip())[:50]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_38(
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
        clean_num = re.sub(r"[^a-zA-Z0-9.\-]+", "", act_number.strip())[:51]
        return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_year};{clean_num}"

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_39(
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

    fallback_id = None
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_40(
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

    fallback_id = content_hash[:17] if content_hash else str(uuid.uuid4())[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_41(
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

    fallback_id = content_hash[:16] if content_hash else str(None)[:8]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"


def x_generate_canonical_urn__mutmut_42(
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

    fallback_id = content_hash[:16] if content_hash else str(uuid.uuid4())[:9]
    return f"urn:lex:{clean_territory}:federal:{clean_type}:{act_date.isoformat()};{fallback_id}"

mutants_x_generate_canonical_urn__mutmut['_mutmut_orig'] = x_generate_canonical_urn__mutmut_orig # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_1'] = x_generate_canonical_urn__mutmut_1 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_2'] = x_generate_canonical_urn__mutmut_2 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_3'] = x_generate_canonical_urn__mutmut_3 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_4'] = x_generate_canonical_urn__mutmut_4 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_5'] = x_generate_canonical_urn__mutmut_5 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_6'] = x_generate_canonical_urn__mutmut_6 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_7'] = x_generate_canonical_urn__mutmut_7 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_8'] = x_generate_canonical_urn__mutmut_8 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_9'] = x_generate_canonical_urn__mutmut_9 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_10'] = x_generate_canonical_urn__mutmut_10 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_11'] = x_generate_canonical_urn__mutmut_11 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_12'] = x_generate_canonical_urn__mutmut_12 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_13'] = x_generate_canonical_urn__mutmut_13 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_14'] = x_generate_canonical_urn__mutmut_14 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_15'] = x_generate_canonical_urn__mutmut_15 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_16'] = x_generate_canonical_urn__mutmut_16 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_17'] = x_generate_canonical_urn__mutmut_17 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_18'] = x_generate_canonical_urn__mutmut_18 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_19'] = x_generate_canonical_urn__mutmut_19 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_20'] = x_generate_canonical_urn__mutmut_20 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_21'] = x_generate_canonical_urn__mutmut_21 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_22'] = x_generate_canonical_urn__mutmut_22 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_23'] = x_generate_canonical_urn__mutmut_23 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_24'] = x_generate_canonical_urn__mutmut_24 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_25'] = x_generate_canonical_urn__mutmut_25 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_26'] = x_generate_canonical_urn__mutmut_26 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_27'] = x_generate_canonical_urn__mutmut_27 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_28'] = x_generate_canonical_urn__mutmut_28 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_29'] = x_generate_canonical_urn__mutmut_29 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_30'] = x_generate_canonical_urn__mutmut_30 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_31'] = x_generate_canonical_urn__mutmut_31 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_32'] = x_generate_canonical_urn__mutmut_32 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_33'] = x_generate_canonical_urn__mutmut_33 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_34'] = x_generate_canonical_urn__mutmut_34 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_35'] = x_generate_canonical_urn__mutmut_35 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_36'] = x_generate_canonical_urn__mutmut_36 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_37'] = x_generate_canonical_urn__mutmut_37 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_38'] = x_generate_canonical_urn__mutmut_38 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_39'] = x_generate_canonical_urn__mutmut_39 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_40'] = x_generate_canonical_urn__mutmut_40 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_41'] = x_generate_canonical_urn__mutmut_41 # type: ignore # mutmut generated
mutants_x_generate_canonical_urn__mutmut['x_generate_canonical_urn__mutmut_42'] = x_generate_canonical_urn__mutmut_42 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁGazetteMapperǁto_domain__mutmut: MutantDict = {}  # type: ignore
mutants_xǁGazetteMapperǁto_normative_act__mutmut: MutantDict = {}  # type: ignore
mutants_xǁGazetteMapperǁ_resolve_date__mutmut: MutantDict = {}  # type: ignore


class GazetteMapper:
    """Anti-Corruption Layer translator from web scraping DTOs to Domain Entities."""

    @_mutmut_mutated(mutants_xǁGazetteMapperǁ__init____mutmut)
    def __init__(self, text_extractor: StreamTextExtractorPort) -> None:
        self._extractor = text_extractor

    def xǁGazetteMapperǁ__init____mutmut_orig(self, text_extractor: StreamTextExtractorPort) -> None:
        self._extractor = text_extractor

    def xǁGazetteMapperǁ__init____mutmut_1(self, text_extractor: StreamTextExtractorPort) -> None:
        self._extractor = None

    @_mutmut_mutated(mutants_xǁGazetteMapperǁto_domain__mutmut)
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

    def xǁGazetteMapperǁto_domain__mutmut_orig(self, payload: RawGazettePayload) -> GazetteEdition:
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

    def xǁGazetteMapperǁto_domain__mutmut_1(self, payload: RawGazettePayload) -> GazetteEdition:
        """Translate a RawGazettePayload DTO into a valid GazetteEdition domain entity."""
        summary_text = None
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

    def xǁGazetteMapperǁto_domain__mutmut_2(self, payload: RawGazettePayload) -> GazetteEdition:
        """Translate a RawGazettePayload DTO into a valid GazetteEdition domain entity."""
        summary_text = (
            payload.raw_content
            if isinstance(payload.raw_content, str)
            else (payload.source_url - f"-{payload.total_acts}-{payload.edition_number}")
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

    def xǁGazetteMapperǁto_domain__mutmut_3(self, payload: RawGazettePayload) -> GazetteEdition:
        """Translate a RawGazettePayload DTO into a valid GazetteEdition domain entity."""
        summary_text = (
            payload.raw_content
            if isinstance(payload.raw_content, str)
            else (payload.source_url + f"-{payload.total_acts}-{payload.edition_number}")
        )
        resolved_date = None

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

    def xǁGazetteMapperǁto_domain__mutmut_4(self, payload: RawGazettePayload) -> GazetteEdition:
        """Translate a RawGazettePayload DTO into a valid GazetteEdition domain entity."""
        summary_text = (
            payload.raw_content
            if isinstance(payload.raw_content, str)
            else (payload.source_url + f"-{payload.total_acts}-{payload.edition_number}")
        )
        resolved_date = self._resolve_date(None)

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

    def xǁGazetteMapperǁto_domain__mutmut_5(self, payload: RawGazettePayload) -> GazetteEdition:
        """Translate a RawGazettePayload DTO into a valid GazetteEdition domain entity."""
        summary_text = (
            payload.raw_content
            if isinstance(payload.raw_content, str)
            else (payload.source_url + f"-{payload.total_acts}-{payload.edition_number}")
        )
        resolved_date = self._resolve_date(payload)

        territory_id = None
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

    def xǁGazetteMapperǁto_domain__mutmut_6(self, payload: RawGazettePayload) -> GazetteEdition:
        """Translate a RawGazettePayload DTO into a valid GazetteEdition domain entity."""
        summary_text = (
            payload.raw_content
            if isinstance(payload.raw_content, str)
            else (payload.source_url + f"-{payload.total_acts}-{payload.edition_number}")
        )
        resolved_date = self._resolve_date(payload)

        territory_id = TerritoryId.from_code(None)
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

    def xǁGazetteMapperǁto_domain__mutmut_7(self, payload: RawGazettePayload) -> GazetteEdition:
        """Translate a RawGazettePayload DTO into a valid GazetteEdition domain entity."""
        summary_text = (
            payload.raw_content
            if isinstance(payload.raw_content, str)
            else (payload.source_url + f"-{payload.total_acts}-{payload.edition_number}")
        )
        resolved_date = self._resolve_date(payload)

        territory_id = TerritoryId.from_code(payload.territory_code)
        tier = None
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

    def xǁGazetteMapperǁto_domain__mutmut_8(self, payload: RawGazettePayload) -> GazetteEdition:
        """Translate a RawGazettePayload DTO into a valid GazetteEdition domain entity."""
        summary_text = (
            payload.raw_content
            if isinstance(payload.raw_content, str)
            else (payload.source_url + f"-{payload.total_acts}-{payload.edition_number}")
        )
        resolved_date = self._resolve_date(payload)

        territory_id = TerritoryId.from_code(payload.territory_code)
        tier = FederativeTier(None)
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

    def xǁGazetteMapperǁto_domain__mutmut_9(self, payload: RawGazettePayload) -> GazetteEdition:
        """Translate a RawGazettePayload DTO into a valid GazetteEdition domain entity."""
        summary_text = (
            payload.raw_content
            if isinstance(payload.raw_content, str)
            else (payload.source_url + f"-{payload.total_acts}-{payload.edition_number}")
        )
        resolved_date = self._resolve_date(payload)

        territory_id = TerritoryId.from_code(payload.territory_code)
        tier = FederativeTier(payload.tier.upper())
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

    def xǁGazetteMapperǁto_domain__mutmut_10(self, payload: RawGazettePayload) -> GazetteEdition:
        """Translate a RawGazettePayload DTO into a valid GazetteEdition domain entity."""
        summary_text = (
            payload.raw_content
            if isinstance(payload.raw_content, str)
            else (payload.source_url + f"-{payload.total_acts}-{payload.edition_number}")
        )
        resolved_date = self._resolve_date(payload)

        territory_id = TerritoryId.from_code(payload.territory_code)
        tier = FederativeTier(payload.tier.lower())
        gazette_date = None
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

    def xǁGazetteMapperǁto_domain__mutmut_11(self, payload: RawGazettePayload) -> GazetteEdition:
        """Translate a RawGazettePayload DTO into a valid GazetteEdition domain entity."""
        summary_text = (
            payload.raw_content
            if isinstance(payload.raw_content, str)
            else (payload.source_url + f"-{payload.total_acts}-{payload.edition_number}")
        )
        resolved_date = self._resolve_date(payload)

        territory_id = TerritoryId.from_code(payload.territory_code)
        tier = FederativeTier(payload.tier.lower())
        gazette_date = GazetteDate.from_date(None)
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

    def xǁGazetteMapperǁto_domain__mutmut_12(self, payload: RawGazettePayload) -> GazetteEdition:
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
        summary_hash = None

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

    def xǁGazetteMapperǁto_domain__mutmut_13(self, payload: RawGazettePayload) -> GazetteEdition:
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
        summary_hash = DocumentHash.from_text(None)

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

    def xǁGazetteMapperǁto_domain__mutmut_14(self, payload: RawGazettePayload) -> GazetteEdition:
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
        summary_hash = DocumentHash.from_text(summary_text and payload.source_url)

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

    def xǁGazetteMapperǁto_domain__mutmut_15(self, payload: RawGazettePayload) -> GazetteEdition:
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
            territory_id=None,
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

    def xǁGazetteMapperǁto_domain__mutmut_16(self, payload: RawGazettePayload) -> GazetteEdition:
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
            tier=None,
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

    def xǁGazetteMapperǁto_domain__mutmut_17(self, payload: RawGazettePayload) -> GazetteEdition:
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
            date=None,
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

    def xǁGazetteMapperǁto_domain__mutmut_18(self, payload: RawGazettePayload) -> GazetteEdition:
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
            edition_number=None,
            section=payload.section,
            is_extra_edition=payload.is_extra_edition,
            power=payload.power,
            source_url=payload.source_url,
            summary_hash=summary_hash,
            total_acts=payload.total_acts,
            ingestion_status=IngestionStatus.COMPLETED,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_domain__mutmut_19(self, payload: RawGazettePayload) -> GazetteEdition:
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
            section=None,
            is_extra_edition=payload.is_extra_edition,
            power=payload.power,
            source_url=payload.source_url,
            summary_hash=summary_hash,
            total_acts=payload.total_acts,
            ingestion_status=IngestionStatus.COMPLETED,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_domain__mutmut_20(self, payload: RawGazettePayload) -> GazetteEdition:
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
            is_extra_edition=None,
            power=payload.power,
            source_url=payload.source_url,
            summary_hash=summary_hash,
            total_acts=payload.total_acts,
            ingestion_status=IngestionStatus.COMPLETED,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_domain__mutmut_21(self, payload: RawGazettePayload) -> GazetteEdition:
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
            power=None,
            source_url=payload.source_url,
            summary_hash=summary_hash,
            total_acts=payload.total_acts,
            ingestion_status=IngestionStatus.COMPLETED,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_domain__mutmut_22(self, payload: RawGazettePayload) -> GazetteEdition:
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
            source_url=None,
            summary_hash=summary_hash,
            total_acts=payload.total_acts,
            ingestion_status=IngestionStatus.COMPLETED,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_domain__mutmut_23(self, payload: RawGazettePayload) -> GazetteEdition:
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
            summary_hash=None,
            total_acts=payload.total_acts,
            ingestion_status=IngestionStatus.COMPLETED,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_domain__mutmut_24(self, payload: RawGazettePayload) -> GazetteEdition:
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
            total_acts=None,
            ingestion_status=IngestionStatus.COMPLETED,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_domain__mutmut_25(self, payload: RawGazettePayload) -> GazetteEdition:
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
            ingestion_status=None,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_domain__mutmut_26(self, payload: RawGazettePayload) -> GazetteEdition:
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
            scraped_at=None,
        )

    def xǁGazetteMapperǁto_domain__mutmut_27(self, payload: RawGazettePayload) -> GazetteEdition:
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

    def xǁGazetteMapperǁto_domain__mutmut_28(self, payload: RawGazettePayload) -> GazetteEdition:
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

    def xǁGazetteMapperǁto_domain__mutmut_29(self, payload: RawGazettePayload) -> GazetteEdition:
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

    def xǁGazetteMapperǁto_domain__mutmut_30(self, payload: RawGazettePayload) -> GazetteEdition:
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
            section=payload.section,
            is_extra_edition=payload.is_extra_edition,
            power=payload.power,
            source_url=payload.source_url,
            summary_hash=summary_hash,
            total_acts=payload.total_acts,
            ingestion_status=IngestionStatus.COMPLETED,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_domain__mutmut_31(self, payload: RawGazettePayload) -> GazetteEdition:
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
            is_extra_edition=payload.is_extra_edition,
            power=payload.power,
            source_url=payload.source_url,
            summary_hash=summary_hash,
            total_acts=payload.total_acts,
            ingestion_status=IngestionStatus.COMPLETED,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_domain__mutmut_32(self, payload: RawGazettePayload) -> GazetteEdition:
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
            power=payload.power,
            source_url=payload.source_url,
            summary_hash=summary_hash,
            total_acts=payload.total_acts,
            ingestion_status=IngestionStatus.COMPLETED,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_domain__mutmut_33(self, payload: RawGazettePayload) -> GazetteEdition:
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
            source_url=payload.source_url,
            summary_hash=summary_hash,
            total_acts=payload.total_acts,
            ingestion_status=IngestionStatus.COMPLETED,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_domain__mutmut_34(self, payload: RawGazettePayload) -> GazetteEdition:
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
            summary_hash=summary_hash,
            total_acts=payload.total_acts,
            ingestion_status=IngestionStatus.COMPLETED,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_domain__mutmut_35(self, payload: RawGazettePayload) -> GazetteEdition:
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
            total_acts=payload.total_acts,
            ingestion_status=IngestionStatus.COMPLETED,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_domain__mutmut_36(self, payload: RawGazettePayload) -> GazetteEdition:
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
            ingestion_status=IngestionStatus.COMPLETED,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_domain__mutmut_37(self, payload: RawGazettePayload) -> GazetteEdition:
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
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_domain__mutmut_38(self, payload: RawGazettePayload) -> GazetteEdition:
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
            )

    def xǁGazetteMapperǁto_domain__mutmut_39(self, payload: RawGazettePayload) -> GazetteEdition:
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
            scraped_at=payload.scraped_at and datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_domain__mutmut_40(self, payload: RawGazettePayload) -> GazetteEdition:
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
            scraped_at=payload.scraped_at or datetime.now(None),
        )

    @_mutmut_mutated(mutants_xǁGazetteMapperǁto_normative_act__mutmut)
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

    def xǁGazetteMapperǁto_normative_act__mutmut_orig(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_1(
        self,
        payload: RawNormativeActPayload,
        edition_id: uuid.UUID | None = None,
    ) -> NormativeAct:
        """Translate a RawNormativeActPayload DTO into a valid NormativeAct domain entity."""
        raw_text = None
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

    def xǁGazetteMapperǁto_normative_act__mutmut_2(
        self,
        payload: RawNormativeActPayload,
        edition_id: uuid.UUID | None = None,
    ) -> NormativeAct:
        """Translate a RawNormativeActPayload DTO into a valid NormativeAct domain entity."""
        raw_text = payload.raw_content.strip()
        if raw_text:
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

    def xǁGazetteMapperǁto_normative_act__mutmut_3(
        self,
        payload: RawNormativeActPayload,
        edition_id: uuid.UUID | None = None,
    ) -> NormativeAct:
        """Translate a RawNormativeActPayload DTO into a valid NormativeAct domain entity."""
        raw_text = payload.raw_content.strip()
        if not raw_text:
            raise CorruptedGazettePayloadError(None)

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

    def xǁGazetteMapperǁto_normative_act__mutmut_4(
        self,
        payload: RawNormativeActPayload,
        edition_id: uuid.UUID | None = None,
    ) -> NormativeAct:
        """Translate a RawNormativeActPayload DTO into a valid NormativeAct domain entity."""
        raw_text = payload.raw_content.strip()
        if not raw_text:
            raise CorruptedGazettePayloadError("XXNormative act raw_content cannot be empty.XX")

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

    def xǁGazetteMapperǁto_normative_act__mutmut_5(
        self,
        payload: RawNormativeActPayload,
        edition_id: uuid.UUID | None = None,
    ) -> NormativeAct:
        """Translate a RawNormativeActPayload DTO into a valid NormativeAct domain entity."""
        raw_text = payload.raw_content.strip()
        if not raw_text:
            raise CorruptedGazettePayloadError("normative act raw_content cannot be empty.")

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

    def xǁGazetteMapperǁto_normative_act__mutmut_6(
        self,
        payload: RawNormativeActPayload,
        edition_id: uuid.UUID | None = None,
    ) -> NormativeAct:
        """Translate a RawNormativeActPayload DTO into a valid NormativeAct domain entity."""
        raw_text = payload.raw_content.strip()
        if not raw_text:
            raise CorruptedGazettePayloadError("NORMATIVE ACT RAW_CONTENT CANNOT BE EMPTY.")

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

    def xǁGazetteMapperǁto_normative_act__mutmut_7(
        self,
        payload: RawNormativeActPayload,
        edition_id: uuid.UUID | None = None,
    ) -> NormativeAct:
        """Translate a RawNormativeActPayload DTO into a valid NormativeAct domain entity."""
        raw_text = payload.raw_content.strip()
        if not raw_text:
            raise CorruptedGazettePayloadError("Normative act raw_content cannot be empty.")

        content_hash = None
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

    def xǁGazetteMapperǁto_normative_act__mutmut_8(
        self,
        payload: RawNormativeActPayload,
        edition_id: uuid.UUID | None = None,
    ) -> NormativeAct:
        """Translate a RawNormativeActPayload DTO into a valid NormativeAct domain entity."""
        raw_text = payload.raw_content.strip()
        if not raw_text:
            raise CorruptedGazettePayloadError("Normative act raw_content cannot be empty.")

        content_hash = DocumentHash.from_text(None)
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

    def xǁGazetteMapperǁto_normative_act__mutmut_9(
        self,
        payload: RawNormativeActPayload,
        edition_id: uuid.UUID | None = None,
    ) -> NormativeAct:
        """Translate a RawNormativeActPayload DTO into a valid NormativeAct domain entity."""
        raw_text = payload.raw_content.strip()
        if not raw_text:
            raise CorruptedGazettePayloadError("Normative act raw_content cannot be empty.")

        content_hash = DocumentHash.from_text(raw_text)
        char_count = None
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

    def xǁGazetteMapperǁto_normative_act__mutmut_10(
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
        territory_id = None
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

    def xǁGazetteMapperǁto_normative_act__mutmut_11(
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
        territory_id = TerritoryId.from_code(None)
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

    def xǁGazetteMapperǁto_normative_act__mutmut_12(
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
        gazette_date = None

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

    def xǁGazetteMapperǁto_normative_act__mutmut_13(
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
        gazette_date = GazetteDate.from_date(None)

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

    def xǁGazetteMapperǁto_normative_act__mutmut_14(
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

        group, rank, nature = None
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

    def xǁGazetteMapperǁto_normative_act__mutmut_15(
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

        group, rank, nature = resolve_hierarchy(None, payload.section)
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

    def xǁGazetteMapperǁto_normative_act__mutmut_16(
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

        group, rank, nature = resolve_hierarchy(payload.act_type, None)
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

    def xǁGazetteMapperǁto_normative_act__mutmut_17(
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

        group, rank, nature = resolve_hierarchy(payload.section)
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

    def xǁGazetteMapperǁto_normative_act__mutmut_18(
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

        group, rank, nature = resolve_hierarchy(payload.act_type, )
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

    def xǁGazetteMapperǁto_normative_act__mutmut_19(
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
        canonical_urn = None

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

    def xǁGazetteMapperǁto_normative_act__mutmut_20(
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
            territory_code=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_21(
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
            act_type=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_22(
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
            act_number=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_23(
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
            act_year=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_24(
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
            act_date=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_25(
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
            content_hash=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_26(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_27(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_28(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_29(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_30(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_31(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_32(
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
            edition_id=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_33(
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
            territory_id=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_34(
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
            date=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_35(
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
            section=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_36(
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
            edition_number=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_37(
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
            is_extra_edition=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_38(
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
            act_type=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_39(
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
            act_number=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_40(
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
            act_year=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_41(
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
            title=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_42(
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
            ementa=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_43(
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
            hierarchy=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_44(
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
            authority_name=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_45(
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
            authority_role=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_46(
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
            source_url=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_47(
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
            content_hash=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_48(
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
            char_count=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_49(
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
            raw_content=None,
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

    def xǁGazetteMapperǁto_normative_act__mutmut_50(
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
            classification_source=None,
            classification_confidence=payload.classification_confidence,
            hierarchical_group=group,
            hierarchical_rank=rank,
            publication_nature=nature,
            canonical_urn=canonical_urn,
            is_stub=False,
            metadata_json=payload.metadata_json,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_normative_act__mutmut_51(
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
            classification_confidence=None,
            hierarchical_group=group,
            hierarchical_rank=rank,
            publication_nature=nature,
            canonical_urn=canonical_urn,
            is_stub=False,
            metadata_json=payload.metadata_json,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_normative_act__mutmut_52(
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
            hierarchical_group=None,
            hierarchical_rank=rank,
            publication_nature=nature,
            canonical_urn=canonical_urn,
            is_stub=False,
            metadata_json=payload.metadata_json,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_normative_act__mutmut_53(
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
            hierarchical_rank=None,
            publication_nature=nature,
            canonical_urn=canonical_urn,
            is_stub=False,
            metadata_json=payload.metadata_json,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_normative_act__mutmut_54(
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
            publication_nature=None,
            canonical_urn=canonical_urn,
            is_stub=False,
            metadata_json=payload.metadata_json,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_normative_act__mutmut_55(
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
            canonical_urn=None,
            is_stub=False,
            metadata_json=payload.metadata_json,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_normative_act__mutmut_56(
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
            is_stub=None,
            metadata_json=payload.metadata_json,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_normative_act__mutmut_57(
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
            metadata_json=None,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_normative_act__mutmut_58(
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
            scraped_at=None,
        )

    def xǁGazetteMapperǁto_normative_act__mutmut_59(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_60(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_61(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_62(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_63(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_64(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_65(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_66(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_67(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_68(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_69(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_70(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_71(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_72(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_73(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_74(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_75(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_76(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_77(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_78(
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

    def xǁGazetteMapperǁto_normative_act__mutmut_79(
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
            classification_confidence=payload.classification_confidence,
            hierarchical_group=group,
            hierarchical_rank=rank,
            publication_nature=nature,
            canonical_urn=canonical_urn,
            is_stub=False,
            metadata_json=payload.metadata_json,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_normative_act__mutmut_80(
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
            hierarchical_group=group,
            hierarchical_rank=rank,
            publication_nature=nature,
            canonical_urn=canonical_urn,
            is_stub=False,
            metadata_json=payload.metadata_json,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_normative_act__mutmut_81(
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
            hierarchical_rank=rank,
            publication_nature=nature,
            canonical_urn=canonical_urn,
            is_stub=False,
            metadata_json=payload.metadata_json,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_normative_act__mutmut_82(
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
            publication_nature=nature,
            canonical_urn=canonical_urn,
            is_stub=False,
            metadata_json=payload.metadata_json,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_normative_act__mutmut_83(
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
            canonical_urn=canonical_urn,
            is_stub=False,
            metadata_json=payload.metadata_json,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_normative_act__mutmut_84(
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
            is_stub=False,
            metadata_json=payload.metadata_json,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_normative_act__mutmut_85(
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
            metadata_json=payload.metadata_json,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_normative_act__mutmut_86(
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
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_normative_act__mutmut_87(
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
            )

    def xǁGazetteMapperǁto_normative_act__mutmut_88(
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
            classification_source=ClassificationSource(None),
            classification_confidence=payload.classification_confidence,
            hierarchical_group=group,
            hierarchical_rank=rank,
            publication_nature=nature,
            canonical_urn=canonical_urn,
            is_stub=False,
            metadata_json=payload.metadata_json,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_normative_act__mutmut_89(
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
            is_stub=True,
            metadata_json=payload.metadata_json,
            scraped_at=payload.scraped_at or datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_normative_act__mutmut_90(
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
            scraped_at=payload.scraped_at and datetime.now(UTC),
        )

    def xǁGazetteMapperǁto_normative_act__mutmut_91(
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
            scraped_at=payload.scraped_at or datetime.now(None),
        )

    @staticmethod
    @_mutmut_mutated(mutants_xǁGazetteMapperǁ_resolve_date__mutmut)
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

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_orig(payload: RawGazettePayload) -> date:
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

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_1(payload: RawGazettePayload) -> date:
        """Resolve date from date_obj or standard Brazilian string representations."""
        if payload.date_obj is None:
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

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_2(payload: RawGazettePayload) -> date:
        """Resolve date from date_obj or standard Brazilian string representations."""
        if payload.date_obj is not None:
            return payload.date_obj

        if payload.raw_date_str is not None:
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

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_3(payload: RawGazettePayload) -> date:
        """Resolve date from date_obj or standard Brazilian string representations."""
        if payload.date_obj is not None:
            return payload.date_obj

        if payload.raw_date_str is None:
            raise InvalidGazetteDateError(None)

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

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_4(payload: RawGazettePayload) -> date:
        """Resolve date from date_obj or standard Brazilian string representations."""
        if payload.date_obj is not None:
            return payload.date_obj

        if payload.raw_date_str is None:
            raise InvalidGazetteDateError("XXNo publication date provided in payload.XX")

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

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_5(payload: RawGazettePayload) -> date:
        """Resolve date from date_obj or standard Brazilian string representations."""
        if payload.date_obj is not None:
            return payload.date_obj

        if payload.raw_date_str is None:
            raise InvalidGazetteDateError("no publication date provided in payload.")

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

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_6(payload: RawGazettePayload) -> date:
        """Resolve date from date_obj or standard Brazilian string representations."""
        if payload.date_obj is not None:
            return payload.date_obj

        if payload.raw_date_str is None:
            raise InvalidGazetteDateError("NO PUBLICATION DATE PROVIDED IN PAYLOAD.")

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

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_7(payload: RawGazettePayload) -> date:
        """Resolve date from date_obj or standard Brazilian string representations."""
        if payload.date_obj is not None:
            return payload.date_obj

        if payload.raw_date_str is None:
            raise InvalidGazetteDateError("No publication date provided in payload.")

        raw_str = None

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

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_8(payload: RawGazettePayload) -> date:
        """Resolve date from date_obj or standard Brazilian string representations."""
        if payload.date_obj is not None:
            return payload.date_obj

        if payload.raw_date_str is None:
            raise InvalidGazetteDateError("No publication date provided in payload.")

        raw_str = payload.raw_date_str.strip()

        # Try ISO format YYYY-MM-DD
        if ISO_DATE_PATTERN.match(None):
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

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_9(payload: RawGazettePayload) -> date:
        """Resolve date from date_obj or standard Brazilian string representations."""
        if payload.date_obj is not None:
            return payload.date_obj

        if payload.raw_date_str is None:
            raise InvalidGazetteDateError("No publication date provided in payload.")

        raw_str = payload.raw_date_str.strip()

        # Try ISO format YYYY-MM-DD
        if ISO_DATE_PATTERN.match(raw_str):
            try:
                return datetime.strptime(raw_str, "%Y-%m-%d").replace(tzinfo=None).date()
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

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_10(payload: RawGazettePayload) -> date:
        """Resolve date from date_obj or standard Brazilian string representations."""
        if payload.date_obj is not None:
            return payload.date_obj

        if payload.raw_date_str is None:
            raise InvalidGazetteDateError("No publication date provided in payload.")

        raw_str = payload.raw_date_str.strip()

        # Try ISO format YYYY-MM-DD
        if ISO_DATE_PATTERN.match(raw_str):
            try:
                return datetime.strptime(None, "%Y-%m-%d").replace(tzinfo=UTC).date()
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

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_11(payload: RawGazettePayload) -> date:
        """Resolve date from date_obj or standard Brazilian string representations."""
        if payload.date_obj is not None:
            return payload.date_obj

        if payload.raw_date_str is None:
            raise InvalidGazetteDateError("No publication date provided in payload.")

        raw_str = payload.raw_date_str.strip()

        # Try ISO format YYYY-MM-DD
        if ISO_DATE_PATTERN.match(raw_str):
            try:
                return datetime.strptime(raw_str, None).replace(tzinfo=UTC).date()
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

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_12(payload: RawGazettePayload) -> date:
        """Resolve date from date_obj or standard Brazilian string representations."""
        if payload.date_obj is not None:
            return payload.date_obj

        if payload.raw_date_str is None:
            raise InvalidGazetteDateError("No publication date provided in payload.")

        raw_str = payload.raw_date_str.strip()

        # Try ISO format YYYY-MM-DD
        if ISO_DATE_PATTERN.match(raw_str):
            try:
                return datetime.strptime("%Y-%m-%d").replace(tzinfo=UTC).date()
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

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_13(payload: RawGazettePayload) -> date:
        """Resolve date from date_obj or standard Brazilian string representations."""
        if payload.date_obj is not None:
            return payload.date_obj

        if payload.raw_date_str is None:
            raise InvalidGazetteDateError("No publication date provided in payload.")

        raw_str = payload.raw_date_str.strip()

        # Try ISO format YYYY-MM-DD
        if ISO_DATE_PATTERN.match(raw_str):
            try:
                return datetime.strptime(raw_str, ).replace(tzinfo=UTC).date()
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

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_14(payload: RawGazettePayload) -> date:
        """Resolve date from date_obj or standard Brazilian string representations."""
        if payload.date_obj is not None:
            return payload.date_obj

        if payload.raw_date_str is None:
            raise InvalidGazetteDateError("No publication date provided in payload.")

        raw_str = payload.raw_date_str.strip()

        # Try ISO format YYYY-MM-DD
        if ISO_DATE_PATTERN.match(raw_str):
            try:
                return datetime.strptime(raw_str, "XX%Y-%m-%dXX").replace(tzinfo=UTC).date()
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

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_15(payload: RawGazettePayload) -> date:
        """Resolve date from date_obj or standard Brazilian string representations."""
        if payload.date_obj is not None:
            return payload.date_obj

        if payload.raw_date_str is None:
            raise InvalidGazetteDateError("No publication date provided in payload.")

        raw_str = payload.raw_date_str.strip()

        # Try ISO format YYYY-MM-DD
        if ISO_DATE_PATTERN.match(raw_str):
            try:
                return datetime.strptime(raw_str, "%y-%m-%d").replace(tzinfo=UTC).date()
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

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_16(payload: RawGazettePayload) -> date:
        """Resolve date from date_obj or standard Brazilian string representations."""
        if payload.date_obj is not None:
            return payload.date_obj

        if payload.raw_date_str is None:
            raise InvalidGazetteDateError("No publication date provided in payload.")

        raw_str = payload.raw_date_str.strip()

        # Try ISO format YYYY-MM-DD
        if ISO_DATE_PATTERN.match(raw_str):
            try:
                return datetime.strptime(raw_str, "%Y-%M-%D").replace(tzinfo=UTC).date()
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

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_17(payload: RawGazettePayload) -> date:
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
                err_msg = None
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

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_18(payload: RawGazettePayload) -> date:
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
                raise InvalidGazetteDateError(None) from exc

        # Try Brazilian formats DD/MM/YYYY or DD-MM-YYYY
        for fmt in BRAZILIAN_DATE_FORMATS:
            try:
                return datetime.strptime(raw_str, fmt).replace(tzinfo=UTC).date()
            except ValueError:
                continue

        raise InvalidGazetteDateError(
            f"Unable to parse date string '{raw_str}'. Expected ISO or Brazilian format."
        )

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_19(payload: RawGazettePayload) -> date:
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
                return datetime.strptime(raw_str, fmt).replace(tzinfo=None).date()
            except ValueError:
                continue

        raise InvalidGazetteDateError(
            f"Unable to parse date string '{raw_str}'. Expected ISO or Brazilian format."
        )

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_20(payload: RawGazettePayload) -> date:
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
                return datetime.strptime(None, fmt).replace(tzinfo=UTC).date()
            except ValueError:
                continue

        raise InvalidGazetteDateError(
            f"Unable to parse date string '{raw_str}'. Expected ISO or Brazilian format."
        )

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_21(payload: RawGazettePayload) -> date:
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
                return datetime.strptime(raw_str, None).replace(tzinfo=UTC).date()
            except ValueError:
                continue

        raise InvalidGazetteDateError(
            f"Unable to parse date string '{raw_str}'. Expected ISO or Brazilian format."
        )

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_22(payload: RawGazettePayload) -> date:
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
                return datetime.strptime(fmt).replace(tzinfo=UTC).date()
            except ValueError:
                continue

        raise InvalidGazetteDateError(
            f"Unable to parse date string '{raw_str}'. Expected ISO or Brazilian format."
        )

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_23(payload: RawGazettePayload) -> date:
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
                return datetime.strptime(raw_str, ).replace(tzinfo=UTC).date()
            except ValueError:
                continue

        raise InvalidGazetteDateError(
            f"Unable to parse date string '{raw_str}'. Expected ISO or Brazilian format."
        )

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_24(payload: RawGazettePayload) -> date:
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
                break

        raise InvalidGazetteDateError(
            f"Unable to parse date string '{raw_str}'. Expected ISO or Brazilian format."
        )

    @staticmethod
    def xǁGazetteMapperǁ_resolve_date__mutmut_25(payload: RawGazettePayload) -> date:
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
            None
        )

mutants_xǁGazetteMapperǁ__init____mutmut['_mutmut_orig'] = GazetteMapper.xǁGazetteMapperǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ__init____mutmut['xǁGazetteMapperǁ__init____mutmut_1'] = GazetteMapper.xǁGazetteMapperǁ__init____mutmut_1 # type: ignore # mutmut generated

mutants_xǁGazetteMapperǁto_domain__mutmut['_mutmut_orig'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_orig # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_1'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_1 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_2'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_2 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_3'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_3 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_4'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_4 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_5'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_5 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_6'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_6 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_7'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_7 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_8'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_8 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_9'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_9 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_10'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_10 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_11'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_11 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_12'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_12 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_13'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_13 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_14'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_14 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_15'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_15 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_16'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_16 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_17'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_17 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_18'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_18 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_19'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_19 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_20'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_20 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_21'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_21 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_22'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_22 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_23'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_23 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_24'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_24 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_25'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_25 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_26'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_26 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_27'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_27 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_28'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_28 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_29'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_29 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_30'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_30 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_31'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_31 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_32'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_32 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_33'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_33 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_34'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_34 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_35'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_35 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_36'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_36 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_37'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_37 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_38'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_38 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_39'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_39 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_domain__mutmut['xǁGazetteMapperǁto_domain__mutmut_40'] = GazetteMapper.xǁGazetteMapperǁto_domain__mutmut_40 # type: ignore # mutmut generated

mutants_xǁGazetteMapperǁto_normative_act__mutmut['_mutmut_orig'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_orig # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_1'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_1 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_2'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_2 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_3'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_3 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_4'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_4 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_5'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_5 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_6'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_6 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_7'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_7 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_8'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_8 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_9'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_9 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_10'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_10 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_11'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_11 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_12'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_12 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_13'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_13 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_14'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_14 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_15'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_15 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_16'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_16 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_17'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_17 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_18'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_18 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_19'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_19 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_20'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_20 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_21'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_21 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_22'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_22 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_23'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_23 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_24'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_24 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_25'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_25 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_26'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_26 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_27'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_27 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_28'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_28 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_29'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_29 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_30'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_30 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_31'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_31 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_32'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_32 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_33'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_33 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_34'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_34 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_35'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_35 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_36'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_36 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_37'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_37 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_38'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_38 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_39'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_39 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_40'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_40 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_41'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_41 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_42'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_42 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_43'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_43 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_44'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_44 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_45'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_45 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_46'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_46 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_47'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_47 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_48'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_48 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_49'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_49 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_50'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_50 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_51'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_51 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_52'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_52 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_53'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_53 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_54'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_54 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_55'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_55 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_56'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_56 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_57'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_57 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_58'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_58 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_59'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_59 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_60'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_60 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_61'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_61 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_62'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_62 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_63'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_63 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_64'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_64 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_65'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_65 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_66'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_66 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_67'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_67 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_68'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_68 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_69'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_69 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_70'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_70 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_71'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_71 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_72'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_72 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_73'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_73 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_74'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_74 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_75'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_75 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_76'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_76 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_77'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_77 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_78'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_78 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_79'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_79 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_80'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_80 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_81'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_81 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_82'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_82 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_83'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_83 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_84'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_84 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_85'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_85 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_86'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_86 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_87'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_87 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_88'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_88 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_89'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_89 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_90'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_90 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁto_normative_act__mutmut['xǁGazetteMapperǁto_normative_act__mutmut_91'] = GazetteMapper.xǁGazetteMapperǁto_normative_act__mutmut_91 # type: ignore # mutmut generated

mutants_xǁGazetteMapperǁ_resolve_date__mutmut['_mutmut_orig'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_orig # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_1'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_1 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_2'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_2 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_3'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_3 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_4'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_4 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_5'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_5 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_6'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_6 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_7'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_7 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_8'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_8 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_9'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_9 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_10'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_10 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_11'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_11 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_12'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_12 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_13'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_13 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_14'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_14 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_15'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_15 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_16'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_16 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_17'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_17 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_18'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_18 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_19'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_19 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_20'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_20 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_21'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_21 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_22'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_22 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_23'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_23 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_24'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_24 # type: ignore # mutmut generated
mutants_xǁGazetteMapperǁ_resolve_date__mutmut['xǁGazetteMapperǁ_resolve_date__mutmut_25'] = GazetteMapper.xǁGazetteMapperǁ_resolve_date__mutmut_25 # type: ignore # mutmut generated
