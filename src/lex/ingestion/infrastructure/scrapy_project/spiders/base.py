"""Base Gazette Spider for Brazilian Ingestion Architecture.

Establishes common date range iteration, parameter parsing, metadata contracts,
and Scrapy 2.18+ async start() entrypoints for all federal, state, and municipal spiders.
Supports descending chronological order by default (most recent date to oldest).
"""

from collections.abc import AsyncIterator, Generator
from datetime import date, datetime, timedelta
from typing import Any

import scrapy
from scrapy.http import Request

# Earliest publication available in the modern digital DOU portal (in.gov.br)
EARLIEST_MODERN_DOU_DATE = date(2002, 1, 2)


class BaseGazetteSpider(scrapy.Spider):
    """Abstract baseline spider providing uniform date range generators."""

    territory_code: str
    tier: str
    start_date: date
    end_date: date
    reverse: bool

    def __init__(
        self,
        start_date: str | date | None = None,
        end_date: str | date | None = None,
        reverse: bool | str = True,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)

        today = date.today()
        parsed_start = self._parse_date_param(start_date)
        parsed_end = self._parse_date_param(end_date)

        if parsed_start is not None and parsed_end is None:
            self.start_date = parsed_start
            self.end_date = parsed_start
        elif parsed_start is None and parsed_end is not None:
            self.start_date = EARLIEST_MODERN_DOU_DATE
            self.end_date = parsed_end
        elif parsed_start is not None and parsed_end is not None:
            self.start_date = parsed_start
            self.end_date = parsed_end
        else:
            self.start_date = EARLIEST_MODERN_DOU_DATE
            self.end_date = today

        self.reverse = (
            (str(reverse).lower() in ("true", "1", "yes"))
            if isinstance(reverse, str)
            else bool(reverse)
        )

        if self.start_date > self.end_date:
            raise ValueError(
                f"start_date ({self.start_date}) cannot be after end_date ({self.end_date})"
            )

    @staticmethod
    def _parse_date_param(param: str | date | None) -> date | None:
        """Parse incoming CLI/Runner date parameter."""
        if param is None or isinstance(param, date):
            return param

        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(param, fmt).date()
            except ValueError:
                continue

        raise ValueError(f"Invalid date parameter format: '{param}'")

    def date_range(self) -> Generator[date, None, None]:
        """Yield each date in the inclusive [start_date, end_date] interval.

        By default (reverse=True), yields in descending chronological order
        (from the most recent date down to the oldest date).
        """
        if self.reverse:
            current = self.end_date
            while current >= self.start_date:
                yield current
                current -= timedelta(days=1)
        else:
            current = self.start_date
            while current <= self.end_date:
                yield current
                current += timedelta(days=1)

    def date_necklace(
        self,
        completed_dates: set[date] | None = None,
    ) -> Generator[date, None, None]:
        """Yield dates split into two contiguous blocks anchored on historical boundaries.

        If completed_dates is provided and non-empty:
          - In descending order (reverse=True):
            1. Block 1 (Historical Backlog): Starts from oldest completed date (min)
               down to self.start_date, repeating the oldest date to ensure completeness.
            2. Block 2 (Recent Slice): Starts from self.end_date down to oldest + 1 day.
          - In ascending order (reverse=False):
            1. Block 1: Starts from newest completed date (max) up to self.end_date.
            2. Block 2: Starts from self.start_date up to (newest_completed - 1 day).
        Otherwise, falls back to the standard linear date_range().
        """
        if not completed_dates:
            yield from self.date_range()
            return

        if self.reverse:
            oldest_completed = min(completed_dates)

            # Block 1: From oldest_completed down to start_date
            current = min(oldest_completed, self.end_date)
            while current >= self.start_date:
                yield current
                current -= timedelta(days=1)

            # Block 2: From end_date down to (oldest_completed + 1 day)
            current = self.end_date
            while current > oldest_completed:
                yield current
                current -= timedelta(days=1)
        else:
            newest_completed = max(completed_dates)

            # Block 1: From newest_completed up to end_date
            current = max(newest_completed, self.start_date)
            while current <= self.end_date:
                yield current
                current += timedelta(days=1)

            # Block 2: From start_date up to (newest_completed - 1 day)
            current = self.start_date
            while current < newest_completed:
                yield current
                current += timedelta(days=1)

    def start_requests(self) -> Generator[Request, None, None]:
        """Generate starting requests (overridden by concrete spiders)."""
        yield from ()

    async def start(self) -> AsyncIterator[Request]:
        """Scrapy 2.18+ async start entrypoint bridging to start_requests generator."""
        for req in self.start_requests():
            yield req
