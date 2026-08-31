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

## 2. Explicit Connection Pool Disposal on Engine Teardown

### Vulnerability Identified (VULN-07 - P1)
Spiders ([`dou_spider.py`](file:///home/stangler/Documents/Python/LEX/src/lex/ingestion/infrastructure/scrapy_project/spiders/federal/dou_spider.py)) and pipelines ([`ingestion_pipeline.py`](file:///home/stangler/Documents/Python/LEX/src/lex/ingestion/infrastructure/scrapy_project/pipelines/ingestion_pipeline.py)) created local `create_engine()` instances during `from_crawler` setup. While sessions were closed in shutdown hooks, `engine.dispose()` was omitted, retaining TCP connection pool descriptors and socket handles until Python garbage collection.

### Remediated Architecture (SOTA-KISS)
Spiders and pipelines must track `_engine` instances and explicitly dispose them during teardown:

```python
def closed(self, reason: str) -> None:
    """Teardown hook disposing sessions and connection pools."""
    if hasattr(self, "_session") and self._session is not None:
        self._session.close()
    if hasattr(self, "_engine") and self._engine is not None:
        self._engine.dispose()
```
