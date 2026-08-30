# SPEC-003: Normative Hierarchy, Typology Taxonomy, and Dual-Track Classification Specification

**Linked ADR:** [ADR-007](../adr/ADR-007-normative-hierarchy-kelsen-strata-and-dual-track-pipeline.md)  
**Status:** APPROVED  
**Date:** 2026-08-29  
**Bounded Context:** `shared_kernel`, `ingestion`, `treatment`, `consolidation`  

---

## 1. Overview & Objectives

This specification establishes the precision contracts, value objects, domain invariants, complete empirical typology registries (covering all 8 groups and hundreds of gazette subtypes), top-down precedence matching rules, and LINDB validation mechanics for the **LEX Normative Hierarchy & Classification Engine**. It operationalizes the constitutional and administrative principles codified in [ADR-007](../adr/ADR-007-normative-hierarchy-kelsen-strata-and-dual-track-pipeline.md).

---

## 2. Value Objects & Type Definitions

```python
from enum import IntEnum, StrEnum
from pydantic import BaseModel, Field


class HierarchicalGroup(IntEnum):
    """Eight empirical publication strata grounded in Hans Kelsen's pyramid."""

    GRUPO_1_PRIMARIO = 1  # CF, EC, LC, Lei Ordinária, MP, Decreto Legislativo
    GRUPO_2_EXECUTIVO = 2  # Decretos do Chefe do Executivo
    GRUPO_3_COLEGIADO_REGULATORIO = 3  # Resoluções, Deliberações, INs, Provimentos
    GRUPO_4_ORDINATORIO_MINISTERIAL = 4  # Portarias, Atos Declaratórios Executivos
    GRUPO_5_DECISORIO_CONCRETO = (
        5  # Acórdãos, Decisões, Despachos, Alvarás, Soluções de Consulta
    )
    GRUPO_6_EDITALICIO = 6  # Editais, Atos Convocatórios, Atas
    GRUPO_7_CONTRATUAL = 7  # Contratos, Convênios, Acordos de Cooperação
    GRUPO_8_PUBLICIDADE_EXTRATOS = (
        8  # Extratos, Avisos de Licitação, Resultados, Retificações, Pautas
    )


class HierarchicalRank(IntEnum):
    """Numerical authority weights for Kelsenian & LINDB precedence validation."""

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
    """Routing classifier for Dual-Track Stage 2 processing."""

    NORMATIVA_ABSTRATA = "normativa_abstrata"  # Trilha A: Deep AST & Delta Ledger
    REGULATORIA_SETORIAL = (
        "regulatoria_setorial"  # Trilha A: Deep AST & Delta Ledger
    )
    CONCRETA_INDIVIDUAL = (
        "concreta_individual"  # Trilha B: Fast-Path NER Entity Extraction
    )
    PUBLICIDADE_OPERACIONAL = (
        "publicidade_operacional"  # Trilha B: Fast-Path NER Entity Extraction
    )
```

---

## 3. Complete Empirical Typology & Subtype Registry

The following registry codifies all empirical subtypes and aliases discovered across Brazilian official gazette publications:

### 3.1 Grupo 1: Atos Normativos Primários (Rank: 70–80)
* **`LEI COMPLEMENTAR`** (Rank 80, Nature: `normativa_abstrata`)
* **`LEI`** / `LEIS` (Rank 70, Nature: `normativa_abstrata`)
* **`MEDIDA PROVISÓRIA`** / `MEDIDA PROVISORIA` (Rank 70, Nature: `normativa_abstrata`)
* **`DECRETO LEGISLATIVO`** (Rank 70, Nature: `normativa_abstrata`)
* **`LEI DELEGADA`** (Rank 70, Nature: `normativa_abstrata`)

### 3.2 Grupo 2: Decretos do Poder Executivo (Rank: 60)
* **`DECRETO`** / `DECRETOS` / `DECRETO NÃO NUMERADO` (Rank 60, Nature: `normativa_abstrata`)

