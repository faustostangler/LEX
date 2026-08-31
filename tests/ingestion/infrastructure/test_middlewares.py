"""Precision Unit Tests for Scrapy Resilience Middlewares.

Verifies DomainCircuitBreakerMiddleware and DecorrelatedJitterRetryMiddleware
behavior specified in SPEC-001 (Section 4 Scenario 3).
"""

from unittest.mock import MagicMock

import pytest
from scrapy.exceptions import IgnoreRequest
from scrapy.http import Request, Response
from scrapy.spiders import Spider

from lex.ingestion.infrastructure.scrapy_project.middlewares.circuit_breaker import (
    DomainCircuitBreakerMiddleware,
)
from lex.ingestion.infrastructure.scrapy_project.middlewares.retry import (
    DecorrelatedJitterRetryMiddleware,
)


@pytest.fixture
def mock_spider() -> Spider:
    spider = MagicMock(spec=Spider)
    spider.name = "federal_dou"
    return spider


class TestDomainCircuitBreakerMiddleware:
    """Acceptance tests for DomainCircuitBreakerMiddleware."""

    def test_circuit_trips_after_consecutive_failures(self, mock_spider: Spider) -> None:
        """Scenario: Domain error threshold trips circuit breaker to OPEN."""
        middleware = DomainCircuitBreakerMiddleware(failure_threshold=3, reset_timeout=10.0)
        req = Request(url="https://pesquisa.in.gov.br/endpoint")
        resp_503 = Response(url="https://pesquisa.in.gov.br/endpoint", status=503)

        # 1st failure
        middleware.process_response(req, resp_503, mock_spider)
        assert middleware.is_open("pesquisa.in.gov.br") is False

        # 2nd failure
        middleware.process_response(req, resp_503, mock_spider)
        assert middleware.is_open("pesquisa.in.gov.br") is False

        # 3rd failure (trips)
        middleware.process_response(req, resp_503, mock_spider)
        assert middleware.is_open("pesquisa.in.gov.br") is True

        # Next request must be ignored
        with pytest.raises(IgnoreRequest, match="Circuit breaker OPEN for domain"):
            middleware.process_request(req, mock_spider)

    def test_circuit_resets_on_success(self, mock_spider: Spider) -> None:
        """Scenario: 200 OK response resets error counter."""
        middleware = DomainCircuitBreakerMiddleware(failure_threshold=3, reset_timeout=10.0)
        req = Request(url="https://pesquisa.in.gov.br/endpoint")
        resp_503 = Response(url="https://pesquisa.in.gov.br/endpoint", status=503)
        resp_200 = Response(url="https://pesquisa.in.gov.br/endpoint", status=200)

        middleware.process_response(req, resp_503, mock_spider)
        middleware.process_response(req, resp_503, mock_spider)
        assert middleware.get_failure_count("pesquisa.in.gov.br") == 2

        middleware.process_response(req, resp_200, mock_spider)
        assert middleware.get_failure_count("pesquisa.in.gov.br") == 0


class TestDecorrelatedJitterRetryMiddleware:
    """Acceptance tests for DecorrelatedJitterRetryMiddleware."""

    def test_calculate_jitter_delay_bounds(self) -> None:
        """Scenario: Calculated jitter delay stays within min/max bounds."""
        middleware = DecorrelatedJitterRetryMiddleware(
            min_delay=1.0,
            max_delay=30.0,
            max_retry_times=3,
        )

        prev_delay = 2.0
        new_delay = middleware.compute_next_delay(prev_delay)
        assert 1.0 <= new_delay <= 30.0

    def test_retry_on_429_rate_limit(self, mock_spider: Spider) -> None:
        """Scenario: 429 Too Many Requests schedules a jittered retry."""
        middleware = DecorrelatedJitterRetryMiddleware(
            min_delay=0.1,
            max_delay=5.0,
            max_retry_times=2,
        )
        req = Request(url="https://pesquisa.in.gov.br/item")
        resp_429 = Response(url="https://pesquisa.in.gov.br/item", status=429)

        retried_req = middleware.process_response(req, resp_429, mock_spider)
        assert isinstance(retried_req, Request)
        assert retried_req.meta.get("retry_times") == 1
        assert "retry_delay" in retried_req.meta
        assert "download_delay" in retried_req.meta
        assert retried_req.meta["download_delay"] == retried_req.meta["retry_delay"]
        assert retried_req.dont_filter is True
