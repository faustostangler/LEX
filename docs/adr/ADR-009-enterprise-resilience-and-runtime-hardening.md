# ADR-009: Enterprise Resilience, Security Hardening & Concurrency Lifecycle Management

- **Status**: Accepted
- **Date**: 2026-08-31
- **Deciders**: Principal Socio-Technical Architect, High-Performance Implementer
- **Consulted**: SRE & Resilience Specialist, AppSec Lead
- **Informed**: Engineering Team

---

## 1. Context and Problem Statement

A full system audit of the LEX ecosystem identified operational vulnerabilities, concurrency blockers, and resource management deficiencies that compromised international-class enterprise resilience under high-concurrency production workloads:

1. **Database Session & Connection Leaks in REST API (P0)**: The FastAPI dependency provider returned raw SQLAlchemy `Session` instances without generator context cleanup (`yield` + `finally: session.close()`). Under high concurrent traffic, PostgreSQL connection pool descriptors were exhausted, causing complete API Denial of Service.
2. **Synchronous Blocking in Scrapy Downloader Middleware (P0)**: `DecorrelatedJitterRetryMiddleware` invoked synchronous `time.sleep()`, halting the single-threaded Twisted reactor event loop and freezing all concurrent spiders during transient HTTP 429/503 backoffs.
3. **Infinite Pagination Loop in CLI Stage 2 Treatment (P0)**: `lex treat --force` executed `limit(CHUNK_SIZE)` without cursor/keyset pagination (`WHERE id > last_seen_id`), re-querying and processing the same initial 500 records infinitely.
4. **CORS Security Misconfiguration (P0)**: `CORSMiddleware` configured `allow_origins=["*"]` with `allow_credentials=True`, violating W3C CORS specifications and exposing endpoints to CSRF/token exfiltration risks.
5. **Memory Sasturation (OOM) on LexML URN Consolidation Queries (P1)**: `get_compiled_act_by_urn` loaded all rows of `compiled_normative_acts` into RAM before filtering via Python in-memory loops, posing severe Out-Of-Memory risks on large datasets.
6. **Connection Pool Leaks on Worker Shutdown (P1)**: Spiders and ingestion pipelines instantiated SQLAlchemy `Engine` objects without explicitly invoking `engine.dispose()` during lifecycle teardown hooks (`closed` / `close_spider`).
7. **Unhandled Session Poisoning in Treatment Adapter (P2)**: `PostgresTreatmentRepository` executed commits without `session.rollback()` in exception handlers, leaving sessions in dirty/poisoned states upon database constraint violations.
8. **Hardcoded Federative Tier in Canonical URN Minting (P2)**: `generate_canonical_urn` hardcoded `:federal:` regardless of whether the source gazette was state or municipal.

---

## 2. Decision Drivers

- **Zero Downtime & Connection Safety**: Connection pool lifecycles must be deterministic, bounded, and guaranteed via context managers.
- **Asynchronous Non-Blocking Execution**: No synchronous sleeping or blocking I/O on Twisted or asyncio event loops.
- **Scalable Keyset Cursor Processing**: Continuous batching must support deterministic O(1) cursor pagination regardless of volume or force flags.
- **Fail-Safe Persistence Boundaries**: Every database write must be atomic, isolated, and automatically rolled back upon failure.
- **Constitutional & Standardized URN Compliance**: URN generation must dynamically respect Federative Tiers (federal, state, municipal).

---

## 3. Considered Options

- **Option 1: Ad-hoc localized patches**: Fix issues individually in presentation and persistence without formalizing lifecycle standards. *(Rejected: Leaves systemic patterns unaddressed).*
- **Option 2: Comprehensive Hexagonal & SRE Hardening (SOTA-KISS)**: Establish strict generator-based dependency injection for FastAPI, non-blocking Scrapy request delay scheduling, SQL/JSONB-level filtering for LexML URNs, cursor pagination in CLI loops, and full engine disposal. *(Accepted).*

---

## 4. Decision Outcome

We will implement **Comprehensive Hexagonal & SRE Hardening (Option 2)** across all bounded contexts:

### 4.1 FastAPI Session Lifecycle
All API session dependencies will use generator functions with strict `try...finally: session.close()` semantics, ensuring deterministic connection return to the connection pool upon request completion.

### 4.2 Non-Blocking Twisted Retry Scheduling
Scrapy retries will schedule backoff delays asynchronously via request metadata (`retry_req.meta["download_delay"] = sleep_delay`), completely eliminating `time.sleep()` from middleware execution.

### 4.3 Keyset Cursor Pagination for Treatment
Batch processing in CLI treatment will utilize UUID cursor pagination (`NormativeActModel.id > last_id` ordered by `id ASC`) to guarantee linear, non-repeating processing across arbitrarily large datasets.

### 4.4 Optimized JSONB & Column Querying
`get_compiled_act_by_urn` will query directly at the database layer using native SQLAlchemy JSONB operators (`compiled_ast["canonical_urn"].astext == canonical_urn`), eliminating full table scans.

### 4.5 Multi-Tier LexML URN Formatting
`generate_canonical_urn` will accept a `tier` parameter (`federal`, `estadual`, `municipal`) derived from `FederativeTier`.

---

## 5. Consequences and Trade-offs

### Positive
- API achieves enterprise-grade connection pool safety under high concurrent RPS.
- Scrapy crawler maintains full asynchronous throughput across concurrent domains during rate-limiting.
- CLI processing eliminates CPU-bound infinite loops and memory leaks.
- URNs strictly conform to the Brazilian LexML/FRBR standard across all federative tiers.

### Negative / Operational Constraints
- Developers must never instantiate database sessions in API routes without using `Depends(get_db_session)`.
- Custom Scrapy downloader middlewares must never call blocking standard library calls (`time.sleep`, `requests.get`).

---

## 6. Compliance & Hexagonal Verification

- [x] Hexagonal Architecture layers respected
- [x] No framework dependencies in Domain layer
- [x] Connection pool lifecycle governed at Composition Root
- [x] Observability and rollback safety ensured across all persistence adapters
