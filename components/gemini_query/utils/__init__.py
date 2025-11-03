"""Utility modules for gemini-query."""

from .errors import (
    BrowserError,
    BrowserLaunchError,
    BrowserStrategyError,
    ConfigurationError,
    GeminiQueryError,
    NetworkError,
    TimeoutError,
    ValidationError,
    suppress_and_log,
)
from .retry import (
    create_retry_decorator,
    retry_browser,
    retry_general,
    retry_network,
)

__all__ = [
    # Exceptions
    "GeminiQueryError",
    "ConfigurationError",
    "BrowserError",
    "BrowserLaunchError",
    "BrowserStrategyError",
    "NetworkError",
    "ValidationError",
    "TimeoutError",
    # Error utilities
    "suppress_and_log",
    # Retry utilities
    "retry_network",
    "retry_browser",
    "retry_general",
    "create_retry_decorator",
]
