# SPEC-002: Legislative Delta Extraction, Mutation Ledger, and AST Compilation Specification

**Linked ADR:** [ADR-006](../adr/ADR-006-legislative-delta-mutation-ledger-and-compiled-ast-consolidation-engine.md)  
**Status:** APPROVED  
**Date:** 2026-08-29  
**Bounded Context:** `treatment` & `consolidation`  

---

## 1. Overview & Objectives

This specification establishes the precision contracts, domain invariants, parsing grammars, deterministic state machine transitions, and test boundaries for the **LEX Legislative Consolidation Engine**. It operationalizes the decisions codified in [ADR-006](../adr/ADR-006-legislative-delta-mutation-ledger-and-compiled-ast-consolidation-engine.md) into concrete, testable specifications for TDD implementation.

---

## 2. Bounded Context & Domain Invariants

### 2.1 Value Objects & Type Definitions

* **`CanonicalNodePath`**:
  * **Rule:** A dot-separated hierarchical string identifier adhering strictly to Brazilian legislative structure:
    `^(art_[0-9]+[a-z]?)(?:\.(par_[0-9]+[a-z]?|par_unico))?(?:\.(inc_[0-9]+[a-z]?))?(?:\.(ali_[a-z]+))?(?:\.(item_[0-9]+))?$`
  * **Valid Examples:** `art_3`, `art_15_a`, `art_3.par_2`, `art_3.par_unico`, `art_3.par_1.inc_14`, `art_3.inc_2.ali_a.item_1`.
  * **Invariants:**
    1. Must be lowercase.
    2. Must begin with an article prefix (`art_`).
    3. Hierarchy levels cannot be skipped (e.g., `art_3.ali_a` without an intervening `inc_` is rejected unless specified in an atypical historical decree).
  * **Exception:** `InvalidCanonicalNodePathError`

* **`MutationType`**:
  * **Rule:** Strict `StrEnum` covering all normative amendment modalities:
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
  * **Rule:** Strict `StrEnum` indicating the operational legal state of a provision node:
    ```python
    class DispositivoStatus(StrEnum):
        ORIGINAL_ACTIVE = "original_active"  # Unaltered since base publication
        MODIFIED_ACTIVE = "modified_active"  # Text altered by a subsequent act
        REVOKED = "revoked"  # Revoked / lost efficacy (rendered with <strike>)
        SUSPENDED = "suspended"  # Efficacy suspended (e.g. STF ADI / Senate Res)
    ```

---

### 2.2 Domain Entities & Aggregate Roots

#### `NormativeActMutation` (Write Model Entity)
* **Fields:**
  * `id`: `UUID`
  * `target_act_id`: `UUID` (Target Statute ID)
  * `target_node_path`: `CanonicalNodePath` (Target provision, e.g. `art_3.inc_1`)
  * `author_act_id`: `UUID` (Amending Statute ID)
  * `author_dispositivo_ref`: `str` (e.g., `"Art. 189, inciso I"`)
  * `mutation_type`: `MutationType`
  * `new_text`: `str | None`
  * `new_structured_payload`: `dict[str, Any] | None`
  * `publication_date`: `GazetteDate`
  * `effective_date`: `GazetteDate`
  * `mutation_sha256`: `DocumentHash`
* **Invariants:**
  1. If `mutation_type in (ACRESCIMO, ALTERACAO_NR, RETIFICACAO)`, `new_text` must be a non-empty string.
  2. If `mutation_type in (REVOGACAO_EXPRESSA, REVOGACAO_TACITA, SUSPENSAO_EFICACIA)`, `new_text` is allowed to be `None`.
  3. `effective_date` must not precede `publication_date` by more than zero days unless an explicit retroactivity clause is validated.

#### `CompiledNormativeAct` (Read Model Aggregate Root)
* **Fields:**
  * `act_id`: `UUID` (Primary Key)
  * `compiled_version_hash`: `DocumentHash`
  * `total_mutations_applied`: `int`
  * `last_mutation_effective_date`: `date | None`
  * `compiled_ast`: `dict[str, Any]` (Serialized `NormativeActAST`)
  * `compiled_html`: `str` (LZ4 TOAST compressed HTML document)
  * `compiled_markdown`: `str` (LZ4 TOAST compressed Markdown document)
  * `active_articles_count`: `int`
  * `revoked_articles_count`: `int`
  * `last_compiled_at`: `datetime`

---

## 3. Parsing Specification (LC 95/1998 Regex AST Grammar)

The deterministic mutation extractor detects amendment directives in legislative texts using canonical syntactic patterns:

### 3.1 Amending Article Header Regexes
```python
# Matches: "Art. 1º A Lei nº 14.133, de 1º de abril de 2021, passa a vigorar com as seguintes alterações:"
RE_ALTERATION_HEADER = re.compile(
    r"[Aa]rt\.\s*\d+[ºo]?\s+(?:O|A|Os|As)?\s*(Lei|Decreto|Medida\s+Provisória|Portaria|Resolução)"
    r"(?:\s+Complementar)?\s+(?:n[ºo°\.]?\s*)?([\d\.]+)(?:,\s+de\s+[\w\s]+de\s+\d{4})?"
    r",?\s+passa[m]?\s+a\s+vigorar\s+com\s+a[s]?\s+seguinte[s]?\s+alteraç[ãõ]e[s]?:?",
    re.IGNORECASE,
)
```

### 3.2 Provision Identification & `(NR)` Marker Regexes
```python
# Identifies provision label: "Art. 3º", "§ 1º", "Parágrafo único.", "XIV -", "a)", "1."
RE_PROVISION_LABEL = re.compile(
    r"^(?:(Art\.\s*\d+[ºo\-]?[A-Za-z]?)|(§\s*\d+[ºo]?|Parágrafo\s+único)|([IVXLCDM]+\s*[-–])|([a-z]\s*[\)\-])|(\d+\s*[\.\-]))\s*(.*)$",
    re.MULTILINE,
)

# Identifies (NR) marker at the end of altered provisions
RE_NR_MARKER = re.compile(r"\s*\((?:NR|nr)\)\s*$", re.MULTILINE)
```

### 3.3 Express Revocation Regexes
```python
# Matches: "Revogam-se os incisos I e II do caput do art. 3º da Lei nº 10.000..."
RE_EXPRESS_REVOCATION = re.compile(
    r"[Rr]evoga[m]?\s*-\s*se\s+(?:expressamente\s+)?"
    r"(?:o|a|os|as|o[s]?\s+seguinte[s]?\s+dispositivo[s]?:\s*)?"
    r"((?:(?:art|artigo|parágrafo|inciso|alínea|item|§|caput|[0-9IVXLCDMa-zº\s,\.e–\-])+))"
    r"(?:,\s*(?:d[ao]|d[ae]|do\s+artigo|da\s+Lei)\s+([^\.]+))?\.",
    re.IGNORECASE,
)
```

---

## 4. Pure Functional Reducer Specification

$$\operatorname{reduce}(\text{BaseAST}, [\text{Mutation}_1, \dots, \text{Mutation}_k]) \longrightarrow \text{CompiledAST}$$

```
                MUTATION STATE MACHINE TRANSITION RULES
 ┌──────────────────┐               ALTERACAO_NR              ┌──────────────────┐
 │ ORIGINAL_ACTIVE  │ ──────────────────────────────────────> │ MODIFIED_ACTIVE  │
 └──────────────────┘                                         └──────────────────┘
          │                                                            │
          │ REVOGACAO_EXPRESSA                                         │ REVOGACAO_EXPRESSA
          ▼                                                            ▼
 ┌──────────────────┐               ALTERACAO_NR              ┌──────────────────┐
 │     REVOKED      │ <────────────────────────────────────── │     REVOKED      │
 └──────────────────┘                                         └──────────────────┘
```

### Reducer Algorithmic Steps

1. **Sort Mutations Chronologically**:
   Sort input mutation list by `(effective_date ASC, publication_date ASC, created_at ASC)`.
2. **Sequential Application**:
   For each `mutation` in the sorted stream:
   - **Case `ALTERACAO_NR`**:
     1. Locate target node by `target_node_path`.
     2. Push existing `current_text`, `status`, and `effective_date` into `target_node.history`.
     3. Update `target_node.current_text = mutation.new_text`.
     4. Set `target_node.status = DispositivoStatus.MODIFIED_ACTIVE`.
   - **Case `REVOGACAO_EXPRESSA`**:
     1. Locate target node by `target_node_path`.
     2. Push metadata note to `target_node.history`.
     3. Set `target_node.status = DispositivoStatus.REVOKED`.
     4. **Subtree Cascade Invariant**: Recursively set all child nodes (parágrafos, incisos, alíneas) of the target node to `DispositivoStatus.REVOKED`.
   - **Case `ACRESCIMO`**:
     1. Parse parent path and target index (e.g. `art_3.inc_14` $\to$ parent: `art_3`, index: `inc_14`).
     2. Locate parent node.
     3. Construct new `DispositivoNode` with `status = DispositivoStatus.MODIFIED_ACTIVE`.
     4. Insert child node into parent's `children` array adhering to natural statutory sequence (Roman numerals for incisos, alphabetical for alíneas).