### 3.3 Grupo 3: Atos Normativos Secundários Colegiados e Diretivos (Rank: 50)
* **Resoluções e Subtipos (1.731+ variações)**: `RESOLUÇÃO-RE`, `RESOLUÇÃO`, `RESOLUÇÃO AUTORIZATIVA`, `RESOLUÇÃO GECEX`, `RESOLUÇÃO OPERACIONAL ANS`, `RESOLUÇÃO CFFA`, `RESOLUÇÃO COFIEX/MPO`, `RESOLUÇÃO CZPE/MDIC`, `RESOLUÇÃO CFN`, `RESOLUÇÃO DA DIRETORIA COLEGIADA ANVISA`, `RESOLUÇÃO - CDR`, `RESOLUÇÃO SUSEP`, `RESOLUÇÃO-COFFITO`, `RESOLUÇÃO HOMOLOGATÓRIA`, `RESOLUÇÃO - CD`, `RESOLUÇÃO BCB`, `RESOLUÇÃO CATI`, `RESOLUÇÃO ADMINISTRATIVA`, `RESOLUÇÃO CCFGTS`, `RESOLUÇÃO CMN`, `RESOLUÇÃO CRD`, `RESOLUÇÃO CFM`, `RESOLUÇÃO ANA`, `RESOLUÇÃO ANM`, `RESOLUÇÃO ANTAQ`, `RESOLUÇÃO ANP`, `RESOLUÇÃO CFC`, `RESOLUÇÃO CONTRAN`, `RESOLUÇÃO CCFCVS`, `RESOLUÇÃO CER-PROAGRO`, `RESOLUÇÃO CNAS/MDS`, `RESOLUÇÃO COFEN`, `RESOLUÇÃO CPPI`, `RESOLUÇÃO PRES`, `RESOLUÇÃO ANTT`, `RESOLUÇÃO CAISAN/MDS`, `RESOLUÇÃO CFBM`, `RESOLUÇÃO CGSN`, `RESOLUÇÃO CJF`, `RESOLUÇÃO CNSP`, `RESOLUÇÃO CONDEL/SUDECO`, `RESOLUÇÃO CONSUP/IFSUL`, `RESOLUÇÃO DC/SUDENE`, `RESOLUÇÃO SUDECO`, `RESOLUÇÃO CD/FNDCT MCTI`, `RESOLUÇÃO CD/FNDE`, `RESOLUÇÃO CDPNB`, `RESOLUÇÃO CFBIO`, `RESOLUÇÃO CFO`, `RESOLUÇÃO CFQ`, `RESOLUÇÃO CITSB`, `RESOLUÇÃO CNRM`, `RESOLUÇÃO CNRMS`, `RESOLUÇÃO CONDEL/SUDENE`, `RESOLUÇÃO CONSUP`, `RESOLUÇÃO CONTER`, `RESOLUÇÃO CRCRO`, `RESOLUÇÃO CRCSE`, `RESOLUÇÃO CSMPF`, `RESOLUÇÃO GGPAA`, `RESOLUÇÃO/CEPE/UFES`, `RESOLUÇÃO ANATEL`, `RESOLUÇÃO CDPEB`, `RESOLUÇÃO CVM`, `RESOLUÇÃO CADE`, `RESOLUÇÕES`.
* **Deliberações e Subtipos (287+ variações)**: `DELIBERAÇÃO`, `DELIBERAÇÃO ANTT`, `DELIBERAÇÃO-SOG`, `DELIBERAÇÃO-DG`, `DELIBERAÇÃO PAS`, `DELIBERAÇÃO CRCSC`, `DELIBERAÇÃO DO PLENÁRIO DO CONCEA/MCTI`, `DELIBERAÇÃO AD REFERENDUM`, `DELIBERAÇÃO CFC`, `DELIBERAÇÃO CRC SP`, `DELIBERAÇÃO CRCMT`, `DELIBERAÇÃO SAOC`.
* **Instruções e Normas Regulamentares (137+ variações)**: `INSTRUÇÃO`, `INSTRUÇÃO NORMATIVA`, `CIRCULAR`, `NORMA BRASILEIRA DE CONTABILIDADE NBC TSP`, `NORMA`, `NORMA BRASILEIRA DE CONTABILIDADE - NBC ITP`.
* **Provimentos e Regimentais (6+ variações)**: `PROVIMENTO COGER`, `PROVIMENTO`, `PROVIMENTO CG-CJF`, `EMENDA REGIMENTAL`.

