"""São Paulo State Official Gazette Spider (DOE SP).

Crawls official gazette editions from Imprensa Oficial do Estado de São Paulo (IMESP / DOE SP).
"""

from lex.ingestion.infrastructure.scrapy_project.spiders.archetypes.rest_api import (
    RestApiGazetteSpider,
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class SpGazetteSpider(RestApiGazetteSpider):
    """Spider for São Paulo State Official Gazette."""

    name = "state_sp"
    territory_code = "SP"
    tier = "state"
    allowed_domains = ["doe.sp.gov.br", "imprensaoficial.com.br"]

    api_endpoint_template = "https://doe.sp.gov.br/api/v1/edicoes?data={iso_date}"
    json_pdf_url_key = "url_pdf"
    json_edition_key = "numero_edicao"
    json_section_key = "secao"
    json_is_extra_key = "suplementar"
