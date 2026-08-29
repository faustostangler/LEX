#!/usr/bin/env python3
"""Export database tables from PostgreSQL to CSV files.

Supports exporting all public tables by default, or a specific table if parameterized.
Escapes embedded newlines (\\n) by default so each database record occupies exactly
one physical line in the CSV, enabling seamless import into Google Sheets / Excel.

Usage:
    # Export all tables to CSV in playground/ directory (default)
    python playground/export_table_to_csv.py

    # Export a specific table
    python playground/export_table_to_csv.py --table normative_acts
    python playground/export_table_to_csv.py --table gazette_editions --output playground/editions.csv

    # Filter specific table by date/limit
    python playground/export_table_to_csv.py --table normative_acts --date 2024-01-15 --limit 500
"""

import argparse
import csv
import json
from pathlib import Path
import sys

from sqlalchemy import create_engine, inspect, text

from lex.shared_kernel.config import LexSettings

DEFAULT_OUTPUT_DIR = Path("playground")


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
) -> int:
    """Export a single table's rows to a CSV file."""
    output_file.parent.mkdir(parents=True, exist_ok=True)

    inspector = inspect(engine)
    columns_info = inspector.get_columns(table_name, schema="public")
    column_names = [col["name"] for col in columns_info]

    where_clauses = []
    params: dict[str, object] = {}

    if target_date and "date" in column_names:
        where_clauses.append("date = :target_date")
        params["target_date"] = target_date

    where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
    limit_sql = f"LIMIT {limit}" if limit else ""

    query = text(
        f"""
        SELECT *
        FROM {table_name}
        {where_sql}
        {limit_sql}
    """
    )

    count = 0
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
                    formatted_values.append(val)

                writer.writerow(formatted_values)
                count += 1

    return count


def main() -> None:
    settings = LexSettings()

    parser = argparse.ArgumentParser(
        description="Export PostgreSQL tables to CSV."
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
    escape_newlines = not args.no_escape_newlines

    for tbl in tables_to_export:
        if len(tables_to_export) == 1 and args.output and args.output.suffix == ".csv":
            out_file = args.output
        else:
            out_file = target_dir / f"{tbl}.csv"

        rows = export_single_table(
            engine=engine,
            table_name=tbl,
            output_file=out_file,
            target_date=args.date,
            limit=args.limit,
            escape_newlines=escape_newlines,
        )
        total_all_rows += rows
        size_mb = out_file.stat().st_size / (1024 * 1024)
        print(f"  ✓ {tbl:<20} → {rows:>6,} rows | {size_mb:>6.2f} MB | {out_file}")

    print(f"\n[✓] Export complete: {total_all_rows:,} total rows across {len(tables_to_export)} table(s).")


if __name__ == "__main__":
    main()
