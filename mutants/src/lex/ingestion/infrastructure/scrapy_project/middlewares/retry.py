"""Decorrelated Jitter Retry Middleware for Scrapy.

Implements exponential backoff with full decorrelated jitter to prevent thundering herds:
t_retry = min(t_max, uniform(t_min, t_prev * 3))
"""

import random
import time
from collections.abc import Sequence
from typing import Any

from scrapy.crawler import Crawler
from scrapy.http import Request, Response

# -----------------------------------------------------------------------------
# Module Constants (ADR-003)
# -----------------------------------------------------------------------------
DEFAULT_RETRY_TIMES: int = 3
DEFAULT_RETRY_MIN_DELAY: float = 1.0
DEFAULT_RETRY_MAX_DELAY: float = 60.0
DEFAULT_RETRY_BACKOFF_FACTOR: float = 3.0
DEFAULT_RETRY_HTTP_CODES: Sequence[int] = (408, 429, 500, 502, 503, 504)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut: MutantDict = {}  # type: ignore
mutants_xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut: MutantDict = {}  # type: ignore
mutants_xǁDecorrelatedJitterRetryMiddlewareǁcompute_next_delay__mutmut: MutantDict = {}  # type: ignore
mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut: MutantDict = {}  # type: ignore
mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut: MutantDict = {}  # type: ignore
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut: MutantDict = {}  # type: ignore


