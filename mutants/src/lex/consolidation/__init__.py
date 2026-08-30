"""Consolidation Bounded Context for LEX.

Maintains the CQRS Out-of-Order Engine, Stub Entity Resolution,
Pure AST Reduction, and Pre-rendered Materialized Read Projections.
"""


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
