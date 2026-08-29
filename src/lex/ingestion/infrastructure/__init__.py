"""Infrastructure layer for the Ingestion Bounded Context."""

from .dto import RawGazettePayload, RawNormativeActPayload

__all__ = [
    "RawGazettePayload",
    "RawNormativeActPayload",
]