### 3.4 Grupo 4: Atos Normativos e Ordinatórios Ministeriais (Rank: 40)
* **Portarias em Geral (38.808+ variações)**: `PORTARIA`, `PORTARIAS`, `PORTARIA DE PESSOAL`, `PORTARIA DGP/PF`, `PORTARIA CGBEN/DECIPEX/SGP/MGI`, `PORTARIA MCOM`, `PORTARIA GM/MS`, `PORTARIA SE/MAPA`, `PORTARIA SE/MTE`, `PORTARIA SAES/MS`, `PORTARIA SSC/MGI`, `PORTARIA SGA/AGU`, `PORTARIA PRES/INSS`, `PORTARIA DG`, `PORTARIA DCOMB-RPPU/INSS`, `PORTARIA SE/CC/PR`, `PORTARIA SGP`, `PORTARIA SE/MS`, `PORTARIA MPS`, `PORTARIA IFRJ`, `PORTARIA CGBEN/MGI`, `PORTARIA UFPR`, `PORTARIA MIDR`, `PORTARIA DEPRO/SGP/MGI`, `PORTARIA SE/MJSP`, `PORTARIA STJ/GDG`, `PORTARIA SEGEP/RJ`, `PORTARIA MINC`, `PORTARIA PGR/MPF`, `PORTARIA SEFIC/MINC`, `PORTARIA SERES/MEC`, `PORTARIA GABAER`, `PORTARIA PROGEPE/UFJF`, `PORTARIA MEC`, `PORTARIA SE/MF`, `PORTARIA - C EX`, `PORTARIA SG/MPF`, `PORTARIA GPR`, `PORTARIA STJ/GP`, `PORTARIA FUNAI`, `PORTARIA IBAMA`, `PORTARIA CAPES`, `PORTARIA PREVIC`, `PORTARIA CONJUNTA`, `PORTARIAS DE PESSOAL`.
* **Atos e Subtipos (3.447+ variações)**: `ATO`, `ATOS`, `ATO PRESI`, `ATO PR`, `ATO DE PESSOAL`, `ATO PRES`, `ATO CPV`, `ATO VPCRE`, `ATO TRT/DG/GP`, `ATO COTEPE/ICMS`, `ATO DO PRESIDENTE DA MESA DO CONGRESSO NACIONAL`.
* **Atos Declaratórios (427+ variações)**: `ATO DECLARATÓRIO EXECUTIVO`, `ATO DECLARATÓRIO DECEX/RJO`, `ATO DECLARATÓRIO CVM`, `ATO DECLARATÓRIO ALF/CTA`, `ATO DECLARATÓRIO CORAT`, `ATO DECLARATÓRIO DRF/SOR`, `ATO DECLARATÓRIO COANA`, `ATO DECLARATÓRIO INTERPRETATIVO RFB`.

### 3.5 Grupo 5: Atos Administrativos Decisórios e Regulatórios Concretos (Rank: 20)
* **Acórdãos e Arestos (276+ variações)**: `ACÓRDÃO`, `ACÓRDÃO COFEN`, `ACÓRDÃOS`, `ARESTO`, `ACORDÃO`, `ACÓRDÃO-COFFITO`, `ACÓRDÃO CG-FUST`, `ACORDÃO PLENÁRIO`.
* **Decisões (1.503+ variações)**: `DECISÃO SUROD`, `DECISÃO SUPAS`, `DECISÃO`, `DECISÃO SUROC`, `DECISÕES`, `DECISÃO SUFER`, `DECISÃO PLENÁRIA`, `DECISÃO COFEN`, `DECISÃO ADMINISTRATIVA`.
* **Despachos (6.166+ variações)**: `DESPACHO`, `DESPACHOS`, `DESPACHO SDL-ANP`, `DESPACHO DECISÓRIO`, `DESPACHO SEP-ANP`, `DESPACHO STM-ANP`, `DESPACHO SG`, `DESPACHO MINC`, `DESPACHO ANP`, `DESPACHO GM/MS`, `DESPACHO ICMBIO`, `DESPACHO DECISÓRIO CD/ANPD`.
* **Alvarás, Licenças e Autorizações (893+ variações)**: `ALVARÁ`, `AUTORIZAÇÃO SDL-ANP`, `AUTORIZAÇÃO SIM-ANP`, `AUTORIZAÇÃO SPC-ANP`, `AUTORIZAÇÃO CPT-ANP`, `AUTORIZAÇÃO ANP`, `LICENÇA`, `PERMISSÃO`.
* **Soluções de Consulta (74+ variações)**: `SOLUÇÃO DE CONSULTA`, `SOLUÇÃO DE CONSULTA COSIT`.

