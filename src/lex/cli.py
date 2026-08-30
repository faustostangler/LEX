"""Command Line Interface (CLI) for LEX Ingestion Engine.

Provides database initialization, schema migration, and crawler orchestration.
Defaults to crawling in reverse chronological order (from today back to 2002-01-02).
"""

import argparse
import sys
from datetime import date
from typing import Any

import anyio
import uvicorn
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from lex.consolidation.application.use_cases import (
    CompileNormativeActUseCase,
    TimeTravelCompilationUseCase,
)
from lex.consolidation.domain.entities import CompiledNormativeAct
from lex.consolidation.infrastructure.persistence.postgres_repository import (
    PostgresConsolidationRepository,
)
from lex.ingestion.infrastructure.persistence.models import Base, NormativeActModel
from lex.ingestion.infrastructure.persistence.postgres_repository import (
    PostgresGazetteRepository,
)
from lex.shared_kernel.config import LexSettings
from lex.treatment.application.use_cases import ProcessNormativeActUseCase
from lex.treatment.domain.entities import ActAst
from lex.treatment.infrastructure.persistence.postgres_repository import (
    PostgresTreatmentRepository,
)

# -----------------------------------------------------------------------------
# Module Constants (ADR-003)
# -----------------------------------------------------------------------------
# Earliest publication available in the modern digital DOU portal (in.gov.br)
EARLIEST_MODERN_DOU_DATE: str = "2002-01-02"
DEFAULT_SPIDER_NAME: str = "federal_dou"


