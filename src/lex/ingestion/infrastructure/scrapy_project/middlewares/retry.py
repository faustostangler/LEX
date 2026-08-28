"""Decorrelated Jitter Exponential Backoff Retry Middleware for Scrapy.

Implements the AWS/Decorrelated Jitter algorithm:
t_retry = min(t_max, random.uniform(t_min, t_prev * 3))
to prevent thundering-herd synchronizations against government portals.
"""

import random

from scrapy import Spider
from scrapy.crawler import Crawler
from scrapy.http import Request, Response
from twisted.internet import defer
from twisted.internet.error import (
    ConnectError,
    ConnectionDone,
    ConnectionLost,
    ConnectionRefusedError,
    DNSLookupError,
    TCPTimedOutError,
    TimeoutError,
)


class DecorrelatedJitterRetryMiddleware:
    """Downloader middleware calculating Decorrelated Jitter delays between retry attempts."""

    EXCEPTIONS_TO_RETRY = (
        defer.TimeoutError,
        TimeoutError,
        DNSLookupError,
        ConnectionRefusedError,
        ConnectionDone,
        ConnectError,
        ConnectionLost,
        TCPTimedOutError,
    )

    def __init__(
        self,
        min_delay: float = 1.0,
        max_delay: float = 60.0,
        max_retry_times: int = 3,
        retry_http_codes: tuple[int, ...] = (408, 429, 500, 502, 503, 504),
    ) -> None:
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.max_retry_times = max_retry_times
        self.retry_http_codes = retry_http_codes

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        min_delay = settings.getfloat("RETRY_MIN_DELAY", 1.0)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", 60.0)
        max_retry_times = settings.getint("RETRY_TIMES", 3)
        retry_http_codes = tuple(
            settings.getlist("RETRY_HTTP_CODES", [408, 429, 500, 502, 503, 504])
        )
        return cls(
            min_delay=min_delay,
            max_delay=max_delay,
            max_retry_times=max_retry_times,
            retry_http_codes=retry_http_codes,
        )

    def compute_next_delay(self, prev_delay: float) -> float:
        """Compute the next sleep delay using Decorrelated Jitter."""
        high = max(self.min_delay, prev_delay * 3.0)
        jittered = random.uniform(self.min_delay, high)  # noqa: S311
        return min(self.max_delay, jittered)

    def process_response(
        self,
        request: Request,
        response: Response,
        spider: Spider,
    ) -> Response | Request:
        """Intercept retriable HTTP responses and schedule a jittered retry."""
        if request.meta.get("dont_retry", False):
            return response

        if response.status in self.retry_http_codes:
            reason = f"HTTP {response.status}"
            return self._retry(request, reason, spider) or response

        return response

    def process_exception(
        self,
        request: Request,
        exception: Exception,
        spider: Spider,
    ) -> Request | None:
        """Intercept retriable connection errors and schedule a jittered retry."""
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) and not request.meta.get(
            "dont_retry", False
        ):
            return self._retry(request, str(exception), spider)
        return None

    def _retry(self, request: Request, reason: str, spider: Spider) -> Request | None:
        retries = request.meta.get("retry_times", 0) + 1
        if retries <= self.max_retry_times:
            prev_delay = request.meta.get("retry_delay", self.min_delay)
            next_delay = self.compute_next_delay(prev_delay)

            retry_req = request.copy()
            retry_req.meta["retry_times"] = retries
            retry_req.meta["retry_delay"] = next_delay
            retry_req.meta["download_delay"] = next_delay
            retry_req.dont_filter = True
            retry_req.priority = request.priority - 10
            return retry_req

        return None
