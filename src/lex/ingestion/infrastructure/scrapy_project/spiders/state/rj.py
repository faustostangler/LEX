"""Rio de Janeiro State Official Gazette Spider (DOERJ).

Crawls official gazette editions from Imprensa Oficial do Estado do Rio de Janeiro.
"""

from lex.ingestion.infrastructure.scrapy_project.spiders.archetypes.monthly_directory import (
    MonthlyDirectoryGazetteSpider,
)


class RjGazetteSpider(MonthlyDirectoryGazetteSpider):
    """Spider for Rio de Janeiro State Official Gazette."""

    name = "state_rj"
    territory_code = "RJ"
    tier = "state"
    allowed_domains = ["doe.rj.gov.br", "imprensaoficial.rj.gov.br"]

    directory_url_template = (
        "https://doe.rj.gov.br/consulta?ano={year}&mes={month:02d}&dia={day:02d}"
    )
    edition_link_xpath = "//a[contains(@href, '.pdf')]"
