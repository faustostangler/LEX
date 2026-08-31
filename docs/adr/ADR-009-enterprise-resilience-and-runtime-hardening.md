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

> [!NOTE]
> **API & SRE Development Status**: Active feature development is currently centered on the Core Legislative Engine (CLI, scrapers, segmentation, treatment, and consolidation). All REST API specifications and SRE telemetry endpoints (Sections 4.1, 4.6, 4.7) serve as architectural reference baselines and draft specifications pending explicit future phase approval before production expansion.

### 4.1 FastAPI Session Lifecycle (Reference Baseline / Pending Future Approval)
All API session dependencies will use generator functions with strict `try...finally: session.close()` semantics, ensuring deterministic connection return to the connection pool upon request completion.

### 4.2 Non-Blocking Twisted Retry Scheduling
Scrapy retries will schedule backoff delays asynchronously via request metadata (`retry_req.meta["download_delay"] = sleep_delay`), completely eliminating `time.sleep()` from middleware execution.

### 4.3 Keyset Cursor Pagination for Treatment
Batch processing in CLI treatment will utilize UUID cursor pagination (`NormativeActModel.id > last_id` ordered by `id ASC`) to guarantee linear, non-repeating processing across arbitrarily large datasets.

### 4.4 Optimized JSONB & Column Querying
`get_compiled_act_by_urn` will query directly at the database layer using native SQLAlchemy JSONB operators (`compiled_ast["canonical_urn"].astext == canonical_urn`), eliminating full table scans.

### 4.5 Multi-Tier LexML URN Formatting
`generate_canonical_urn` will accept a `tier` parameter (`federal`, `estadual`, `municipal`) derived from `FederativeTier`.

### 4.6 Synchronous Threadpool Dispatching for SQLAlchemy ORM Workloads
FastAPI routes that execute synchronous database operations (e.g. `get_compiled_legislation`) and their underlying application use cases / persistence adapters (`ConsolidationRepositoryPort`, `PostgresConsolidationRepository`, `CompileNormativeActUseCase`, `TimeTravelCompilationUseCase`) are declared as pure synchronous `def` functions. This delegates request execution directly to Starlette's worker threadpool (`anyio.to_thread.run_sync`), completely eliminating event loop starvation on the main ASGI `asyncio` event loop.

### 4.7 Centralized Exception Sanitization & RFC-7807 Compliance (CWE-209 Mitigation)
All unhandled database (`SQLAlchemyError`) and infrastructure exceptions are intercepted by global exception handlers and a `TraceIdMiddleware`. Responses are sanitized into standardized RFC-7807 problem details payloads with diagnostic `trace_id` headers (`X-Trace-ID`), while raw stack traces and internal queries are securely routed to internal application logs (Sentry/Loki), strictly preventing information exposure.

### 4.8 Multi-Spider Database Connection Pool Lifecycle in Crawlers
In ingestion pipelines (`GazetteIngestionPipeline`) and spiders (`FederalDouSpider`), shutdown hooks (`close_spider`, `closed`) flush buffered entities and close active transactional `Session` instances without invoking `engine.dispose()`. This preserves connection pools for concurrent and sequential spiders running within a single `CrawlerProcess` (e.g. `lex crawl all`), eliminating premature pool destruction and `PoolClosedError`.

### 4.9 ReDoS Prevention (CWE-1333 Mitigation) in Legislative Extraction Regexes
In `MutationExtractor`, alteration header regex patterns eliminate nested overlapping whitespace quantifiers (`[\w\s]+` with `\s+`), replacing them with non-overlapping tokens (`[A-Za-zçãéíóú]+` and bounded digit patterns). This guarantees linear-time $O(N)$ evaluation and eliminates CPU starvation from catastrophic polynomial/exponential backtracking.

### 4.10 PostgreSQL Catalog Statistics Non-Positive Tuple Bounds
In CLI streaming treatment (`run_treat`), queries against `pg_class.reltuples` strictly enforce `est > 0` before assigning progress totals. Unanalyzed or vacuum-pending tables returning `-1` gracefully fall back to continuous streaming (`total_acts = None`), preventing invalid or corrupted CLI progress bars.

### 4.11 JSON SQL Engine Filtering for Non-PostgreSQL Adapters (CWE-400 Mitigation)
In `PostgresConsolidationRepository.get_compiled_act_by_urn`, fallback lookups on non-PostgreSQL engines (such as hermetic SQLite test suites) execute `func.json_extract(CompiledNormativeActModel.compiled_ast, "$.canonical_urn") == canonical_urn` inside the database query engine rather than loading all table records into Python memory (`scalars(stmt).all()`). This enforces bounded $O(1)$ memory consumption and eliminates test suite out-of-memory crashes (CWE-400).

---

## 5. Consequences and Trade-offs

### Positive
- API achieves enterprise-grade connection pool safety under high concurrent RPS.
- Main ASGI `asyncio` event loop remains 100% non-blocking; database queries execute concurrently in worker threadpools.
- Unhandled database and system failures are sanitized, preventing CWE-209 information disclosure and complying with LGPD.
- Distributed tracing and SRE triage enabled via ubiquitous `trace_id` in response headers and RFC-7807 payloads.
- Scrapy crawler maintains full asynchronous throughput across concurrent domains during rate-limiting.
- CLI processing eliminates CPU-bound infinite loops and memory leaks.
- URNs strictly conform to the Brazilian LexML/FRBR standard across all federative tiers.

### Negative / Operational Constraints
- Developers must never instantiate database sessions in API routes without using `Depends(get_db_session)`.
- Developers must never declare `async def` routes that perform synchronous SQLAlchemy ORM calls without offloading.
- Custom Scrapy downloader middlewares must never call blocking standard library calls (`time.sleep`, `requests.get`).

---

## 6. Compliance & Hexagonal Verification

- [x] Hexagonal Architecture layers respected
- [x] No framework dependencies in Domain layer
- [x] Connection pool lifecycle governed at Composition Root
- [x] Observability and rollback safety ensured across all persistence adapters