### 3.6 Grupo 6: Instrumentos Editalícios e Convocatórios (Rank: 10)
* **Editais e Subtipos (10.963+ variações)**: `EDITAL DE`, `EDITAL`, `EDITAL DE INTIMAÇÃO`, `EDITAL DE CONVOCAÇÃO`, `EDITAL PROGEP`, `EDITAL DE CIÊNCIA DE ELIMINAÇÃO DE DOCUMENTOS`, `EDITAL ELEITORAL`, `EDITAL DE HOMOLOGAÇÃO`, `EDITAL DE CHAMAMENTO PÚBLICO`, `EDITAIS`, `EDITAL DE CONCURSO PÚBLICO`.
* **Atos Convocatórios & Atas (109+ variações)**: `ATO CONVOCATÓRIO`, `ATA`, `ATA DA ASSEMBLEIA GERAL EXTRAORDINÁRIA`, `ATA DA REUNIÃO`.

### 3.7 Grupo 7: Instrumentos Contratuais e Convênios (Rank: 10)
* **Contratos e Aditamentos (32+ variações)**: `TERMO`, `AJUSTE`, `CONTRATO`, `CONTRATO/SEE`, `TERMO ADITIVO`, `TERMO DE CONTRATO`, `TERMO DE PATROCÍNIO`, `ADITAMENTO`, `DISTRATO`, `RESCISÃO`, `RESUMO DE CONTRATO`, `PROTOCOLO DE INTENÇÕES`.
* **Convênios e Cooperação (11+ variações)**: `ACORDO`, `ACORDO DE COOPERAÇÃO`, `CONVÊNIO`.

### 3.8 Grupo 8: Instrumentos de Publicidade, Extratos e Avisos (Rank: 10)
* **Extratos e Subtipos (38.835+ variações)**: `EXTRATO`, `EXTRATO DE TERMO ADITIVO`, `EXTRATO DE CONTRATO`, `EXTRATO DE APOSTILAMENTO`, `EXTRATOS`, `EXTRATO DO CONTRATO`, `EXTRATO DE CREDENCIAMENTO`, `EXTRATO DE DOAÇÃO`, `EXTRATO DE RESCISÃO DO CONTRATO`, `EXTRATO DE REGISTRO DE PREÇOS`, `EXTRATO DE CONVÊNIO`, `EXTRATO DE INEXIGIBILIDADE DE LICITAÇÃO`, `EXTRATO DE DISPENSA DE LICITAÇÃO`, `EXTRATO DE ACORDO DE COOPERAÇÃO TÉCNICA`.
* **Avisos de Licitação e Subtipos (27.241+ variações)**: `AVISO`, `AVISOS`, `AVISO DE LICITAÇÃO PREGÃO ELETRÔNICO`, `AVISO DE LICITAÇÃO`, `AVISO DE CREDENCIAMENTO`, `AVISO DE CHAMAMENTO PÚBLICO`, `AVISO DE DISPENSA DE LICITAÇÃO`, `AVISO DE HOMOLOGAÇÃO PREGÃO ELETRÔNICO`, `AVISO DE CONSULTA PÚBLICA`.
* **Resultados e Julgamentos (1.233+ variações)**: `RESULTADO`, `RESULTADOS`, `RESULTADO DE JULGAMENTO PREGÃO ELETRÔNICO`, `RESULTADO DE HABILITAÇÃO CONCORRÊNCIA`.
* **Retificações e Rerratificações (2.463+ variações)**: `RETIFICAÇÃO`, `RETIFICAÇÕES`, `RETIFICACÃO`, `RETIFICAÇÃO CONTRATO`, `RETIFICAÇÃO DE TERMO ADITIVO`.
* **Comunicados, Notas, Pautas e Súmulas (822+ variações)**: `PAUTA`, `COMUNICADO`, `SÚMULA`, `SÚMULA DO PARECER CNE/CES`, `COMUNICADO RELEVANTE`, `CONSULTA PÚBLICA`, `ENUNCIADO DA CONSULTORIA-GERAL DA UNIÃO`, `RECOMENDAÇÃO`, `RELATÓRIO`, `MOÇÃO`.

---

