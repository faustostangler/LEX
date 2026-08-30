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


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁBaseGazetteSpiderǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁBaseGazetteSpiderǁ_parse_date_param__mutmut: MutantDict = {}  # type: ignore
mutants_xǁBaseGazetteSpiderǁdate_range__mutmut: MutantDict = {}  # type: ignore


class BaseGazetteSpider(scrapy.Spider):
    """Abstract baseline spider providing uniform date range generators."""

    territory_code: str
    tier: str
    start_date: date
    end_date: date
    reverse: bool

    @_mutmut_mutated(mutants_xǁBaseGazetteSpiderǁ__init____mutmut)
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

    def xǁBaseGazetteSpiderǁ__init____mutmut_orig(
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

    def xǁBaseGazetteSpiderǁ__init____mutmut_1(
        self,
        start_date: str | date | None = None,
        end_date: str | date | None = None,
        reverse: bool | str = False,
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

    def xǁBaseGazetteSpiderǁ__init____mutmut_2(
        self,
        start_date: str | date | None = None,
        end_date: str | date | None = None,
        reverse: bool | str = True,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

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

    def xǁBaseGazetteSpiderǁ__init____mutmut_3(
        self,
        start_date: str | date | None = None,
        end_date: str | date | None = None,
        reverse: bool | str = True,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, )

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

    def xǁBaseGazetteSpiderǁ__init____mutmut_4(
        self,
        start_date: str | date | None = None,
        end_date: str | date | None = None,
        reverse: bool | str = True,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)

        today = None
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

    def xǁBaseGazetteSpiderǁ__init____mutmut_5(
        self,
        start_date: str | date | None = None,
        end_date: str | date | None = None,
        reverse: bool | str = True,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)

        today = date.today()
        parsed_start = None
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

    def xǁBaseGazetteSpiderǁ__init____mutmut_6(
        self,
        start_date: str | date | None = None,
        end_date: str | date | None = None,
        reverse: bool | str = True,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)

        today = date.today()
        parsed_start = self._parse_date_param(None)
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

    def xǁBaseGazetteSpiderǁ__init____mutmut_7(
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
        parsed_end = None

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

    def xǁBaseGazetteSpiderǁ__init____mutmut_8(
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
        parsed_end = self._parse_date_param(None)

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

    def xǁBaseGazetteSpiderǁ__init____mutmut_9(
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

        if parsed_start is not None or parsed_end is None:
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

    def xǁBaseGazetteSpiderǁ__init____mutmut_10(
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

        if parsed_start is None and parsed_end is None:
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

    def xǁBaseGazetteSpiderǁ__init____mutmut_11(
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

        if parsed_start is not None and parsed_end is not None:
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

    def xǁBaseGazetteSpiderǁ__init____mutmut_12(
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
            self.start_date = None
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

    def xǁBaseGazetteSpiderǁ__init____mutmut_13(
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
            self.end_date = None
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

    def xǁBaseGazetteSpiderǁ__init____mutmut_14(
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
        elif parsed_start is None or parsed_end is not None:
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

    def xǁBaseGazetteSpiderǁ__init____mutmut_15(
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
        elif parsed_start is not None and parsed_end is not None:
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

    def xǁBaseGazetteSpiderǁ__init____mutmut_16(
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
        elif parsed_start is None and parsed_end is None:
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

    def xǁBaseGazetteSpiderǁ__init____mutmut_17(
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
            self.start_date = None
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

    def xǁBaseGazetteSpiderǁ__init____mutmut_18(
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
            self.end_date = None
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

    def xǁBaseGazetteSpiderǁ__init____mutmut_19(
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
        elif parsed_start is not None or parsed_end is not None:
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

    def xǁBaseGazetteSpiderǁ__init____mutmut_20(
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
        elif parsed_start is None and parsed_end is not None:
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

    def xǁBaseGazetteSpiderǁ__init____mutmut_21(
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
        elif parsed_start is not None and parsed_end is None:
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

    def xǁBaseGazetteSpiderǁ__init____mutmut_22(
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
            self.start_date = None
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

    def xǁBaseGazetteSpiderǁ__init____mutmut_23(
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
            self.end_date = None
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

    def xǁBaseGazetteSpiderǁ__init____mutmut_24(
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
            self.start_date = None
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

    def xǁBaseGazetteSpiderǁ__init____mutmut_25(
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
            self.end_date = None

        self.reverse = (
            (str(reverse).lower() in ("true", "1", "yes"))
            if isinstance(reverse, str)
            else bool(reverse)
        )

        if self.start_date > self.end_date:
            raise ValueError(
                f"start_date ({self.start_date}) cannot be after end_date ({self.end_date})"
            )

    def xǁBaseGazetteSpiderǁ__init____mutmut_26(
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

        self.reverse = None

        if self.start_date > self.end_date:
            raise ValueError(
                f"start_date ({self.start_date}) cannot be after end_date ({self.end_date})"
            )

    def xǁBaseGazetteSpiderǁ__init____mutmut_27(
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
            (str(reverse).upper() in ("true", "1", "yes"))
            if isinstance(reverse, str)
            else bool(reverse)
        )

        if self.start_date > self.end_date:
            raise ValueError(
                f"start_date ({self.start_date}) cannot be after end_date ({self.end_date})"
            )

    def xǁBaseGazetteSpiderǁ__init____mutmut_28(
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
            (str(None).lower() in ("true", "1", "yes"))
            if isinstance(reverse, str)
            else bool(reverse)
        )

        if self.start_date > self.end_date:
            raise ValueError(
                f"start_date ({self.start_date}) cannot be after end_date ({self.end_date})"
            )

    def xǁBaseGazetteSpiderǁ__init____mutmut_29(
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
            (str(reverse).lower() not in ("true", "1", "yes"))
            if isinstance(reverse, str)
            else bool(reverse)
        )

        if self.start_date > self.end_date:
            raise ValueError(
                f"start_date ({self.start_date}) cannot be after end_date ({self.end_date})"
            )

    def xǁBaseGazetteSpiderǁ__init____mutmut_30(
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
            (str(reverse).lower() in ("XXtrueXX", "1", "yes"))
            if isinstance(reverse, str)
            else bool(reverse)
        )

        if self.start_date > self.end_date:
            raise ValueError(
                f"start_date ({self.start_date}) cannot be after end_date ({self.end_date})"
            )

    def xǁBaseGazetteSpiderǁ__init____mutmut_31(
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
            (str(reverse).lower() in ("TRUE", "1", "yes"))
            if isinstance(reverse, str)
            else bool(reverse)
        )

        if self.start_date > self.end_date:
            raise ValueError(
                f"start_date ({self.start_date}) cannot be after end_date ({self.end_date})"
            )

    def xǁBaseGazetteSpiderǁ__init____mutmut_32(
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
            (str(reverse).lower() in ("true", "XX1XX", "yes"))
            if isinstance(reverse, str)
            else bool(reverse)
        )

        if self.start_date > self.end_date:
            raise ValueError(
                f"start_date ({self.start_date}) cannot be after end_date ({self.end_date})"
            )

    def xǁBaseGazetteSpiderǁ__init____mutmut_33(
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
            (str(reverse).lower() in ("true", "1", "XXyesXX"))
            if isinstance(reverse, str)
            else bool(reverse)
        )

        if self.start_date > self.end_date:
            raise ValueError(
                f"start_date ({self.start_date}) cannot be after end_date ({self.end_date})"
            )

    def xǁBaseGazetteSpiderǁ__init____mutmut_34(
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
            (str(reverse).lower() in ("true", "1", "YES"))
            if isinstance(reverse, str)
            else bool(reverse)
        )

        if self.start_date > self.end_date:
            raise ValueError(
                f"start_date ({self.start_date}) cannot be after end_date ({self.end_date})"
            )

    def xǁBaseGazetteSpiderǁ__init____mutmut_35(
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
            else bool(None)
        )

        if self.start_date > self.end_date:
            raise ValueError(
                f"start_date ({self.start_date}) cannot be after end_date ({self.end_date})"
            )

    def xǁBaseGazetteSpiderǁ__init____mutmut_36(
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

        if self.start_date >= self.end_date:
            raise ValueError(
                f"start_date ({self.start_date}) cannot be after end_date ({self.end_date})"
            )

    def xǁBaseGazetteSpiderǁ__init____mutmut_37(
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
                None
            )

    @staticmethod
    @_mutmut_mutated(mutants_xǁBaseGazetteSpiderǁ_parse_date_param__mutmut)
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

    @staticmethod
    def xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_orig(param: str | date | None) -> date | None:
        """Parse incoming CLI/Runner date parameter."""
        if param is None or isinstance(param, date):
            return param

        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(param, fmt).date()
            except ValueError:
                continue

        raise ValueError(f"Invalid date parameter format: '{param}'")

    @staticmethod
    def xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_1(param: str | date | None) -> date | None:
        """Parse incoming CLI/Runner date parameter."""
        if param is None and isinstance(param, date):
            return param

        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(param, fmt).date()
            except ValueError:
                continue

        raise ValueError(f"Invalid date parameter format: '{param}'")

    @staticmethod
    def xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_2(param: str | date | None) -> date | None:
        """Parse incoming CLI/Runner date parameter."""
        if param is not None or isinstance(param, date):
            return param

        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(param, fmt).date()
            except ValueError:
                continue

        raise ValueError(f"Invalid date parameter format: '{param}'")

    @staticmethod
    def xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_3(param: str | date | None) -> date | None:
        """Parse incoming CLI/Runner date parameter."""
        if param is None or isinstance(param, date):
            return param

        for fmt in ("XX%Y-%m-%dXX", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(param, fmt).date()
            except ValueError:
                continue

        raise ValueError(f"Invalid date parameter format: '{param}'")

    @staticmethod
    def xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_4(param: str | date | None) -> date | None:
        """Parse incoming CLI/Runner date parameter."""
        if param is None or isinstance(param, date):
            return param

        for fmt in ("%y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(param, fmt).date()
            except ValueError:
                continue

        raise ValueError(f"Invalid date parameter format: '{param}'")

    @staticmethod
    def xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_5(param: str | date | None) -> date | None:
        """Parse incoming CLI/Runner date parameter."""
        if param is None or isinstance(param, date):
            return param

        for fmt in ("%Y-%M-%D", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(param, fmt).date()
            except ValueError:
                continue

        raise ValueError(f"Invalid date parameter format: '{param}'")

    @staticmethod
    def xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_6(param: str | date | None) -> date | None:
        """Parse incoming CLI/Runner date parameter."""
        if param is None or isinstance(param, date):
            return param

        for fmt in ("%Y-%m-%d", "XX%d/%m/%YXX", "%d-%m-%Y"):
            try:
                return datetime.strptime(param, fmt).date()
            except ValueError:
                continue

        raise ValueError(f"Invalid date parameter format: '{param}'")

    @staticmethod
    def xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_7(param: str | date | None) -> date | None:
        """Parse incoming CLI/Runner date parameter."""
        if param is None or isinstance(param, date):
            return param

        for fmt in ("%Y-%m-%d", "%d/%m/%y", "%d-%m-%Y"):
            try:
                return datetime.strptime(param, fmt).date()
            except ValueError:
                continue

        raise ValueError(f"Invalid date parameter format: '{param}'")

    @staticmethod
    def xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_8(param: str | date | None) -> date | None:
        """Parse incoming CLI/Runner date parameter."""
        if param is None or isinstance(param, date):
            return param

        for fmt in ("%Y-%m-%d", "%D/%M/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(param, fmt).date()
            except ValueError:
                continue

        raise ValueError(f"Invalid date parameter format: '{param}'")

    @staticmethod
    def xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_9(param: str | date | None) -> date | None:
        """Parse incoming CLI/Runner date parameter."""
        if param is None or isinstance(param, date):
            return param

        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "XX%d-%m-%YXX"):
            try:
                return datetime.strptime(param, fmt).date()
            except ValueError:
                continue

        raise ValueError(f"Invalid date parameter format: '{param}'")

    @staticmethod
    def xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_10(param: str | date | None) -> date | None:
        """Parse incoming CLI/Runner date parameter."""
        if param is None or isinstance(param, date):
            return param

        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%y"):
            try:
                return datetime.strptime(param, fmt).date()
            except ValueError:
                continue

        raise ValueError(f"Invalid date parameter format: '{param}'")

    @staticmethod
    def xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_11(param: str | date | None) -> date | None:
        """Parse incoming CLI/Runner date parameter."""
        if param is None or isinstance(param, date):
            return param

        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%D-%M-%Y"):
            try:
                return datetime.strptime(param, fmt).date()
            except ValueError:
                continue

        raise ValueError(f"Invalid date parameter format: '{param}'")

    @staticmethod
    def xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_12(param: str | date | None) -> date | None:
        """Parse incoming CLI/Runner date parameter."""
        if param is None or isinstance(param, date):
            return param

        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(None, fmt).date()
            except ValueError:
                continue

        raise ValueError(f"Invalid date parameter format: '{param}'")

    @staticmethod
    def xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_13(param: str | date | None) -> date | None:
        """Parse incoming CLI/Runner date parameter."""
        if param is None or isinstance(param, date):
            return param

        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(param, None).date()
            except ValueError:
                continue

        raise ValueError(f"Invalid date parameter format: '{param}'")

    @staticmethod
    def xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_14(param: str | date | None) -> date | None:
        """Parse incoming CLI/Runner date parameter."""
        if param is None or isinstance(param, date):
            return param

        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(fmt).date()
            except ValueError:
                continue

        raise ValueError(f"Invalid date parameter format: '{param}'")

    @staticmethod
    def xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_15(param: str | date | None) -> date | None:
        """Parse incoming CLI/Runner date parameter."""
        if param is None or isinstance(param, date):
            return param

        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(param, ).date()
            except ValueError:
                continue

        raise ValueError(f"Invalid date parameter format: '{param}'")

    @staticmethod
    def xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_16(param: str | date | None) -> date | None:
        """Parse incoming CLI/Runner date parameter."""
        if param is None or isinstance(param, date):
            return param

        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(param, fmt).date()
            except ValueError:
                break

        raise ValueError(f"Invalid date parameter format: '{param}'")

    @staticmethod
    def xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_17(param: str | date | None) -> date | None:
        """Parse incoming CLI/Runner date parameter."""
        if param is None or isinstance(param, date):
            return param

        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(param, fmt).date()
            except ValueError:
                continue

        raise ValueError(None)

    @_mutmut_mutated(mutants_xǁBaseGazetteSpiderǁdate_range__mutmut)
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

    def xǁBaseGazetteSpiderǁdate_range__mutmut_orig(self) -> Generator[date, None, None]:
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

    def xǁBaseGazetteSpiderǁdate_range__mutmut_1(self) -> Generator[date, None, None]:
        """Yield each date in the inclusive [start_date, end_date] interval.

        By default (reverse=True), yields in descending chronological order
        (from the most recent date down to the oldest date).
        """
        if self.reverse:
            current = None
            while current >= self.start_date:
                yield current
                current -= timedelta(days=1)
        else:
            current = self.start_date
            while current <= self.end_date:
                yield current
                current += timedelta(days=1)

    def xǁBaseGazetteSpiderǁdate_range__mutmut_2(self) -> Generator[date, None, None]:
        """Yield each date in the inclusive [start_date, end_date] interval.

        By default (reverse=True), yields in descending chronological order
        (from the most recent date down to the oldest date).
        """
        if self.reverse:
            current = self.end_date
            while current > self.start_date:
                yield current
                current -= timedelta(days=1)
        else:
            current = self.start_date
            while current <= self.end_date:
                yield current
                current += timedelta(days=1)

    def xǁBaseGazetteSpiderǁdate_range__mutmut_3(self) -> Generator[date, None, None]:
        """Yield each date in the inclusive [start_date, end_date] interval.

        By default (reverse=True), yields in descending chronological order
        (from the most recent date down to the oldest date).
        """
        if self.reverse:
            current = self.end_date
            while current >= self.start_date:
                yield current
                current = timedelta(days=1)
        else:
            current = self.start_date
            while current <= self.end_date:
                yield current
                current += timedelta(days=1)

    def xǁBaseGazetteSpiderǁdate_range__mutmut_4(self) -> Generator[date, None, None]:
        """Yield each date in the inclusive [start_date, end_date] interval.

        By default (reverse=True), yields in descending chronological order
        (from the most recent date down to the oldest date).
        """
        if self.reverse:
            current = self.end_date
            while current >= self.start_date:
                yield current
                current += timedelta(days=1)
        else:
            current = self.start_date
            while current <= self.end_date:
                yield current
                current += timedelta(days=1)

    def xǁBaseGazetteSpiderǁdate_range__mutmut_5(self) -> Generator[date, None, None]:
        """Yield each date in the inclusive [start_date, end_date] interval.

        By default (reverse=True), yields in descending chronological order
        (from the most recent date down to the oldest date).
        """
        if self.reverse:
            current = self.end_date
            while current >= self.start_date:
                yield current
                current -= timedelta(days=None)
        else:
            current = self.start_date
            while current <= self.end_date:
                yield current
                current += timedelta(days=1)

    def xǁBaseGazetteSpiderǁdate_range__mutmut_6(self) -> Generator[date, None, None]:
        """Yield each date in the inclusive [start_date, end_date] interval.

        By default (reverse=True), yields in descending chronological order
        (from the most recent date down to the oldest date).
        """
        if self.reverse:
            current = self.end_date
            while current >= self.start_date:
                yield current
                current -= timedelta(days=2)
        else:
            current = self.start_date
            while current <= self.end_date:
                yield current
                current += timedelta(days=1)

    def xǁBaseGazetteSpiderǁdate_range__mutmut_7(self) -> Generator[date, None, None]:
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
            current = None
            while current <= self.end_date:
                yield current
                current += timedelta(days=1)

    def xǁBaseGazetteSpiderǁdate_range__mutmut_8(self) -> Generator[date, None, None]:
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
            while current < self.end_date:
                yield current
                current += timedelta(days=1)

    def xǁBaseGazetteSpiderǁdate_range__mutmut_9(self) -> Generator[date, None, None]:
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
                current = timedelta(days=1)

    def xǁBaseGazetteSpiderǁdate_range__mutmut_10(self) -> Generator[date, None, None]:
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
                current -= timedelta(days=1)

    def xǁBaseGazetteSpiderǁdate_range__mutmut_11(self) -> Generator[date, None, None]:
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
                current += timedelta(days=None)

    def xǁBaseGazetteSpiderǁdate_range__mutmut_12(self) -> Generator[date, None, None]:
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
                current += timedelta(days=2)

    def start_requests(self) -> Generator[Request, None, None]:
        """Generate starting requests (overridden by concrete spiders)."""
        yield from ()

    async def start(self) -> AsyncIterator[Request]:
        """Scrapy 2.18+ async start entrypoint bridging to start_requests generator."""
        for req in self.start_requests():
            yield req

mutants_xǁBaseGazetteSpiderǁ__init____mutmut['_mutmut_orig'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_1'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_2'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_3'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_3 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_4'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_4 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_5'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_5 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_6'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_6 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_7'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_7 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_8'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_8 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_9'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_9 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_10'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_10 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_11'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_11 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_12'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_12 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_13'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_13 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_14'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_14 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_15'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_15 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_16'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_16 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_17'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_17 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_18'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_18 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_19'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_19 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_20'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_20 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_21'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_21 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_22'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_22 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_23'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_23 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_24'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_24 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_25'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_25 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_26'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_26 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_27'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_27 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_28'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_28 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_29'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_29 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_30'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_30 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_31'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_31 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_32'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_32 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_33'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_33 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_34'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_34 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_35'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_35 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_36'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_36 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ__init____mutmut['xǁBaseGazetteSpiderǁ__init____mutmut_37'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ__init____mutmut_37 # type: ignore # mutmut generated

mutants_xǁBaseGazetteSpiderǁ_parse_date_param__mutmut['_mutmut_orig'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_orig # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ_parse_date_param__mutmut['xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_1'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_1 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ_parse_date_param__mutmut['xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_2'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_2 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ_parse_date_param__mutmut['xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_3'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_3 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ_parse_date_param__mutmut['xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_4'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_4 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ_parse_date_param__mutmut['xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_5'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_5 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ_parse_date_param__mutmut['xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_6'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_6 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ_parse_date_param__mutmut['xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_7'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_7 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ_parse_date_param__mutmut['xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_8'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_8 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ_parse_date_param__mutmut['xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_9'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_9 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ_parse_date_param__mutmut['xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_10'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_10 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ_parse_date_param__mutmut['xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_11'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_11 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ_parse_date_param__mutmut['xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_12'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_12 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ_parse_date_param__mutmut['xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_13'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_13 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ_parse_date_param__mutmut['xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_14'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_14 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ_parse_date_param__mutmut['xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_15'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_15 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ_parse_date_param__mutmut['xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_16'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_16 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁ_parse_date_param__mutmut['xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_17'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁ_parse_date_param__mutmut_17 # type: ignore # mutmut generated

mutants_xǁBaseGazetteSpiderǁdate_range__mutmut['_mutmut_orig'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁdate_range__mutmut_orig # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁdate_range__mutmut['xǁBaseGazetteSpiderǁdate_range__mutmut_1'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁdate_range__mutmut_1 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁdate_range__mutmut['xǁBaseGazetteSpiderǁdate_range__mutmut_2'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁdate_range__mutmut_2 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁdate_range__mutmut['xǁBaseGazetteSpiderǁdate_range__mutmut_3'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁdate_range__mutmut_3 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁdate_range__mutmut['xǁBaseGazetteSpiderǁdate_range__mutmut_4'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁdate_range__mutmut_4 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁdate_range__mutmut['xǁBaseGazetteSpiderǁdate_range__mutmut_5'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁdate_range__mutmut_5 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁdate_range__mutmut['xǁBaseGazetteSpiderǁdate_range__mutmut_6'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁdate_range__mutmut_6 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁdate_range__mutmut['xǁBaseGazetteSpiderǁdate_range__mutmut_7'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁdate_range__mutmut_7 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁdate_range__mutmut['xǁBaseGazetteSpiderǁdate_range__mutmut_8'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁdate_range__mutmut_8 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁdate_range__mutmut['xǁBaseGazetteSpiderǁdate_range__mutmut_9'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁdate_range__mutmut_9 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁdate_range__mutmut['xǁBaseGazetteSpiderǁdate_range__mutmut_10'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁdate_range__mutmut_10 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁdate_range__mutmut['xǁBaseGazetteSpiderǁdate_range__mutmut_11'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁdate_range__mutmut_11 # type: ignore # mutmut generated
mutants_xǁBaseGazetteSpiderǁdate_range__mutmut['xǁBaseGazetteSpiderǁdate_range__mutmut_12'] = BaseGazetteSpider.xǁBaseGazetteSpiderǁdate_range__mutmut_12 # type: ignore # mutmut generated
