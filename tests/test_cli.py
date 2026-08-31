"""Precision Unit Tests for CLI Entrypoint.

Verifies default 'crawl' action, spider routing, --force flag, date options, and argument parsing.
"""

from typing import Any
from unittest.mock import patch

import pytest

from lex.cli import build_parser, main, parse_cli_args


def test_build_parser_structure() -> None:
    """Scenario: build_parser defines expected sub-commands and default values."""
    parser = build_parser()
    assert parser.prog == "lex"

    # Test crawl subcommand defaults
    args = parser.parse_args(["crawl"])
    assert args.command == "crawl"
    assert args.spider is None
    assert args.date is None
    assert args.start_date is None
    assert args.end_date is None
    assert args.ascending is False
    assert args.force is False

    # Test crawl subcommand with force and ascending
    args_forced = parser.parse_args(["crawl", "--force", "--ascending"])
    assert args_forced.force is True
    assert args_forced.ascending is True

    # Test init-db subcommand
    args_db = parser.parse_args(["init-db"])
    assert args_db.command == "init-db"


def test_parse_cli_args_shorthand_routing() -> None:
    """Scenario: parse_cli_args normalizes shorthand arguments."""
    # Empty args -> crawl all
    parsed_empty = parse_cli_args([])
    assert parsed_empty.command == "crawl"
    assert parsed_empty.spider is None
    assert parsed_empty.force is False

    # Spider shorthand -> crawl state_sp
    parsed_spider = parse_cli_args(["state_sp", "--start-date", "2024-05-10"])
    assert parsed_spider.command == "crawl"
    assert parsed_spider.spider == "state_sp"
    assert parsed_spider.start_date == "2024-05-10"

    # Flag shorthand -> crawl with flag (defaults to all spiders)
    parsed_flag = parse_cli_args(["--start-date", "2024-01-02"])
    assert parsed_flag.command == "crawl"
    assert parsed_flag.spider is None
    assert parsed_flag.start_date == "2024-01-02"


def test_parse_cli_args_invalid_command_raises_system_exit() -> None:
    """Scenario: Passing an invalid command raises SystemExit and does not crawl (LOW-01)."""
    with pytest.raises(SystemExit):
        parse_cli_args(["treate", "--date", "2024-01-02"])

    with pytest.raises(SystemExit):
        parse_cli_args(["unknown_cmd"])


def test_cli_no_args_defaults_to_crawl_all_spiders() -> None:
    """Scenario: Invoking CLI with no arguments defaults to crawling all spiders descending."""
    with patch("lex.cli.run_crawler") as mock_run_crawler:
        main([])
        mock_run_crawler.assert_called_once_with(
            spider_name=None,
            start_date=None,
            end_date=None,
            single_date=None,
            force=False,
            reverse=True,
        )


def test_cli_spider_name_shorthand_defaults_to_crawl() -> None:
    """Scenario: Running 'lex state_sp' automatically routes to crawl state_sp."""
    with patch("lex.cli.run_crawler") as mock_run_crawler:
        main(["state_sp", "--start-date", "2024-05-10"])
        mock_run_crawler.assert_called_once_with(
            spider_name="state_sp",
            start_date="2024-05-10",
            end_date=None,
            single_date=None,
            force=False,
            reverse=True,
        )


def test_cli_flag_only_defaults_to_crawl_all_spiders() -> None:
    """Scenario: Running 'lex --start-date 2024-01-02' defaults spider to None (all)."""
    with patch("lex.cli.run_crawler") as mock_run_crawler:
        main(["--start-date", "2024-01-02", "--force"])
        mock_run_crawler.assert_called_once_with(
            spider_name=None,
            start_date="2024-01-02",
            end_date=None,
            single_date=None,
            force=True,
            reverse=True,
        )


def test_cli_single_date_shorthand() -> None:
    """Scenario: Running 'lex --date 2024-01-15' targets single date."""
    with patch("lex.cli.run_crawler") as mock_run_crawler:
        main(["--date", "2024-01-15"])
        mock_run_crawler.assert_called_once_with(
            spider_name=None,
            start_date=None,
            end_date=None,
            single_date="2024-01-15",
            force=False,
            reverse=True,
        )


def test_cli_init_db_routing() -> None:
    """Scenario: 'init-db' command calls init_db function."""
    with patch("lex.cli.init_db") as mock_init_db:
        main(["init-db"])
        mock_init_db.assert_called_once()


def test_cli_treat_routing() -> None:
    """Scenario: 'treat' command calls run_treat function."""
    with patch("lex.cli.run_treat") as mock_run_treat:
        main(
            [
                "treat",
                "--date",
                "2024-01-15",
                "--territory",
                "BR",
                "--section",
                "1",
                "--limit",
                "50",
            ]
        )
        mock_run_treat.assert_called_once_with(
            date_str="2024-01-15",
            territory="BR",
            section="1",
            limit=50,
            force=False,
            only_failures=False,
        )


def test_cli_treat_force_and_failures_routing() -> None:
    """Scenario: 'treat --force --only-failures' passes flags correctly to run_treat."""
    with patch("lex.cli.run_treat") as mock_run_treat:
        main(["treat", "--force", "--only-failures"])
        mock_run_treat.assert_called_once_with(
            date_str=None,
            territory=None,
            section=None,
            limit=None,
            force=True,
            only_failures=True,
        )


