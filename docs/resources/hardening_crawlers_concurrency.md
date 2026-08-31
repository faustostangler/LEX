# Crawlers & Ingestion Concurrency Hardening Guide (LEX)

This document specifies asynchronous networking, non-blocking retries, and connection cleanup rules for the Scrapy crawling engine.

---

## 1. Non-Blocking Downloader Retries & Twisted Reactor Safety

### Vulnerability Identified (VULN-02 - P0)
Scrapy operates on the Twisted framework's single-threaded asynchronous reactor loop. In `DecorrelatedJitterRetryMiddleware`, invoking `time.sleep(sleep_delay)` blocked the OS thread executing the Twisted reactor. 

If an upstream government portal returned a `429 Too Many Requests` or `503 Service Unavailable`, a 30-second `time.sleep` completely halted all concurrent spiders, active HTTP requests, and pipeline flushing across the entire application process.

### Remediated Architecture (SOTA-KISS)
Retries are scheduled non-blockingly using Scrapy's native request metadata controls (`download_delay`):

```python
def _retry(self, request: Request, reason: str) -> Request | None:
    retries = request.meta.get("retry_times", 0) + 1
    if retries <= self.retry_times:
        prev_delay = request.meta.get("retry_delay", self.min_delay)
        sleep_delay = self.calculate_delay(prev_delay)

        retry_req = request.copy()
        retry_req.meta["retry_times"] = retries
        retry_req.meta["retry_delay"] = sleep_delay
        retry_req.meta["download_delay"] = sleep_delay  # Non-blocking async delay
        retry_req.dont_filter = True
        return retry_req

    return None
```

---

---

## 2. Multi-Spider Database Connection Pool Lifecycle & Non-Disposal on Spider Close

### Vulnerability Identified (VULN-05 - P1)
When the command `lex crawl all` initiates multiple spiders inside a single `CrawlerProcess`, each spider and its associated `GazetteIngestionPipeline` shares or independently opens database sessions from SQLAlchemy connection pools. 

Executing `self._engine.dispose()` inside individual spider/pipeline shutdown hooks (`close_spider` or spider `closed`) destroys the underlying connection pool immediately when the first spider terminates. Any concurrent or sequential spiders still in-flight will subsequently crash with `PoolClosedError` or `StatementError`.

### Remediated Architecture (SOTA-KISS)
1. **Per-Spider Session Lifecycle**: In `close_spider` and spider `closed()` hooks, spiders and pipelines flush remaining buffers and close only their active `Session` (`self._session.close()`), returning database connections cleanly to the pool.
2. **Engine Pool Preservation**: Individual spider shutdowns must **never** call `self._engine.dispose()`. Connection pools remain open for concurrent spiders and are safely reclaimed upon `CrawlerProcess` exit.

```python
# Ingestion Pipeline Shutdown Hook (GazetteIngestionPipeline)
def close_spider(self, spider: Any = None) -> None:
    """Flush any pending buffered acts and clean up database session on spider shutdown."""
    self._flush_acts()
    if self._session is not None:
        try:
            self._session.close()
        except Exception as exc:
            logger.warning(f"Error closing pipeline database session: {exc}")
    # Note: Do NOT call self._engine.dispose() here to preserve multi-spider pools.
```

### Invariants:
1. **Never Dispose Shared Engines in `close_spider`**: Spiders and pipelines must only close transactional sessions.
2. **Safe Session Cleanup**: Session closures must be wrapped in exception guards to prevent teardown crashes from masking crawl outcomes.
