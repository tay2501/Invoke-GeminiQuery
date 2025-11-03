#!/usr/bin/env python3
"""Browser strategy implementations following modern async Python best practices.

This module implements the Strategy pattern for cross-platform browser automation
using async/await for improved performance and resource management.

Key improvements:
- Async subprocess management with asyncio
- EAFP (Easier to Ask for Forgiveness than Permission) error handling
- Structured logging with context
- Type hints throughout
"""

import asyncio
from abc import ABC, abstractmethod
from pathlib import Path

from gemini_query.config import AppConfig, Platform
from gemini_query.logging import get_logger


class BrowserStrategy(ABC):
    """Abstract base class for async browser launching strategies.

    Implements the Strategy pattern with async/await support for
    improved performance and resource management.
    """

    def __init__(self, config: AppConfig) -> None:
        """Initialize browser strategy with configuration.

        Args:
            config: Application configuration instance
        """
        self.config = config
        self.logger = get_logger(f"browser.{self.__class__.__name__}")

    @abstractmethod
    def get_commands(self) -> list[str]:
        """Get browser commands in priority order.

        Returns:
            List of command strings to attempt
        """
        ...

    @abstractmethod
    async def _execute_command(self, command: str, url: str) -> tuple[int, str, str]:
        """Execute browser command asynchronously.

        Args:
            command: Browser command to execute
            url: URL to open

        Returns:
            Tuple of (return_code, stdout, stderr)

        Raises:
            BrowserStrategyError: If command execution fails critically
        """
        ...

    async def launch(self, url: str) -> bool:
        """Launch browser with specified URL using async subprocess.

        Tries each command in priority order until one succeeds.
        Uses EAFP principle for error handling.

        Args:
            url: URL to open in browser

        Returns:
            True if any command succeeded, False otherwise
        """
        commands = self.get_commands()

        for command in commands:
            try:
                success = await self._try_command(command, url)
                if success:
                    return True
            except Exception as error:
                self.logger.debug(
                    "Command attempt failed with exception",
                    command=command,
                    error=str(error),
                    error_type=type(error).__name__
                )
                continue

        return False

    async def _try_command(self, command: str, url: str) -> bool:
        """Try to execute a browser command asynchronously.

        Uses EAFP principle - attempts execution and handles exceptions.

        Args:
            command: Browser command to try
            url: URL to open

        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.debug("Attempting browser launch", command=command)

            return_code, stdout, stderr = await self._execute_command(command, url)

            if return_code == 0:
                self.logger.info("Browser launched successfully", command=command)
                return True

            self.logger.debug(
                "Browser command failed",
                command=command,
                return_code=return_code,
                stderr=stderr.strip() if stderr else None
            )
            return False

        except TimeoutError:
            self.logger.debug("Browser command timed out", command=command)
            return False
        except FileNotFoundError:
            self.logger.debug("Browser command not found", command=command)
            return False
        except OSError as error:
            # EAFP: catch OS-level errors like permission denied
            self.logger.debug(
                "OS error during browser launch",
                command=command,
                error=str(error)
            )
            return False


class WindowsBrowserStrategy(BrowserStrategy):
    """Windows-specific async browser launching strategy.

    Uses Windows-specific commands like 'start' and auto-detects
    common browser installation paths.
    """

    def get_commands(self) -> list[str]:
        """Get Windows browser commands in priority order.

        Returns:
            Deduplicated list of browser commands to try
        """
        commands: list[str] = []

        # User-configured paths (highest priority)
        commands.extend(self._get_user_paths())

        # Auto-detected Windows paths
        commands.extend(self._get_windows_paths())

        # System commands
        commands.append('start')

        # Standard browser commands
        commands.extend(['firefox', 'chrome', 'msedge'])

        # Remove duplicates while preserving order
        return list(dict.fromkeys(commands))

    def _get_user_paths(self) -> list[str]:
        """Get user-configured browser paths using EAFP.

        Returns:
            List of valid user-configured paths
        """
        paths: list[str] = []

        # EAFP: try to use paths, catch AttributeError if not set
        try:
            if self.config.browser_path:
                browser_path = Path(self.config.browser_path)
                if browser_path.exists():
                    paths.append(str(browser_path))
        except (AttributeError, TypeError):
            pass

        try:
            if hasattr(self.config, 'firefox_path') and self.config.firefox_path:
                firefox_path = Path(self.config.firefox_path)
                if firefox_path.exists():
                    paths.append(str(firefox_path))
        except (AttributeError, TypeError):
            pass

        return paths

    def _get_windows_paths(self) -> list[str]:
        """Get auto-detected Windows browser paths.

        Returns:
            List of existing browser executable paths
        """
        potential_paths = [
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        ]

        # EAFP: try each path, ignore if doesn't exist
        existing_paths: list[str] = []
        for path_str in potential_paths:
            try:
                path = Path(path_str)
                if path.exists():
                    existing_paths.append(path_str)
            except (OSError, ValueError):
                continue

        return existing_paths

    async def _execute_command(self, command: str, url: str) -> tuple[int, str, str]:
        """Execute Windows browser command asynchronously.

        Args:
            command: Browser command or path to execute
            url: URL to open

        Returns:
            Tuple of (return_code, stdout, stderr)

        Raises:
            asyncio.TimeoutError: If command times out
        """
        timeout = getattr(self.config, 'browser_timeout', 5.0)

        if command == 'start':
            # Windows start command requires shell=True
            process = await asyncio.create_subprocess_shell(
                f'start "" "{url}"',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
        else:
            # Direct executable
            process = await asyncio.create_subprocess_exec(
                command,
                url,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

        try:
            stdout_bytes, stderr_bytes = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
            return_code = process.returncode or 0
            stdout = stdout_bytes.decode('utf-8', errors='ignore')
            stderr = stderr_bytes.decode('utf-8', errors='ignore')

            return (return_code, stdout, stderr)

        except TimeoutError:
            # Kill process on timeout
            try:
                process.kill()
                await process.wait()
            except ProcessLookupError:
                pass
            raise


class MacOSBrowserStrategy(BrowserStrategy):
    """macOS-specific async browser launching strategy.

    Uses macOS-specific commands like 'open' and auto-detects
    common browser installation paths in /Applications.
    """

    def get_commands(self) -> list[str]:
        """Get macOS browser commands in priority order.

        Returns:
            Deduplicated list of browser commands to try
        """
        commands: list[str] = []

        # User-configured paths
        commands.extend(self._get_user_paths())

        # Auto-detected macOS paths
        commands.extend(self._get_macos_paths())

        # System commands
        commands.append('open')

        # Standard browser commands
        commands.extend(['firefox', 'chrome', 'safari'])

        return list(dict.fromkeys(commands))

    def _get_user_paths(self) -> list[str]:
        """Get user-configured browser paths using EAFP.

        Returns:
            List of valid user-configured paths
        """
        paths: list[str] = []

        try:
            if self.config.browser_path:
                browser_path = Path(self.config.browser_path)
                if browser_path.exists():
                    paths.append(str(browser_path))
        except (AttributeError, TypeError):
            pass

        return paths

    def _get_macos_paths(self) -> list[str]:
        """Get auto-detected macOS browser paths.

        Returns:
            List of existing browser executable paths
        """
        potential_paths = [
            "/Applications/Firefox.app/Contents/MacOS/firefox",
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Safari.app/Contents/MacOS/Safari",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        ]

        existing_paths: list[str] = []
        for path_str in potential_paths:
            try:
                path = Path(path_str)
                if path.exists():
                    existing_paths.append(path_str)
            except (OSError, ValueError):
                continue

        return existing_paths

    async def _execute_command(self, command: str, url: str) -> tuple[int, str, str]:
        """Execute macOS browser command asynchronously.

        Args:
            command: Browser command or path to execute
            url: URL to open

        Returns:
            Tuple of (return_code, stdout, stderr)

        Raises:
            asyncio.TimeoutError: If command times out
        """
        timeout = getattr(self.config, 'browser_timeout', 5.0)

        process = await asyncio.create_subprocess_exec(
            command,
            url,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        try:
            stdout_bytes, stderr_bytes = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
            return_code = process.returncode or 0
            stdout = stdout_bytes.decode('utf-8', errors='ignore')
            stderr = stderr_bytes.decode('utf-8', errors='ignore')

            return (return_code, stdout, stderr)

        except TimeoutError:
            try:
                process.kill()
                await process.wait()
            except ProcessLookupError:
                pass
            raise


class LinuxBrowserStrategy(BrowserStrategy):
    """Linux-specific async browser launching strategy.

    Uses Linux-specific commands like 'xdg-open' and standard
    browser commands available in PATH.
    """

    def get_commands(self) -> list[str]:
        """Get Linux browser commands in priority order.

        Returns:
            Deduplicated list of browser commands to try
        """
        commands: list[str] = []

        # User-configured paths
        commands.extend(self._get_user_paths())

        # System commands
        commands.append('xdg-open')

        # Standard browser commands
        commands.extend(['firefox', 'google-chrome', 'chromium-browser', 'chromium'])

        return list(dict.fromkeys(commands))

    def _get_user_paths(self) -> list[str]:
        """Get user-configured browser paths using EAFP.

        Returns:
            List of valid user-configured paths
        """
        paths: list[str] = []

        try:
            if self.config.browser_path:
                browser_path = Path(self.config.browser_path)
                if browser_path.exists():
                    paths.append(str(browser_path))
        except (AttributeError, TypeError):
            pass

        return paths

    async def _execute_command(self, command: str, url: str) -> tuple[int, str, str]:
        """Execute Linux browser command asynchronously.

        Args:
            command: Browser command or path to execute
            url: URL to open

        Returns:
            Tuple of (return_code, stdout, stderr)

        Raises:
            asyncio.TimeoutError: If command times out
        """
        timeout = getattr(self.config, 'browser_timeout', 5.0)

        process = await asyncio.create_subprocess_exec(
            command,
            url,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        try:
            stdout_bytes, stderr_bytes = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
            return_code = process.returncode or 0
            stdout = stdout_bytes.decode('utf-8', errors='ignore')
            stderr = stderr_bytes.decode('utf-8', errors='ignore')

            return (return_code, stdout, stderr)

        except TimeoutError:
            try:
                process.kill()
                await process.wait()
            except ProcessLookupError:
                pass
            raise


class WebbrowserFallbackStrategy(BrowserStrategy):
    """Fallback strategy using Python's webbrowser module.

    This is the last resort when all other browser launching
    strategies fail. Uses Python's built-in webbrowser module.
    """

    def get_commands(self) -> list[str]:
        """Get webbrowser module command.

        Returns:
            Single-item list with 'webbrowser' command
        """
        return ['webbrowser']

    async def _execute_command(self, command: str, url: str) -> tuple[int, str, str]:
        """Execute webbrowser module in thread pool.

        Since webbrowser.open() is synchronous, we run it in
        an executor to avoid blocking the event loop.

        Args:
            command: Must be 'webbrowser'
            url: URL to open

        Returns:
            Tuple of (return_code, stdout, stderr)

        Raises:
            ValueError: If command is not 'webbrowser'
        """
        if command != 'webbrowser':
            raise ValueError(f"Unsupported command: {command}")

        # Import here to avoid unnecessary dependency
        import webbrowser

        # Run blocking operation in thread pool
        loop = asyncio.get_running_loop()

        try:
            # webbrowser.open() is synchronous, so run in executor
            success = await loop.run_in_executor(
                None,
                webbrowser.open,
                url
            )

            if success:
                self.logger.info("Browser launched using webbrowser module")
                return (0, '', '')
            else:
                self.logger.warning("Webbrowser module returned False")
                return (1, '', 'webbrowser.open returned False')

        except Exception as error:
            self.logger.error(
                "Webbrowser module failed",
                error=str(error),
                error_type=type(error).__name__
            )
            return (1, '', str(error))


class BrowserStrategyFactory:
    """Factory for creating platform-specific browser strategies.

    Implements the Factory pattern for creating appropriate browser
    launch strategies based on the current platform.
    """

    _strategies: dict[Platform, type[BrowserStrategy]] = {
        Platform.WINDOWS: WindowsBrowserStrategy,
        Platform.MACOS: MacOSBrowserStrategy,
        Platform.LINUX: LinuxBrowserStrategy
    }

    @classmethod
    def create_strategy(
        cls,
        config: AppConfig,
        platform: Platform | None = None
    ) -> BrowserStrategy:
        """Create appropriate browser strategy for platform.

        Args:
            config: Application configuration
            platform: Target platform (auto-detected if None)

        Returns:
            Platform-specific browser strategy instance
        """
        if platform is None:
            platform = Platform.current()

        strategy_class = cls._strategies.get(platform, LinuxBrowserStrategy)
        return strategy_class(config)

    @classmethod
    def create_fallback_strategy(cls, config: AppConfig) -> BrowserStrategy:
        """Create fallback strategy using webbrowser module.

        Args:
            config: Application configuration

        Returns:
            Webbrowser fallback strategy instance
        """
        return WebbrowserFallbackStrategy(config)

    @classmethod
    def register_strategy(
        cls,
        platform: Platform,
        strategy_class: type[BrowserStrategy]
    ) -> None:
        """Register custom browser strategy for platform.

        Args:
            platform: Target platform
            strategy_class: Strategy class to register
        """
        cls._strategies[platform] = strategy_class

        logger = get_logger("browser_factory")
        logger.info(
            "Custom browser strategy registered",
            platform=platform.value,
            strategy_class=strategy_class.__name__
        )
