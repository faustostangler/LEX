"""Precision Unit Tests for Shared Kernel Configuration.

Verifies fail-fast behavior and validation boundaries for LexSettings
specified in SPEC-001 (Section 4 Scenario 4).
"""

import pytest
from pydantic import ValidationError

from lex.shared_kernel.config import LexSettings


class TestLexSettings:
    """Acceptance tests for LexSettings fail-fast configuration."""

    def test_valid_configuration(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Scenario: Valid environment variables load successfully."""
        monkeypatch.setenv("LEX_DATABASE_URL", "postgresql://user:pass@localhost:5432/lex_test")
        monkeypatch.setenv("LEX_MAX_MEMORY_SPOOL_MB", "25")
        monkeypatch.setenv("LEX_LOG_LEVEL", "DEBUG")

        settings = LexSettings()
        assert str(settings.database_url).startswith("postgresql://")
        assert settings.max_memory_spool_mb == 25
        assert settings.log_level == "DEBUG"
        assert settings.autothrottle_enabled is True

    def test_missing_mandatory_database_url_raises_validation_error(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Boundary condition: Missing LEX_DATABASE_URL fails fast at startup."""
        monkeypatch.delenv("LEX_DATABASE_URL", raising=False)

        with pytest.raises(ValidationError, match="LEX_DATABASE_URL must be defined"):
            LexSettings()
