"""Value Objects and Types for the LEX Shared Kernel.

Defines the core cross-context value objects including the Constitutional Kelsenian
Hierarchy Strata, Authority Ranks, and Publication Nature.
"""

from enum import IntEnum, StrEnum


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class HierarchicalGroup(IntEnum):
    """Eight empirical publication strata grounded in Hans Kelsen's pyramid (ADR-007)."""

    GRUPO_1_PRIMARIO = 1  # CF, EC, LC, Lei Ordinária, MP, Decreto Legislativo
    GRUPO_2_EXECUTIVO = 2  # Decretos do Chefe do Executivo
    GRUPO_3_COLEGIADO_REGULATORIO = 3  # Resoluções, Deliberações, INs, Provimentos
    GRUPO_4_ORDINATORIO_MINISTERIAL = 4  # Portarias, Atos Declaratórios Executivos
    GRUPO_5_DECISORIO_CONCRETO = 5  # Acórdãos, Decisões, Despachos, Alvarás, Soluções de Consulta
    GRUPO_6_EDITALICIO = 6  # Editais, Atos Convocatórios, Atas
    GRUPO_7_CONTRATUAL = 7  # Contratos, Convênios, Acordos de Cooperação
    GRUPO_8_PUBLICIDADE_EXTRATOS = (
        8  # Extratos, Avisos de Licitação, Resultados, Retificações, Pautas
    )


class HierarchicalRank(IntEnum):
    """Numerical authority weights for Kelsenian & LINDB precedence validation (SPEC-003)."""

    EMENDA_CONSTITUCIONAL = 100
    TRATADO_SUPRALEGAL = 90
    LEI_COMPLEMENTAR = 80
    LEI_ORDINARIA = 70
    MEDIDA_PROVISORIA = 70
    DECRETO_LEGISLATIVO = 70
    LEI_DELEGADA = 70
    DECRETO_EXECUTIVO = 60
    RESOLUCAO_REGULATORIA = 50
    INSTRUCAO_NORMATIVA = 50
    PORTARIA_NORMATIVA = 40
    ATO_ADMINISTRATIVO_CONCRETO = 20
    PUBLICIDADE_OPERACIONAL = 10


class PublicationNature(StrEnum):
    """Routing classifier for Dual-Track processing pipeline (ADR-007)."""

    NORMATIVA_ABSTRATA = "normativa_abstrata"  # Trilha A: Deep AST & Delta Ledger
    REGULATORIA_SETORIAL = "regulatoria_setorial"  # Trilha A: Deep AST & Delta Ledger
    CONCRETA_INDIVIDUAL = "concreta_individual"  # Trilha B: Fast-Path NER Entity Extraction
    PUBLICIDADE_OPERACIONAL = "publicidade_operacional"  # Trilha B: Fast-Path NER Entity Extraction
