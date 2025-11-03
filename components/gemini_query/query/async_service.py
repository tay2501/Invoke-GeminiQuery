"""Asynchronous query processing for improved performance and responsiveness."""

import asyncio
import time
from contextlib import asynccontextmanager
from typing import AsyncContextManager

import httpx

from ..core.config.unified import AppConfig
from ..utils.errors import GeminiQueryError
from ..utils.logging import get_logger
from ..utils.structured_logging import with_structured_logging
from .query import QueryRequest, URLGenerator


class AsyncQueryProcessor:
    """Asynchronous query processor with improved performance and resource management.

    This processor provides async/await support for better concurrency and
    resource utilization, especially useful for handling multiple queries
    or when combined with other async operations.
    """

    def __init__(self, config: AppConfig) -> None:
        """Initialize async query processor.

        Args:
            config: Application configuration
        """
        self.config = config
        self.logger = get_logger(__name__)
        self.url_generator = URLGenerator(config)
        self.client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "AsyncQueryProcessor":
        """Async context manager entry."""
        self.client = httpx.AsyncClient(
            timeout=self.config.network.browser_timeout,
            limits=httpx.Limits(max_connections=10, max_keepalive_connections=5)
        )
        self.logger.debug("AsyncQueryProcessor initialized with HTTP client")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        if self.client:
            await self.client.aclose()
            self.logger.debug("AsyncQueryProcessor HTTP client closed")

    @with_structured_logging("async_query_processing")
    async def process_query_async(self, prompt: str, max_length: int | None = None) -> bool:
        """Process a query asynchronously with concurrent operations.

        Args:
            prompt: Query text
            max_length: Optional maximum length override

        Returns:
            True if successful, False otherwise

        Raises:
            GeminiQueryError: If query processing fails
        """
        from ..utils.structured_logging import (
            get_structured_logger,
            log_performance_metrics,
            with_retry_and_logging,
        )

        struct_logger = get_structured_logger(__name__).bind(
            prompt_length=len(prompt),
            max_length=max_length
        )

        try:
            struct_logger.info("Starting async query processing")

            # Define retry-enabled operations
            async def validation_operation():
                return await self._validate_request_async(prompt, max_length)

            async def url_generation_operation():
                return await self._generate_url_async(prompt, max_length)

            async def browser_prep_operation():
                return await self._prepare_browser_context_async()

            # Execute operations with retry logic and structured logging
            start_time = time.time()

            validation_task = with_retry_and_logging(
                validation_operation,
                "request_validation",
                max_retries=2,
                logger=struct_logger
            )

            url_generation_task = with_retry_and_logging(
                url_generation_operation,
                "url_generation",
                max_retries=2,
                logger=struct_logger
            )

            browser_prep_task = with_retry_and_logging(
                browser_prep_operation,
                "browser_preparation",
                max_retries=1,
                logger=struct_logger
            )

            # Execute tasks concurrently with timeout
            try:
                request, url, browser_ready = await asyncio.wait_for(
                    asyncio.gather(
                        validation_task,
                        url_generation_task,
                        browser_prep_task
                    ),
                    timeout=self.config.network.connection_timeout
                )
            except TimeoutError:
                struct_logger.error("Concurrent operations timed out")
                raise GeminiQueryError("Query processing operations timed out")

            preparation_time = time.time() - start_time

            # Launch browser with prepared context
            browser_start_time = time.time()
            success = await with_retry_and_logging(
                lambda: self._launch_browser_async(url),
                "browser_launch",
                max_retries=self.config.network.max_retries,
                base_delay=self.config.network.retry_delay,
                logger=struct_logger
            )

            browser_time = time.time() - browser_start_time
            total_time = time.time() - start_time

            # Log performance metrics
            log_performance_metrics(
                struct_logger,
                "async_query_processing",
                preparation_time_seconds=preparation_time,
                browser_launch_time_seconds=browser_time,
                total_time_seconds=total_time,
                success=success
            )

            if success:
                struct_logger.info("Async query processed successfully")
            else:
                struct_logger.error("Failed to launch browser asynchronously")

            return success

        except Exception as e:
            struct_logger.error(
                "Async query processing failed",
                error_type=type(e).__name__,
                error_message=str(e)
            )
            raise GeminiQueryError(f"Failed to process async query: {e}") from e

    async def _validate_request_async(self, prompt: str, max_length: int | None = None) -> QueryRequest:
        """Validate query request asynchronously.

        Args:
            prompt: Query text
            max_length: Optional maximum length override

        Returns:
            Validated QueryRequest
        """
        # Run validation in thread pool for CPU-intensive tasks
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: QueryRequest(prompt=prompt, max_length=max_length)
        )

    async def _generate_url_async(self, prompt: str, max_length: int | None = None) -> str:
        """Generate URL asynchronously.

        Args:
            prompt: Query text
            max_length: Optional maximum length override

        Returns:
            Generated URL
        """
        request = QueryRequest(prompt=prompt, max_length=max_length)

        # Run URL generation in thread pool
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.url_generator.create_url,
            request
        )

    async def _prepare_browser_context_async(self) -> bool:
        """Prepare browser context asynchronously.

        Returns:
            True if browser context is ready
        """
        # Simulate async browser preparation
        await asyncio.sleep(0.1)  # Small delay to simulate async work

        # In the future, this could include:
        # - Pre-loading browser profiles
        # - Checking browser availability
        # - Setting up browser extensions

        self.logger.debug("Browser context prepared asynchronously")
        return True

    async def _launch_browser_async(self, url: str) -> bool:
        """Launch browser asynchronously with modern automation.

        Args:
            url: URL to open

        Returns:
            True if browser launched successfully
        """
        try:
            # Use modern async browser manager
            from .async_browser import AsyncBrowserManager

            async with AsyncBrowserManager(self.config) as browser_manager:
                return await browser_manager.launch_async(url)

        except Exception as e:
            self.logger.error(f"Modern async browser launch failed: {e}")

            # Fallback to legacy method
            try:
                self.logger.info("Attempting fallback to legacy browser method")
                from .browser import BrowserManager

                browser_manager = BrowserManager(self.config)

                # Run legacy browser launch in thread pool
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(
                    None,
                    browser_manager.launch,
                    url
                )
            except Exception as fallback_error:
                self.logger.error(f"Legacy browser fallback also failed: {fallback_error}")
                return False

    @asynccontextmanager
    async def batch_processor(self) -> AsyncContextManager["AsyncQueryProcessor"]:
        """Context manager for batch processing multiple queries.

        Yields:
            Configured AsyncQueryProcessor for batch operations
        """
        async with self:
            self.logger.info("Batch processing context initialized")
            try:
                yield self
            finally:
                self.logger.info("Batch processing context closed")

    async def process_multiple_queries(self, queries: list[str]) -> list[bool]:
        """Process multiple queries concurrently.

        Args:
            queries: List of query texts

        Returns:
            List of success indicators for each query
        """
        async with self.batch_processor() as processor:
            tasks = [
                processor.process_query_async(query)
                for query in queries
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Convert exceptions to False, keep boolean results
            return [
                result if isinstance(result, bool) else False
                for result in results
            ]


# Factory function for easier usage
async def create_async_processor(config: AppConfig) -> AsyncQueryProcessor:
    """Factory function to create and initialize AsyncQueryProcessor.

    Args:
        config: Application configuration

    Returns:
        Initialized AsyncQueryProcessor
    """
    processor = AsyncQueryProcessor(config)
    return processor
