# ADR-011: Circuit Breaker Non-Dropping Deferred Rescheduling Pattern

- **Status**: Accepted
- **Date**: 2026-08-31
- **Deciders**: Principal Socio-Technical Architect, High-Performance Implementer
- **Consulted**: SRE & Crawler Performance Lead
- **Informed**: Engineering Team
- **Bounded Context**: `ingestion`

---

## 1. Context and Problem Statement

During high-concurrency ingestion across federal and state official gazette portals (e.g. *Imprensa Nacional / in.gov.br*, *DOE BA*, *DOE RJ*), fragile government infrastructure frequently returns transient rate-limiting status codes (`HTTP 429 Too Many Requests`) or temporary service unavailability (`HTTP 503 Service Unavailable`).

In vulnerability audit item **CRIT-03**, a critical data loss flaw was identified in `DomainCircuitBreakerMiddleware`:
1. When a domain accumulated consecutive failures exceeding `failure_threshold`, the circuit breaker transitioned to `OPEN` state for a 60-second cooldown period.
2. While `is_open(domain)` evaluated to `True`, `process_request` raised Scrapy's `IgnoreRequest` exception.
3. In the Scrapy crawler architecture, `IgnoreRequest` causes the downloader engine to **permanently discard** the request without re-queuing or retry.
4. As a result, all gazette edition downloads and discrete act scraping requests enqueued during that 60-second interval were permanently lost, leaving silent historical gaps in the legislative database.

---

## 2. Decision Drivers

- **Zero-Drop Guarantee**: No valid gazette or act request may ever be silently dropped due to transient server outages.
- **Asynchronous Cooldown Backoff**: Suspended requests must be delayed asynchronously on the Twisted reactor without blocking the event loop or starving other healthy domains.
- **Priority Re-weighting**: Delayed requests must have their scheduler priority decremented (`request.priority -= 10`) to allow healthy domains to progress while backlogged domains recover.
- **Filter Immunity**: Retried and rescheduled requests must set `request.dont_filter = True` to bypass duplicate request filters.

---

## 3. Considered Options

- **Option 1: Retain `IgnoreRequest` and rely on manual re-crawl**: Discard requests during circuit open state and force operators to re-run spiders with `--force`. *(Rejected: Defeats autonomous 24/7 ingestion, creates data gaps, and violates enterprise SLA).*
- **Option 2: Synchronous sleep inside middleware**: Block the thread with `time.sleep(cooldown)`. *(Rejected: Halts Twisted reactor, freezing all concurrent spiders).*
- **Option 3: Non-Dropping Deferred Rescheduling with `task.deferLater` (SOTA-KISS)**: Calculate remaining cooldown time, re-weight priority (`request.priority -= 10`), set `request.dont_filter = True`, and return an asynchronous Twisted `Deferred` via `task.deferLater(reactor, remaining, lambda: None)`. *(Accepted).*

---

## 4. Decision Outcome

We implement **Option 3: Non-Dropping Deferred Rescheduling with `task.deferLater`**:

```mermaid
flowchart TD
    A["Incoming Request for Domain"] --> B{"Is Circuit OPEN?<br/>(Cooldown active)"}
    B -->|No (Closed / Normal)| C["Return None -> Proceed to Downloader"]
    B -->|Yes (Tripped)| D["Calculate remaining_cooldown = max(0.1, reset_timeout - elapsed)"]
    D --> E["request.priority -= 10<br/>request.dont_filter = True"]
    E --> F["Return task.deferLater(reactor, remaining_cooldown, lambda: None)"]
    F --> G["Twisted pauses request non-blockingly"]
    G -->|Cooldown expires| H["Resume Downloader Pipeline for Request"]
```

### 4.1 Implementation Details
Inside `DomainCircuitBreakerMiddleware.process_request`:
```python
if self.is_open(domain):
    tripped_ts = self._tripped_at.get(domain, time.time())
    elapsed = time.time() - tripped_ts
    remaining = max(0.1, self.reset_timeout - elapsed)
    request.priority -= 10
    request.dont_filter = True
    try:
        from twisted.internet import reactor, task
        return task.deferLater(reactor, remaining, lambda: None)
    except Exception:
        return None
```

---

## 5. Consequences

### Positive
- **Zero Request Dropping**: Transient 429/503 errors no longer lead to missing gazette dates or lost normative acts.
- **Non-Blocking Reactor**: Healthy domains continue crawling at full throughput while troubled domains back off.
- **Self-Healing**: Once the government portal recovers and cooldown expires, deferred requests execute cleanly.

### Negative / Operational Constraints
- During prolonged outages exceeding maximum retries, the scheduler queue retains delayed requests until cooldown expires or crawler termination.

---

## 6. Compliance & Hexagonal Verification

- [x] Hexagonal Architecture layers respected (Downloader middleware isolated in Infrastructure layer).
- [x] No framework dependencies leaked into Domain or Application layers.
- [x] Non-blocking event-driven concurrency maintained on Twisted reactor.
