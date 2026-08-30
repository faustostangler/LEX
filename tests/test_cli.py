"""Precision Unit Tests for CLI Entrypoint.

Verifies default 'crawl' action, spider routing, --force flag, date options, and argument parsing.
"""

from unittest.mock import patch

from lex.cli import build_parser, main, parse_cli_args


def test_build_parser_structure() -> None:
    """Scenario: build_parser defines expected sub-commands and default values."""
    parser = build_parser()
    assert parser.prog == "lex"

    # Test crawl subcommand defaults
    args = parser.parse_args(["crawl"])
    assert args.command == "crawl"
    assert args.spider == "federal_dou"
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
    # Empty args -> crawl federal_dou
    parsed_empty = parse_cli_args([])
    assert parsed_empty.command == "crawl"
    assert parsed_empty.spider == "federal_dou"
    assert parsed_empty.force is False

    # Spider shorthand -> crawl state_sp
    parsed_spider = parse_cli_args(["state_sp", "--start-date", "2024-05-10"])
    assert parsed_spider.command == "crawl"
    assert parsed_spider.spider == "state_sp"
    assert parsed_spider.start_date == "2024-05-10"

    # Flag shorthand -> crawl federal_dou with flag
    parsed_flag = parse_cli_args(["--start-date", "2024-01-02"])
    assert parsed_flag.command == "crawl"
    assert parsed_flag.spider == "federal_dou"
    assert parsed_flag.start_date == "2024-01-02"


def test_cli_no_args_defaults_to_crawl_federal_dou() -> None:
    """Scenario: Invoking CLI with no arguments defaults to crawling federal_dou descending."""
    with patch("lex.cli.run_crawler") as mock_run_crawler:
        main([])
        mock_run_crawler.assert_called_once_with(
            spider_name="federal_dou",
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


def test_cli_flag_only_defaults_to_crawl_federal_dou() -> None:
    """Scenario: Running 'lex --start-date 2024-01-02' defaults spider to federal_dou."""
    with patch("lex.cli.run_crawler") as mock_run_crawler:
        main(["--start-date", "2024-01-02", "--force"])
        mock_run_crawler.assert_called_once_with(
            spider_name="federal_dou",
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
            spider_name="federal_dou",
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
