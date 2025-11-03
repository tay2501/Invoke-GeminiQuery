"""Browser automation interface definitions using Protocol for loose coupling and type safety.

This module defines protocols for browser management following modern Python best practices:
- Async/await support for improved performance
- Protocol-based interfaces for dependency inversion
- Runtime checkable protocols for flexibility
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class BrowserLauncher(Protocol):
    """Protocol for browser launching implementations.

    This protocol defines the async interface for browser automation,
    allowing different implementations while maintaining loose coupling.
    Supports both sync and async operations for backward compatibility.
    """

    async def launch(self, url: str) -> bool:
        """Launch browser with the given URL asynchronously.

        Args:
            url: URL to open in the browser

        Returns:
            True if successful, False otherwise

        Raises:
            BrowserLaunchError: If browser launch fails critically
        """
        ...

    def get_available_commands(self) -> list[str]:
        """Get list of available browser commands for diagnostics.

        Returns:
            List of browser command strings that could be used
        """
        ...


@runtime_checkable
class BrowserStrategy(Protocol):
    """Protocol for browser automation strategies.

    Defines the async interface for different browser automation approaches
    (e.g., command-line launch, Playwright, native browser automation).
    Implements the Strategy pattern for cross-platform compatibility.
    """

    async def launch(self, url: str) -> bool:
        """Execute browser automation strategy asynchronously.

        Args:
            url: URL to open in the browser

        Returns:
            True if successful, False otherwise

        Raises:
            BrowserStrategyError: If strategy execution fails
        """
        ...

    def get_commands(self) -> list[str]:
        """Get the browser commands used by this strategy.

        Returns:
            List of command strings this strategy attempts to use
        """
        ...
