# ADR-010: Out-of-Order Stub Entity Auto-Materialization and Mutation Foreign Key Resilience

- **Status**: Accepted
- **Date**: 2026-08-31
- **Deciders**: Principal Socio-Technical Architect, High-Performance Implementer
- **Consulted**: Database Administrator, Domain Modeler
- **Informed**: Engineering Team
- **Bounded Context**: `treatment` & `consolidation`

---

## 1. Context and Problem Statement

In Brazilian legislative drafting (governed by **Lei Complementar nº 95/1998**), amending statutes (e.g. *Lei nº 14.133/2021*) amend base codes and laws enacted decades earlier (e.g. *Lei nº 8.666/1993*, *Código Penal / Decreto-Lei nº 2.848/1940*). Because daily gazette ingestion is non-linear and asynchronous, modern amending statutes are frequently ingested and treated **before** their historical base statutes exist in the database.

During vulnerability audit (CRIT-02), a critical foreign key violation was identified:
1. `MutationExtractor` generated a synthetic fallback UUID (`uuid.uuid5(uuid.NAMESPACE_DNS, f"{territory}:target_placeholder")`) whenever `target_act_id` was not explicitly pre-provided.
2. In PostgreSQL, `normative_act_mutations.target_act_id` defines a non-nullable foreign key referencing `normative_acts.id` (`ForeignKey("normative_acts.id", ondelete="CASCADE")`).
3. When `PostgresTreatmentRepository.save_mutations()` attempted to insert mutation rows targeting non-existent base laws, PostgreSQL immediately raised `ForeignKeyViolationError` on commit, causing transaction rollback, failure of `lex treat`, and total loss of extracted mutation deltas.

---

## 2. Decision Drivers

- **Absolute Relational Integrity**: Maintain strict database foreign keys on `normative_act_mutations.target_act_id` without resorting to loose untyped strings or disabling database constraints.
- **Zero-Failure Out-of-Order Ingestion**: Amending statutes must be treated and persisted cleanly at any time, regardless of whether the target base statute has already been scraped.
- **Deterministic Addressing (LexML Standard)**: Target base statutes must be addressed via deterministic LexML Canonical URNs, ensuring that multiple mutations targeting the same base law attach to the identical Stub UUID.
- **JIT Discovery Queue Synchronization**: Every encounter with an un-ingested base statute must automatically register or increment citation counts in `legislation_backfill_queue` to drive historical backfill crawlers.
- **Atomic Persistence**: Auto-materialization of stub editions, stub normative acts, backfill tasks, and mutation deltas must execute within a single atomic database transaction.

---

## 3. Considered Options

- **Option 1: Allow Nullable `target_act_id` with Text URN column**: Relax the database foreign key constraint and store target URNs as raw text strings. *(Rejected: Destroys relational integrity, breaks cascading operations, and complicates CQRS AST compilation).*
- **Option 2: Discard Mutations for Missing Base Acts**: Skip mutation persistence if the target act is not found. *(Rejected: Fatal data loss; un-ingested base statutes would never accumulate historical mutations).*
- **Option 3: Deterministic Stub Auto-Materialization at Persistence Boundary (SOTA-KISS)**: Extract target statute natural metadata in `MutationExtractor`, mint deterministic UUIDv5 from LexML URN, and atomically create placeholder Stub entities (`is_stub = TRUE`) in `normative_acts` and `legislation_backfill_queue` prior to inserting mutation deltas. *(Accepted).*

---

## 4. Decision Outcome

We implement **Deterministic Stub Auto-Materialization at Persistence Boundary (Option 3)**:

```mermaid
flowchart TD
    A["Amending Act Text (e.g. Lei 14.133/2021)"] -->|Parse LC 95 Header| B["MutationExtractor"]
    B -->|Extracts Target Natural Key| C["Target: Lei 8.666/1993"]
    C -->|Generate Canonical URN| D["urn:lex:br:federal:lei:1993;8666"]
    D -->|UUIDv5(DNS, URN)| E["Deterministic Stub UUID"]
    E -->|NormativeActMutation| F["PostgresTreatmentRepository.save_mutations()"]
    
    subgraph "Atomic Database Transaction"
        F --> G{"Target Act exists<br/>in normative_acts?"}
        G -->|No| H["1. Ensure Stub Edition Container<br/>2. Insert Stub NormativeAct (is_stub=True)<br/>3. Upsert legislation_backfill_queue"]
        G -->|Yes| I["Skip Stub Creation"]
        H --> J["Insert NormativeActMutationModel (FK valid!)"]
        I --> J
        J --> K["Commit Transaction"]
    end
```

### 4.1 Target Statute URN Resolution in `MutationExtractor`
`MutationExtractor` parses target typology, number, and year from alteration headers (`RE_ALTERATION_HEADER`) and revocation clauses:
- `target_urn = generate_canonical_urn(territory_code, act_type, act_number, act_year, tier="federal")`
- `target_act_id = uuid.uuid5(uuid.NAMESPACE_DNS, target_urn)`
- `NormativeActMutation` carries `target_act_id`, `target_canonical_urn`, and natural metadata.

### 4.2 Atomic Stub Materialization in `PostgresTreatmentRepository`
Inside `save_mutations(mutations)`:
1. Identify all distinct `target_act_id` values in the batch.
2. Query existing IDs in `normative_acts`.
3. For any missing ID, instantiate and persist:
   - A stub `GazetteEditionModel` (if not already present for that territory and year).
   - A stub `NormativeActModel` with `id=target_act_id`, `canonical_urn=target_urn`, `title=f"{act_type} nº {act_number}/{act_year}"`, `is_stub=True`, `raw_content=""`, `char_count=0`.
   - A `LegislationBackfillQueueModel` task (or increment `citation_count` via `on_conflict_do_update`).
4. Persist all `NormativeActMutationModel` instances. All foreign keys are guaranteed valid.

---

## 5. Consequences

### Positive
- **Zero Foreign Key Violations**: Eliminates transaction rollbacks during `lex treat` when processing amending legislation.
- **Preserved CQRS Write Model**: All statutory amendments are safely recorded and ready for compilation as soon as the base statute is hydrated.
- **Automated Discovery**: Popular base laws (e.g. *Lei 8.666*, *CLT*, *Código Civil*) are automatically prioritized in the backfill queue with accurate citation metrics.
- **Idempotent Hydration**: When the authentic historical base statute is ingested later, an upsert on `canonical_urn` updates `is_stub = False` and sets `raw_content` without changing `id` or breaking existing mutation links.

### Negative / Operational Constraints
- Stub entities occupy lightweight rows in `normative_acts` with `is_stub = TRUE` until hydrated by historical crawlers.
- API read models for stub entities must return status `PENDING_BASE_INGESTION`.

---

## 6. Compliance & Hexagonal Verification

- [x] Hexagonal Architecture layers respected (Domain defines Value Objects; Persistence Adapter manages relational stubs).
- [x] No framework dependencies in Domain layer.
- [x] Entities enforce invariants at construction time.
- [x] Full transaction atomicity and rollback safety guaranteed.
