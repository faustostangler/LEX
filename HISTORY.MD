LEX Project

The LEX system coordinates multi-tier legal data ingestion across federal, state, and municipal jurisdictions. The current federal corpus comprises roughly eleven gigabytes across ninety nine thousand documents and three Diário Oficial da União sections. Ingestion pipelines require SHA256 cryptographic hashing for persistent content deduplication. State persistence mechanisms ensure crawler fault tolerance across expansive execution cycles.

The engineering strategy deploys an asynchronous crawling framework across tiered execution phases. Federal document retrieval establishes the baseline ingestion layer. Subsequent ingestion phases target Tier Zero state gazetes before proceeding to secondary federative units. Municipal operations incorporate specialized extraction mixins across thousands of regional territories.

Architectural hardening requires systematic verification across thirteen domain chapters. Formal Architecture Decison Records will codify the selected pipeline paradigms. Project initialization workflows generate domain glossaries alongside contextual registers during systematic technical reviews. Production components assimilate validated prototype algorithms into maintainable parsing structures.

**Decision Record: Architectural Decisions for the LEX Project**

**01.1 In-Memory Binary Streaming vs. Ephemeral Disk Spooling for High-Volume PDFs**

* **Chosen Decision:** Option A with low-memory bounds and a conditional fallback to Option B for oversized files. Pure in-memory extraction executes via `io.BytesIO` inside the item pipeline, converting PDF binary streams directly to plain text and structural metadata before dropping the byte references for immediate garbage collection. Ephemeral disk spooling via `/dev/shm` or temporary files is reserved strictly for oversized streams exceeding heap thresholds.
* **Rationale:** Eliminates disk I/O bottlenecks and enforces the zero-retention invariant for binary gazettes while maintaining deterministic memory limits via concurrency ceilings.
* **Discarded Options:** Option C (Chained Producer-Consumer with distributed queues) was discarded because it introduces premature infrastructure overhead and violates the Modular Monolith standard.

**01.2 Network I/O Resiliency, TCP Connection Pooling & Adaptive Backoff**

* **Chosen Decision:** Hybrid Option A + Option C. Scrapy AutoThrottle dynamically manages request latencies with an exponential backoff retry middleware utilizing the Decorrelated Jitter algorithm ($t_{retry} = \min(t_{max}, \text{random}(t_{min}, t_{prev} \times 3))$) for transient errors, coupled with a per-domain threshold-based Circuit Breaker middleware.
* **Rationale:** Mitigates thundering herd conditions against fragile public portals and prevents thread or socket starvation by temporarily pausing spiders dedicated to failing hosts without interrupting the broader ingestion runner.
* **Discarded Options:** Option B (Fixed rate limiting via commercial proxy rotators) was discarded because it imposes high operational costs and unethical traffic patterns against public sector infrastructure.

**02.1 Hexagonal Boundary & Anti-Corruption Layer (ACL) between Scrapy and Domain Entities**

* **Chosen Decision:** Option B (Two-Stage DTO $\to$ ACL Mapper $\to$ Domain Entity). Spiders yield unvalidated `RawGazettePayload` DTOs containing extracted strings and streams. An intermediate pipeline serves as the Anti-Corruption Layer, invoking a `GazetteMapper` to validate invariants and construct immutable `GazetteEdition` domain entities before invoking the repository port.
* **Rationale:** Preserves strict hexagonal isolation, preventing parsing errors from bubbling up as domain invariant violations while keeping the domain pure of framework dependencies.
* **Discarded Options:** Option A (direct Pydantic domain entities yielded by Scrapy) and Option C (untyped dictionaries) were discarded because they couple domain models to infrastructure or introduce untyped schema drift.

**02.2 Ports Contract Definition, Fail-Fast Centralized Config & Exception Hierarchy**

* **Chosen Decision:** Option A. Application ports are specified as structural subtypes via `@runtime_checkable typing.Protocol`. Centralized configuration uses immutable `pydantic-settings` models that fail fast at boot on missing or invalid environment variables. Infrastructure adapters explicitly catch external errors and wrap them into a strongly typed `LexDomainError` hierarchy.
* **Rationale:** Enables structural subtyping without rigid class hierarchies, simplifies mock-free test doubles, guarantees boot-time configuration integrity, and prevents third-party exceptions from crossing the adapter boundary.
* **Discarded Options:** Option B (Nominal `abc.ABC` subtyping) and Option C (direct concrete adapters with global `os.environ` lookups) were discarded because they introduce nominal coupling or runtime fragility.

**03.1 PostgreSQL Schema Design, Primary Key Strategy & Digestion Data Model**

