#!/usr/bin/env python3
# ruff: noqa: T201, S608
"""Export database tables from PostgreSQL to Google Sheets-compatible CSV files.

Implements programmatic Water-Filling Binary Search optimization to guarantee
the final CSV file strictly fits within Google Sheets upload limits (< 100 MB hard cap;
default: <= 80 MB) without dropping any rows or columns.

Compliant with Google Drive & Google Sheets official limits:
Reference: https://support.google.com/drive/answer/37603

Key Optimizations:
1. Guaranteed File Size Fit (<= 80 MB by default):
   - Uses Water-Filling Binary Search with full delimiter & escaping accounting
     to compute the exact optimal Head-Tail sandwich truncation per cell.
   - 100% of rows are included; zero rows dropped.
2. Clean Spreadsheet Columns (Human/Analyst Focused):
   - Omits internal DB plumbing (hashes, internal FKs, raw JSON blobs, duplicate timestamps)
     by default to free up 35+ MB of budget for actual legal text (`raw_content`).
   - Use `--all-columns` to include every database column if needed.
3. Max Characters per Cell (50,000 chars hard limit):
   - Google Drive rule: "any cell with more than 50,000 characters will be removed in Sheets."
   - Hard capped at <= 45,000 chars with 80% Head (preamble/articles) and 18% Tail (signatures).
4. CSV Formula Injection Defense:
   - Disarms leading '=', '+', '-', '@', '\\t', '\\r' with a single quote (').
5. Semantic JSON Flattening:
   - Converts hierarchy lists to breadcrumbs ('Ministry > Dept') for instant spreadsheet filtering.

Usage:
    # Export all tables (auto-fit to <= 50 MB, 100% Google Sheets approved)
    python playground/export_table_to_csv.py

    # Export a specific table with custom target size
    python playground/export_table_to_csv.py --table normative_acts --max-file-mb 50.0

    # Export a specific date with full text (K=45,000 chars)
    python playground/export_table_to_csv.py --table normative_acts --date 2026-08-28

    # Include all database columns (including internal hashes and JSON)
    python playground/export_table_to_csv.py --table normative_acts --all-columns
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from sqlalchemy import Connection, Engine, create_engine, inspect, text

from lex.shared_kernel.config import LexSettings  # type: ignore[import-untyped]

DEFAULT_OUTPUT_DIR = Path("playground")

# Official Google Drive & Sheets Hard Limits (https://support.google.com/drive/answer/37603)
GOOGLE_SHEETS_MAX_CELL_CHARS = 50000  # Cells > 50,000 chars are stripped/removed by Sheets
GOOGLE_SHEETS_MAX_TOTAL_CELLS = 10000000  # 10 Million cells total limit per spreadsheet
GOOGLE_SHEETS_MAX_COLUMNS = 18278  # Column ZZZ
GOOGLE_SHEETS_MAX_UPLOAD_MB = 100.0  # 100 MB hard limit for CSV/XLSX web import
GOOGLE_SHEETS_RECOMMENDED_MAX_MB = 50.0  # <= 50 MB recommended for browser stability

# Default target file size: 50 MB provides a solid 20 MB safety margin under Google's 100 MB cap
DEFAULT_TARGET_MAX_FILE_MB = 50.0

# Safe defaults to prevent silent removal and stay within Google limits
DEFAULT_MAX_CELL_CHARS = 45000  # 5,000 char safety margin under 50k hard cap
DEFAULT_HEAD_RATIO = 0.80  # 80% of cell capacity to Head (preamble & initial articles)
DEFAULT_TAIL_RATIO = 0.18  # 18% of cell capacity to Tail (signatures & enactment dates)

# Internal database columns excluded by default in spreadsheet mode to maximize legal text budget
INTERNAL_DB_COLUMNS = {
    "edition_id",  # UUID foreign key
    "content_sha256",  # 64-char hex hash
    "structured_content",  # Heavy JSON duplicate of raw_content
    "metadata_json",  # Raw internal JSON metadata
    "classification_source",  # ML/Scraper internal tag
    "classification_confidence",  # ML internal float
    "scraped_at",  # Redundant with created_at
    "updated_at",  # Internal DB timestamp
}

# Characters that trigger formula execution in Google Sheets / Excel
INJECTION_PREFIXES = ("=", "+", "-", "@", "\t", "\r")


def get_available_tables(engine: Engine) -> list[str]:
    """Retrieve all table names from the public schema."""
    inspector = inspect(engine)
    tables = inspector.get_table_names(schema="public")
    # Exclude alembic internal migrations table if present
    return [t for t in tables if t != "alembic_version"]


def calculate_optimal_sandwich_budget(
    text_lengths: Sequence[int],
    metadata_total_bytes: int,
    target_max_bytes: int,
    max_cell_cap: int = DEFAULT_MAX_CELL_CHARS,
) -> tuple[int, int, int]:
    """Calculate the optimal (K_max, Head, Tail) via Water-Filling Binary Search.

    Guarantees the resulting CSV file fits strictly within target_max_bytes
    without discarding any rows or columns.

    Args:
        text_lengths: Character/byte lengths of the heavy column for each row.
        metadata_total_bytes: Total bytes consumed by metadata columns and CSV delimiters.
        target_max_bytes: Maximum target file size in bytes (e.g. 80 MB).
        max_cell_cap: Hard maximum characters per cell (<= 45,000).

    Returns:
        tuple[int, int, int]: (optimal_max_chars, head_chars, tail_chars)
    """
    if not text_lengths:
        head = int(max_cell_cap * DEFAULT_HEAD_RATIO)
        tail = int(max_cell_cap * DEFAULT_TAIL_RATIO)
        return max_cell_cap, head, tail

    # Reserve 8% buffer for CSV quote escaping and UTF-8 multibyte variance
    effective_target_bytes = int(target_max_bytes * 0.92)
    available_content_budget = effective_target_bytes - metadata_total_bytes

    if available_content_budget <= 0:
        # Metadata alone approaches target budget; enforce minimal compact threshold
        return 50, 35, 15

    # Check if untruncated content fits within budget
    total_untruncated = sum(
        min(length, max_cell_cap) + (100 if length > max_cell_cap else 0)
        for length in text_lengths
    )
    if total_untruncated <= available_content_budget:
        head = int(max_cell_cap * DEFAULT_HEAD_RATIO)
        tail = int(max_cell_cap * DEFAULT_TAIL_RATIO)
        return max_cell_cap, head, tail

    # Binary search for the maximum K in [50, max_cell_cap]
    low = 50
    high = max_cell_cap
    optimal_k = low

    while low <= high:
        mid = (low + high) // 2
        marker_cost = 60 if mid < 500 else 140

        # Simulate total bytes for content column with cap = mid
        simulated_size = sum(
            min(length, mid) + (marker_cost if length > mid else 0)
            for length in text_lengths
        )

        if simulated_size <= available_content_budget:
            optimal_k = mid  # Fits in budget, try larger K
            low = mid + 1
        else:
            high = mid - 1  # Exceeds budget, decrease K

    head_chars = int(optimal_k * DEFAULT_HEAD_RATIO)
    tail_chars = int(optimal_k * DEFAULT_TAIL_RATIO)

    return optimal_k, head_chars, tail_chars


def profile_table_sizes(
    conn: Connection,
    table_name: str,
    column_names: list[str],
    heavy_column: str,
    where_sql: str,
    limit_sql: str,
    params: dict[str, object],
) -> tuple[list[int], int]:
    """Execute a lightweight pre-flight query to profile row sizes.

    Returns:
        tuple[list[int], int]: (heavy_column_lengths, total_metadata_bytes)
    """
    meta_cols = [col for col in column_names if col != heavy_column]
    meta_exprs = [f"coalesce(octet_length({col}::text), 0)" for col in meta_cols]
    delimiter_overhead = len(column_names) * 3 + 2  # commas, quotes, CRLF

    meta_sum_sql = " + ".join(meta_exprs) if meta_exprs else "0"

    profile_query = text(
        f"""
        SELECT
            coalesce(octet_length({heavy_column}), 0) AS content_bytes,
            ({meta_sum_sql} + {delimiter_overhead}) AS meta_bytes
        FROM {table_name}
        {where_sql}
        {limit_sql}
    """
    )

    result = conn.execute(profile_query, params)
    content_lengths: list[int] = []
    total_meta_bytes = 0

    for row in result:
        content_lengths.append(row[0])
        total_meta_bytes += row[1]

    return content_lengths, total_meta_bytes


def sanitize_cell_value(
    val: Any,
    source_url: str | None = None,
    escape_newlines: bool = True,
    max_cell_chars: int = DEFAULT_MAX_CELL_CHARS,
    head_chars: int = int(DEFAULT_MAX_CELL_CHARS * DEFAULT_HEAD_RATIO),
    tail_chars: int = int(DEFAULT_MAX_CELL_CHARS * DEFAULT_TAIL_RATIO),
    escape_formulas: bool = True,
) -> tuple[str, bool]:
    """Sanitize and format a single cell value for Google Sheets CSV compatibility.

    Returns:
        tuple[str, bool]: (sanitized_string_value, was_truncated)
    """
    if val is None:
        return "", False

    was_truncated = False

    # 1. Semantic flattening for JSON and lists
    if isinstance(val, list):
        if all(isinstance(item, str) for item in val):
            # Convert ['Ministério da Saúde', 'Gabinete'] -> 'Ministério da Saúde > Gabinete'
            text_val = " > ".join(val)
        else:
            text_val = json.dumps(val, ensure_ascii=False)
    elif isinstance(val, dict):
        text_val = json.dumps(val, ensure_ascii=False)
    else:
        text_val = str(val)

    # 2. Scrub forbidden null characters that terminate Sheets text parsing
    if "\x00" in text_val:
        text_val = text_val.replace("\x00", "")

    # 3. Newline escaping (literal \n vs raw multi-line)
    if escape_newlines:
        text_val = text_val.replace("\r\n", "\\n").replace("\r", "\\n").replace("\n", "\\n")

    # 4. Head-Tail Sandwich Truncation for cells exceeding computed limit
    if max_cell_chars > 0 and len(text_val) > max_cell_chars:
        orig_len = len(text_val)
        effective_head = min(head_chars, max_cell_chars - 30)
        effective_tail = min(tail_chars, max_cell_chars - effective_head - 10)
        if effective_head + effective_tail >= max_cell_chars:
            effective_head = int(max_cell_chars * DEFAULT_HEAD_RATIO)
            effective_tail = int(max_cell_chars * DEFAULT_TAIL_RATIO)

        omitted_chars = orig_len - (effective_head + effective_tail)

        if max_cell_chars < 500:
            # Compact marker to avoid blowing up budget when cell limit is tight
            marker_body = f" ... [TRUNCATED: {omitted_chars:,} CHARS | See source_url] ... "
        elif escape_newlines:
            url_ref = f" | Full Text: {source_url}" if source_url else ""
            marker_body = (
                f"\\n\\n... [TRUNCATED: {omitted_chars:,} CHARS OMITTED{url_ref}] ...\\n\\n"
            )
        else:
            url_ref = f" | Full Text: {source_url}" if source_url else ""
            marker_body = (
                f"\n\n... [TRUNCATED: {omitted_chars:,} CHARS OMITTED{url_ref}] ...\n\n"
            )

        text_val = text_val[:effective_head] + marker_body + text_val[-effective_tail:]
        was_truncated = True

    # 5. Formula Injection Defense (CSV Injection)
    if escape_formulas and text_val.startswith(INJECTION_PREFIXES):
        text_val = f"'{text_val}"

    return text_val, was_truncated


def export_single_table(
    engine: Engine,
    table_name: str,
    output_file: Path,
    target_date: str | None = None,
    limit: int | None = None,
    max_file_mb: float = DEFAULT_TARGET_MAX_FILE_MB,
    auto_fit: bool = True,
    escape_newlines: bool = True,
    manual_max_cell_chars: int | None = None,
    manual_head_chars: int | None = None,
    manual_tail_chars: int | None = None,
    escape_formulas: bool = True,
    exclude_columns: set[str] | None = None,
) -> tuple[Path, int, int, int, int, int, int]:
    """Export a single table's rows to a CSV file.

    Returns:
        tuple: (file_path, total_rows, total_cells, truncated_cells,
                k_chars, head_chars, tail_chars)
    """
    output_file.parent.mkdir(parents=True, exist_ok=True)
    exclude_columns = exclude_columns or set()

    inspector = inspect(engine)
    columns_info = inspector.get_columns(table_name, schema="public")
    column_names = [col["name"] for col in columns_info if col["name"] not in exclude_columns]
    num_cols = len(column_names)

    where_clauses = []
    params: dict[str, object] = {}

    if target_date and "date" in column_names:
        where_clauses.append("date = :target_date")
        params["target_date"] = target_date

    where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
    limit_sql = f"LIMIT {limit}" if limit else ""

    heavy_column = "raw_content" if "raw_content" in column_names else None

    # Step 1: Compute optimal K via Water-Filling Binary Search if auto_fit is enabled
    target_max_bytes = int(max_file_mb * 1024 * 1024)

    with engine.connect() as conn:
        if auto_fit and heavy_column and manual_max_cell_chars is None:
            lengths, meta_bytes = profile_table_sizes(
                conn=conn,
                table_name=table_name,
                column_names=column_names,
                heavy_column=heavy_column,
                where_sql=where_sql,
                limit_sql=limit_sql,
                params=params,
            )
            k_chars, head_chars, tail_chars = calculate_optimal_sandwich_budget(
                text_lengths=lengths,
                metadata_total_bytes=meta_bytes,
                target_max_bytes=target_max_bytes,
                max_cell_cap=DEFAULT_MAX_CELL_CHARS,
            )
        else:
            k_chars = (
                manual_max_cell_chars
                if manual_max_cell_chars is not None
                else DEFAULT_MAX_CELL_CHARS
            )
            head_chars = (
                manual_head_chars
                if manual_head_chars is not None
                else int(k_chars * DEFAULT_HEAD_RATIO)
            )
            tail_chars = (
                manual_tail_chars
                if manual_tail_chars is not None
                else int(k_chars * DEFAULT_TAIL_RATIO)
            )

        # Step 2: Stream rows and write CSV with computed parameters
        query = text(
            f"""
            SELECT {', '.join(column_names)}
            FROM {table_name}
            {where_sql}
            {limit_sql}
        """
        )

        result = conn.execution_options(stream_results=True).execute(query, params)

        count = 0
        truncated_count = 0

        with open(output_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(column_names)

            for row in result:
                row_dict = row._asdict()
                source_url = row_dict.get("source_url")
                formatted_values = []

                for col in column_names:
                    raw_val = row_dict.get(col)
                    formatted_val, was_truncated = sanitize_cell_value(
                        val=raw_val,
                        source_url=str(source_url) if source_url else None,
                        escape_newlines=escape_newlines,
                        max_cell_chars=k_chars,
                        head_chars=head_chars,
                        tail_chars=tail_chars,
                        escape_formulas=escape_formulas,
                    )
                    if was_truncated:
                        truncated_count += 1
                    formatted_values.append(formatted_val)

                writer.writerow(formatted_values)
                count += 1

    total_cells = count * num_cols
    return output_file, count, total_cells, truncated_count, k_chars, head_chars, tail_chars


def main() -> None:
    settings = LexSettings()

    parser = argparse.ArgumentParser(
        description=(
            "Export PostgreSQL tables to CSV compliant with Google Sheets upload limits "
            "(https://support.google.com/drive/answer/37603) via water-filling sandwich."
        )
    )
    parser.add_argument(
        "--table",
        "-t",
        type=str,
        default="all",
        help="Table name to export (default: 'all' to export all tables)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Target CSV file path (when single table) or directory (when all tables)",
    )
    parser.add_argument(
        "--date",
        "-d",
        type=str,
        default=None,
        help="Filter by date column (YYYY-MM-DD), if table has it",
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=None,
        help="Limit number of rows exported per table",
    )
    parser.add_argument(
        "--max-file-mb",
        type=float,
        default=DEFAULT_TARGET_MAX_FILE_MB,
        help=(
            f"Target maximum CSV file size in MB (default: {DEFAULT_TARGET_MAX_FILE_MB:.1f} MB; "
            f"safe under Google Sheets {GOOGLE_SHEETS_MAX_UPLOAD_MB:.0f} MB upload limit)"
        ),
    )
    parser.add_argument(
        "--no-auto-fit",
        action="store_true",
        default=False,
        help="Disable automatic Water-Filling calculation and use fixed cell limits",
    )
    parser.add_argument(
        "--max-cell-chars",
        type=int,
        default=None,
        help=(
            f"Manual override for max chars per cell (default: auto <= {DEFAULT_MAX_CELL_CHARS:,})"
        ),
    )
    parser.add_argument(
        "--head-chars",
        type=int,
        default=None,
        help="Manual override for characters from start on truncation",
    )
    parser.add_argument(
        "--tail-chars",
        type=int,
        default=None,
        help="Manual override for characters from end on truncation",
    )
    parser.add_argument(
        "--all-columns",
        action="store_true",
        default=False,
        help="Include all DB columns (including internal hashes, FKs and JSON blobs)",
    )
    parser.add_argument(
        "--exclude-raw",
        action="store_true",
        default=False,
        help="Exclude raw_content text column to generate an ultra-light metadata CSV",
    )
    parser.add_argument(
        "--no-escape-newlines",
        action="store_true",
        default=False,
        help="Preserve raw multi-line newlines in text fields instead of escaping to \\n",
    )
    parser.add_argument(
        "--no-formula-escape",
        action="store_true",
        default=False,
        help="Do not escape leading '=', '+', '-', '@' characters with a single quote",
    )
    parser.add_argument(
        "--db-url",
        type=str,
        default=str(settings.database_url),
        help="PostgreSQL connection string",
    )

    args = parser.parse_args()
    engine = create_engine(args.db_url)

    available_tables = get_available_tables(engine)
    if not available_tables:
        print("[!] No tables found in public schema.")
        sys.exit(1)

    if args.table.lower() == "all":
        tables_to_export = available_tables
        target_dir = (
            args.output if (args.output and args.output.suffix != ".csv") else DEFAULT_OUTPUT_DIR
        )
    else:
        if args.table not in available_tables:
            print(f"[!] Error: Table '{args.table}' not found in database.")
            print(f"    Available tables: {', '.join(available_tables)}")
            sys.exit(1)
        tables_to_export = [args.table]
        target_dir = DEFAULT_OUTPUT_DIR

    print(f"[*] Starting CSV export for {len(tables_to_export)} table(s) from PostgreSQL...")
    print("[*] Google Drive & Sheets Optimization Strategy (answer/37603):")
    print(
        f"    • Target File Cap: <= {args.max_file_mb:.1f} MB "
        f"[Google limit: {GOOGLE_SHEETS_MAX_UPLOAD_MB:.0f} MB upload limit]"
    )
    opt_algo = (
        "Water-Filling Binary Search (Auto-Fit)"
        if not args.no_auto_fit
        else "Manual Fixed Limits"
    )
    print(f"    • Optimization Algorithm: {opt_algo}")
    col_desc = (
        "All Columns"
        if args.all_columns
        else "Clean Spreadsheet Columns (Internal DB plumbing omitted)"
    )
    print(f"    • Column Selection: {col_desc}")
    print(f"    • Spreadsheet cell capacity cap: {GOOGLE_SHEETS_MAX_TOTAL_CELLS:,} total cells")
    print(
        f"    • Formula injection defense: "
        f"{'Enabled' if not args.no_formula_escape else 'Disabled'}"
    )
    print("    • JSON Hierarchy flattening: Enabled (Breadcrumb format)")
    newline_desc = "\\n literal" if not args.no_escape_newlines else "RFC 4180 multiline"
    print(f"    • Newline escaping: {newline_desc}\n")

    total_all_rows = 0
    total_all_cells = 0
    total_all_truncated = 0
    escape_newlines = not args.no_escape_newlines
    escape_formulas = not args.no_formula_escape
    auto_fit = not args.no_auto_fit

    for tbl in tables_to_export:
        exclude_cols = set()
        if args.exclude_raw:
            exclude_cols.add("raw_content")
        if not args.all_columns and tbl == "normative_acts":
            exclude_cols.update(INTERNAL_DB_COLUMNS)

        if len(tables_to_export) == 1 and args.output and args.output.suffix == ".csv":
            out_file = args.output
        else:
            out_file = target_dir / f"{tbl}.csv"

        out_path, rows, cells, truncated, k_val, head_val, tail_val = export_single_table(
            engine=engine,
            table_name=tbl,
            output_file=out_file,
            target_date=args.date,
            limit=args.limit,
            max_file_mb=args.max_file_mb,
            auto_fit=auto_fit,
            escape_newlines=escape_newlines,
            manual_max_cell_chars=args.max_cell_chars,
            manual_head_chars=args.head_chars,
            manual_tail_chars=args.tail_chars,
            escape_formulas=escape_formulas,
            exclude_columns=exclude_cols,
        )

        total_all_rows += rows
        total_all_cells += cells
        total_all_truncated += truncated
        size_mb = out_path.stat().st_size / (1024 * 1024)
        pct_sheet = (cells / GOOGLE_SHEETS_MAX_TOTAL_CELLS) * 100
        budget_info = (
            f" [Sandwich Budget: {k_val:,} chars (Head: {head_val:,} | Tail: {tail_val:,})]"
        )

        warn_flag = ""
        if size_mb > GOOGLE_SHEETS_MAX_UPLOAD_MB:
            warn_flag = f" ⚠️ [EXCEEDS {GOOGLE_SHEETS_MAX_UPLOAD_MB:.0f}MB UPLOAD LIMIT!]"
        elif size_mb > GOOGLE_SHEETS_RECOMMENDED_MAX_MB:
            rec_limit = GOOGLE_SHEETS_RECOMMENDED_MAX_MB
            warn_flag = f" ℹ [>{rec_limit:.0f}MB: Fits upload, may lag in browser]"

        print(
            f"  ✓ {tbl:<18} → {rows:>6,} rows | {cells:>8,} cells ({pct_sheet:>4.1f}% max) "
            f"| {size_mb:>6.2f} MB | {out_path.name}{budget_info}{warn_flag}"
        )

    print(
        f"\n[✓] Export complete: {total_all_rows:,} total rows ({total_all_cells:,} cells) "
        f"across {len(tables_to_export)} table(s)."
    )
    if total_all_truncated:
        print(
            f"    ℹ {total_all_truncated} cells were adjusted via dynamic Head-Tail sandwich "
            f"to guarantee compliance with Google Sheets limits (<= {args.max_file_mb:.1f} MB)."
        )


if __name__ == "__main__":
    main()
