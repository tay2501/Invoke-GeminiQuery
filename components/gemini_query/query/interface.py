"""Query processing interface definitions using Protocol for loose coupling."""

from typing import Protocol, runtime_checkable

from pydantic import BaseModel


@runtime_checkable
class URLGenerator(Protocol):
    """Protocol for URL generation implementations.

    This protocol defines the interface for URL generation,
    allowing different implementations while maintaining loose coupling.
    """

    def create_url(self, request: BaseModel) -> str:
        """Create a URL from a query request.

        Args:
            request: Query request with prompt and settings

        Returns:
            Generated URL string

        Raises:
            ValidationError: If URL generation fails
        """
        ...


@runtime_checkable
class QueryProcessor(Protocol):
    """Protocol for query processing implementations.

    Defines the interface for processing user queries and
    orchestrating the query workflow.
    """

    def process_query(self, prompt: str, max_length: int | None = None) -> bool:
        """Process a query from start to finish.

        Args:
            prompt: Query text
            max_length: Optional maximum length override

        Returns:
            True if successful, False otherwise

        Raises:
            ValidationError: If query processing fails
        """
        ...


@runtime_checkable
class InputProcessor(Protocol):
    """Protocol for input processing implementations.

    Defines the interface for processing and validating user input.
    """

    def process_input(self, raw_input: str) -> str:
        """Process raw input and return validated text.

        Args:
            raw_input: Raw input string

        Returns:
            Processed and validated input

        Raises:
            ValidationError: If input is invalid
        """
        ...
