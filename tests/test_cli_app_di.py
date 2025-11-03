"""Tests for CLI application with dependency injection."""

import pytest
from unittest.mock import patch

# Note: CLI app is now in bases, not available as module
# This test needs to be updated to test the actual CLI commands via typer
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "bases"))

from gemini_query.cli_app.core import app, get_container


class TestCLIAppDI:
    """Test cases for CLI application dependency injection."""

    def test_create_app_with_default_profile(self):
        """Test app creation with default profile."""
        app = create_app()

        assert app is not None
        assert isinstance(app, CLIApp)

    def test_create_app_with_custom_profile(self):
        """Test app creation with custom profile."""
        app = create_app("test")

        assert app is not None
        assert isinstance(app, CLIApp)

    def test_cli_app_initialization(self):
        """Test that CLI app initializes correctly."""
        app = CLIApp()
        assert app is not None

    def test_run_query_basic_functionality(self):
        """Test run_query method with basic functionality."""
        app = CLIApp()

        # Test run_query doesn't raise exceptions
        with patch('gemini_query.cli_app.core.console') as mock_console:
            app.run_query("test query")

            # Verify some output was generated
            assert mock_console.print.call_count >= 1

    def test_run_query_interactive_mode(self):
        """Test run_query with interactive flag."""
        app = CLIApp()

        with patch('gemini_query.cli_app.core.console') as mock_console:
            app.run_query("test query", interactive=True)

            # Verify output includes interactive mode indication
            calls = [str(call) for call in mock_console.print.call_args_list]
            assert any("Interactive mode: True" in call for call in calls)

    def test_run_query_handles_exceptions(self):
        """Test that run_query properly handles exceptions."""
        import typer

        app = CLIApp()

        # Mock console.print to raise an exception on the third call
        with patch('gemini_query.cli_app.core.console') as mock_console:
            mock_console.print.side_effect = [None, None, Exception("Test error"), None]

            with pytest.raises(typer.Exit):  # typer.Exit raises specific Exit exception
                app.run_query("test query")

    def test_create_app_uses_di_container(self):
        """Test that create_app uses DI container."""
        with patch('gemini_query.di.container.create_container') as mock_create:
            mock_create.return_value = object()  # Mock container

            app = create_app("development")

            assert app is not None
            mock_create.assert_called_once_with("development")