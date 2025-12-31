"""Tests for CLI application with Typer framework and dependency injection.

Tests the Typer-based CLI commands, DI container integration,
and error handling.
"""

import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

# Add bases directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "bases"))

from gemini_query.cli_app.core import app, get_container


class TestTyperCLICommands:
    """Test cases for Typer-based CLI commands."""

    def test_app_help_displays_correctly(self, cli_runner: CliRunner) -> None:
        """Test that CLI help message displays without errors."""
        result = cli_runner.invoke(app, ["--help"])

        assert result.exit_code == 0
        assert "gemini-query" in result.stdout
        assert "Advanced CLI for Google Gemini AI" in result.stdout

    def test_version_option_displays_version(self, cli_runner: CliRunner) -> None:
        """Test --version option displays version and exits."""
        result = cli_runner.invoke(app, ["--version"])

        assert result.exit_code == 0
        assert "gemini-query version" in result.stdout


class TestDIContainerIntegration:
    """Test cases for DI container integration with CLI."""

    def test_get_container_creates_singleton(self) -> None:
        """Test get_container() returns same instance on multiple calls."""
        # Reset module-level container
        import gemini_query.cli_app.core

        gemini_query.cli_app.core.container = None

        container1 = get_container()
        container2 = get_container()

        assert container1 is container2

        # Cleanup
        gemini_query.cli_app.core.container = None

    def test_get_container_returns_configured_container(self) -> None:
        """Test get_container() returns properly configured Container instance."""
        # Reset module-level container
        import gemini_query.cli_app.core

        gemini_query.cli_app.core.container = None

        container = get_container()

        # Verify container has necessary providers
        assert container is not None
        assert hasattr(container, "query_processor")
        assert hasattr(container, "browser_manager")
        assert hasattr(container, "url_generator")

        # Cleanup
        gemini_query.cli_app.core.container = None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
