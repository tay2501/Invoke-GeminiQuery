"""Query processing and URL generation with modern Python patterns."""

import urllib.parse

from pydantic import BaseModel, ConfigDict, Field, field_validator

from gemini_query.browser.service import BrowserManager
from gemini_query.config.unified import AppConfig
from gemini_query.logging import get_logger
from gemini_query.utils.errors import ValidationError

logger = get_logger(__name__)


class QueryRequest(BaseModel):
    """Query request with validation using Pydantic."""

    prompt: str = Field(
        ...,
        min_length=1,
        description="Query text to send to Gemini AI"
    )
    max_length: int | None = Field(
        None,
        gt=0,
        description="Maximum length for the prompt"
    )

    @field_validator("prompt", mode="after")
    @classmethod
    def validate_prompt(cls, v: str) -> str:
        """Validate prompt content.

        Args:
            v: Prompt string

        Returns:
            Validated prompt

        Raises:
            ValueError: If prompt is invalid
        """
        if not v.strip():
            raise ValueError("Prompt cannot be empty or whitespace only")
        return v.strip()

    model_config = ConfigDict(extra="forbid")


class URLGenerator:
    """URL generator for Gemini AI queries with proper encoding."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize URL generator.

        Args:
            config: Application configuration
        """
        self.config = config
        self.logger = get_logger(__name__)

    def create_url(self, request: QueryRequest) -> str:
        """Create a properly formatted Gemini URL with the prompt parameter.

        Args:
            request: Query request with prompt

        Returns:
            Complete URL with encoded prompt parameter

        Raises:
            ValidationError: If URL generation fails
        """
        try:
            self.logger.debug(
                "url_generation_started", prompt_length=len(request.prompt)
            )

            # Determine max length
            max_length = request.max_length or self.config.max_prompt_length

            # Truncate prompt if needed
            processed_prompt = self._truncate_if_needed(request.prompt, max_length)

            # URL encode the prompt to handle special characters
            encoded_prompt = urllib.parse.quote(processed_prompt, safe="")
            self.logger.debug("prompt_encoded", encoded_length=len(encoded_prompt))

            # Build final URL
            final_url = self._build_url(encoded_prompt)

            # Validate URL
            if not self._validate_url(final_url):
                raise ValidationError(f"Generated URL is invalid: {final_url}")

            self.logger.info(
                "url_generated",
                url_length=len(final_url),
                was_truncated=(len(processed_prompt) != len(request.prompt)),
            )

            return final_url

        except Exception as e:
            self.logger.error("url_generation_failed", error=str(e))
            raise ValidationError(f"Failed to generate URL: {e}") from e

    def _truncate_if_needed(self, prompt: str, max_length: int) -> str:
        """Truncate prompt if it exceeds maximum length.

        Args:
            prompt: Original prompt
            max_length: Maximum allowed length

        Returns:
            Potentially truncated prompt
        """
        if len(prompt) <= max_length:
            return prompt

        truncated = prompt[:max_length - 3] + "..."
        self.logger.warning(
            "prompt_truncated",
            original_length=len(prompt),
            truncated_length=len(truncated),
        )
        return truncated

    def _build_url(self, encoded_prompt: str) -> str:
        """Build final URL with proper parameter handling.

        Args:
            encoded_prompt: URL-encoded prompt

        Returns:
            Complete URL
        """
        separator = '&' if '?' in self.config.gemini_url else '?'
        return f"{self.config.gemini_url}{separator}prompt={encoded_prompt}"

    def _validate_url(self, url: str) -> bool:
        """Validate that URL is properly formatted.

        Args:
            url: URL to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            result = urllib.parse.urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception as e:
            self.logger.debug("url_validation_failed", error=str(e))
            return False


class QueryProcessor:
    """Async query processor that orchestrates the entire query workflow.

    Coordinates URL generation and browser launching using async/await
    for improved performance and resource management.
    """

    def __init__(self, config: AppConfig) -> None:
        """Initialize query processor.

        Args:
            config: Application configuration
        """
        self.config = config
        self.logger = get_logger(__name__)
        self.url_generator = URLGenerator(config)
        self.browser_manager = BrowserManager(config)

    async def process_query(self, prompt: str, max_length: int | None = None) -> bool:
        """Process a query from start to finish asynchronously.

        Args:
            prompt: Query text
            max_length: Optional maximum length override

        Returns:
            True if successful, False otherwise

        Raises:
            ValidationError: If query processing fails
        """
        try:
            self.logger.info(f"Processing query (length: {len(prompt)})")

            # Create and validate request
            request = QueryRequest(prompt=prompt, max_length=max_length)

            # Generate URL
            url = self.url_generator.create_url(request)

            # Launch browser asynchronously
            success = await self.browser_manager.launch(url)

            if success:
                self.logger.info("Query processed successfully")
            else:
                self.logger.error("Failed to launch browser")

            return success

        except Exception as error:
            self.logger.error(f"Query processing failed: {error}")
            raise ValidationError(f"Failed to process query: {error}") from error
