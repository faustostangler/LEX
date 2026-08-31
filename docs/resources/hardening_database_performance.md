# Database & Persistence Hardening Guide (LEX)

This document specifies the database query optimizations, JSONB indexing rules, and transaction safety guarantees across PostgreSQL 16 persistence adapters.

---

## 1. Native JSONB Filtering vs. Unbounded Full-Table Scans

### Vulnerability Identified (VULN-05 - P1)
The method `get_compiled_act_by_urn` previously executed:
```python
# ❌ Antipattern: Loading entire dataset into RAM
stmt = select(CompiledNormativeActModel)
rows = self._session.scalars(stmt).all()
for r in rows:
    if r.compiled_ast.get("canonical_urn") == canonical_urn:
        ...
```
With 100,000 compiled statutes (averaging 50KB-500KB of AST/HTML payload each), this operation required loading 5GB-50GB of raw text into Python heap memory on every single URN lookup, causing immediate OOM crashes.

### Remediated Architecture (SOTA-KISS)
Leverage PostgreSQL 16 native JSONB path operators (`->>` / `.astext`) with GIN indexing:

```python
# ✅ SOTA-KISS: Push down filter directly to PostgreSQL engine
stmt = select(CompiledNormativeActModel).where(
    CompiledNormativeActModel.compiled_ast["canonical_urn"].astext == canonical_urn
)
row = self._session.scalars(stmt).first()
```

### Invariants:
- All queries filtering on metadata or AST properties must push expressions down to the SQL engine.
- RAM usage remains constant $O(1)$ regardless of table size.

---

## 2. Transaction Rollback Safety & Session Poisoning Prevention

### Vulnerability Identified (VULN-09 - P2)
In `PostgresTreatmentRepository`, methods called `self._session.commit()` without catching database exceptions and triggering `self._session.rollback()`. When an `IntegrityError` or network timeout occurred, the `Session` entered a *poisoned/dirty* state, causing subsequent operations on that same session to fail with `PendingRollbackError`.

### Remediated Architecture (SOTA-KISS)
All write operations in persistence adapters must wrap commits in explicit rollback blocks:

```python
try:
    for m in mutations:
        self._session.add(...)
    self._session.commit()
except Exception:
    self._session.rollback()
    raise
```
