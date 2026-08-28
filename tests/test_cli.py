"""Precision Unit Tests for CLI Entrypoint.

Verifies default 'crawl' action, spider routing, and argument pre-processing.
"""

from unittest.mock import patch

from lex.cli import main


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