* **Chosen Decision:** Option A (Normalized Two-Tier Relational Model). The Ingestion tier stores administrative containers in `gazette_editions` with UUIDv7 primary keys, natural composite unique constraints, content SHA-256 hashes, and TOAST-compressed raw text. The Treatment tier parses these into individual `normative_acts` linked via foreign keys, complete with enumerated normative levels, authorities, and thematic classifications.
* **Rationale:** Establishes transactional consistency across parent issues and child acts while enabling efficient multi-dimensional filtering across active or revoked statutes without write amplification.
* **Discarded Options:** Option B (JSONB documents in a single table) and Option C (hybrid CQRS with external document stores) were discarded because they cause query degradation during statutory updates or introduce distributed storage hazards.

**04.1 Multi-Role Container Topology & Local Development Compose Stack**

* **Chosen Decision:** Option A. A single multi-stage Dockerfile built with `uv` creates a hardened, non-root (`UID 10001`) base image that executes crawler, migration, CLI, or API roles through entrypoint overrides, orchestrated locally via `docker-compose.yml` with health-checked PostgreSQL 16 services.
* **Rationale:** Guarantees a single source of truth for deployment artifacts, minimizes image layers, accelerates build caching, and ensures absolute parity between local development and production runtimes.
* **Discarded Options:** Option B (separate Dockerfiles per role) and Option C (bare-metal developer host dependencies) were discarded because they duplicate configuration or create environment drift.

**05.1 Classification Strategy for Normative Acts**

* **Chosen Decision:** Option A + Active Feedback Loop. A multi-tier hybrid engine processes text first through deterministic regex AST parsers and canonical authority registries, falling back to a structured LLM classifier only when confidence drops below 0.85, with classified edge cases feeding a feedback flywheel to systematically refine deterministic rules over time.
* **Rationale:** Maximizes throughput and determinism while reducing API token costs by processing standard legislative publications through heuristics, reserving AI for unstructured ambiguities.
* **Discarded Options:** Option B (pure end-to-end LLM processing) and Option C (classical bag-of-words machine learning) were discarded because they incur high costs and latency or lack semantic nuance for legal hierarchies.

**08.1 Langfuse Telemetry, Structured Outputs & Golden Dataset Eval Gates**

* **Chosen Decision:** Option A. The fallback AI layer enforces Pydantic structured schemas for all completions, routes execution traces through the Langfuse SDK with contextual tags and cost tracking, routes ambiguous outcomes ($< 0.90$ confidence) to manual triage, and logs validated examples into a golden evaluation dataset.
* **Rationale:** Prevents schema corruption in the primary database and establishes deterministic evaluation gates for continuous heuristic rule improvements.
* **Discarded Options:** Option B (unstructured prompt parsing via regex) and Option C (unmonitored batch dumps) were discarded because they cause extraction failures or eliminate operational observability.

**10.1 State DOE Spider Architecture**

* **Chosen Decision:** Option A. Spiders derive from platform archetype mixins (e.g., `RestApiGazetteSpider`, `CalendarFormGazetteSpider`, `AspxViewerGazetteSpider`) layered on top of a common `BaseGazetteSpider`, with individual state spiders supplying declarative selectors, date schemas, and composite municipal discovery hooks.
* **Rationale:** Maximizes code reuse across the 27 federative units utilizing identical third-party publishing software while centralizing bug fixes within platform mixins.
* **Discarded Options:** Option B (27 standalone bespoke spiders) and Option C (a single monolithic parameterized regex spider) were discarded because they produce excessive boilerplate or collapse under complex state portal mechanics.

**11.1 LGPD/PII Redaction, Secret Sanitization & DevSecOps Supply Chain**

* **Chosen Decision:** Option A. A centralized structured logging adapter sanitizes CPFs, personal identification records, credentials, and tokens via regex masking before emission, paired with Sentry `before_send` scrubbing hooks and CI/CD pre-commit security audits using `ruff` and `pip-audit`.
* **Rationale:** Guarantees compliance with Brazilian data protection laws (LGPD) and prevents sensitive personal or infrastructure secrets from leaking into external telemetry collectors.
* **Discarded Options:** Option B (manual developer review) and Option C (post-hoc log pipeline scrubbing) were discarded because they introduce severe compliance risks or allow raw PII to traverse networks.

**12.1 Prometheus Golden Signals, Ubiquitous Domain Metrics & Scrapy Telemetry Extension**

* **Chosen Decision:** Option A. A Scrapy `PrometheusStatsExtension` maps crawler signals directly to a centralized domain metrics registry, publishing Prometheus counters and histograms covering extraction durations, circuit breaker states, digested acts, and LLM fallback rates.
* **Rationale:** Delivers real-time operational visibility into crawler throughput and state portal health for immediate alerting and Grafana visualization.
* **Discarded Options:** Option B (parsing log files via Loki) and Option C (periodic SQL aggregation queries) were discarded because they introduce alert latency or place unnecessary query overhead on the database.

