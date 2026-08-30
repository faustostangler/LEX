"""Treatment and Digestion Bounded Context for LEX.

Performs Dual-Track legislative parsing (Trilha A: Deep AST & LC 95 Mutation Ledger)
and operational entity extraction (Trilha B: Fast-Path NER).
"""


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