3. **Compile Projections**:
   - Walk the final `CompiledAST` to generate hyperlinked, semantic HTML and Markdown with `<strike>` tags and annotation badges.
   - Compute deterministic SHA-256 hash over the compiled AST JSON structure (`compiled_version_hash`).

---

## 5. Acceptance Criteria (BDD Scenarios)

### Scenario 1: `ALTERACAO_NR` with Historical Preservation & Formatting
- **Given** an active statute with `art_3.inc_1` text: `"I - proposta mais vantajosa;"`.
- **When** an amending act applies `ALTERACAO_NR` with text: `"I - proposta mais vantajosa e sustentável; (NR)"` from `Lei nº 14.000/2020`.
- **Then** `art_3.inc_1.status` transitions to `MODIFIED_ACTIVE`.
- **And** `art_3.inc_1.history` contains the previous text `"I - proposta mais vantajosa;"`.
- **And** the compiled HTML renders:
  ```html
  <strike>I - proposta mais vantajosa;</strike>
  <span class="vigente">I - proposta mais vantajosa e sustentável;</span>
  <small class="nota-alteracao">(Redação dada pela <a href="/legislation/lei-14000-2020">Lei nº 14.000, de 2020</a>)</small>
  ```

### Scenario 2: `ACRESCIMO` Injects Leaf Node in Proper Order
- **Given** `art_3` containing incisos `inc_1` (`I - ...`) and `inc_2` (`II - ...`).
- **When** an amending act injects `inc_3` (`III - promoção da integridade pública;`).
- **Then** `art_3.children` length increases from 2 to 3.
- **And** `art_3.children[2].node_path` equals `"art_3.inc_3"`.
- **And** the node is marked with `(Incluído pela Lei nº ...)`.

### Scenario 3: `REVOGACAO_EXPRESSA` Cascades to Child Subtrees
- **Given** `art_5` containing `par_1` with two child incisos `inc_1` and `inc_2`.
- **When** a revocation directive revokes `art_5.par_1`.
- **Then** `art_5.par_1.status` becomes `REVOKED`.
- **And** `art_5.par_1.inc_1.status` and `art_5.par_1.inc_2.status` both cascade to `REVOKED`.
- **And** the entire paragraph and its incisos are enclosed within `<strike>` tags in `compiled_html`.

### Scenario 4: Bi-Temporal Time-Travel Reconstructs Historical Point-in-Time State
- **Given** a statute enacted on `2010-01-01` amended on `2015-06-01` and again on `2022-01-01`.
- **When** a client queries `GET /legislation/:id?as_of=2018-12-31`.
- **Then** the reducer applies only mutations where `effective_date <= '2018-12-31'`.
- **And** mutations from `2022-01-01` are completely excluded from the resulting AST and HTML.

### Scenario 5: Idempotent Replay on Zero-Scrape Re-Execution
- **Given** a complete set of `normative_act_mutations` for a statute.
- **When** the compiler runs repeatedly without new mutations.
- **Then** `compiled_version_hash` remains identical.
- **And** zero database write operations occur if the hash has not changed.

---

## 6. Test Strategy & Quality Gates

| Test Level | Scope | Tools | Success Criteria |
|---|---|---|---|
| **Unit (Domain Core)** | `CanonicalNodePath`, `DispositivoNode`, `NormativeActAST` validation | `pytest` + `polyfactory` | 100% branch coverage; pure memory. |
| **Unit (AST Reducer)** | State machine transitions, ordering, and cascade revocations | `pytest` | Validated against complex multi-amendment synthetic suites. |
| **Integration (Persistence)** | `PostgresMutationRepository` and `CompiledActRepository` | `pytest` + PostgreSQL 16 test container | Verifies GIN indexes, LZ4 TOAST compression, and cascade deletes. |
| **Mutation Testing** | `src/lex/consolidation/` | `mutmut` | **0 surviving functional mutants**. |
| **Property-Based Testing** | Node insertion ordering and chronological stability | `hypothesis` | Invariant: $\forall \text{ permutation of mutations}, \text{reduce}(\text{sort}(M)) \equiv \text{deterministic AST}$. |

---

## 7. Telemetry, Observability & Performance SLOs

1. **Prometheus Domain Metrics**:
   - `lex_mutations_extracted_total{mutation_type, source}`
   - `lex_consolidation_duration_seconds{act_type}` (Histogram)
   - `lex_time_travel_replay_duration_seconds` (Histogram)
2. **Performance Service Level Objectives (SLOs)**:
   - **$O(1)$ Current Version Read (`GET /legislation/:id`)**: $P_{99} < 5\text{ms}$.
   - **$O(k)$ Time-Travel Point-in-Time Replay (`GET /legislation/:id?as_of=...`)**: $P_{99} < 20\text{ms}$ for statutes with up to 100 historical mutations.