**13.1 Database Storage Lifecycle, PostgreSQL TOAST LZ4 Compression & Backup Strategy**

* **Chosen Decision:** Option A. Large relational text columns (`full_text`) in `gazette_editions` and `normative_acts` utilize PostgreSQL 16 native LZ4 TOAST compression, supported by automated daily custom-format dumps (`pg_dump -Fc`) and WAL archiving from dedicated volume storage.
* **Rationale:** Delivers rapid decompression speeds for downstream NLP workloads, reduces disk footprint by 70% to 75%, and maintains atomic backup guarantees with zero storage sprawl.
* **Discarded Options:** Option B (Parquet cold-storage offloading) and Option C (uncompressed raw storage) were discarded because they break transactional query simplicity or waste storage bandwidth.

--

**Stage 1 & Stage 1.5 Ingestion Engine & State Archetypes Summary**

**Phase Objective and Scope**
Completed Stage 1 (Federal DOU Ingestion Engine) and Stage 1.5 (Platform Archetypes & P0 State Spiders) adhering to Hexagonal Architecture, Domain-Driven Design (DDD), and the Doctor Stangler Method.

**Implemented Core Components**
1. **Domain Core (`src/lex/ingestion/domain/`)**:
   - `value_objects.py`: `TerritoryId`, `GazetteDate`, `DocumentHash`, `FederativeTier`.
   - `entities.py`: `GazetteEdition` Aggregate Root with full invariant enforcement.
   - `exceptions.py`: `LexDomainError` typed domain exception hierarchy.
2. **Shared Kernel (`src/lex/shared_kernel/`)**:
   - `config.py`: `LexSettings` fail-fast configuration via `pydantic-settings`.
3. **Infrastructure Adapters (`src/lex/ingestion/infrastructure/`)**:
   - `adapters/stream_extractor.py`: `PdfStreamTextExtractor` implementing in-memory `io.BytesIO` and `SpooledTemporaryFile` fallback text extraction.
   - `adapters/gazette_mapper.py`: `GazetteMapper` Anti-Corruption Layer translating untyped `RawGazettePayload` DTOs into validated `GazetteEdition` domain entities.
   - `persistence/models.py`: SQLAlchemy 2.0 Declarative ORM model `GazetteEditionModel` with TOAST-compressed text columns, UUID primary keys, and natural composite unique constraints.
   - `persistence/postgres_repository.py`: `PostgresGazetteRepository` implementing `GazetteRepositoryPort` with PostgreSQL idempotent ON CONFLICT upsert semantics.
4. **Scrapy Crawler Framework & Spiders (`src/lex/ingestion/infrastructure/scrapy_project/`)**:
   - `spiders/base.py`: `BaseGazetteSpider` with date range iteration.
   - `spiders/archetypes/rest_api.py`: `RestApiGazetteSpider` archetype for JSON endpoint state portals.
   - `spiders/archetypes/monthly_directory.py`: `MonthlyDirectoryGazetteSpider` archetype for calendar directory portals.
   - `spiders/archetypes/aspx_viewer.py`: `AspxViewerGazetteSpider` archetype for ASP.NET WebForms portals.
   - **Federal & State Spiders (8 Discovered Spiders)**:
     - `federal_dou`: Imprensa Nacional (Federal DOU Sections 1, 2, 3, Extra, Suplementar).
     - `state_sp`: São Paulo (IMESP / DOE SP).
     - `state_rj`: Rio de Janeiro (Imprensa Oficial RJ).
     - `state_mg`: Minas Gerais (IOF MG).
     - `state_rs`: Rio Grande do Sul (CORAG / DOE RS).
     - `state_ba`: Bahia (EGBA / DOE BA).
     - `state_df`: Distrito Federal (DODF).
     - `state_pr`: Paraná (DIOE PR).
   - `middlewares/circuit_breaker.py`: `DomainCircuitBreakerMiddleware` to safeguard fragile government portals.
   - `middlewares/retry.py`: `DecorrelatedJitterRetryMiddleware` preventing thundering herd spikes.
   - `pipelines/ingestion_pipeline.py`: `GazetteIngestionPipeline` coordinating extractor, ACL mapper, and database persistence.
   - `settings.py` & `scrapy.cfg`: Complete Scrapy configuration.

**Verification and Quality Gate Metrics**
- **Test Suite**: 89 passed unit & integration tests in 5.45s.
- **Static Analysis (Ruff)**: 0 errors, 0 warnings, 100% formatted, Bandit security lint rules active.
- **Strict Typing (Mypy)**: 0 issues found across 35 source files (`mypy --strict`).
- **Mutation Testing (Mutmut)**: 37 mutants killed with zero surviving functional domain bugs.
- **Spider Registry Discovery**: `scrapy list` automatically discovers all 8 spiders.