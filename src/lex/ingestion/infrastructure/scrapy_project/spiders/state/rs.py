"""Rio Grande do Sul State Official Gazette Spider (DOE RS).

Crawls official gazette editions from Imprensa Oficial do Estado do RS (CORAG / DOE RS).
"""

from lex.ingestion.infrastructure.scrapy_project.spiders.archetypes.rest_api import (
    RestApiGazetteSpider,
)


class RsGazetteSpider(RestApiGazetteSpider):
    """Spider for Rio Grande do Sul State Official Gazette."""

    name = "state_rs"
    territory_code = "RS"
    tier = "state"
    allowed_domains = ["corag.rs.gov.br", "doe.rs.gov.br"]

    api_endpoint_template = "https://doe.rs.gov.br/api/v1/diarios?data={iso_date}"
    json_pdf_url_key = "pdf_url"
    json_edition_key = "numero"
    json_section_key = "caderno"
    json_is_extra_key = "extra"
