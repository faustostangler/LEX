#!/usr/bin/env python3
"""Export database tables from PostgreSQL to CSV files.

Supports exporting all public tables by default, or a specific table if parameterized.
Escapes embedded newlines (\\n) and strictly caps cell lengths at 45,000 characters
AFTER escaping to guarantee 100% compatibility with Google Sheets' 50,000 char per cell limit.

Usage:
    # Export all tables to CSV in playground/ directory (default Google Sheets safe)
    python playground/export_table_to_csv.py

    # Export a specific table
    python playground/export_table_to_csv.py --table normative_acts
    python playground/export_table_to_csv.py --table gazette_editions --output playground/editions.csv

    # Omit heavy raw_content column for ultra-light metadata spreadsheet
    python playground/export_table_to_csv.py --table normative_acts --exclude-raw

    # Export with custom cell length or unlimited
    python playground/export_table_to_csv.py --max-cell-chars 0  # Unlimited (not Google Sheets safe)
"""

import argparse
import csv
import json
from pathlib import Path
import sys

from sqlalchemy import create_engine, inspect, text

from lex.shared_kernel.config import LexSettings

DEFAULT_OUTPUT_DIR = Path("playground")
DEFAULT_MAX_CELL_CHARS = 45000  # Google Sheets hard cap is 50,000 chars per cell


def get_available_tables(engine) -> list[str]:
    """Retrieve all table names from the public schema."""
    inspector = inspect(engine)
    tables = inspector.get_table_names(schema="public")
    # Exclude alembic internal migrations table if present
    return [t for t in tables if t != "alembic_version"]


def export_single_table(
    engine,
    table_name: str,
    output_file: Path,
    target_date: str | None = None,
    limit: int | None = None,
    escape_newlines: bool = True,
    max_cell_chars: int = DEFAULT_MAX_CELL_CHARS,
    exclude_columns: set[str] | None = None,
) -> tuple[int, int]:
    """Export a single table's rows to a CSV file.

    Returns:
        (total_rows_exported, total_truncated_cells)
    """
    output_file.parent.mkdir(parents=True, exist_ok=True)
    exclude_columns = exclude_columns or set()

    inspector = inspect(engine)
    columns_info = inspector.get_columns(table_name, schema="public")
    column_names = [
        col["name"] for col in columns_info if col["name"] not in exclude_columns
    ]

    where_clauses = []
    params: dict[str, object] = {}

    if target_date and "date" in column_names:
        where_clauses.append("date = :target_date")
        params["target_date"] = target_date

    where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
    limit_sql = f"LIMIT {limit}" if limit else ""

    query = text(
        f"""
        SELECT {', '.join(column_names)}
        FROM {table_name}
        {where_sql}
        {limit_sql}
    """
    )

    count = 0
    truncated_count = 0

    with engine.connect() as conn:
        result = conn.execution_options(stream_results=True).execute(
            query, params
        )

        with open(output_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(
                f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            writer.writerow(column_names)

            for row in result:
                row_dict = row._asdict()
                formatted_values = []
                for col in column_names:
                    val = row_dict.get(col)
                    if isinstance(val, (list, dict)):
                        val = json.dumps(val, ensure_ascii=False)
                    elif isinstance(val, str) and escape_newlines:
                        # Replace raw multiline breaks with literal \n so Google Sheets / Excel
                        # imports each record as a single row without creating spurious extra rows.
                        val = (
                            val.replace("\r\n", "\\n")
                            .replace("\r", "\\n")
                            .replace("\n", "\\n")
                        )

                    # Strictly enforce maximum cell characters AFTER all string transformations
                    if (
                        isinstance(val, str)
                        and max_cell_chars > 0
                        and len(val) > max_cell_chars
                    ):
                        original_len = len(val)
                        suffix = (
                            f" ...[TRUNCATED: TOTAL {original_len:,} CHARS]"
                        )
                        val = val[: max_cell_chars - len(suffix)] + suffix
                        truncated_count += 1

                    formatted_values.append(val)

                writer.writerow(formatted_values)
                count += 1

    return count, truncated_count


def main() -> None:
    settings = LexSettings()

    parser = argparse.ArgumentParser(
        description="Export PostgreSQL tables to CSV (Google Sheets & Excel compatible)."
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
        "--max-cell-chars",
        type=int,
        default=DEFAULT_MAX_CELL_CHARS,
        help="Maximum characters per cell (default: 45,000 for Google Sheets compatibility; 0 for unlimited)",
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

    # Determine which tables to export
    if args.table.lower() == "all":
        tables_to_export = available_tables
        target_dir = (
            args.output
            if (args.output and args.output.suffix != ".csv")
            else DEFAULT_OUTPUT_DIR
        )
    else:
        if args.table not in available_tables:
            print(f"[!] Error: Table '{args.table}' not found in database.")
            print(f"    Available tables: {', '.join(available_tables)}")
            sys.exit(1)
        tables_to_export = [args.table]
        target_dir = DEFAULT_OUTPUT_DIR

    print(
        f"[*] Starting CSV export for {len(tables_to_export)} table(s) from PostgreSQL..."
    )
    total_all_rows = 0
    total_all_truncated = 0
    escape_newlines = not args.no_escape_newlines
    exclude_cols = {"raw_content"} if args.exclude_raw else set()

    for tbl in tables_to_export:
        if len(tables_to_export) == 1 and args.output and args.output.suffix == ".csv":
            out_file = args.output
        else:
            out_file = target_dir / f"{tbl}.csv"

        rows, truncated = export_single_table(
            engine=engine,
            table_name=tbl,
            output_file=out_file,
            target_date=args.date,
            limit=args.limit,
            escape_newlines=escape_newlines,
            max_cell_chars=args.max_cell_chars,
            exclude_columns=exclude_cols,
        )
        total_all_rows += rows
        total_all_truncated += truncated
        size_mb = out_file.stat().st_size / (1024 * 1024)
        trunc_info = f" ({truncated} cells safely capped < 45k chars)" if truncated else ""
        print(f"  ✓ {tbl:<20} → {rows:>6,} rows | {size_mb:>6.2f} MB | {out_file}{trunc_info}")

    print(
        f"\n[✓] Export complete: {total_all_rows:,} total rows across {len(tables_to_export)} table(s)."
    )
    if total_all_truncated:
        print(
            f"    ℹ {total_all_truncated} large cells were truncated to {args.max_cell_chars:,} chars "
            "for 100% Google Sheets compatibility."
        )


if __name__ == "__main__":
    main()
