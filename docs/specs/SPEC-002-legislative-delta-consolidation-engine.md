# SPEC-002: Legislative Delta Extraction, Out-of-Order Ingestion, Mutation Ledger, and AST Compilation Specification

**Linked ADR:** [ADR-006](../adr/ADR-006-legislative-delta-mutation-ledger-and-compiled-ast-consolidation-engine.md)  
**Status:** APPROVED  
**Date:** 2026-08-29  
**Bounded Context:** `treatment` & `consolidation`  

---

## 1. Overview & Objectives

This specification establishes the precision contracts, domain invariants, parsing grammars, out-of-order ingestion state machine transitions, event-driven catch-up mechanics, and test boundaries for the **LEX Legislative Consolidation Engine**. It operationalizes the architectural decisions codified in [ADR-006](../adr/ADR-006-legislative-delta-mutation-ledger-and-compiled-ast-consolidation-engine.md).

---

## 2. Bounded Context & Domain Invariants

### 2.1 Value Objects & Type Definitions

* **`CanonicalUrn`**:
  * **Rule:** A strict LexML/FRBR-compliant uniform resource name:
    `^urn:lex:br:(federal|[a-z]{2}):(lei|lei\.complementar|decreto|decreto\.lei|medida\.provisoria|portaria|resolucao):([0-9]{4}(?:-[0-9]{2}-[0-9]{2})?);([0-9a-z\.\-]+)$`
  * **Examples:** `urn:lex:br:federal:lei:1993-06-21;8666`, `urn:lex:br:federal:decreto.lei:1940;2848`, `urn:lex:br:sp:lei:2015;15854`.
  * **Exception:** `InvalidCanonicalUrnError`

* **`CanonicalNodePath`**:
  * **Rule:** Dot-separated hierarchical provision address:
    `^(art_[0-9]+[a-z]?)(?:\.(par_[0-9]+[a-z]?|par_unico))?(?:\.(inc_[0-9]+[a-z]?))?(?:\.(ali_[a-z]+))?(?:\.(item_[0-9]+))?$`
  * **Examples:** `art_3`, `art_15_a`, `art_3.par_2`, `art_3.par_unico`, `art_3.par_1.inc_14`, `art_3.inc_2.ali_a.item_1`.
  * **Exception:** `InvalidCanonicalNodePathError`

* **`MutationType`**:
  * **Rule:** Strict `StrEnum` covering all amendment modalities:
    ```python
    class MutationType(StrEnum):
        ACRESCIMO = "ACRESCIMO"
        ALTERACAO_NR = "ALTERACAO_NR"
        REVOGACAO_EXPRESSA = "REVOGACAO_EXPRESSA"
        REVOGACAO_TACITA = "REVOGACAO_TACITA"
        SUSPENSAO_EFICACIA = "SUSPENSAO_EFICACIA"
        RENUMERACAO = "RENUMERACAO"
        RETIFICACAO = "RETIFICACAO"
    ```

* **`DispositivoStatus`**:
  * **Rule:** Strict `StrEnum` indicating operational legal state:
    ```python
    class DispositivoStatus(StrEnum):
        ORIGINAL_ACTIVE = "original_active"  # Unaltered since base enactment
        MODIFIED_ACTIVE = "modified_active"  # Altered by subsequent act
        REVOKED = "revoked"  # Revoked (rendered with <strike>)
        SUSPENDED = "suspended"  # Efficacy suspended (e.g. STF ADI)
    ```

---

### 2.2 Domain Entities, Aggregate Roots & Domain Events

#### `NormativeAct` (Aggregate Root Enhancements)
* **New Fields:**
  * `canonical_urn`: `CanonicalUrn`
  * `is_stub`: `bool` (Default: `False`. Set to `True` when created as a placeholder for an out-of-order referenced base act).
* **Invariants for Stub Entities:**
  1. If `is_stub == True`, `raw_content` may be `None` and `char_count` may be `0`.
  2. If `is_stub == False`, `raw_content` must be a non-empty string and `char_count == len(raw_content.strip())`.

#### `NormativeActMutation` (Write Model Entity)
* **Fields:**
  * `id`: `UUID`
  * `target_act_id`: `UUID` (Foreign key to target `NormativeAct`, even if it is a Stub)
  * `target_node_path`: `CanonicalNodePath`
  * `author_act_id`: `UUID`
  * `author_dispositivo_ref`: `str`
  * `mutation_type`: `MutationType`
  * `new_text`: `str | None`
  * `new_structured_payload`: `dict[str, Any] | None`
  * `publication_date`: `GazetteDate`
  * `effective_date`: `GazetteDate`
  * `mutation_sha256`: `DocumentHash`

