"""Decorrelated Jitter Retry Middleware for Scrapy.

Implements exponential backoff with full decorrelated jitter to prevent thundering herds:
t_retry = min(t_max, uniform(t_min, t_prev * 3))
"""

import random
import time
from typing import Any

from scrapy.crawler import Crawler
from scrapy.http import Request, Response


class DecorrelatedJitterRetryMiddleware:
    """Downloader middleware implementing full decorrelated jitter backoff."""

    def __init__(
        self,
        retry_times: int = 3,
        retry_http_codes: list[int] | None = None,
        min_delay: float = 1.0,
        max_delay: float = 60.0,
        max_retry_times: int | None = None,
    ) -> None:
        self.retry_times = max_retry_times if max_retry_times is not None else retry_times
        self.retry_http_codes = set(retry_http_codes or [408, 429, 500, 502, 503, 504])
        self.min_delay = min_delay
        self.max_delay = max_delay

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", 3)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", [408, 429, 500, 502, 503, 504])
        min_delay = settings.getfloat("RETRY_MIN_DELAY", 1.0)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", 60.0)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    def calculate_delay(self, prev_delay: float) -> float:
        """Calculate next sleep interval using AWS Decorrelated Jitter formula."""
        upper = prev_delay * 3.0
        delay = random.uniform(self.min_delay, upper)  # noqa: S311
        return min(self.max_delay, delay)

    def compute_next_delay(self, prev_delay: float) -> float:
        """Alias for calculate_delay."""
        return self.calculate_delay(prev_delay)

    def process_response(
        self, request: Request, response: Response, spider: Any = None
    ) -> Response | Request:
        """Evaluate response status and retry with decorrelated jitter if matching error code."""
        if response.status in self.retry_http_codes:
            return self._retry(request, f"HTTP status {response.status}") or response
        return response

    def process_exception(
        self, request: Request, exception: Exception, spider: Any = None
    ) -> Request | None:
        """Catch connection drop/timeout and retry with jitter."""
        return self._retry(request, str(exception))

    def _retry(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 0) + 1
        if retries <= self.retry_times:
            prev_delay = request.meta.get("retry_delay", self.min_delay)
            sleep_delay = self.calculate_delay(prev_delay)

            time.sleep(sleep_delay)

            retry_req = request.copy()
            retry_req.meta["retry_times"] = retries
            retry_req.meta["retry_delay"] = sleep_delay
            retry_req.dont_filter = True
            return retry_req

        return None
