# ADR-005: Micro-Batch Ingestion and Streaming Persistence for Normative Acts

**Status:** APPROVED  
**Date:** 2026-08-29  
**Decision Makers:** Lead Architect (@stangler), High-Performance Implementer (Antigravity)

---

## Context

Brazilian Official Gazette editions frequently contain thousands of discrete normative acts per publication. For example, Section 3 of the Federal Official Gazette (DOU - DO3) regularly publishes between 2,000 and 3,000 acts per daily issue.

Under the previous monolithic gather implementation:
1. `FederalDouSpider.parse_modern_section` scheduled all 2,000+ acts into a single `asyncio.gather(*tasks)` invocation.
2. During the 30 to 90 seconds required to download all acts over HTTP, zero items were yielded to the Scrapy engine or persisted to PostgreSQL.
3. If the crawling process was interrupted (`Ctrl+C`), crashed, or encountered an unhandled network error at 99% progress, all 2,000+ downloaded acts held in memory were lost without recovery.
4. Conversely, committing each act individually ($N=1$) inside `GazetteIngestionPipeline` generated 2,000 to 3,000 separate database transactions, WAL fsync operations, and TCP roundtrips per edition.

We require a **high-performance, KISS, and resilient ingestion pattern** that eliminates long write starvation windows, bounds memory consumption, preserves strict publication ordering, and minimizes database transaction overhead.

---

## Decision

We will implement a **Chunked Micro-Batch Streaming Ingestion Pattern** with an optimal batch size of $N=50$ acts (`DEFAULT_ACT_BATCH_SIZE = 50`) across both the spider extraction layer and the persistence pipeline because:

1. **Deterministic Sequential Chunks in Spider (`FederalDouSpider`)**:
   - `articles` are segmented into chunks of `DEFAULT_ACT_BATCH_SIZE = 50`.
   - Each chunk executes concurrently via `await asyncio.gather(*chunk_tasks)` bounded by `DEFAULT_CONCURRENT_SEMAPHORE = 50`.
   - As each chunk completes (~0.5 to 1.5 seconds), its payloads are immediately yielded to Scrapy while preserving exact publication order.
   - The unified `tqdm` progress bar continues tracking total acts ($0 \to \text{total}$) with zero UI disruption.

2. **Micro-Batch Database Persistence (`GazetteIngestionPipeline`)**:
   - `GazetteIngestionPipeline` buffers incoming `RawNormativeActPayload` items up to `BATCH_SIZE = 50`.
   - When the buffer reaches capacity or when `close_spider` is triggered, acts are persisted in a single bulk transaction via `GazetteRepositoryPort.save_normative_acts_bulk(batch)`.
   - Amortizes PostgreSQL transaction overhead and WAL lock acquisition by 98%.

---

## Technical Batch Size Evaluation

| Batch Size ($N$) | Time Between DB Writes | Memory Footprint | DB Transaction Overhead | Risk on Interruption | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **$N = 1$** (Unbuffered) | Instant (< 5ms) | Minimal (< 10 KB) | **Very High** (2,400 commits/edition; slow) | Zero data loss | **Rejected** (I/O & WAL bottleneck) |
| **$N = 50$** (Micro-Batch) | **~1.0 to 1.8s** | **~500 KB** | **Optimal** (48 commits/edition; ~98% reduction) | **Max 50 acts** | **SELECTED (SOTA / KISS)** |
| **$N = 250$** | ~6.0 to 10.0s | ~2.5 MB | Low (~10 commits/edition) | Max 250 acts | Sub-optimal UX latency |
| **$N = 2,400$** (Per Gazette) | 45.0 to 90.0s | ~25 MB | Minimal (1 commit/edition) | **2,400 acts lost** | **Rejected** (Original bottleneck) |

---

## Consequences

### Positive
- **Real-Time Database Progress**: PostgreSQL row counts increment continuously every 1-2 seconds in lockstep with the CLI progress bar.
- **Bounded Memory Usage**: In-memory act buffers are capped at $\le 50$ acts ($\le 500\text{ KB}$), preventing memory spikes during multi-date concurrent crawling.
- **Crash Resilience**: In case of process interruption, at most 50 acts need to be re-fetched.
- **Preserved Determinism**: Publication sequence order is 100% maintained.
- **Database Efficiency**: Bulk upserts eliminate 98% of individual transaction commit overhead.

### Negative
- `GazetteIngestionPipeline` maintains a small internal batch buffer that must be flushed on shutdown (`close_spider`).

---

## Alternatives Considered

### Alternative A: Async Worker Queue with `asyncio.Queue`
- **Pros:** Completely decouples fetcher tasks from item yielding.
- **Cons:** Introduces complex queue lifecycle management, background task exception handling, and higher cognitive load.
- **Why rejected:** Violates KISS. Sequential chunking with `asyncio.gather(*chunk)` delivers the exact same batching performance with zero state machine complexity.

### Alternative B: Direct Streaming with `asyncio.as_completed`
- **Pros:** Yields acts the millisecond each HTTP request finishes.
- **Cons:** Scrambles publication order because shorter HTML pages complete ahead of longer ones, breaking the natural document hierarchy in gazette editions.
- **Why rejected:** Fails the domain requirement for deterministic legal act sequencing.

---

## Compliance Checklist

- [x] Hexagonal Architecture layers respected (Domain $\to$ Application $\to$ Infrastructure)
- [x] Zero framework dependencies in Domain layer
- [x] Bounded context boundaries and ports preserved (`GazetteRepositoryPort.save_normative_acts_bulk`)
- [x] Fail-fast centralized constant governance (`DEFAULT_ACT_BATCH_SIZE = 50`)
- [x] Test specifications defined for chunked yielding and batch persistence flush