#### `LegislationBackfillTask` (JIT Queue Entity)
* **Fields:**
  * `id`: `UUID`
  * `canonical_urn`: `CanonicalUrn`
  * `territory_id`: `TerritoryId`
  * `act_type`: `ActType`
  * `act_number`: `str`
  * `act_year`: `int`
  * `citation_count`: `int` (Priority weight: increments on each incoming mutation referencing this missing act)
  * `status`: `str` (`"PENDING"`, `"IN_PROGRESS"`, `"RESOLVED"`)

#### Domain Events
* **`NormativeActHydrated`**:
  * **Payload:** `act_id: UUID`, `canonical_urn: CanonicalUrn`, `hydrated_at: datetime`.
  * **Handler:** Automatically invokes `CompiledActReducer.recompile(act_id)` to process all accumulated mutations for this statute.

---

## 3. Parsing Specification (LC 95/1998 Regex AST Grammar)

```python
# 1. Matches: "Art. 1º A Lei nº 14.133, de 1º de abril de 2021, passa a vigorar com as seguintes alterações:"
RE_ALTERATION_HEADER = re.compile(
    r"[Aa]rt\.\s*\d+[ºo]?\s+(?:O|A|Os|As)?\s*(Lei|Decreto|Medida\s+Provisória|Portaria|Resolução)"
    r"(?:\s+Complementar)?\s+(?:n[ºo°\.]?\s*)?([\d\.]+)(?:,\s+de\s+[\w\s]+de\s+\d{4})?"
    r",?\s+passa[m]?\s+a\s+vigorar\s+com\s+a[s]?\s+seguinte[s]?\s+alteraç[ãõ]e[s]?:?",
    re.IGNORECASE,
)

# 2. Identifies provision labels: "Art. 3º", "§ 1º", "Parágrafo único.", "XIV -", "a)", "1."
RE_PROVISION_LABEL = re.compile(
    r"^(?:(Art\.\s*\d+[ºo\-]?[A-Za-z]?)|(§\s*\d+[ºo]?|Parágrafo\s+único)|([IVXLCDM]+\s*[-–])|([a-z]\s*[\)\-])|(\d+\s*[\.\-]))\s*(.*)$",
    re.MULTILINE,
)

# 3. Identifies (NR) marker at the end of altered provisions
RE_NR_MARKER = re.compile(r"\s*\((?:NR|nr)\)\s*$", re.MULTILINE)

# 4. Matches express revocations: "Revogam-se os incisos I e II do caput do art. 3º da Lei nº 10.000..."
RE_EXPRESS_REVOCATION = re.compile(
    r"[Rr]evoga[m]?\s*-\s*se\s+(?:expressamente\s+)?"
    r"(?:o|a|os|as|o[s]?\s+seguinte[s]?\s+dispositivo[s]?:\s*)?"
    r"((?:(?:art|artigo|parágrafo|inciso|alínea|item|§|caput|[0-9IVXLCDMa-zº\s,\.e–\-])+))"
    r"(?:,\s*(?:d[ao]|d[ae]|do\s+artigo|da\s+Lei)\s+([^\.]+))?\.",
    re.IGNORECASE,
)
```

---

## 4. Out-of-Order State Machine & Reducer Specification

$$\operatorname{reduce}(\text{BaseAST}, [\text{Mutation}_1, \dots, \text{Mutation}_k]) \longrightarrow \text{CompiledAST}$$

```
                   OUT-OF-ORDER INGESTION & REDUCTION FLOW
                   
       [ Spider Ingests Amending Act ]
                     │
                     ▼
          [ Extract Mutations ]
                     │
                     ▼
        [ Check Target Statute in DB ]
         /                          \
        ▼ (Target Missing)           ▼ (Target Exists)
  [ Create Stub Entity ]       [ Attach Mutation ]
  [ Enqueue in JIT Backfill ]         │
  [ Attach Mutation to Stub ]          ▼
         │                     [ Run Pure Reducer ]
         │                             │
         ▼ (Time passes)               ▼
  [ Backfill Crawls Base Act ]   [ Update Materialized ]
  [ Hydrate Stub: is_stub=F ]    [   compiled_acts     ]
         │
         ▼ (Emit NormativeActHydrated)
  [ Run Catch-Up Reducer on All Accumulated Mutations ]
```

