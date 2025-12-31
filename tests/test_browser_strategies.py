#!/usr/bin/env python3
"""Unit tests for browser strategy implementations.

Tests individual browser strategies for Windows, macOS, Linux,
and the webbrowser fallback mechanism.
"""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gemini_query.browser.strategies import (
    BrowserStrategy,
    BrowserStrategyFactory,
    LinuxBrowserStrategy,
    MacOSBrowserStrategy,
    WebbrowserFallbackStrategy,
    WindowsBrowserStrategy,
)
from gemini_query.config import Platform
from gemini_query.config.legacy import AppConfig


class TestBrowserStrategy:
    """Test abstract base class behavior."""

    def test_abstract_base_class(self) -> None:
        """Test that BrowserStrategy is abstract and cannot be instantiated."""
        with pytest.raises(TypeError):
            BrowserStrategy(AppConfig())  # type: ignore


class TestWindowsBrowserStrategy:
    """Test Windows-specific browser strategy."""

    def test_get_commands_includes_start(self) -> None:
        """Test that Windows strategy includes 'start' command."""
        # Arrange
        config = AppConfig()
        strategy = WindowsBrowserStrategy(config)

        # Act
        commands = strategy.get_commands()

        # Assert
        assert 'start' in commands

    def test_get_commands_priority_order(self) -> None:
        """Test that user-configured paths have highest priority."""
        # Arrange
        config = AppConfig(browser_path=r"C:\custom\browser.exe")
        strategy = WindowsBrowserStrategy(config)

        with patch.object(Path, 'exists', return_value=True):
            # Act
            commands = strategy.get_commands()

            # Assert - Custom path should be first
            assert commands[0] == r"C:\custom\browser.exe"

    def test_get_commands_excludes_nonexistent_paths(self) -> None:
        """Test that non-existent paths are excluded."""
        # Arrange
        config = AppConfig(browser_path="/nonexistent/path")
        strategy = WindowsBrowserStrategy(config)

        with patch.object(Path, 'exists', return_value=False):
            # Act
            commands = strategy.get_commands()

            # Assert
            assert "/nonexistent/path" not in commands

    def test_get_commands_no_duplicates(self) -> None:
        """Test that command list has no duplicates."""
        # Arrange
        config = AppConfig()
        strategy = WindowsBrowserStrategy(config)

        # Act
        commands = strategy.get_commands()

        # Assert
        assert len(commands) == len(set(commands))

    @pytest.mark.asyncio
    async def test_execute_command_windows_start(self) -> None:
        """Test Windows 'start' command uses shell=True."""
        # Arrange
        config = AppConfig()
        strategy = WindowsBrowserStrategy(config)
        url = "https://example.com"

        # Mock asyncio subprocess
        mock_process = AsyncMock()
        mock_process.returncode = 0
        mock_process.communicate = AsyncMock(return_value=(b'', b''))

        with patch('asyncio.create_subprocess_shell', return_value=mock_process) as mock_shell:
            # Act
            return_code, stdout, stderr = await strategy._execute_command('start', url)

            # Assert
            assert return_code == 0
            mock_shell.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_execute_command_direct_executable(self) -> None:
        """Test direct executable uses create_subprocess_exec."""
        # Arrange
        config = AppConfig()
        strategy = WindowsBrowserStrategy(config)
        url = "https://example.com"

        mock_process = AsyncMock()
        mock_process.returncode = 0
        mock_process.communicate = AsyncMock(return_value=(b'', b''))

        with patch('asyncio.create_subprocess_exec', return_value=mock_process) as mock_exec:
            # Act
            return_code, stdout, stderr = await strategy._execute_command('firefox', url)

            # Assert
            assert return_code == 0
            mock_exec.assert_awaited_once()


class TestMacOSBrowserStrategy:
    """Test macOS-specific browser strategy."""

    def test_get_commands_includes_open(self) -> None:
        """Test macOS strategy includes 'open' command."""
        # Arrange
        config = AppConfig()
        strategy = MacOSBrowserStrategy(config)

        # Act
        commands = strategy.get_commands()

        # Assert
        assert 'open' in commands

    def test_get_commands_no_duplicates(self) -> None:
        """Test that command list has no duplicates."""
        # Arrange
        config = AppConfig()
        strategy = MacOSBrowserStrategy(config)

        # Act
        commands = strategy.get_commands()

        # Assert
        assert len(commands) == len(set(commands))


