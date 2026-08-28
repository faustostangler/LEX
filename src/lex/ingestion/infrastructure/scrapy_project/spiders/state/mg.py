"""Minas Gerais State Official Gazette Spider (IOF MG).

Crawls official gazette editions from Imprensa Oficial do Estado de Minas Gerais.
"""

from lex.ingestion.infrastructure.scrapy_project.spiders.archetypes.aspx_viewer import (
    AspxViewerGazetteSpider,
)


class MgGazetteSpider(AspxViewerGazetteSpider):
    """Spider for Minas Gerais State Official Gazette."""

    name = "state_mg"
    territory_code = "MG"
    tier = "state"
    allowed_domains = ["iof.mg.gov.br", "jornal.iof.mg.gov.br"]

    form_url = "https://jornal.iof.mg.gov.br/Default.aspx"
    pdf_link_xpath = "//a[contains(@href, '.pdf') or contains(@href, 'Download')]"
