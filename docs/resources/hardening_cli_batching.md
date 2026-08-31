# CLI Batching & Keyset Pagination Hardening Guide (LEX)

This document establishes the batch iteration, pagination algorithms, and federative URN generation standards for the LEX CLI and extraction tools.

---

## 1. Keyset Cursor Pagination vs. Infinite Processing Loops

### Vulnerability Identified (VULN-03 - P0)
In `src/lex/cli.py`, the `run_treat` command queried batches of pending normative acts using `while True: chunk_stmt = stmt.limit(current_chunk_size)`.

When running in forced re-treatment mode (`--force`), the query filter did not exclude already-treated rows. Because there was no offset or pagination cursor, the query repeatedly retrieved the exact same first 500 rows over and over, hanging in an infinite loop consuming 100% CPU.

### Remediated Architecture (SOTA-KISS)
Implement **Keyset Cursor Pagination** ordered by primary key (`id`):

```python
last_seen_id: uuid.UUID | None = None

while True:
    chunk_stmt = stmt
    if last_seen_id is not None:
        chunk_stmt = chunk_stmt.where(NormativeActModel.id > last_seen_id)
    chunk_stmt = chunk_stmt.order_by(NormativeActModel.id.asc()).limit(current_chunk_size)

    models = session.scalars(chunk_stmt).all()
    if not models:
        break

    for m in models:
        last_seen_id = m.id
        ...
```

### Advantages of Keyset Pagination:
1. **Zero Repeated Rows**: Progress is guaranteed strictly forward regardless of `--force` or database updates during execution.
2. **$O(1)$ Index Traversal**: Uses the B-Tree primary key index directly without expensive SQL `OFFSET` scans.

---

## 2. Multi-Tier LexML URN Minting

### Vulnerability Identified (VULN-10 - P2)
The function `generate_canonical_urn` previously hardcoded `:federal:` in its formatting string (`f"urn:lex:{clean_territory}:federal:..."`). When state or municipal gazette spiders (such as São Paulo, Bahia, or Rio de Janeiro) ingested acts, they were minted with invalid federal identifiers.

### Remediated Architecture (SOTA-KISS)
Accept a `tier: str = "federal"` argument and normalize the federative tier to standard LexML hierarchy:
- `federal` $\rightarrow$ `federal`
- `state` / `estadual` $\rightarrow$ `estadual`
- `municipal` $\rightarrow$ `municipal`

```python
def generate_canonical_urn(
    territory_code: str,
    act_type: str,
    act_number: str | None,
    act_year: int | None,
    act_date: date,
    content_hash: str | None = None,
    tier: str = "federal",
) -> str:
    clean_tier = tier.strip().lower()
    if clean_tier in ("state", "estadual"):
        clean_tier = "estadual"
    elif clean_tier in ("municipal", "city"):
        clean_tier = "municipal"
    else:
        clean_tier = "federal"

    ...
    return f"urn:lex:{clean_territory}:{clean_tier}:{clean_type}:{act_year};{clean_num}"
```

---

## 3. ReDoS (Catastrophic Backtracking) Mitigation in Legislative Extraction (CWE-1333)

### Vulnerability Identified (VULN-06 - P2)
In `src/lex/treatment/domain/services/mutation_extractor.py`, the `RE_ALTERATION_HEADER` regex combined nested, overlapping quantifiers matching whitespace and word characters:
```python
# Vulnerable Pattern (overlapping \w\s with \s and optional groups)
r"(?:[,\s/]+(?:de\s+)?(?:[\w\s]+(?:de\s+)?)?(\d{4}))?,?\s+passa[m]?\s+a\s+vigorar..."
```
When encountering malformed or lengthy gazette text lines where the trailing match failed, the Python regex engine performed polynomial / exponential backtracking ($O(2^N)$), causing severe CPU starvation and worker hangs.

### Remediated Architecture (SOTA-KISS)
Replaced overlapping quantifiers with non-overlapping, deterministic tokens for date and year capture:

```python
# ReDoS-Safe Pattern (CWE-1333 Mitigation)
RE_ALTERATION_HEADER = re.compile(
    r"[Aa]rt\.\s*\d+[ºo]?\s+(?:[OoAa]s?\s+)?(Lei|Decreto|Medida\s+Provisória|Portaria|Resolução)"
    r"(?:\s+Complementar)?\s+(?:n[ºo°\.]?\s*)?([\d\.]+)"
    r"(?:[,\s/]+(?:de\s+)?(?:\d{1,2}\s+de\s+[A-Za-zçãéíóú]+\s+de\s+|[A-Za-zçãéíóú]+\s+de\s+)?(\d{4}))?"
    r",?\s+passa[m]?\s+a\s+vigorar\s*(?:com\s+a[s]?\s+seguinte[s]?\s+alteraç[ãõ]e[s]?)?:?",
    re.IGNORECASE,
)
```

### Invariants:
1. **Zero Overlapping Whitespace Quantifiers**: Character classes (`[A-Za-zçãéíóú]+`) do not match whitespace, ensuring strict boundary transitions.
2. **Linear Time Performance ($O(N)$)**: Matching terminates deterministically in sub-millisecond execution even on large adversarial inputs.

---

## 4. PostgreSQL Catalog Statistics Negative Value Handling

### Vulnerability Identified (VULN-11 - P2)
In `src/lex/cli.py` (`run_treat`), the CLI retrieves approximate pending act counts via `SELECT (reltuples::bigint) FROM pg_class WHERE relname = '...'`.

In PostgreSQL, freshly created tables or indexes that have not yet been vacuumed or analyzed return `reltuples = -1`. Passing negative values to `tqdm(total=total_acts)` resulted in corrupted progress displays and invalid batch total calculations.

### Remediated Architecture (SOTA-KISS)
Enforce positive integer bounds on catalog statistics queries, falling back gracefully to continuous stream mode (`total_acts = None`):

```python
try:
    est = session.execute(
        text(
            "SELECT (reltuples::bigint) FROM pg_class "
            "WHERE relname = 'ix_normative_acts_pending_treatment'"
        )
    ).scalar()
    if est is not None and est > 0:
        total_acts = int(est)
    else:
        total_acts = None
except Exception:
    total_acts = None
```

### Invariants:
1. **Strict Positive Threshold**: Only `est > 0` sets a finite progress bar total.
2. **Deterministic Stream Fallback**: Negative (`-1`), zero, or `None` values switch the CLI to unmetered continuous chunk streaming.