def test_cli_compile_routing() -> None:
    """Scenario: 'compile' command calls run_compile function."""
    with patch("lex.cli.run_compile") as mock_run_compile:
        main(["compile", "urn:lex:br:federal:lei:1993;8666"])
        mock_run_compile.assert_called_once_with(identifier="urn:lex:br:federal:lei:1993;8666")


def test_cli_query_routing() -> None:
    """Scenario: 'query' command calls run_query function."""
    with patch("lex.cli.run_query") as mock_run_query:
        main(
            [
                "query",
                "urn:lex:br:federal:lei:1993;8666",
                "--as-of",
                "2020-01-01",
                "--format",
                "html",
            ]
        )
        mock_run_query.assert_called_once_with(
            identifier="urn:lex:br:federal:lei:1993;8666",
            as_of="2020-01-01",
            output_format="html",
        )


def test_run_treat_keyset_pagination(monkeypatch: pytest.MonkeyPatch) -> None:
    """Scenario: run_treat executes streaming keyset cursor pagination."""
    import uuid
    from datetime import UTC, date, datetime
    from unittest.mock import AsyncMock, MagicMock

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool

    from lex.cli import run_treat
    from lex.ingestion.infrastructure.persistence.models import Base, NormativeActModel

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)

    # Insert 3 test acts
    with session_factory() as session:
        edition_id = uuid.uuid4()
        for i in range(3):
            act = NormativeActModel(
                id=uuid.uuid4(),
                edition_id=edition_id,
                territory_id="BR",
                date=date(2024, 1, 2),
                section="secao_1",
                edition_number="1",
                is_extra_edition=False,
                act_type="LEI",
                title=f"Lei {i}",
                canonical_urn=f"urn:lex:br:federal:lei:2024;{i}",
                publication_nature="normativa_abstrata",
                raw_content=f"Art. 1 Texto {i}",
                content_sha256=f"{i}" * 64,
                char_count=20,
                source_url=f"https://in.gov.br/{i}",
                scraped_at=datetime.now(UTC),
            )
            session.add(act)
        session.commit()

    monkeypatch.setattr("lex.cli.get_session_factory", lambda **kwargs: session_factory)

    with patch("lex.cli.ProcessNormativeActUseCase") as mock_use_case_cls:
        mock_instance = MagicMock()
        mock_instance.execute = AsyncMock(return_value=MagicMock(track="A", mutations_extracted=0))
        mock_use_case_cls.return_value = mock_instance

        run_treat(force=True, limit=2)
        assert mock_instance.execute.call_count == 2


def test_run_treat_handles_negative_catalog_statistics(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Scenario: Negative or non-positive reltuples from pg_class fallback to continuous stream."""
    import uuid
    from datetime import UTC, date, datetime
    from unittest.mock import AsyncMock, MagicMock

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool

    from lex.cli import run_treat
    from lex.ingestion.infrastructure.persistence.models import Base, NormativeActModel

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)

    with session_factory() as session:
        act = NormativeActModel(
            id=uuid.uuid4(),
            edition_id=uuid.uuid4(),
            territory_id="BR",
            date=date(2024, 1, 2),
            section="secao_1",
            edition_number="1",
            is_extra_edition=False,
            act_type="LEI",
            title="Lei Teste",
            canonical_urn="urn:lex:br:federal:lei:2024;1",
            publication_nature="normativa_abstrata",
            raw_content="Art. 1 Texto",
            content_sha256="1" * 64,
            char_count=20,
            source_url="https://in.gov.br/1",
            scraped_at=datetime.now(UTC),
        )
        session.add(act)
        session.commit()

    # Mock session dialect as postgresql returning -1 for reltuples (unanalyzed catalog state)
    orig_session_factory = sessionmaker(bind=engine)

    class MockSession:
        def __init__(self) -> None:
            self._real_session = orig_session_factory()
            mock_bind = MagicMock()
            mock_bind.dialect.name = "postgresql"
            self.bind = mock_bind

        def execute(self, *args: Any, **kwargs: Any) -> Any:
            mock_res = MagicMock()
            mock_res.scalar.return_value = -1  # Negative reltuples!
            return mock_res

        def scalars(self, *args: Any, **kwargs: Any) -> Any:
            return self._real_session.scalars(*args, **kwargs)

        def commit(self) -> None:
            self._real_session.commit()

        def rollback(self) -> None:
            self._real_session.rollback()

        def close(self) -> None:
            self._real_session.close()

        def __enter__(self) -> "MockSession":
            return self

        def __exit__(self, *args: Any) -> None:
            self.close()

    monkeypatch.setattr("lex.cli.get_session_factory", lambda **kwargs: (lambda: MockSession()))

    with patch("lex.cli.ProcessNormativeActUseCase") as mock_use_case_cls:
        mock_instance = MagicMock()
        mock_instance.execute = AsyncMock(return_value=MagicMock(track="A", mutations_extracted=0))
        mock_use_case_cls.return_value = mock_instance

        run_treat(force=True, limit=None)
        assert mock_instance.execute.call_count == 1

    captured = capsys.readouterr()
    assert "Processing Stage 2 treatment (continuous chunk stream)..." in captured.out
