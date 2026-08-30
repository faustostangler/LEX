"""Bahia State Official Gazette Spider (DOE BA).

Crawls official gazette editions from Empresa Gráfica da Bahia (EGBA / DOE BA).
"""

from lex.ingestion.infrastructure.scrapy_project.spiders.archetypes.monthly_directory import (
    MonthlyDirectoryGazetteSpider,
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class BaGazetteSpider(MonthlyDirectoryGazetteSpider):
    """Spider for Bahia State Official Gazette."""

    name = "state_ba"
    territory_code = "BA"
    tier = "state"
    allowed_domains = ["egba.ba.gov.br", "diariooficial.ba.gov.br"]

    directory_url_template = (
        "https://diariooficial.ba.gov.br/consulta?ano={year}&mes={month:02d}&dia={day:02d}"
    )
    edition_link_xpath = "//a[contains(@href, '.pdf')]"
