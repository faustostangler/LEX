# SPEC-001: Gazette Ingestion Engine & Hexagonal Persistence Specification

**Linked ADR:** [ADR-001](../adr/ADR-001-gazette-ingestion-and-digestion-architecture.md)  
**Status:** APPROVED  
**Date:** 2026-08-28  
**Bounded Context:** Ingestion  

---

## 1. Overview & Objectives

This specification defines the precision acceptance criteria, domain invariants, exception mapping, and test boundaries for the **LEX Ingestion Engine**. It operationalizes the decisions made in [ADR-001](../adr/ADR-001-gazette-ingestion-and-digestion-architecture.md) into concrete, testable contracts for TDD implementation.

---

## 2. Bounded Context & Domain Invariants

### 2.1 Value Objects

* **`TerritoryId`**:
  * **Rule:** Must be either `"BR"` (Federal), a valid 2-letter Brazilian State Code (`"SP"`, `"RJ"`, `"MG"`, etc.), or a 7-digit numeric IBGE municipality code (`"3550308"`).
  * **Invariant:** Reject empty strings, lowercase strings, whitespace, non-numeric strings of length $\neq 2$, and numbers of length $\neq 7$.
  * **Exception:** `InvalidTerritoryCodeError`

* **`GazetteDate`**:
  * **Rule:** Must be a valid `datetime.date` between `1808-09-10` (first Brazilian official press publication) and the current UTC date.
  * **Invariant:** Future dates ($> \text{today}$) or dates $< 1808-09-10$ are rejected at construction.
  * **Exception:** `InvalidGazetteDateError`

* **`DocumentHash`**:
  * **Rule:** A strict 64-character lowercase hexadecimal string representing the SHA-256 digest of the extracted text content.
  * **Invariant:** Must match `^[a-f0-9]{64}$`. Reject uppercase, non-hex, or length $\neq 64$.
  * **Exception:** `InvalidDocumentHashError`

* **`FederativeTier`**:
  * **Rule:** Strict `StrEnum` with members `FEDERAL = "federal"`, `STATE = "state"`, `MUNICIPAL = "municipal"`.

### 2.2 Domain Entities

* **`GazetteEdition`** (Aggregate Root):
  * **Invariants enforced at construction (`__init__` / `@model_validator`):**
    1. `char_count` must equal `len(full_text.strip())` and be $> 0$.
    2. `source_url` must be a valid HTTP/HTTPS URL.
    3. `territory_id`, `tier`, `date`, and `file_hash` must be non-null valid Value Objects.
    4. If `tier == FederativeTier.FEDERAL`, `territory_id.code` must equal `"BR"`.
    5. If `tier == FederativeTier.STATE`, `len(territory_id.code)` must equal $2$.
    6. If `tier == FederativeTier.MUNICIPAL`, `len(territory_id.code)` must equal $7$.
  * **Exception:** `DomainInvariantViolationError`

---

## 3. Test Strategy Classification

| Level | Target Scope | Mock Boundary | Tool |
|-------|--------------|---------------|------|
| **Unit (Domain & Ports)** | `domain/value_objects.py`, `domain/entities.py`, `application/use_cases.py` | 100% pure memory. Zero I/O, zero network, zero PostgreSQL. | `pytest` + `polyfactory` |
| **Unit (ACL Mapper & Extractor)** | `infrastructure/adapters/gazette_mapper.py`, `infrastructure/adapters/stream_extractor.py` | Feed synthetic `io.BytesIO` PDF streams and verify text extraction without disk I/O. | `pytest` |
| **Integration (PostgreSQL Repository)** | `infrastructure/persistence/postgres_repository.py` | Real PostgreSQL 16 test database (via test container / local compose DB). Verify `ON CONFLICT` updates and LZ4 TOAST compression. | `pytest` |
| **Integration (Scrapy Middlewares)** | `infrastructure/scrapy_project/middlewares.py` | Simulated HTTP 429/503/504 responses to test `DomainCircuitBreaker` and exponential backoff retry. | `pytest` |
| **Mutation Testing** | `src/lex/ingestion/domain/` | 0 surviving mutants target. | `mutmut` |

---

## 4. Acceptance Criteria (BDD Scenarios)

### Scenario 1: Successful In-Memory Gazette Stream Ingestion
- **Given** a valid PDF byte stream from the Federal DOU (e.g. Seção 1) with publication date `2024-01-02`.
- **When** the `EphemeralStreamTextExtractor` processes the stream in memory.
- **Then** plain text is extracted without writing any `.pdf` or binary file to disk.
- **And** the `GazetteMapper` constructs a valid `GazetteEdition` domain entity with computed SHA-256 hash.
- **And** the entity is persisted to `gazette_editions` table in PostgreSQL.

### Scenario 2: Idempotent Deduplication on Re-Scrape
- **Given** an existing `GazetteEdition` in the database for `(territory_id='SP', date='2024-05-10', section='1')`.
- **When** the SP DOE spider runs again for the same date and encounters the same gazette.
- **Then** the repository executes `INSERT ... ON CONFLICT DO UPDATE`.
- **And** the `scraped_at` timestamp is updated to the latest run timestamp.
- **And** the total row count in `gazette_editions` does not increase.

### Scenario 3: Domain Circuit Breaker Trips on Consecutive Portal Failures
- **Given** a State DOE portal (e.g., `diario.ac.gov.br`) returning consecutive `HTTP 500` errors.
- **When** 5 consecutive requests fail across all retries for `diario.ac.gov.br`.
- **Then** the `DomainCircuitBreaker` transitions from `CLOSED` to `OPEN` for that domain.
- **And** subsequent requests to `diario.ac.gov.br` are immediately dropped for 60 seconds without network calls.
- **And** requests to other state domains (e.g., `doe.sp.gov.br`) continue executing normally.

### Scenario 4: Fail-Fast Centralized Configuration
- **Given** an environment missing the mandatory `LEX_DATABASE_URL` variable.
- **When** the application starts and initializes `LexSettings()`.
- **Then** a `ValidationError` is raised immediately, halting process execution before connecting to any network resource.

---

## 5. Boundary Conditions & Exception Mapping

| Input / Condition | Boundary Value | Expected Domain Exception |
|-------------------|----------------|---------------------------|
| `TerritoryId.from_code(code)` | `""` or `"São Paulo"` or `"123"` | `InvalidTerritoryCodeError` |
| `GazetteDate.from_date(d)` | `date(2099, 1, 1)` (Future) | `InvalidGazetteDateError` |
| `GazetteDate.from_date(d)` | `date(1700, 1, 1)` (Pre-1808) | `InvalidGazetteDateError` |
| `DocumentHash.from_hex(h)` | `"ABCDEF..."` (Uppercase / Non-hex) | `InvalidDocumentHashError` |
| `GazetteEdition(...)` | `full_text=""` (Empty text) | `DomainInvariantViolationError` |
| `EphemeralStreamTextExtractor` | Corrupted non-PDF binary payload | `CorruptedGazettePayloadError` |

---

## 6. Observability & Telemetry Assertions

* **Prometheus Metrics**:
  * On every successful gazette ingestion: `lex_gazettes_ingested_total{tier, territory_id, spider}` is incremented by 1.
  * When a circuit breaker opens: `lex_circuit_breaker_events_total{domain, state="OPEN"}` is incremented by 1.
* **Structured Logs**:
  * All log events output JSON with `trace_id`, `session_id`, `territory_id`, and `spider_name`.
  * Regex filters must mask any CPF pattern (`***.***.***-**`) before `stdout` export.
