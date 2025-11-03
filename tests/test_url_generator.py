#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URL generator tests for Gemini Auto Query.

Tests URL generation, encoding, and validation functionality.
"""

import sys
import unittest
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gemini_query.query import URLGenerator


class TestURLGenerator(unittest.TestCase):
    """Test URLGenerator functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.base_url = "https://aistudio.google.com/prompts/new_chat"
        self.generator = URLGenerator(self.base_url)
    
    def test_simple_prompt(self):
        """Test URL generation with simple prompt"""
        prompt = "Hello, world!"
        result = self.generator.create_url(prompt)
        
        expected = f"{self.base_url}?prompt=Hello%2C%20world%21"
        self.assertEqual(result, expected)
    
    def test_japanese_prompt(self):
        """Test URL generation with Japanese text"""
        prompt = "こんにちは世界"
        result = self.generator.create_url(prompt)
        
        self.assertIn("prompt=", result)
        self.assertTrue(result.startswith(self.base_url))
        # Japanese characters should be URL-encoded
        self.assertNotIn("こんにちは", result)
    
    def test_special_characters(self):
        """Test URL generation with special characters"""
        prompt = "Test & symbols: @#$%^&*()"
        result = self.generator.create_url(prompt)
        
        # Special characters should be encoded
        self.assertIn("prompt=", result)
        self.assertNotIn("&", result.split("prompt=")[1])  # & should be encoded in prompt part
        self.assertNotIn("@", result.split("prompt=")[1])  # @ should be encoded
    
    def test_empty_prompt(self):
        """Test URL generation with empty prompt"""
        with self.assertRaises(ValueError) as cm:
            self.generator.create_url("")
        
        self.assertIn("Prompt cannot be empty", str(cm.exception))
    
    def test_whitespace_only_prompt(self):
        """Test URL generation with whitespace-only prompt"""
        with self.assertRaises(ValueError) as cm:
            self.generator.create_url("   \n\t   ")
        
        self.assertIn("Prompt cannot be empty", str(cm.exception))
    
    def test_long_prompt_truncation(self):
        """Test prompt truncation when exceeding max length"""
        generator = URLGenerator(self.base_url, max_length=10)
        prompt = "This is a very long prompt that exceeds the maximum length"
        
        result = generator.create_url(prompt)
        
        # Should contain truncated prompt with ellipsis
        self.assertIn("prompt=", result)
        encoded_part = result.split("prompt=")[1]
        # The original prompt should be truncated to 10 chars + "..."
        self.assertTrue(len(encoded_part) < len(prompt) * 3)  # Much shorter due to truncation
    
    def test_base_url_with_existing_params(self):
        """Test URL generation when base URL already has parameters"""
        base_url = "https://example.com/test?existing=param"
        generator = URLGenerator(base_url)
        
        result = generator.create_url("test")
        
        expected = f"{base_url}&prompt=test"
        self.assertEqual(result, expected)
    
    def test_validate_url_valid(self):
        """Test URL validation with valid URL"""
        valid_url = "https://example.com/path?param=value"
        self.assertTrue(self.generator.validate_url(valid_url))
    
    def test_validate_url_invalid_scheme(self):
        """Test URL validation with missing scheme"""
        invalid_url = "example.com/path"
        self.assertFalse(self.generator.validate_url(invalid_url))
    
    def test_validate_url_invalid_netloc(self):
        """Test URL validation with missing netloc"""
        invalid_url = "https:///path"
        self.assertFalse(self.generator.validate_url(invalid_url))
    
    def test_validate_url_malformed(self):
        """Test URL validation with malformed URL"""
        invalid_url = "not a url at all"
        self.assertFalse(self.generator.validate_url(invalid_url))
    
    def test_multiline_prompt(self):
        """Test URL generation with multiline prompt"""
        prompt = "Line 1\nLine 2\nLine 3"
        result = self.generator.create_url(prompt)
        
        self.assertIn("prompt=", result)
        self.assertTrue(result.startswith(self.base_url))
        # Newlines should be encoded
        self.assertNotIn("\n", result.split("prompt=")[1])
    
    def test_unicode_prompt(self):
        """Test URL generation with Unicode characters"""
        prompt = "Test with émojis: 🚀🌟✨"
        result = self.generator.create_url(prompt)
        
        self.assertIn("prompt=", result)
        self.assertTrue(result.startswith(self.base_url))
        # Unicode characters should be encoded
        self.assertNotIn("🚀", result.split("prompt=")[1])


if __name__ == '__main__':
    unittest.main()