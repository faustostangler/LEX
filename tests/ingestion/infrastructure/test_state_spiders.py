"""Precision Unit Tests for Initial Tier-0 State Spiders.

Verifies declarative configuration, naming contracts, and territory assignments
for SP, RJ, MG, RS, BA, DF, and PR state spiders.
"""

from datetime import date

import pytest

from lex.ingestion.infrastructure.scrapy_project.spiders.state.ba import (
    BaGazetteSpider,
)
from lex.ingestion.infrastructure.scrapy_project.spiders.state.df import (
    DfGazetteSpider,
)
from lex.ingestion.infrastructure.scrapy_project.spiders.state.mg import (
    MgGazetteSpider,
)
from lex.ingestion.infrastructure.scrapy_project.spiders.state.pr import (
    PrGazetteSpider,
)
from lex.ingestion.infrastructure.scrapy_project.spiders.state.rj import (
    RjGazetteSpider,
)
from lex.ingestion.infrastructure.scrapy_project.spiders.state.rs import (
    RsGazetteSpider,
)
from lex.ingestion.infrastructure.scrapy_project.spiders.state.sp import (
    SpGazetteSpider,
)


@pytest.mark.parametrize(
    ("spider_cls", "expected_name", "expected_uf"),
    [
        (SpGazetteSpider, "state_sp", "SP"),
        (RjGazetteSpider, "state_rj", "RJ"),
        (MgGazetteSpider, "state_mg", "MG"),
        (RsGazetteSpider, "state_rs", "RS"),
        (BaGazetteSpider, "state_ba", "BA"),
        (DfGazetteSpider, "state_df", "DF"),
        (PrGazetteSpider, "state_pr", "PR"),
    ],
)
def test_state_spider_declarations(spider_cls: type, expected_name: str, expected_uf: str) -> None:
    """Scenario: State spiders declare canonical name, state tier, and valid UF code."""
    spider = spider_cls(start_date="2024-05-10", end_date="2024-05-10")
    assert spider.name == expected_name
    assert spider.territory_code == expected_uf
    assert spider.tier == "state"
    assert spider.start_date == date(2024, 5, 10)
    assert spider.end_date == date(2024, 5, 10)
