"""Retry utilities using tenacity for robust operation handling.

This module provides pre-configured retry decorators for common use cases,
leveraging the tenacity library for production-grade retry logic.
"""

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from .errors import BrowserError, NetworkError, TimeoutError

# ============================================================================
# Pre-configured Retry Decorators
# ============================================================================

# Network operations retry with exponential backoff
retry_network = retry(
    retry=retry_if_exception_type((NetworkError, TimeoutError)),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=0.1, max=10),
    reraise=True,
)
"""Retry decorator for network operations.

Retries up to 3 times with exponential backoff (0.1s to 10s) on NetworkError
or TimeoutError.

Example:
    >>> @retry_network
    ... def fetch_data():
    ...     return make_api_request()
"""

# Browser operations retry with shorter backoff
retry_browser = retry(
    retry=retry_if_exception_type(BrowserError),
    stop=stop_after_attempt(2),
    wait=wait_exponential(multiplier=0.5, min=0.1, max=5),
    reraise=True,
)
"""Retry decorator for browser operations.

Retries up to 2 times with exponential backoff (0.1s to 5s) on BrowserError.

Example:
    >>> @retry_browser
    ... def launch_browser():
    ...     return browser_manager.launch()
"""

# General purpose retry for any exception
retry_general = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=0.1, max=10),
    reraise=True,
)
"""General purpose retry decorator.

Retries up to 3 times with exponential backoff on any exception.

Example:
    >>> @retry_general
    ... def unstable_operation():
    ...     return risky_function()
"""


# ============================================================================
# Custom Retry Configurations
# ============================================================================


def create_retry_decorator(
    max_attempts: int = 3,
    min_wait: float = 0.1,
    max_wait: float = 10.0,
    multiplier: float = 1.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> retry:
    """Create a custom retry decorator with specified parameters.

    Args:
        max_attempts: Maximum number of retry attempts
        min_wait: Minimum wait time between retries (seconds)
        max_wait: Maximum wait time between retries (seconds)
        multiplier: Exponential backoff multiplier
        exceptions: Tuple of exception types to retry on

    Returns:
        Configured tenacity retry decorator

    Example:
        >>> custom_retry = create_retry_decorator(
        ...     max_attempts=5,
        ...     min_wait=0.5,
        ...     exceptions=(ValueError, KeyError)
        ... )
        >>> @custom_retry
        ... def custom_operation():
        ...     return process_data()
    """
    return retry(
        retry=retry_if_exception_type(exceptions),
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=multiplier, min=min_wait, max=max_wait),
        reraise=True,
    )
