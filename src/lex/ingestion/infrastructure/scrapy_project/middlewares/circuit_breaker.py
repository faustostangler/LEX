"""Domain Circuit Breaker Downloader Middleware for Scrapy.

Tracks transient server errors (429, 503) and connection drops on fragile
government portals, temporarily pausing domain requests to prevent starvation.
"""

import time
from collections import defaultdict
from typing import Any
from urllib.parse import urlparse

from scrapy.crawler import Crawler
from scrapy.http import Request, Response

# -----------------------------------------------------------------------------
# Module Constants (ADR-003)
# -----------------------------------------------------------------------------
DEFAULT_CIRCUIT_BREAKER_FAILURE_THRESHOLD: int = 5
DEFAULT_CIRCUIT_BREAKER_RESET_TIMEOUT: float = 60.0
CIRCUIT_BREAKER_ERROR_STATUSES: tuple[int, ...] = (429, 503)
HTTP_OK_STATUS: int = 200


class DomainCircuitBreakerMiddleware:
    """Monitors per-domain failure rates and trips a circuit breaker on thresholds."""

    def __init__(
        self,
        failure_threshold: int = DEFAULT_CIRCUIT_BREAKER_FAILURE_THRESHOLD,
        reset_timeout: float = DEFAULT_CIRCUIT_BREAKER_RESET_TIMEOUT,
    ) -> None:
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self._failures: dict[str, int] = defaultdict(int)
        self._tripped_at: dict[str, float] = {}

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> "DomainCircuitBreakerMiddleware":
        settings = crawler.settings
        failure_threshold = settings.getint(
            "CIRCUIT_BREAKER_FAILURE_THRESHOLD",
            DEFAULT_CIRCUIT_BREAKER_FAILURE_THRESHOLD,
        )
        reset_timeout = settings.getfloat(
            "CIRCUIT_BREAKER_RESET_TIMEOUT",
            DEFAULT_CIRCUIT_BREAKER_RESET_TIMEOUT,
        )
        return cls(failure_threshold=failure_threshold, reset_timeout=reset_timeout)

    def _get_domain(self, request_or_url: str | Request) -> str:
        url = request_or_url.url if isinstance(request_or_url, Request) else request_or_url
        return urlparse(url).netloc

    def is_open(self, domain: str) -> bool:
        """Check whether the circuit is currently OPEN (tripped) for a domain."""
        if domain not in self._tripped_at:
            return False

        tripped_timestamp = self._tripped_at[domain]
        if time.time() - tripped_timestamp > self.reset_timeout:
            # Circuit cooldown expired, enter half-open/closed state
            del self._tripped_at[domain]
            self._failures[domain] = 0
            return False

        return True

    def get_failure_count(self, domain: str) -> int:
        """Get the current failure count for a domain."""
        return self._failures[domain]

    def process_request(self, request: Request, spider: Any = None) -> Any:
        """Intercept request and defer execution non-blockingly if the domain circuit is open."""
        domain = self._get_domain(request)
        if self.is_open(domain):
            tripped_ts = self._tripped_at.get(domain, time.time())
            elapsed = time.time() - tripped_ts
            remaining = max(0.1, self.reset_timeout - elapsed)
            request.priority -= 10
            request.dont_filter = True

            from twisted.internet import reactor, task

            return task.deferLater(reactor, remaining, lambda: None)

    def process_response(
        self, request: Request, response: Response, spider: Any = None
    ) -> Response:
        """Track response status codes for rate-limits (429) or service outages (503)."""
        domain = self._get_domain(request)

        if response.status in CIRCUIT_BREAKER_ERROR_STATUSES:
            self._record_failure(domain)
        elif response.status == HTTP_OK_STATUS:
            self._failures[domain] = 0
            if domain in self._tripped_at:
                del self._tripped_at[domain]

        return response

    def process_exception(self, request: Request, exception: Exception, spider: Any = None) -> None:
        """Record network drop or timeout exception."""
        domain = self._get_domain(request)
        self._record_failure(domain)

    def _record_failure(self, domain: str) -> None:
        self._failures[domain] += 1
        if self._failures[domain] >= self.failure_threshold:
            self._tripped_at[domain] = time.time()
