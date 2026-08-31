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
