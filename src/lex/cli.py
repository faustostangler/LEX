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
from sqlalchemy import text

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
from lex.shared_kernel.config import get_settings
from lex.shared_kernel.database import get_engine, get_session_factory
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
DEFAULT_SPIDER_NAME: str = "all"


def init_db() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = get_settings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = get_engine(echo=False)

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
    spider_name: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider(s) and date interval."""
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

    # Discover spiders to run: specific name or all discovered spiders
    if spider_name is None or spider_name.lower() == "all":
        spiders_to_run = process.spider_loader.list()
    else:
        spiders_to_run = [spider_name]

    if not spiders_to_run:
        print("No spiders found to execute.")
        return

    for name in spiders_to_run:
        print(f"Starting spider '{name}' ({interval_info}){force_msg}...")
        process.crawl(name, **spider_args)

    process.start()


def run_treat(
    date_str: str | None = None,
    territory: str | None = None,
    section: str | None = None,
    limit: int | None = None,
    force: bool = False,
    only_failures: bool = False,
) -> None:
    """Runs the Dual-Track Stage 2 treatment on un-processed normative acts.

    Args:
        date_str: Optional target gazette date (YYYY-MM-DD).
        territory: Optional territory code (e.g. BR). If None, processes all territories.
        section: Optional gazette section (e.g. '1', '2', '3', 'extra').
            If None, processes all sections.
        limit: Optional maximum number of acts to process. If None, processes all pending acts.
        force: If True, re-processes acts even if already treated.
        only_failures: If True, only processes acts flagged as needing manual review.
    """
    session_factory = get_session_factory(expire_on_commit=False)

    with session_factory() as session:
        gazette_repo = PostgresGazetteRepository(session=session)
        treatment_repo = PostgresTreatmentRepository(session=session)
        use_case = ProcessNormativeActUseCase(repository=treatment_repo)

        from uuid import UUID

        from sqlalchemy import or_, select
        from tqdm import tqdm

        from lex.shared_kernel.value_objects import PublicationNature

        stmt = select(NormativeActModel)
        if territory:
            stmt = stmt.where(NormativeActModel.territory_id == territory)
        if section:
            sec_norm = section.strip().lower()
            if sec_norm in ["1", "secao_1", "do1", "secao1"]:
                possible_sections = ["secao_1", "1", "do1", "secao1"]
            elif sec_norm in ["2", "secao_2", "do2", "secao2"]:
                possible_sections = ["secao_2", "2", "do2", "secao2"]
            elif sec_norm in ["3", "secao_3", "do3", "secao3"]:
                possible_sections = ["secao_3", "3", "do3", "secao3"]
            elif sec_norm in ["e", "extra", "doe"]:
                possible_sections = ["extra", "e", "doe"]
            else:
                possible_sections = [section]
            stmt = stmt.where(NormativeActModel.section.in_(possible_sections))
        if date_str:
            target_date = date.fromisoformat(date_str)
            stmt = stmt.where(NormativeActModel.date == target_date)

        if only_failures:
            stmt = stmt.where(
                NormativeActModel.metadata_json["needs_manual_review"].as_boolean().is_(True)
            )
        elif not force:
            is_trilha_a = NormativeActModel.publication_nature.in_(
                [
                    PublicationNature.NORMATIVA_ABSTRATA.value,
                    PublicationNature.REGULATORIA_SETORIAL.value,
                ]
            )
            is_trilha_b = NormativeActModel.publication_nature.in_(
                [
                    PublicationNature.CONCRETA_INDIVIDUAL.value,
                    PublicationNature.PUBLICIDADE_OPERACIONAL.value,
                ]
            )
            stmt = stmt.where(
                or_(
                    is_trilha_a & NormativeActModel.structured_content.is_(None),
                    is_trilha_b & NormativeActModel.metadata_json["triage_status"].is_(None),
                )
            )

        CHUNK_SIZE = 500

        total_acts: int | None = limit
        if total_acts is None:
            # SOTA-KISS: Instant approximate count from PostgreSQL catalog statistics (0.001s)
            # completely avoiding slow full-table COUNT(*) over 1.2M rows
            is_postgres = session.bind is not None and session.bind.dialect.name == "postgresql"
            if is_postgres and not date_str and not territory and not section and not only_failures:
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

        if total_acts is not None:
            print(f"Processing Stage 2 treatment for ~{total_acts} acts...")
        else:
            print("Processing Stage 2 treatment (continuous chunk stream)...")

        async def _treat_all() -> None:
            processed = 0
            last_seen_id: UUID | None = None
            with tqdm(total=total_acts, desc="Stage 2 Treatment", unit="act") as pbar:
                while True:
                    current_chunk_size = CHUNK_SIZE
                    if limit is not None:
                        remaining = limit - processed
                        if remaining <= 0:
                            break
                        current_chunk_size = min(CHUNK_SIZE, remaining)

                    chunk_stmt = stmt
                    if last_seen_id is not None:
                        chunk_stmt = chunk_stmt.where(NormativeActModel.id > last_seen_id)
                    chunk_stmt = chunk_stmt.order_by(NormativeActModel.id.asc()).limit(
                        current_chunk_size
                    )

                    models = session.scalars(chunk_stmt).all()
                    if not models:
                        break

                    for m in models:
                        last_seen_id = m.id
                        domain_act = gazette_repo.to_domain_act(m)
                        result = await use_case.execute(domain_act, auto_commit=False)
                        processed += 1
                        pbar.set_postfix(
                            track=result.track,
                            muts=result.mutations_extracted,
                        )
                        pbar.update(1)

                    # Single atomic commit per chunk of 500 items (ADR-015)
                    session.commit()

            if processed == 0:
                print("No pending acts found for Stage 2 treatment.")

        anyio.run(_treat_all)
        print("Stage 2 treatment completed successfully.")


def run_compile(identifier: str) -> None:
    """Compiles a statute's base AST and accumulated mutations into a read model."""
    session_factory = get_session_factory()

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
        compiled = use_case.execute(base_ast)
        print(f"Compiled act: {compiled.compiled_ast.title}")
        print(f"Version hash: {compiled.compiled_version_hash}")
        print(f"Total mutations applied: {compiled.total_mutations_applied}")
        print(
            f"Active articles: {compiled.active_articles_count} | "
            f"Revoked articles: {compiled.revoked_articles_count}"
        )


