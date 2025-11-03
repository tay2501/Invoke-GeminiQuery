"""Async browser management service with strategy pattern for cross-platform support.

This module provides the main BrowserManager class that coordinates browser
launching across different platforms using async/await for better performance.
"""


from gemini_query.browser.strategies import BrowserStrategy, BrowserStrategyFactory
from gemini_query.config import AppConfig, Platform
from gemini_query.logging import get_logger


class BrowserManager:
    """Async cross-platform browser management using strategy pattern.

    Coordinates browser launching across different platforms with
    fallback mechanisms and comprehensive error handling.
    """

    def __init__(self, config: AppConfig) -> None:
        """Initialize browser manager with configuration.

        Args:
            config: Application configuration instance
        """
        self.config = config
        self.logger = get_logger(__name__).bind(
            platform=Platform.current().value
        )

        # Initialize strategies
        self.primary_strategy = BrowserStrategyFactory.create_strategy(config)
        self.fallback_strategy = BrowserStrategyFactory.create_fallback_strategy(config)

    async def launch(self, url: str) -> bool:
        """Launch browser with the specified URL using async strategy pattern.

        Tries primary platform-specific strategy first, then falls back
        to webbrowser module if primary fails.

        Args:
            url: The URL to open in the browser

        Returns:
            True if browser launched successfully, False otherwise

        Raises:
            BrowserLaunchError: If critical error occurs during launch
        """
        self.logger.info("browser_launch_requested", url_length=len(url))

        # Try primary platform-specific strategy
        try:
            if await self.primary_strategy.launch(url):
                return True
        except Exception as error:
            self.logger.warning(
                "primary_strategy_failed",
                error=str(error),
                error_type=type(error).__name__,
            )

        self.logger.warning("trying_fallback_strategy")

        # Try fallback strategy
        try:
            if await self.fallback_strategy.launch(url):
                return True
        except Exception as error:
            self.logger.error(
                "fallback_strategy_failed",
                error=str(error),
                error_type=type(error).__name__,
            )

        # All strategies failed
        self.logger.error("all_browser_strategies_failed")
        self.show_error_message(url)
        return False

    def get_available_commands(self) -> list[str]:
        """Get all available browser commands for diagnostics.

        Returns:
            Deduplicated list of all browser commands from all strategies
        """
        commands: list[str] = []
        commands.extend(self.primary_strategy.get_commands())
        commands.extend(self.fallback_strategy.get_commands())
        return list(dict.fromkeys(commands))

    def set_custom_strategy(self, strategy: BrowserStrategy) -> None:
        """Set custom browser strategy for testing or special cases.

        Args:
            strategy: Custom browser strategy instance
        """
        self.primary_strategy = strategy
        self.logger.info(
            "custom_strategy_set", strategy_class=strategy.__class__.__name__
        )

    def show_error_message(self, url: str) -> None:
        """Show user-friendly error message when browser launch fails.

        Args:
            url: The URL that failed to open
        """
        available_commands = self.get_available_commands()

        self.logger.error(
            "browser_launch_failed",
            attempted_commands=available_commands[:10],
            url=url,
        )

        # User-friendly error message (Japanese)
        print("\n" + "="*60)
        print("ブラウザの起動に失敗しました")
        print("="*60)
        print("以下のURLを手動でブラウザで開いてください:")
        print(f"\n{url}\n")
        print("トラブルシューティング:")
        print("1. config.jsonのbrowser_pathを確認してください")
        print("2. Firefoxがインストールされているか確認してください")
        print("3. 他のブラウザ(Chrome、Edge)を試してください")
        print(f"4. 試行されたコマンド: {', '.join(available_commands[:5])}")
        print("="*60)
