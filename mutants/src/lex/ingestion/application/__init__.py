"""Ingestion Bounded Context Application Layer (Ports and Use Cases)."""

from .ports import GazetteRepositoryPort

__all__ = ["GazetteRepositoryPort"]


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
