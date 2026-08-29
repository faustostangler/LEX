"""Scrapy Settings for LEX Ingestion Engine.

Configures AutoThrottle, Decorrelated Jitter Retry Middleware, Domain Circuit Breakers,
and Ingestion Pipelines adhering to the Hexagonal Architecture and 12-Factor App standards.
"""

BOT_NAME = "lex_bot"

SPIDER_MODULES = [
    "lex.ingestion.infrastructure.scrapy_project.spiders.federal",
    # "lex.ingestion.infrastructure.scrapy_project.spiders.state",  # Refactor queue
]
NEWSPIDER_MODULE = "lex.ingestion.infrastructure.scrapy_project.spiders.federal"

# Realistic browser headers for Brazilian public portals & CDNs (Azion / Cloudflare)
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36 (LEX Legislation Ingestion Engine; +https://github.com/faustostangler/LEX)"
)

DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}

ROBOTSTXT_OBEY = False

# Default Concurrency & Latency Controls
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 4
DOWNLOAD_DELAY = 0.5

# AutoThrottle Downloader Middleware
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1.0
AUTOTHROTTLE_MAX_DELAY = 30.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0
AUTOTHROTTLE_DEBUG = False

# Middleware & Pipeline Module Paths
CB_MW = (
    "lex.ingestion.infrastructure.scrapy_project.middlewares."
    "circuit_breaker.DomainCircuitBreakerMiddleware"
)
JITTER_MW = (
    "lex.ingestion.infrastructure.scrapy_project.middlewares."
    "retry.DecorrelatedJitterRetryMiddleware"
)
INGESTION_PL = (
    "lex.ingestion.infrastructure.scrapy_project.pipelines."
    "ingestion_pipeline.GazetteIngestionPipeline"
)

# Network Resilience & Downloader Middlewares
DOWNLOADER_MIDDLEWARES = {
    CB_MW: 50,
    JITTER_MW: 550,
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
}

# Hexagonal Item Pipelines
ITEM_PIPELINES = {
    INGESTION_PL: 300,
}

# Circuit Breaker Defaults
CIRCUIT_BREAKER_FAILURE_THRESHOLD = 5
CIRCUIT_BREAKER_RESET_TIMEOUT = 60.0

# Decorrelated Jitter Retry Defaults
RETRY_MIN_DELAY = 1.0
RETRY_MAX_DELAY = 60.0
RETRY_TIMES = 3
RETRY_HTTP_CODES = [408, 429, 500, 502, 503, 504]

LOG_LEVEL = "DEBUG"  # "INFO" Silencia os logs DEBUG do Scrapy
