"""Precision Unit Tests for CLI Entrypoint.

Verifies default 'crawl' action, spider routing, and argument pre-processing.
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
    assert args.start_date is None
    assert args.end_date is None

    # Test init-db subcommand
    args_db = parser.parse_args(["init-db"])
    assert args_db.command == "init-db"


def test_parse_cli_args_shorthand_routing() -> None:
    """Scenario: parse_cli_args normalizes shorthand arguments."""
    # Empty args -> crawl federal_dou
    parsed_empty = parse_cli_args([])
    assert parsed_empty.command == "crawl"
    assert parsed_empty.spider == "federal_dou"

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
    """Scenario: Invoking CLI with no arguments defaults to crawling federal_dou for today."""
    with patch("lex.cli.run_crawler") as mock_run_crawler:
        main([])
        mock_run_crawler.assert_called_once_with("federal_dou", None, None)


def test_cli_spider_name_shorthand_defaults_to_crawl() -> None:
    """Scenario: Running 'lex state_sp' automatically routes to crawl state_sp."""
    with patch("lex.cli.run_crawler") as mock_run_crawler:
        main(["state_sp", "--start-date", "2024-05-10"])
        mock_run_crawler.assert_called_once_with("state_sp", "2024-05-10", None)


def test_cli_flag_only_defaults_to_crawl_federal_dou() -> None:
    """Scenario: Running 'lex --start-date 2024-01-02' defaults spider to federal_dou."""
    with patch("lex.cli.run_crawler") as mock_run_crawler:
        main(["--start-date", "2024-01-02"])
        mock_run_crawler.assert_called_once_with("federal_dou", "2024-01-02", None)


def test_cli_init_db_routing() -> None:
    """Scenario: 'init-db' command calls init_db function."""
    with patch("lex.cli.init_db") as mock_init_db:
        main(["init-db"])
        mock_init_db.assert_called_once()
