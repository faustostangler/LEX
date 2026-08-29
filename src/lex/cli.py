"""Command Line Interface (CLI) for LEX Ingestion Engine.

Provides administrative database initialization, schema migration, and crawler orchestration.
Defaults to 'crawl federal_dou' when executed without explicit sub-commands.
"""

import argparse
import sys
from datetime import date
from typing import Any

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine, text

from lex.ingestion.infrastructure.persistence.models import Base
from lex.shared_kernel.config import LexSettings

# -----------------------------------------------------------------------------
# Module Constants (ADR-003)
# -----------------------------------------------------------------------------
DEFAULT_FALLBACK_CRAWL_DATE: str = "2024-01-15"
DEFAULT_SPIDER_NAME: str = "federal_dou"


def get_default_crawl_date() -> str:
    """Return default target date for crawling (guaranteeing valid gazettes)."""
    today = date.today()
    if today.year > 2024:
        return DEFAULT_FALLBACK_CRAWL_DATE
    return today.isoformat()


def init_db() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def run_crawler(
    spider_name: str,
    start_date: str | None,
    end_date: str | None,
    force: bool = False,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    default_date = get_default_crawl_date()
    spider_args: dict[str, Any] = {}
    spider_args["start_date"] = start_date or default_date
    spider_args["end_date"] = end_date or start_date or default_date
    spider_args["force"] = force

    interval_msg = f"{spider_args['start_date']} -> {spider_args['end_date']}"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    print(f"Starting spider '{spider_name}' (interval: {interval_msg}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def build_parser() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--start-date",
        help="Start date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def parse_cli_args(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --start-date 2024-01-02`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def main(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = parse_cli_args(args)

    if parsed_args.command == "init-db":
        init_db()
    elif parsed_args.command == "crawl":
        run_crawler(
            parsed_args.spider,
            parsed_args.start_date,
            parsed_args.end_date,
            force=parsed_args.force,
        )
    else:
        build_parser().print_help()


if __name__ == "__main__":
    main()