class TestLinuxBrowserStrategy:
    """Test Linux-specific browser strategy."""

    def test_get_commands_includes_xdg_open(self) -> None:
        """Test Linux includes xdg-open command."""
        # Arrange
        config = AppConfig()
        strategy = LinuxBrowserStrategy(config)

        # Act
        commands = strategy.get_commands()

        # Assert
        assert 'xdg-open' in commands

    def test_get_commands_includes_common_browsers(self) -> None:
        """Test Linux includes common browser commands."""
        # Arrange
        config = AppConfig()
        strategy = LinuxBrowserStrategy(config)

        # Act
        commands = strategy.get_commands()

        # Assert
        # At least one of the common browsers should be present
        common_browsers = ['firefox', 'google-chrome', 'chromium-browser']
        assert any(browser in commands for browser in common_browsers)

    def test_get_commands_no_duplicates(self) -> None:
        """Test that command list has no duplicates."""
        # Arrange
        config = AppConfig()
        strategy = LinuxBrowserStrategy(config)

        # Act
        commands = strategy.get_commands()

        # Assert
        assert len(commands) == len(set(commands))


class TestWebbrowserFallbackStrategy:
    """Test webbrowser module fallback strategy."""

    def test_get_commands_returns_webbrowser(self) -> None:
        """Test fallback strategy only uses webbrowser."""
        # Arrange
        config = AppConfig()
        strategy = WebbrowserFallbackStrategy(config)

        # Act
        commands = strategy.get_commands()

        # Assert
        assert commands == ['webbrowser']

    @pytest.mark.asyncio
    async def test_execute_command_success(self) -> None:
        """Test successful webbrowser.open() call."""
        # Arrange
        config = AppConfig()
        strategy = WebbrowserFallbackStrategy(config)

        with patch('webbrowser.open', return_value=True) as mock_open:
            # Act
            return_code, stdout, stderr = await strategy._execute_command(
                'webbrowser', 'https://example.com'
            )

            # Assert
            assert return_code == 0
            mock_open.assert_called_once_with('https://example.com')

    @pytest.mark.asyncio
    async def test_execute_command_failure(self) -> None:
        """Test webbrowser.open() returning False."""
        # Arrange
        config = AppConfig()
        strategy = WebbrowserFallbackStrategy(config)

        with patch('webbrowser.open', return_value=False):
            # Act
            return_code, stdout, stderr = await strategy._execute_command(
                'webbrowser', 'https://example.com'
            )

            # Assert
            assert return_code == 1
            assert 'False' in stderr

    @pytest.mark.asyncio
    async def test_execute_command_exception(self) -> None:
        """Test exception handling in webbrowser.open()."""
        # Arrange
        config = AppConfig()
        strategy = WebbrowserFallbackStrategy(config)

        with patch('webbrowser.open', side_effect=RuntimeError("Browser error")):
            # Act
            return_code, stdout, stderr = await strategy._execute_command(
                'webbrowser', 'https://example.com'
            )

            # Assert
            assert return_code == 1
            assert 'Browser error' in stderr


class TestBrowserStrategyFactory:
    """Test browser strategy factory."""

    def test_create_strategy_windows(self) -> None:
        """Test factory creates Windows strategy."""
        # Arrange
        config = AppConfig()

        # Act
        strategy = BrowserStrategyFactory.create_strategy(
            config, platform=Platform.WINDOWS
        )

        # Assert
        assert isinstance(strategy, WindowsBrowserStrategy)

    def test_create_strategy_macos(self) -> None:
        """Test factory creates macOS strategy."""
        # Arrange
        config = AppConfig()

        # Act
        strategy = BrowserStrategyFactory.create_strategy(
            config, platform=Platform.MACOS
        )

        # Assert
        assert isinstance(strategy, MacOSBrowserStrategy)

    def test_create_strategy_linux(self) -> None:
        """Test factory creates Linux strategy."""
        # Arrange
        config = AppConfig()

        # Act
        strategy = BrowserStrategyFactory.create_strategy(
            config, platform=Platform.LINUX
        )

        # Assert
        assert isinstance(strategy, LinuxBrowserStrategy)

    def test_create_fallback_strategy(self) -> None:
        """Test factory creates fallback strategy."""
        # Arrange
        config = AppConfig()

        # Act
        strategy = BrowserStrategyFactory.create_fallback_strategy(config)

        # Assert
        assert isinstance(strategy, WebbrowserFallbackStrategy)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
