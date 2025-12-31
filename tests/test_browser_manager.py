#!/usr/bin/env python3
"""Integration tests for BrowserManager orchestration layer.

Tests the coordination between BrowserManager and its strategies,
focusing on fallback mechanisms and public API behavior.
"""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, Mock

import pytest

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gemini_query.browser.service import BrowserManager
from gemini_query.browser.strategies import BrowserStrategy
from gemini_query.config.legacy import AppConfig


@pytest.mark.asyncio
class TestBrowserManagerIntegration:
    """Test BrowserManager orchestration and strategy coordination."""

    async def test_launch_success_with_primary_strategy(self) -> None:
        """Test successful launch using primary strategy."""
        # Arrange
        config = AppConfig()
        manager = BrowserManager(config)

        # Mock primary strategy to succeed
        manager.primary_strategy.launch = AsyncMock(return_value=True)
        manager.fallback_strategy.launch = AsyncMock(return_value=False)

        # Act
        result = await manager.launch("https://example.com")

        # Assert
        assert result is True
        manager.primary_strategy.launch.assert_awaited_once_with("https://example.com")
        manager.fallback_strategy.launch.assert_not_awaited()

    async def test_launch_fallback_when_primary_fails(self) -> None:
        """Test fallback strategy activates when primary fails."""
        # Arrange
        config = AppConfig()
        manager = BrowserManager(config)

        # Primary fails, fallback succeeds
        manager.primary_strategy.launch = AsyncMock(return_value=False)
        manager.fallback_strategy.launch = AsyncMock(return_value=True)

        # Act
        result = await manager.launch("https://example.com")

        # Assert
        assert result is True
        manager.primary_strategy.launch.assert_awaited_once()
        manager.fallback_strategy.launch.assert_awaited_once()

    async def test_launch_all_strategies_fail(self) -> None:
        """Test behavior when all strategies fail."""
        # Arrange
        config = AppConfig()
        manager = BrowserManager(config)

        # Both strategies fail
        manager.primary_strategy.launch = AsyncMock(return_value=False)
        manager.fallback_strategy.launch = AsyncMock(return_value=False)

        # Act
        result = await manager.launch("https://example.com")

        # Assert
        assert result is False

    async def test_launch_primary_raises_exception(self) -> None:
        """Test that exceptions from primary strategy trigger fallback."""
        # Arrange
        config = AppConfig()
        manager = BrowserManager(config)

        # Primary raises exception, fallback succeeds
        manager.primary_strategy.launch = AsyncMock(
            side_effect=RuntimeError("Browser not found")
        )
        manager.fallback_strategy.launch = AsyncMock(return_value=True)

        # Act
        result = await manager.launch("https://example.com")

        # Assert
        assert result is True
        manager.fallback_strategy.launch.assert_awaited_once()

    async def test_launch_both_strategies_raise_exceptions(self) -> None:
        """Test behavior when both strategies raise exceptions."""
        # Arrange
        config = AppConfig()
        manager = BrowserManager(config)

        # Both strategies raise exceptions
        manager.primary_strategy.launch = AsyncMock(
            side_effect=RuntimeError("Primary failed")
        )
        manager.fallback_strategy.launch = AsyncMock(
            side_effect=RuntimeError("Fallback failed")
        )

        # Act
        result = await manager.launch("https://example.com")

        # Assert
        assert result is False

    def test_get_available_commands_aggregates_strategies(self) -> None:
        """Test that available commands are aggregated from all strategies."""
        # Arrange
        config = AppConfig()
        manager = BrowserManager(config)

        manager.primary_strategy.get_commands = Mock(
            return_value=['firefox', 'chrome']
        )
        manager.fallback_strategy.get_commands = Mock(
            return_value=['webbrowser']
        )

        # Act
        commands = manager.get_available_commands()

        # Assert
        assert 'firefox' in commands
        assert 'chrome' in commands
        assert 'webbrowser' in commands
        # Check deduplication (no duplicates)
        assert len(commands) == len(set(commands))

    def test_get_available_commands_deduplicates(self) -> None:
        """Test that duplicate commands are removed."""
        # Arrange
        config = AppConfig()
        manager = BrowserManager(config)

        # Both strategies return overlapping commands
        manager.primary_strategy.get_commands = Mock(
            return_value=['firefox', 'chrome', 'edge']
        )
        manager.fallback_strategy.get_commands = Mock(
            return_value=['chrome', 'webbrowser']
        )

        # Act
        commands = manager.get_available_commands()

        # Assert
        assert len(commands) == len(set(commands))
        assert 'firefox' in commands
        assert 'chrome' in commands
        assert 'edge' in commands
        assert 'webbrowser' in commands

    def test_set_custom_strategy(self) -> None:
        """Test custom strategy injection for testing."""
        # Arrange
        config = AppConfig()
        manager = BrowserManager(config)

        custom_strategy = Mock(spec=BrowserStrategy)
        custom_strategy.__class__.__name__ = "CustomStrategy"

        # Act
        manager.set_custom_strategy(custom_strategy)

        # Assert
        assert manager.primary_strategy == custom_strategy


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
