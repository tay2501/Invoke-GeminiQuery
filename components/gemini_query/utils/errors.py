"""Custom exceptions and error handling utilities for gemini-query.

This module defines the exception hierarchy and provides EAFP-style utilities
for robust error handling.
"""

from collections.abc import Generator
from contextlib import contextmanager

import structlog

logger = structlog.get_logger(__name__)


# ============================================================================
# Exception Hierarchy
# ============================================================================


class GeminiQueryError(Exception):
    """Base exception for all gemini-query related errors."""

    pass


class ConfigurationError(GeminiQueryError):
    """Raised when there's an error with configuration."""

    pass


class BrowserError(GeminiQueryError):
    """Raised when there's an error with browser operations."""

    pass


class BrowserLaunchError(BrowserError):
    """Raised when browser launch fails critically."""

    pass


class BrowserStrategyError(BrowserError):
    """Raised when browser strategy execution fails."""

    pass


class NetworkError(GeminiQueryError):
    """Raised when there's a network-related error."""

    pass


class ValidationError(GeminiQueryError):
    """Raised when input validation fails."""

    pass


class TimeoutError(GeminiQueryError):
    """Raised when operations timeout."""

    pass


# ============================================================================
# EAFP Utilities
# ============================================================================


@contextmanager
def suppress_and_log(*exceptions: type[Exception]) -> Generator[None, None, None]:
    """Context manager that suppresses specified exceptions and logs them.

    EAFP pattern: Try the operation, handle exceptions gracefully.

    Args:
        *exceptions: Exception types to suppress

    Example:
        >>> with suppress_and_log(FileNotFoundError, PermissionError):
        ...     config = load_config_file(path)

    Note:
        For simple suppression without logging, use contextlib.suppress instead.
    """
    try:
        yield
    except exceptions as e:
        logger.debug(
            "exception_suppressed",
            exception_type=type(e).__name__,
            exception_message=str(e),
        )
