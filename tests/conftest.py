"""Shared pytest fixtures and helpers for async browser testing and CLI testing.

Provides reusable fixtures for browser testing with async/await support
and Typer CLI testing.
"""

import sys
from collections.abc import Callable
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, Mock

import pytest
from typer.testing import CliRunner

# Add bases directory to path for CLI imports
sys.path.insert(0, str(Path(__file__).parent.parent / "bases"))

from gemini_query.browser.service import BrowserManager
from gemini_query.browser.strategies import BrowserStrategy
from gemini_query.config.legacy import AppConfig


@pytest.fixture
def app_config() -> AppConfig:
    """Create test configuration with default values.

    Returns:
        AppConfig instance for testing
    """
    return AppConfig()


@pytest.fixture
def mock_browser_strategy() -> BrowserStrategy:
    """Create mock browser strategy for testing.

    Returns:
        Mock BrowserStrategy with common methods mocked
    """
    strategy = Mock(spec=BrowserStrategy)
    strategy.launch = AsyncMock(return_value=True)
    strategy.get_commands = Mock(return_value=['firefox', 'chrome'])
    strategy._execute_command = AsyncMock(return_value=(0, '', ''))
    return strategy


@pytest.fixture
async def browser_manager(app_config: AppConfig) -> BrowserManager:
    """Create browser manager instance for testing.

    Note: This is an async fixture for proper cleanup.

    Args:
        app_config: Application configuration fixture

    Yields:
        BrowserManager instance
    """
    manager = BrowserManager(app_config)
    yield manager
    # Async cleanup if needed in future
    # await manager.cleanup()


@pytest.fixture
def mock_subprocess_success() -> AsyncMock:
    """Create mock subprocess that succeeds.

    Returns:
        Mock process with returncode 0
    """
    process = AsyncMock()
    process.returncode = 0
    process.communicate = AsyncMock(return_value=(b'stdout', b''))
    return process


@pytest.fixture
def mock_subprocess_failure() -> AsyncMock:
    """Create mock subprocess that fails.

    Returns:
        Mock process with returncode 1
    """
    process = AsyncMock()
    process.returncode = 1
    process.communicate = AsyncMock(return_value=(b'', b'error message'))
    return process


@pytest.fixture
def async_timeout() -> float:
    """Default timeout for async operations in tests.

    Returns:
        Timeout in seconds (1.0 is enough for mocked operations)
    """
    return 1.0


# ============================================================================
# CLI Testing Fixtures
# ============================================================================


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provide CliRunner for Typer CLI testing.

    Returns:
        CliRunner instance
    """
    return CliRunner()


@pytest.fixture
def mock_container_factory() -> Callable[[bool, Exception | None], MagicMock]:
    """Factory for creating mock DI containers with configurable behavior.

    Returns:
        Function that creates mock containers with:
        - success: Whether process_query should succeed
        - error: Exception to raise (if any)
    """

    def _create_mock(success: bool = True, error: Exception | None = None) -> MagicMock:
        """Create a mock DI container.

        Args:
            success: Whether the query processor should succeed
            error: Optional exception to raise

        Returns:
            Mock DI container with configured behavior
        """
        mock = MagicMock()
        mock_processor = AsyncMock()

        if error:
            mock_processor.process_query.side_effect = error
        else:
            mock_processor.process_query = AsyncMock(return_value=success)

        mock.query_processor.return_value = mock_processor
        return mock

    return _create_mock
