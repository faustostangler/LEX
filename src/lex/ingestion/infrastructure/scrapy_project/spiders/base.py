"""Base Gazette Spider for Brazilian Ingestion Architecture.

Establishes common date range iteration, parameter parsing, and metadata contracts
for all federal, state, and municipal spiders.
"""

from collections.abc import Generator
from datetime import date, datetime, timedelta
from typing import Any

import scrapy


class BaseGazetteSpider(scrapy.Spider):
    """Abstract baseline spider providing uniform date range generators."""

    territory_code: str
    tier: str
    start_date: date
    end_date: date

    def __init__(
        self,
        start_date: str | date | None = None,
        end_date: str | date | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)

        today = date.today()
        self.start_date = self._parse_date_param(start_date) or today
        self.end_date = self._parse_date_param(end_date) or today

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
        """Yield each date in the inclusive [start_date, end_date] interval."""
        current = self.start_date
        while current <= self.end_date:
            yield current
            current += timedelta(days=1)