## 4. Ingestion ACL Precedence Matcher Specification

The `GazetteMapper` implements a deterministic top-down prefix matcher evaluated in exact descending order of structural specificity:

```python
HIERARCHY_MATCHING_TABLE: list[
    tuple[str, HierarchicalGroup, HierarchicalRank, PublicationNature]
] = [
    # 1. SPECIFIC COMPOSITE PREFIXES (MUST PRECEDE GENERIC TERMS)
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
    # 2. EXTRATOS, AVISOS E PUBLICIDADE (MUST PRECEDE 'CONTRATO'/'CONVÊNIO')
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
    # 3. GENERIC TERMS
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
        "ATA",
        HierarchicalGroup.GRUPO_6_EDITALICIO,
        HierarchicalRank.PUBLICIDADE_OPERACIONAL,
        PublicationNature.PUBLICIDADE_OPERACIONAL,
    ),
]
```

---

## 5. LINDB & Kelsenian Validation Specification

```python
def validate_kelsen_mutation_precedence(
    author_rank: int, target_rank: int, author_title: str, target_title: str
) -> None:
    """Enforces the 'Lex Superior Derogat Inferiori' constitutional invariant.

    Raises:
        LexSuperiorViolationError: If an inferior rank act attempts to mutate a
        superior rank act.
    """
    if author_rank < target_rank:
        raise LexSuperiorViolationError(
            f"Constitutional Violation (LINDB / Kelsen): Act '{author_title}' (Rank {author_rank}) "
            f"cannot alter or revoke superior statute '{target_title}' (Rank {target_rank})."
        )
```

---

## 6. Acceptance Criteria (BDD Scenarios)

### Scenario 1: Precedence of Composite Typology over Generic Term
- **Given** an incoming raw act with `act_type = "LEI COMPLEMENTAR"` and title `"Lei Complementar nº 195"`.
- **When** the `GazetteMapper` executes `resolve_hierarchy()`.
- **Then** `hierarchical_group` is resolved to `1` (GRUPO_1_PRIMARIO).
- **And** `hierarchical_rank` is resolved to `80` (LEI_COMPLEMENTAR), not generic `70`.

### Scenario 2: Extrato de Contrato Precedence over Contrato
- **Given** an incoming raw act with `act_type = "EXTRATO DE CONTRATO Nº 10/2024"`.
- **When** the `GazetteMapper` executes `resolve_hierarchy()`.
- **Then** `hierarchical_group` is resolved to `8` (GRUPO_8_PUBLICIDADE_EXTRATOS).
- **And** `publication_nature` is `publicidade_operacional` (Trilha B), not `7` (CONTRATO).

### Scenario 3: Section Disambiguation for Portarias
- **Given** a `PORTARIA` published in `secao_1`.
- **When** resolved by the mapper.
- **Then** `publication_nature` is set to `normativa_abstrata` (Trilha A).
- **Given** a `PORTARIA` published in `secao_2`.
- **When** resolved by the mapper.
- **Then** `publication_nature` is set to `concreta_individual` (Trilha B).

### Scenario 4: Lex Superior Derogat Inferiori Invariant Rejection
- **Given** a `Portaria Normativa` (Rank 40) containing a parsed regex claiming to revoke `art_10` of a `Lei Ordinária` (Rank 70).
- **When** the validator evaluates `validate_kelsen_mutation_precedence(40, 70)`.
- **Then** a `LexSuperiorViolationError` is raised.
- **And** the mutation is blocked from updating `compiled_normative_acts` and routed to the anomaly audit log.

---

## 7. Test Strategy & Quality Gates

| Level | Scope | Tool | Target |
|---|---|---|---|
| **Unit (Hierarchy Resolution)** | All 8 groups, prefix table, section overrides | `pytest` + `polyfactory` | 100% table coverage across 50+ real DOU strings. |
| **Unit (LINDB Invariants)** | `LexSuperiorViolationError` boundary conditions | `pytest` | Validated for all combinations of rank pairs. |
| **Integration (Persistence)** | PostgreSQL 16 `hierarchical_group` and index queries | `pytest` + PostgreSQL test DB | Verifies index scans on `(hierarchical_group, date)`. |
| **Mutation Testing** | `src/lex/shared_kernel/` and `src/lex/ingestion/adapters/` | `mutmut` | **0 surviving functional mutants**. |
