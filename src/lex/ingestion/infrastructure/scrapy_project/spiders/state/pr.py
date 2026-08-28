"""Paraná State Official Gazette Spider (DIOE PR).

Crawls official gazette editions from Departamento de Imprensa Oficial do Estado do Paraná (DIOE).
"""

from lex.ingestion.infrastructure.scrapy_project.spiders.archetypes.rest_api import (
    RestApiGazetteSpider,
)


class PrGazetteSpider(RestApiGazetteSpider):
    """Spider for Paraná State Official Gazette."""

    name = "state_pr"
    territory_code = "PR"
    tier = "state"
    allowed_domains = ["imprensaoficial.pr.gov.br", "dioe.pr.gov.br"]

    api_endpoint_template = "https://dioe.pr.gov.br/api/edicoes?data={iso_date}"
    json_pdf_url_key = "link_pdf"
    json_edition_key = "numero_edicao"
    json_section_key = "caderno"
    json_is_extra_key = "suplemento"