def init_db() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts, mutations, compiled_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.execute(
                    text(
                        "ALTER TABLE compiled_normative_acts "
                        "ALTER COLUMN compiled_html SET COMPRESSION lz4;"
                    )
                )
                conn.execute(
                    text(
                        "ALTER TABLE compiled_normative_acts "
                        "ALTER COLUMN compiled_markdown SET COMPRESSION lz4;"
                    )
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def run_crawler(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def run_treat(date_str: str | None, territory: str, limit: int) -> None:
    """Runs the Dual-Track Stage 2 treatment on un-processed normative acts."""
    settings = LexSettings()
    engine = create_engine(str(settings.database_url), echo=False)
    session_factory = sessionmaker(bind=engine)

    with session_factory() as session:
        gazette_repo = PostgresGazetteRepository(session=session)
        treatment_repo = PostgresTreatmentRepository(session=session)
        use_case = ProcessNormativeActUseCase(repository=treatment_repo)

        from sqlalchemy import select

        stmt = select(NormativeActModel).where(NormativeActModel.territory_id == territory)
        if date_str:
            target_date = date.fromisoformat(date_str)
            stmt = stmt.where(NormativeActModel.date == target_date)
        stmt = stmt.limit(limit)

        models = session.scalars(stmt).all()
        print(f"Processing Stage 2 treatment for {len(models)} acts...")

        async def _treat_all() -> None:
            for m in models:
                domain_act = gazette_repo.get_act_by_id(m.id)
                if domain_act:
                    result = await use_case.execute(domain_act)
                    print(
                        f"Treated act {domain_act.title} [{result.track}] "
                        f"with {result.mutations_extracted} mutations."
                    )

        anyio.run(_treat_all)
        print("Stage 2 treatment completed successfully.")


def run_compile(identifier: str) -> None:
    """Compiles a statute's base AST and accumulated mutations into a read model."""
    settings = LexSettings()
    engine = create_engine(str(settings.database_url), echo=False)
    session_factory = sessionmaker(bind=engine)

    with session_factory() as session:
        from uuid import UUID

        from sqlalchemy import select

        repo = PostgresConsolidationRepository(session=session)
        use_case = CompileNormativeActUseCase(repository=repo)

        act_model = None
        try:
            act_uuid = UUID(identifier)
            act_model = session.get(NormativeActModel, act_uuid)
        except ValueError:
            stmt = select(NormativeActModel).where(NormativeActModel.canonical_urn == identifier)
            act_model = session.scalars(stmt).first()

        if not act_model:
            print(f"Error: Act '{identifier}' not found in database.")
            return

        if not act_model.structured_content:
            print(
                f"Error: Act '{identifier}' does not have structured AST content. "
                "Run 'lex treat' first."
            )
            return

        base_ast = ActAst.from_dict(act_model.structured_content)

        async def _compile() -> None:
            compiled = await use_case.execute(base_ast)
            print(f"Compiled act: {compiled.compiled_ast.title}")
            print(f"Version hash: {compiled.compiled_version_hash}")
            print(f"Total mutations applied: {compiled.total_mutations_applied}")
            print(
                f"Active articles: {compiled.active_articles_count} | "
                f"Revoked articles: {compiled.revoked_articles_count}"
            )

        anyio.run(_compile)


def run_query(identifier: str, as_of: str | None, output_format: str) -> None:
    """Queries compiled legislation text or performs on-demand time travel."""
    settings = LexSettings()
    engine = create_engine(str(settings.database_url), echo=False)
    session_factory = sessionmaker(bind=engine)

    with session_factory() as session:
        from uuid import UUID

        from sqlalchemy import select

        repo = PostgresConsolidationRepository(session=session)

        act_model = None
        try:
            act_uuid = UUID(identifier)
            act_model = session.get(NormativeActModel, act_uuid)
        except ValueError:
            stmt = select(NormativeActModel).where(NormativeActModel.canonical_urn == identifier)
            act_model = session.scalars(stmt).first()

        if not act_model:
            print(f"Error: Act '{identifier}' not found in database.")
            return

        async def _query() -> None:
            compiled: CompiledNormativeAct | None = None
            if as_of:
                cutoff = date.fromisoformat(as_of)
                if not act_model.structured_content:
                    print("Error: Act structured content missing.")
                    return
                base_ast = ActAst.from_dict(act_model.structured_content)
                tt_case = TimeTravelCompilationUseCase(repository=repo)
                compiled = await tt_case.execute(base_ast, as_of=cutoff)
            else:
                compiled = await repo.get_compiled_act(act_model.id)
                if not compiled and act_model.structured_content:
                    base_ast = ActAst.from_dict(act_model.structured_content)
                    c_case = CompileNormativeActUseCase(repository=repo)
                    compiled = await c_case.execute(base_ast)

            if not compiled:
                print(f"Error: Could not retrieve compiled act for '{identifier}'.")
                return

            if output_format == "html":
                print(compiled.compiled_html)
            elif output_format == "markdown":
                print(compiled.compiled_markdown)
            else:
                print(f"=== {compiled.compiled_ast.title} ===")
                if compiled.compiled_ast.ementa:
                    print(f"Ementa: {compiled.compiled_ast.ementa}\n")
                for n in compiled.compiled_ast.nodes:
                    print(f"{n.label}: {n.text} [{n.status.value}]")

        anyio.run(_query)


def build_parser() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion, Treatment & Consolidation Engine CLI",
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
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    # treat sub-command
    treat_parser = subparsers.add_parser(
        "treat", help="Run Dual-Track Stage 2 treatment on ingested acts"
    )
    treat_parser.add_argument("--date", "-d", help="Target gazette date (YYYY-MM-DD)", default=None)
    treat_parser.add_argument(
        "--territory", "-t", default="BR", help="Territory code (default: BR)"
    )
    treat_parser.add_argument(
        "--limit", type=int, default=100, help="Maximum acts to process (default: 100)"
    )

    # compile sub-command
    compile_parser = subparsers.add_parser(
        "compile", help="Compile base AST and mutations into read model"
    )
    compile_parser.add_argument("identifier", help="Statute UUID or LexML Canonical URN")

    # query sub-command
    query_parser = subparsers.add_parser(
        "query", help="Query compiled legislation text or time-travel state"
    )
    query_parser.add_argument("identifier", help="Statute UUID or LexML Canonical URN")
    query_parser.add_argument(
        "--as-of", help="Historical cutoff date for time travel (YYYY-MM-DD)", default=None
    )
    query_parser.add_argument(
        "--format",
        choices=["text", "html", "markdown"],
        default="text",
        help="Output format",
    )

    # serve sub-command
    serve_parser = subparsers.add_parser("serve", help="Launch the LEX REST API server via Uvicorn")
    serve_parser.add_argument("--host", default="0.0.0.0", help="Bind host (default: 0.0.0.0)")  # noqa: S104
    serve_parser.add_argument("--port", type=int, default=8000, help="Bind port (default: 8000)")
    serve_parser.add_argument(
        "--reload", action="store_true", default=False, help="Enable auto-reload"
    )

    return parser


def parse_cli_args(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    valid_commands = ("init-db", "crawl", "treat", "compile", "query", "serve", "-h", "--help")
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in valid_commands:
        if not raw_args[0].startswith("-"):
            raw_args = ["crawl"] + raw_args
        else:
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def main(args: list[str] | None = None) -> None:
    """CLI routing entrypoint."""
    parsed_args = parse_cli_args(args)

    if parsed_args.command == "init-db":
        init_db()
    elif parsed_args.command == "crawl":
        run_crawler(
            spider_name=parsed_args.spider,
            start_date=parsed_args.start_date,
            end_date=parsed_args.end_date,
            single_date=parsed_args.date,
            force=parsed_args.force,
            reverse=not parsed_args.ascending,
        )
    elif parsed_args.command == "treat":
        run_treat(
            date_str=parsed_args.date,
            territory=parsed_args.territory,
            limit=parsed_args.limit,
        )
    elif parsed_args.command == "compile":
        run_compile(identifier=parsed_args.identifier)
    elif parsed_args.command == "query":
        run_query(
            identifier=parsed_args.identifier,
            as_of=parsed_args.as_of,
            output_format=parsed_args.format,
        )
    elif parsed_args.command == "serve":
        uvicorn.run(
            "lex.api.main:app",
            host=parsed_args.host,
            port=parsed_args.port,
            reload=parsed_args.reload,
        )
    else:
        build_parser().print_help()


if __name__ == "__main__":
    main()
    print("Done!")