### Catch-Up Reducer Algorithmic Steps

1. **Chronological Sorting**: Sort mutations by `(effective_date ASC, publication_date ASC, created_at ASC)`.
2. **Apply Delta Stream**:
   - `ALTERACAO_NR`: Push previous text to node history, set `current_text = mutation.new_text`, set `status = MODIFIED_ACTIVE`.
   - `REVOGACAO_EXPRESSA`: Set `status = REVOKED`. **Cascade**: Recursively mark all child nodes in the subtree as `REVOKED`.
   - `ACRESCIMO`: Insert new child node into parent's `children` array in correct statutory ordering.
3. **Compilation**:
   - Pre-render `compiled_html` and `compiled_markdown` with `<strike>` tags and hyperlinks.
   - Calculate deterministic SHA-256 hash `compiled_version_hash`.

---

## 5. Acceptance Criteria (BDD Scenarios)

### Scenario 1: Out-of-Order Mutation Ingestion Creates Stub without FK Failure
- **Given** a new amending act (e.g., *Lei 14.133/2021*) that alters *Lei 8.666/1993*.
- **And** *Lei 8.666/1993* does **not** exist in `normative_acts`.
- **When** the mutation extractor processes the amendment.
- **Then** a Stub record is inserted into `normative_acts` with `is_stub = True`, `act_number = "8666"`, `act_year = 1993`.
- **And** the mutation is successfully saved in `normative_act_mutations` referencing the Stub ID.
- **And** a task is enqueued in `legislation_backfill_queue` with `citation_count = 1`.

### Scenario 2: Repeated Citations Increment JIT Backfill Priority
- **Given** a Stub for *Lei 8.666/1993* already exists in `legislation_backfill_queue` with `citation_count = 1`.
- **When** another amending act also cites and amends *Lei 8.666/1993*.
- **Then** `citation_count` for that task increments to `2`.
- **And** the second mutation is appended to `normative_act_mutations` without error.

### Scenario 3: Hydration of Base Act Triggers Event-Driven Catch-Up Consolidation
- **Given** a Stub *Lei 8.666/1993* with 15 accumulated mutations recorded over time.
- **When** a historical crawler ingests the authentic base text of *Lei 8.666/1993*.
- **Then** the Stub is updated with `is_stub = False` and the genuine `raw_content`.
- **And** the `NormativeActHydrated` domain event is fired.
- **And** the AST Reducer processes all 15 historical mutations in chronological order.
- **And** a valid `CompiledNormativeAct` projection is populated in `compiled_normative_acts`.

### Scenario 4: API Response for Stub Statute
- **Given** a statute that is currently an unhydrated Stub (`is_stub = True`).
- **When** a client sends `GET /legislation/:id`.
- **Then** the API returns HTTP 200 with `status = "PENDING_BASE_INGESTION"`.
- **And** the response body includes the list of known mutations and amending statutes recorded in the ledger.

---

## 6. Test Strategy & Quality Gates

| Level | Scope | Tools | Acceptance Target |
|---|---|---|---|
| **Unit (Domain Core)** | `CanonicalUrn`, `CanonicalNodePath`, `StubEntity` rules | `pytest` + `polyfactory` | 100% branch coverage; pure memory. |
| **Unit (Out-of-Order Reducer)** | Catch-up reduction, mutation ordering, cascade revocations | `pytest` | 0 failures across 50+ out-of-order test scenarios. |
| **Integration (Persistence & Events)** | Stub creation, JIT queue increments, `NormativeActHydrated` handler | `pytest` + PostgreSQL 16 test DB | Verifies cascade FKs, partial indexes, and JSONB queries. |
| **Mutation Testing** | `src/lex/consolidation/` | `mutmut` | **0 surviving functional mutants**. |

---

## 7. Telemetry & Performance SLOs

1. **Prometheus Domain Metrics**:
   - `lex_stub_entities_created_total{act_type}`
   - `lex_backfill_queue_size{status="PENDING"}`
   - `lex_catchup_consolidation_duration_seconds` (Histogram)
2. **Performance SLOs**:
   - **$O(1)$ Current Version Read**: $P_{99} < 5\text{ms}$.
   - **Catch-Up Consolidation (50 Accumulated Mutations)**: $P_{99} < 15\text{ms}$.
