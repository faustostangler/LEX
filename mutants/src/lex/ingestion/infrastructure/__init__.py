"""Infrastructure layer for the Ingestion Bounded Context."""

from .dto import RawGazettePayload, RawNormativeActPayload

__all__ = [
    "RawGazettePayload",
    "RawNormativeActPayload",
]


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
