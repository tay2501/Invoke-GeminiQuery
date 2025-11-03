#!/usr/bin/env python3
"""
URL generation for Gemini Auto Query.

This module handles URL generation and parameter encoding for Gemini AI queries.
"""

import urllib.parse

from .logging_config import get_application_logger, log_catch, log_execution_time


class URLGenerator:
    """URL generator for Gemini AI queries with proper encoding"""

    def __init__(self, base_url: str, max_length: int = 10000):
        self.base_url = base_url
        self.max_length = max_length
        self.logger = get_application_logger(
            "url_generator",
            base_url=base_url,
            max_length=max_length
        )

    @log_execution_time
    @log_catch()
    def create_url(self, prompt: str) -> str:
        """
        Create a properly formatted Gemini URL with the prompt parameter.

        Args:
            prompt: The question/prompt to send to Gemini

        Returns:
            Complete URL with encoded prompt parameter

        Raises:
            ValueError: If prompt is empty
        """
        self.logger.debug("URL generation started", prompt_length=len(prompt))

        if not prompt.strip():
            self.logger.error("Empty prompt provided")
            raise ValueError("Prompt cannot be empty")

        # Truncate prompt if it exceeds maximum length
        processed_prompt = self._truncate_if_needed(prompt)

        # URL encode the prompt to handle special characters
        encoded_prompt = urllib.parse.quote(processed_prompt, safe='')
        self.logger.debug("Prompt encoded", encoded_length=len(encoded_prompt))

        # Build final URL with proper parameter handling
        final_url = self._build_url(encoded_prompt)

        self.logger.info(
            "URL generated successfully",
            final_url_length=len(final_url),
            was_truncated=len(processed_prompt) != len(prompt)
        )

        return final_url

    def _truncate_if_needed(self, prompt: str) -> str:
        """Truncate prompt if it exceeds maximum length"""
        if len(prompt) <= self.max_length:
            return prompt

        truncated = prompt[:self.max_length] + "..."
        self.logger.warning(
            "Prompt truncated",
            original_length=len(prompt),
            max_length=self.max_length,
            truncated_length=len(truncated)
        )
        return truncated

    def _build_url(self, encoded_prompt: str) -> str:
        """Build final URL with proper parameter handling"""
        separator = '&' if '?' in self.base_url else '?'
        return f"{self.base_url}{separator}prompt={encoded_prompt}"

    def validate_url(self, url: str) -> bool:
        """Validate that URL is properly formatted"""
        try:
            result = urllib.parse.urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