class DecorrelatedJitterRetryMiddleware:
    """Downloader middleware implementing full decorrelated jitter backoff."""

    @_mutmut_mutated(mutants_xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut)
    def __init__(
        self,
        retry_times: int = DEFAULT_RETRY_TIMES,
        retry_http_codes: Sequence[int] | None = None,
        min_delay: float = DEFAULT_RETRY_MIN_DELAY,
        max_delay: float = DEFAULT_RETRY_MAX_DELAY,
        max_retry_times: int | None = None,
    ) -> None:
        self.retry_times = max_retry_times if max_retry_times is not None else retry_times
        self.retry_http_codes = set(retry_http_codes or DEFAULT_RETRY_HTTP_CODES)
        self.min_delay = min_delay
        self.max_delay = max_delay

    def xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut_orig(
        self,
        retry_times: int = DEFAULT_RETRY_TIMES,
        retry_http_codes: Sequence[int] | None = None,
        min_delay: float = DEFAULT_RETRY_MIN_DELAY,
        max_delay: float = DEFAULT_RETRY_MAX_DELAY,
        max_retry_times: int | None = None,
    ) -> None:
        self.retry_times = max_retry_times if max_retry_times is not None else retry_times
        self.retry_http_codes = set(retry_http_codes or DEFAULT_RETRY_HTTP_CODES)
        self.min_delay = min_delay
        self.max_delay = max_delay

    def xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut_1(
        self,
        retry_times: int = DEFAULT_RETRY_TIMES,
        retry_http_codes: Sequence[int] | None = None,
        min_delay: float = DEFAULT_RETRY_MIN_DELAY,
        max_delay: float = DEFAULT_RETRY_MAX_DELAY,
        max_retry_times: int | None = None,
    ) -> None:
        self.retry_times = None
        self.retry_http_codes = set(retry_http_codes or DEFAULT_RETRY_HTTP_CODES)
        self.min_delay = min_delay
        self.max_delay = max_delay

    def xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut_2(
        self,
        retry_times: int = DEFAULT_RETRY_TIMES,
        retry_http_codes: Sequence[int] | None = None,
        min_delay: float = DEFAULT_RETRY_MIN_DELAY,
        max_delay: float = DEFAULT_RETRY_MAX_DELAY,
        max_retry_times: int | None = None,
    ) -> None:
        self.retry_times = max_retry_times if max_retry_times is None else retry_times
        self.retry_http_codes = set(retry_http_codes or DEFAULT_RETRY_HTTP_CODES)
        self.min_delay = min_delay
        self.max_delay = max_delay

    def xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut_3(
        self,
        retry_times: int = DEFAULT_RETRY_TIMES,
        retry_http_codes: Sequence[int] | None = None,
        min_delay: float = DEFAULT_RETRY_MIN_DELAY,
        max_delay: float = DEFAULT_RETRY_MAX_DELAY,
        max_retry_times: int | None = None,
    ) -> None:
        self.retry_times = max_retry_times if max_retry_times is not None else retry_times
        self.retry_http_codes = None
        self.min_delay = min_delay
        self.max_delay = max_delay

    def xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut_4(
        self,
        retry_times: int = DEFAULT_RETRY_TIMES,
        retry_http_codes: Sequence[int] | None = None,
        min_delay: float = DEFAULT_RETRY_MIN_DELAY,
        max_delay: float = DEFAULT_RETRY_MAX_DELAY,
        max_retry_times: int | None = None,
    ) -> None:
        self.retry_times = max_retry_times if max_retry_times is not None else retry_times
        self.retry_http_codes = set(None)
        self.min_delay = min_delay
        self.max_delay = max_delay

    def xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut_5(
        self,
        retry_times: int = DEFAULT_RETRY_TIMES,
        retry_http_codes: Sequence[int] | None = None,
        min_delay: float = DEFAULT_RETRY_MIN_DELAY,
        max_delay: float = DEFAULT_RETRY_MAX_DELAY,
        max_retry_times: int | None = None,
    ) -> None:
        self.retry_times = max_retry_times if max_retry_times is not None else retry_times
        self.retry_http_codes = set(retry_http_codes and DEFAULT_RETRY_HTTP_CODES)
        self.min_delay = min_delay
        self.max_delay = max_delay

    def xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut_6(
        self,
        retry_times: int = DEFAULT_RETRY_TIMES,
        retry_http_codes: Sequence[int] | None = None,
        min_delay: float = DEFAULT_RETRY_MIN_DELAY,
        max_delay: float = DEFAULT_RETRY_MAX_DELAY,
        max_retry_times: int | None = None,
    ) -> None:
        self.retry_times = max_retry_times if max_retry_times is not None else retry_times
        self.retry_http_codes = set(retry_http_codes or DEFAULT_RETRY_HTTP_CODES)
        self.min_delay = None
        self.max_delay = max_delay

    def xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut_7(
        self,
        retry_times: int = DEFAULT_RETRY_TIMES,
        retry_http_codes: Sequence[int] | None = None,
        min_delay: float = DEFAULT_RETRY_MIN_DELAY,
        max_delay: float = DEFAULT_RETRY_MAX_DELAY,
        max_retry_times: int | None = None,
    ) -> None:
        self.retry_times = max_retry_times if max_retry_times is not None else retry_times
        self.retry_http_codes = set(retry_http_codes or DEFAULT_RETRY_HTTP_CODES)
        self.min_delay = min_delay
        self.max_delay = None

    @classmethod
    @_mutmut_mutated(mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut, is_classmethod = True)
    def from_crawler(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_orig(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_1(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = None
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_2(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = None
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_3(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint(None, DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_4(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", None)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_5(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint(DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_6(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", )
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_7(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("XXRETRY_TIMESXX", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_8(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("retry_times", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_9(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = None
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_10(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist(None, list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_11(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", None)
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_12(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist(list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_13(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", )
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_14(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("XXRETRY_HTTP_CODESXX", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_15(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("retry_http_codes", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_16(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(None))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_17(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = None
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_18(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat(None, DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_19(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", None)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_20(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat(DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_21(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", )
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_22(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("XXRETRY_MIN_DELAYXX", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_23(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("retry_min_delay", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_24(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = None
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_25(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat(None, DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_26(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", None)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_27(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat(DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_28(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", )
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_29(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("XXRETRY_MAX_DELAYXX", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_30(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("retry_max_delay", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_31(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=None,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_32(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=None,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_33(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=None,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_34(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=None,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_35(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_36(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            min_delay=min_delay,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_37(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            max_delay=max_delay,
        )

    @classmethod
    def xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_38(cls, crawler: Crawler) -> "DecorrelatedJitterRetryMiddleware":
        settings = crawler.settings
        retry_times = settings.getint("RETRY_TIMES", DEFAULT_RETRY_TIMES)
        retry_http_codes = settings.getlist("RETRY_HTTP_CODES", list(DEFAULT_RETRY_HTTP_CODES))
        min_delay = settings.getfloat("RETRY_MIN_DELAY", DEFAULT_RETRY_MIN_DELAY)
        max_delay = settings.getfloat("RETRY_MAX_DELAY", DEFAULT_RETRY_MAX_DELAY)
        return cls(
            retry_times=retry_times,
            retry_http_codes=retry_http_codes,
            min_delay=min_delay,
            )

    @_mutmut_mutated(mutants_xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut)
    def calculate_delay(self, prev_delay: float) -> float:
        """Calculate next sleep interval using AWS Decorrelated Jitter formula."""
        upper = prev_delay * DEFAULT_RETRY_BACKOFF_FACTOR
        delay = random.uniform(self.min_delay, upper)  # noqa: S311
        return min(self.max_delay, delay)

    def xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_orig(self, prev_delay: float) -> float:
        """Calculate next sleep interval using AWS Decorrelated Jitter formula."""
        upper = prev_delay * DEFAULT_RETRY_BACKOFF_FACTOR
        delay = random.uniform(self.min_delay, upper)  # noqa: S311
        return min(self.max_delay, delay)

    def xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_1(self, prev_delay: float) -> float:
        """Calculate next sleep interval using AWS Decorrelated Jitter formula."""
        upper = None
        delay = random.uniform(self.min_delay, upper)  # noqa: S311
        return min(self.max_delay, delay)

    def xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_2(self, prev_delay: float) -> float:
        """Calculate next sleep interval using AWS Decorrelated Jitter formula."""
        upper = prev_delay / DEFAULT_RETRY_BACKOFF_FACTOR
        delay = random.uniform(self.min_delay, upper)  # noqa: S311
        return min(self.max_delay, delay)

    def xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_3(self, prev_delay: float) -> float:
        """Calculate next sleep interval using AWS Decorrelated Jitter formula."""
        upper = prev_delay * DEFAULT_RETRY_BACKOFF_FACTOR
        delay = None  # noqa: S311
        return min(self.max_delay, delay)

    def xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_4(self, prev_delay: float) -> float:
        """Calculate next sleep interval using AWS Decorrelated Jitter formula."""
        upper = prev_delay * DEFAULT_RETRY_BACKOFF_FACTOR
        delay = random.uniform(None, upper)  # noqa: S311
        return min(self.max_delay, delay)

    def xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_5(self, prev_delay: float) -> float:
        """Calculate next sleep interval using AWS Decorrelated Jitter formula."""
        upper = prev_delay * DEFAULT_RETRY_BACKOFF_FACTOR
        delay = random.uniform(self.min_delay, None)  # noqa: S311
        return min(self.max_delay, delay)

    def xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_6(self, prev_delay: float) -> float:
        """Calculate next sleep interval using AWS Decorrelated Jitter formula."""
        upper = prev_delay * DEFAULT_RETRY_BACKOFF_FACTOR
        delay = random.uniform(upper)  # noqa: S311
        return min(self.max_delay, delay)

    def xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_7(self, prev_delay: float) -> float:
        """Calculate next sleep interval using AWS Decorrelated Jitter formula."""
        upper = prev_delay * DEFAULT_RETRY_BACKOFF_FACTOR
        delay = random.uniform(self.min_delay, )  # noqa: S311
        return min(self.max_delay, delay)

    def xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_8(self, prev_delay: float) -> float:
        """Calculate next sleep interval using AWS Decorrelated Jitter formula."""
        upper = prev_delay * DEFAULT_RETRY_BACKOFF_FACTOR
        delay = random.uniform(self.min_delay, upper)  # noqa: S311
        return min(None, delay)

    def xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_9(self, prev_delay: float) -> float:
        """Calculate next sleep interval using AWS Decorrelated Jitter formula."""
        upper = prev_delay * DEFAULT_RETRY_BACKOFF_FACTOR
        delay = random.uniform(self.min_delay, upper)  # noqa: S311
        return min(self.max_delay, None)

    def xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_10(self, prev_delay: float) -> float:
        """Calculate next sleep interval using AWS Decorrelated Jitter formula."""
        upper = prev_delay * DEFAULT_RETRY_BACKOFF_FACTOR
        delay = random.uniform(self.min_delay, upper)  # noqa: S311
        return min(delay)

    def xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_11(self, prev_delay: float) -> float:
        """Calculate next sleep interval using AWS Decorrelated Jitter formula."""
        upper = prev_delay * DEFAULT_RETRY_BACKOFF_FACTOR
        delay = random.uniform(self.min_delay, upper)  # noqa: S311
        return min(self.max_delay, )

    @_mutmut_mutated(mutants_xǁDecorrelatedJitterRetryMiddlewareǁcompute_next_delay__mutmut)
    def compute_next_delay(self, prev_delay: float) -> float:
        """Alias for calculate_delay."""
        return self.calculate_delay(prev_delay)

    def xǁDecorrelatedJitterRetryMiddlewareǁcompute_next_delay__mutmut_orig(self, prev_delay: float) -> float:
        """Alias for calculate_delay."""
        return self.calculate_delay(prev_delay)

    def xǁDecorrelatedJitterRetryMiddlewareǁcompute_next_delay__mutmut_1(self, prev_delay: float) -> float:
        """Alias for calculate_delay."""
        return self.calculate_delay(None)

    @_mutmut_mutated(mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut)
    def process_response(
        self, request: Request, response: Response, spider: Any = None
    ) -> Response | Request:
        """Evaluate response status and retry with decorrelated jitter if matching error code."""
        # If request explicitly handles this status code (e.g. 502/404 on index checks),
        # pass through directly without retrying.
        if response.status in request.meta.get("handle_httpstatus_list", ()):
            return response
        if response.status in self.retry_http_codes:
            return self._retry(request, f"HTTP status {response.status}") or response
        return response

    def xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_orig(
        self, request: Request, response: Response, spider: Any = None
    ) -> Response | Request:
        """Evaluate response status and retry with decorrelated jitter if matching error code."""
        # If request explicitly handles this status code (e.g. 502/404 on index checks),
        # pass through directly without retrying.
        if response.status in request.meta.get("handle_httpstatus_list", ()):
            return response
        if response.status in self.retry_http_codes:
            return self._retry(request, f"HTTP status {response.status}") or response
        return response

    def xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_1(
        self, request: Request, response: Response, spider: Any = None
    ) -> Response | Request:
        """Evaluate response status and retry with decorrelated jitter if matching error code."""
        # If request explicitly handles this status code (e.g. 502/404 on index checks),
        # pass through directly without retrying.
        if response.status not in request.meta.get("handle_httpstatus_list", ()):
            return response
        if response.status in self.retry_http_codes:
            return self._retry(request, f"HTTP status {response.status}") or response
        return response

    def xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_2(
        self, request: Request, response: Response, spider: Any = None
    ) -> Response | Request:
        """Evaluate response status and retry with decorrelated jitter if matching error code."""
        # If request explicitly handles this status code (e.g. 502/404 on index checks),
        # pass through directly without retrying.
        if response.status in request.meta.get(None, ()):
            return response
        if response.status in self.retry_http_codes:
            return self._retry(request, f"HTTP status {response.status}") or response
        return response

    def xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_3(
        self, request: Request, response: Response, spider: Any = None
    ) -> Response | Request:
        """Evaluate response status and retry with decorrelated jitter if matching error code."""
        # If request explicitly handles this status code (e.g. 502/404 on index checks),
        # pass through directly without retrying.
        if response.status in request.meta.get("handle_httpstatus_list", None):
            return response
        if response.status in self.retry_http_codes:
            return self._retry(request, f"HTTP status {response.status}") or response
        return response

    def xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_4(
        self, request: Request, response: Response, spider: Any = None
    ) -> Response | Request:
        """Evaluate response status and retry with decorrelated jitter if matching error code."""
        # If request explicitly handles this status code (e.g. 502/404 on index checks),
        # pass through directly without retrying.
        if response.status in request.meta.get(()):
            return response
        if response.status in self.retry_http_codes:
            return self._retry(request, f"HTTP status {response.status}") or response
        return response

    def xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_5(
        self, request: Request, response: Response, spider: Any = None
    ) -> Response | Request:
        """Evaluate response status and retry with decorrelated jitter if matching error code."""
        # If request explicitly handles this status code (e.g. 502/404 on index checks),
        # pass through directly without retrying.
        if response.status in request.meta.get("handle_httpstatus_list", ):
            return response
        if response.status in self.retry_http_codes:
            return self._retry(request, f"HTTP status {response.status}") or response
        return response

    def xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_6(
        self, request: Request, response: Response, spider: Any = None
    ) -> Response | Request:
        """Evaluate response status and retry with decorrelated jitter if matching error code."""
        # If request explicitly handles this status code (e.g. 502/404 on index checks),
        # pass through directly without retrying.
        if response.status in request.meta.get("XXhandle_httpstatus_listXX", ()):
            return response
        if response.status in self.retry_http_codes:
            return self._retry(request, f"HTTP status {response.status}") or response
        return response

    def xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_7(
        self, request: Request, response: Response, spider: Any = None
    ) -> Response | Request:
        """Evaluate response status and retry with decorrelated jitter if matching error code."""
        # If request explicitly handles this status code (e.g. 502/404 on index checks),
        # pass through directly without retrying.
        if response.status in request.meta.get("HANDLE_HTTPSTATUS_LIST", ()):
            return response
        if response.status in self.retry_http_codes:
            return self._retry(request, f"HTTP status {response.status}") or response
        return response

    def xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_8(
        self, request: Request, response: Response, spider: Any = None
    ) -> Response | Request:
        """Evaluate response status and retry with decorrelated jitter if matching error code."""
        # If request explicitly handles this status code (e.g. 502/404 on index checks),
        # pass through directly without retrying.
        if response.status in request.meta.get("handle_httpstatus_list", ()):
            return response
        if response.status not in self.retry_http_codes:
            return self._retry(request, f"HTTP status {response.status}") or response
        return response

    def xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_9(
        self, request: Request, response: Response, spider: Any = None
    ) -> Response | Request:
        """Evaluate response status and retry with decorrelated jitter if matching error code."""
        # If request explicitly handles this status code (e.g. 502/404 on index checks),
        # pass through directly without retrying.
        if response.status in request.meta.get("handle_httpstatus_list", ()):
            return response
        if response.status in self.retry_http_codes:
            return self._retry(request, f"HTTP status {response.status}") and response
        return response

    def xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_10(
        self, request: Request, response: Response, spider: Any = None
    ) -> Response | Request:
        """Evaluate response status and retry with decorrelated jitter if matching error code."""
        # If request explicitly handles this status code (e.g. 502/404 on index checks),
        # pass through directly without retrying.
        if response.status in request.meta.get("handle_httpstatus_list", ()):
            return response
        if response.status in self.retry_http_codes:
            return self._retry(None, f"HTTP status {response.status}") or response
        return response

    def xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_11(
        self, request: Request, response: Response, spider: Any = None
    ) -> Response | Request:
        """Evaluate response status and retry with decorrelated jitter if matching error code."""
        # If request explicitly handles this status code (e.g. 502/404 on index checks),
        # pass through directly without retrying.
        if response.status in request.meta.get("handle_httpstatus_list", ()):
            return response
        if response.status in self.retry_http_codes:
            return self._retry(request, None) or response
        return response

    def xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_12(
        self, request: Request, response: Response, spider: Any = None
    ) -> Response | Request:
        """Evaluate response status and retry with decorrelated jitter if matching error code."""
        # If request explicitly handles this status code (e.g. 502/404 on index checks),
        # pass through directly without retrying.
        if response.status in request.meta.get("handle_httpstatus_list", ()):
            return response
        if response.status in self.retry_http_codes:
            return self._retry(f"HTTP status {response.status}") or response
        return response

    def xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_13(
        self, request: Request, response: Response, spider: Any = None
    ) -> Response | Request:
        """Evaluate response status and retry with decorrelated jitter if matching error code."""
        # If request explicitly handles this status code (e.g. 502/404 on index checks),
        # pass through directly without retrying.
        if response.status in request.meta.get("handle_httpstatus_list", ()):
            return response
        if response.status in self.retry_http_codes:
            return self._retry(request, ) or response
        return response

    @_mutmut_mutated(mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut)
    def process_exception(
        self, request: Request, exception: Exception, spider: Any = None
    ) -> Request | None:
        """Catch connection drop/timeout and retry with jitter."""
        return self._retry(request, str(exception))

    def xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut_orig(
        self, request: Request, exception: Exception, spider: Any = None
    ) -> Request | None:
        """Catch connection drop/timeout and retry with jitter."""
        return self._retry(request, str(exception))

    def xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut_1(
        self, request: Request, exception: Exception, spider: Any = None
    ) -> Request | None:
        """Catch connection drop/timeout and retry with jitter."""
        return self._retry(None, str(exception))

    def xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut_2(
        self, request: Request, exception: Exception, spider: Any = None
    ) -> Request | None:
        """Catch connection drop/timeout and retry with jitter."""
        return self._retry(request, None)

    def xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut_3(
        self, request: Request, exception: Exception, spider: Any = None
    ) -> Request | None:
        """Catch connection drop/timeout and retry with jitter."""
        return self._retry(str(exception))

    def xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut_4(
        self, request: Request, exception: Exception, spider: Any = None
    ) -> Request | None:
        """Catch connection drop/timeout and retry with jitter."""
        return self._retry(request, )

    def xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut_5(
        self, request: Request, exception: Exception, spider: Any = None
    ) -> Request | None:
        """Catch connection drop/timeout and retry with jitter."""
        return self._retry(request, str(None))

    @_mutmut_mutated(mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut)
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

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_orig(self, request: Request, reason: str) -> Request | None:
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

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_1(self, request: Request, reason: str) -> Request | None:
        retries = None
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

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_2(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 0) - 1
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

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_3(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get(None, 0) + 1
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

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_4(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", None) + 1
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

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_5(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get(0) + 1
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

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_6(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", ) + 1
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

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_7(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("XXretry_timesXX", 0) + 1
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

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_8(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("RETRY_TIMES", 0) + 1
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

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_9(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 1) + 1
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

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_10(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 0) + 2
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

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_11(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 0) + 1
        if retries < self.retry_times:
            prev_delay = request.meta.get("retry_delay", self.min_delay)
            sleep_delay = self.calculate_delay(prev_delay)

            time.sleep(sleep_delay)

            retry_req = request.copy()
            retry_req.meta["retry_times"] = retries
            retry_req.meta["retry_delay"] = sleep_delay
            retry_req.dont_filter = True
            return retry_req

        return None

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_12(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 0) + 1
        if retries <= self.retry_times:
            prev_delay = None
            sleep_delay = self.calculate_delay(prev_delay)

            time.sleep(sleep_delay)

            retry_req = request.copy()
            retry_req.meta["retry_times"] = retries
            retry_req.meta["retry_delay"] = sleep_delay
            retry_req.dont_filter = True
            return retry_req

        return None

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_13(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 0) + 1
        if retries <= self.retry_times:
            prev_delay = request.meta.get(None, self.min_delay)
            sleep_delay = self.calculate_delay(prev_delay)

            time.sleep(sleep_delay)

            retry_req = request.copy()
            retry_req.meta["retry_times"] = retries
            retry_req.meta["retry_delay"] = sleep_delay
            retry_req.dont_filter = True
            return retry_req

        return None

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_14(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 0) + 1
        if retries <= self.retry_times:
            prev_delay = request.meta.get("retry_delay", None)
            sleep_delay = self.calculate_delay(prev_delay)

            time.sleep(sleep_delay)

            retry_req = request.copy()
            retry_req.meta["retry_times"] = retries
            retry_req.meta["retry_delay"] = sleep_delay
            retry_req.dont_filter = True
            return retry_req

        return None

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_15(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 0) + 1
        if retries <= self.retry_times:
            prev_delay = request.meta.get(self.min_delay)
            sleep_delay = self.calculate_delay(prev_delay)

            time.sleep(sleep_delay)

            retry_req = request.copy()
            retry_req.meta["retry_times"] = retries
            retry_req.meta["retry_delay"] = sleep_delay
            retry_req.dont_filter = True
            return retry_req

        return None

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_16(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 0) + 1
        if retries <= self.retry_times:
            prev_delay = request.meta.get("retry_delay", )
            sleep_delay = self.calculate_delay(prev_delay)

            time.sleep(sleep_delay)

            retry_req = request.copy()
            retry_req.meta["retry_times"] = retries
            retry_req.meta["retry_delay"] = sleep_delay
            retry_req.dont_filter = True
            return retry_req

        return None

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_17(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 0) + 1
        if retries <= self.retry_times:
            prev_delay = request.meta.get("XXretry_delayXX", self.min_delay)
            sleep_delay = self.calculate_delay(prev_delay)

            time.sleep(sleep_delay)

            retry_req = request.copy()
            retry_req.meta["retry_times"] = retries
            retry_req.meta["retry_delay"] = sleep_delay
            retry_req.dont_filter = True
            return retry_req

        return None

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_18(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 0) + 1
        if retries <= self.retry_times:
            prev_delay = request.meta.get("RETRY_DELAY", self.min_delay)
            sleep_delay = self.calculate_delay(prev_delay)

            time.sleep(sleep_delay)

            retry_req = request.copy()
            retry_req.meta["retry_times"] = retries
            retry_req.meta["retry_delay"] = sleep_delay
            retry_req.dont_filter = True
            return retry_req

        return None

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_19(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 0) + 1
        if retries <= self.retry_times:
            prev_delay = request.meta.get("retry_delay", self.min_delay)
            sleep_delay = None

            time.sleep(sleep_delay)

            retry_req = request.copy()
            retry_req.meta["retry_times"] = retries
            retry_req.meta["retry_delay"] = sleep_delay
            retry_req.dont_filter = True
            return retry_req

        return None

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_20(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 0) + 1
        if retries <= self.retry_times:
            prev_delay = request.meta.get("retry_delay", self.min_delay)
            sleep_delay = self.calculate_delay(None)

            time.sleep(sleep_delay)

            retry_req = request.copy()
            retry_req.meta["retry_times"] = retries
            retry_req.meta["retry_delay"] = sleep_delay
            retry_req.dont_filter = True
            return retry_req

        return None

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_21(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 0) + 1
        if retries <= self.retry_times:
            prev_delay = request.meta.get("retry_delay", self.min_delay)
            sleep_delay = self.calculate_delay(prev_delay)

            time.sleep(None)

            retry_req = request.copy()
            retry_req.meta["retry_times"] = retries
            retry_req.meta["retry_delay"] = sleep_delay
            retry_req.dont_filter = True
            return retry_req

        return None

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_22(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 0) + 1
        if retries <= self.retry_times:
            prev_delay = request.meta.get("retry_delay", self.min_delay)
            sleep_delay = self.calculate_delay(prev_delay)

            time.sleep(sleep_delay)

            retry_req = None
            retry_req.meta["retry_times"] = retries
            retry_req.meta["retry_delay"] = sleep_delay
            retry_req.dont_filter = True
            return retry_req

        return None

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_23(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 0) + 1
        if retries <= self.retry_times:
            prev_delay = request.meta.get("retry_delay", self.min_delay)
            sleep_delay = self.calculate_delay(prev_delay)

            time.sleep(sleep_delay)

            retry_req = request.copy()
            retry_req.meta["retry_times"] = None
            retry_req.meta["retry_delay"] = sleep_delay
            retry_req.dont_filter = True
            return retry_req

        return None

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_24(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 0) + 1
        if retries <= self.retry_times:
            prev_delay = request.meta.get("retry_delay", self.min_delay)
            sleep_delay = self.calculate_delay(prev_delay)

            time.sleep(sleep_delay)

            retry_req = request.copy()
            retry_req.meta["XXretry_timesXX"] = retries
            retry_req.meta["retry_delay"] = sleep_delay
            retry_req.dont_filter = True
            return retry_req

        return None

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_25(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 0) + 1
        if retries <= self.retry_times:
            prev_delay = request.meta.get("retry_delay", self.min_delay)
            sleep_delay = self.calculate_delay(prev_delay)

            time.sleep(sleep_delay)

            retry_req = request.copy()
            retry_req.meta["RETRY_TIMES"] = retries
            retry_req.meta["retry_delay"] = sleep_delay
            retry_req.dont_filter = True
            return retry_req

        return None

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_26(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 0) + 1
        if retries <= self.retry_times:
            prev_delay = request.meta.get("retry_delay", self.min_delay)
            sleep_delay = self.calculate_delay(prev_delay)

            time.sleep(sleep_delay)

            retry_req = request.copy()
            retry_req.meta["retry_times"] = retries
            retry_req.meta["retry_delay"] = None
            retry_req.dont_filter = True
            return retry_req

        return None

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_27(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 0) + 1
        if retries <= self.retry_times:
            prev_delay = request.meta.get("retry_delay", self.min_delay)
            sleep_delay = self.calculate_delay(prev_delay)

            time.sleep(sleep_delay)

            retry_req = request.copy()
            retry_req.meta["retry_times"] = retries
            retry_req.meta["XXretry_delayXX"] = sleep_delay
            retry_req.dont_filter = True
            return retry_req

        return None

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_28(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 0) + 1
        if retries <= self.retry_times:
            prev_delay = request.meta.get("retry_delay", self.min_delay)
            sleep_delay = self.calculate_delay(prev_delay)

            time.sleep(sleep_delay)

            retry_req = request.copy()
            retry_req.meta["retry_times"] = retries
            retry_req.meta["RETRY_DELAY"] = sleep_delay
            retry_req.dont_filter = True
            return retry_req

        return None

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_29(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 0) + 1
        if retries <= self.retry_times:
            prev_delay = request.meta.get("retry_delay", self.min_delay)
            sleep_delay = self.calculate_delay(prev_delay)

            time.sleep(sleep_delay)

            retry_req = request.copy()
            retry_req.meta["retry_times"] = retries
            retry_req.meta["retry_delay"] = sleep_delay
            retry_req.dont_filter = None
            return retry_req

        return None

    def xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_30(self, request: Request, reason: str) -> Request | None:
        retries = request.meta.get("retry_times", 0) + 1
        if retries <= self.retry_times:
            prev_delay = request.meta.get("retry_delay", self.min_delay)
            sleep_delay = self.calculate_delay(prev_delay)

            time.sleep(sleep_delay)

            retry_req = request.copy()
            retry_req.meta["retry_times"] = retries
            retry_req.meta["retry_delay"] = sleep_delay
            retry_req.dont_filter = False
            return retry_req

        return None

mutants_xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut['_mutmut_orig'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut_1'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut_2'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut_3'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut_3 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut_4'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut_4 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut_5'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut_5 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut_6'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut_6 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut_7'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ__init____mutmut_7 # type: ignore # mutmut generated

mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['_mutmut_orig'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_orig # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_1'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_1 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_2'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_2 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_3'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_3 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_4'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_4 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_5'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_5 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_6'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_6 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_7'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_7 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_8'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_8 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_9'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_9 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_10'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_10 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_11'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_11 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_12'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_12 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_13'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_13 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_14'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_14 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_15'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_15 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_16'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_16 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_17'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_17 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_18'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_18 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_19'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_19 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_20'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_20 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_21'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_21 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_22'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_22 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_23'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_23 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_24'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_24 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_25'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_25 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_26'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_26 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_27'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_27 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_28'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_28 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_29'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_29 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_30'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_30 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_31'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_31 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_32'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_32 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_33'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_33 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_34'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_34 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_35'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_35 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_36'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_36 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_37'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_37 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_38'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁfrom_crawler__mutmut_38 # type: ignore # mutmut generated

mutants_xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut['_mutmut_orig'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_orig # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_1'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_1 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_2'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_2 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_3'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_3 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_4'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_4 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_5'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_5 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_6'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_6 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_7'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_7 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_8'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_8 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_9'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_9 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_10'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_10 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_11'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁcalculate_delay__mutmut_11 # type: ignore # mutmut generated

mutants_xǁDecorrelatedJitterRetryMiddlewareǁcompute_next_delay__mutmut['_mutmut_orig'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁcompute_next_delay__mutmut_orig # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁcompute_next_delay__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁcompute_next_delay__mutmut_1'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁcompute_next_delay__mutmut_1 # type: ignore # mutmut generated

mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut['_mutmut_orig'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_orig # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_1'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_1 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_2'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_2 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_3'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_3 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_4'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_4 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_5'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_5 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_6'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_6 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_7'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_7 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_8'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_8 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_9'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_9 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_10'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_10 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_11'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_11 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_12'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_12 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_13'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁprocess_response__mutmut_13 # type: ignore # mutmut generated

mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut['_mutmut_orig'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut_orig # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut_1'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut_1 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut_2'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut_2 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut_3'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut_3 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut_4'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut_4 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut_5'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁprocess_exception__mutmut_5 # type: ignore # mutmut generated

mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['_mutmut_orig'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_orig # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_1'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_1 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_2'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_2 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_3'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_3 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_4'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_4 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_5'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_5 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_6'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_6 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_7'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_7 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_8'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_8 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_9'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_9 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_10'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_10 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_11'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_11 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_12'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_12 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_13'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_13 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_14'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_14 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_15'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_15 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_16'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_16 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_17'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_17 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_18'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_18 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_19'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_19 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_20'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_20 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_21'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_21 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_22'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_22 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_23'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_23 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_24'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_24 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_25'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_25 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_26'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_26 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_27'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_27 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_28'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_28 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_29'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_29 # type: ignore # mutmut generated
mutants_xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut['xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_30'] = DecorrelatedJitterRetryMiddleware.xǁDecorrelatedJitterRetryMiddlewareǁ_retry__mutmut_30 # type: ignore # mutmut generated
