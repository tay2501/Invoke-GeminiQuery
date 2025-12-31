#!/usr/bin/env python3
"""
URL generator tests for Gemini Auto Query.

Tests URL generation, encoding, and validation functionality.
"""

import sys
import unittest
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pydantic import ValidationError as PydanticValidationError

from gemini_query.config.legacy import AppConfig
from gemini_query.query import QueryRequest, URLGenerator


class TestURLGenerator(unittest.TestCase):
    """Test URLGenerator functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.config = AppConfig()
        self.generator = URLGenerator(self.config)
        self.base_url = self.config.gemini_url

    def test_simple_prompt(self):
        """Test URL generation with simple prompt"""
        prompt = "Hello, world!"
        request = QueryRequest(prompt=prompt)
        result = self.generator.create_url(request)

        self.assertIn("prompt=Hello%2C%20world%21", result)
        self.assertTrue(result.startswith(self.base_url))

    def test_japanese_prompt(self):
        """Test URL generation with Japanese text"""
        prompt = "こんにちは世界"
        request = QueryRequest(prompt=prompt)
        result = self.generator.create_url(request)

        self.assertIn("prompt=", result)
        self.assertTrue(result.startswith(self.base_url))
        # Japanese characters should be URL-encoded
        self.assertNotIn("こんにちは", result)

    def test_special_characters(self):
        """Test URL generation with special characters"""
        prompt = "Test & symbols: @#$%^&*()"
        request = QueryRequest(prompt=prompt)
        result = self.generator.create_url(request)

        # Special characters should be encoded
        self.assertIn("prompt=", result)
        self.assertNotIn("&", result.split("prompt=")[1])  # & should be encoded in prompt part
        self.assertNotIn("@", result.split("prompt=")[1])  # @ should be encoded

    def test_empty_prompt(self):
        """Test URL generation with empty prompt"""
        with self.assertRaises((PydanticValidationError, ValueError)):
            QueryRequest(prompt="")

    def test_whitespace_only_prompt(self):
        """Test URL generation with whitespace-only prompt"""
        with self.assertRaises((PydanticValidationError, ValueError)):
            QueryRequest(prompt="   \n\t   ")

    def test_long_prompt_truncation(self):
        """Test prompt truncation when exceeding max length"""
        config = AppConfig(max_prompt_length=10)
        generator = URLGenerator(config)
        prompt = "This is a very long prompt that exceeds the maximum length"

        request = QueryRequest(prompt=prompt)
        result = generator.create_url(request)

        # Should contain truncated prompt
        self.assertIn("prompt=", result)
        # The result should be much shorter than the original
        self.assertTrue(len(result) < len(self.base_url) + len(prompt) * 3)

    def test_base_url_with_existing_params(self):
        """Test URL generation when base URL already has parameters"""
        config = AppConfig(gemini_url="https://example.com/test?existing=param")
        generator = URLGenerator(config)

        request = QueryRequest(prompt="test")
        result = generator.create_url(request)

        self.assertIn("prompt=test", result)
        self.assertIn("existing=param", result)

    def test_validate_url_valid(self):
        """Test URL validation with valid URL"""
        valid_url = "https://example.com/path?param=value"
        self.assertTrue(self.generator._validate_url(valid_url))

    def test_validate_url_invalid_scheme(self):
        """Test URL validation with missing scheme"""
        invalid_url = "example.com/path"
        self.assertFalse(self.generator._validate_url(invalid_url))

    def test_validate_url_invalid_netloc(self):
        """Test URL validation with missing netloc"""
        invalid_url = "https:///path"
        self.assertFalse(self.generator._validate_url(invalid_url))

    def test_validate_url_malformed(self):
        """Test URL validation with malformed URL"""
        invalid_url = "not a url at all"
        self.assertFalse(self.generator._validate_url(invalid_url))

    def test_multiline_prompt(self):
        """Test URL generation with multiline prompt"""
        prompt = "Line 1\nLine 2\nLine 3"
        request = QueryRequest(prompt=prompt)
        result = self.generator.create_url(request)

        self.assertIn("prompt=", result)
        self.assertTrue(result.startswith(self.base_url))
        # Newlines should be encoded
        self.assertNotIn("\n", result.split("prompt=")[1])

    def test_unicode_prompt(self):
        """Test URL generation with Unicode characters"""
        prompt = "Test with émojis: 🚀🌟✨"
        request = QueryRequest(prompt=prompt)
        result = self.generator.create_url(request)

        self.assertIn("prompt=", result)
        self.assertTrue(result.startswith(self.base_url))
        # Unicode characters should be encoded
        self.assertNotIn("🚀", result.split("prompt=")[1])


if __name__ == '__main__':
    unittest.main()
