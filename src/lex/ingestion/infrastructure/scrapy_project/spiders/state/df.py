"""Distrito Federal Official Gazette Spider (DODF).

Crawls official gazette editions from Imprensa Oficial do Distrito Federal (DODF).
"""

from lex.ingestion.infrastructure.scrapy_project.spiders.archetypes.aspx_viewer import (
    AspxViewerGazetteSpider,
)


class DfGazetteSpider(AspxViewerGazetteSpider):
    """Spider for Distrito Federal Official Gazette."""

    name = "state_df"
    territory_code = "DF"
    tier = "state"
    allowed_domains = ["dodf.df.gov.br", "imprensa.df.gov.br"]

    form_url = "https://dodf.df.gov.br/diario/consulta"
    pdf_link_xpath = "//a[contains(@href, '.pdf')]"