def run_query(identifier: str, as_of: str | None, output_format: str) -> None:
    """Queries compiled legislation text or performs on-demand time travel."""
    session_factory = get_session_factory()

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

        compiled: CompiledNormativeAct | None = None
        if as_of:
            cutoff = date.fromisoformat(as_of)
            if not act_model.structured_content:
                print("Error: Act structured content missing.")
                return
            base_ast = ActAst.from_dict(act_model.structured_content)
            tt_case = TimeTravelCompilationUseCase(repository=repo)
            compiled = tt_case.execute(base_ast, as_of=cutoff)
        else:
            compiled = repo.get_compiled_act(act_model.id)
            if not compiled and act_model.structured_content:
                base_ast = ActAst.from_dict(act_model.structured_content)
                c_case = CompileNormativeActUseCase(repository=repo)
                compiled = c_case.execute(base_ast)

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
        default=None,
        help="Spider name (options: federal_dou, or omit/'all' for all spiders).",
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
        "--territory", "-t", default=None, help="Territory code (default: all territories)"
    )
    treat_parser.add_argument(
        "--section",
        "-s",
        default=None,
        help="Gazette section (e.g. 1, 2, 3, extra; default: all sections)",
    )
    treat_parser.add_argument(
        "--limit", type=int, default=None, help="Maximum acts to process (default: all pending)"
    )
    treat_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-treatment of acts even if already processed.",
    )
    treat_parser.add_argument(
        "--only-failures",
        action="store_true",
        default=False,
        help="Only process/re-process acts flagged as needing manual review.",
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


def _is_likely_spider_or_date_shorthand(token: str) -> bool:
    """Returns True if token matches a known spider prefix, alias, or ISO date (LOW-01)."""
    clean = token.strip().lower()
    if clean in ("all", "dou", "federal_dou"):
        return True
    if clean.startswith(("state_", "federal_", "municipal_")):
        return True
    import re

    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", clean))


def parse_cli_args(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    valid_commands = ("init-db", "crawl", "treat", "compile", "query", "serve", "-h", "--help")
    if not raw_args:
        raw_args = ["crawl"]
    elif raw_args[0] not in valid_commands:
        if raw_args[0].startswith("-"):
            raw_args = ["crawl"] + raw_args
        elif _is_likely_spider_or_date_shorthand(raw_args[0]):
            raw_args = ["crawl"] + raw_args
        # Unrecognized commands remain untouched so ArgumentParser raises invalid choice error

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
            section=parsed_args.section,
            limit=parsed_args.limit,
            force=parsed_args.force,
            only_failures=parsed_args.only_failures,
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
