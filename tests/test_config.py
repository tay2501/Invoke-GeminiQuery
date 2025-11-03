#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration module tests for Gemini Auto Query.

Tests configuration loading, validation, and platform detection.
"""

import sys
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gemini_query.config import AppConfig


class TestAppConfig(unittest.TestCase):
    """Test AppConfig dataclass functionality"""
    
    def test_default_config(self):
        """Test default configuration values"""
        config = AppConfig()
        
        self.assertEqual(config.gemini_url, "https://aistudio.google.com/prompts/new_chat")
        self.assertEqual(config.browser_path, "")
        self.assertEqual(config.max_prompt_length, 10000)
        self.assertEqual(config.browser_timeout, 30)
        self.assertEqual(config.encoding, "utf-8")
        self.assertIsInstance(config.supported_browsers, list)
    
    def test_from_dict(self):
        """Test configuration creation from dictionary"""
        data = {
            "gemini_url": "https://example.com",
            "max_prompt_length": 5000,
            "invalid_key": "should_be_ignored"
        }
        
        config = AppConfig.from_dict(data)
        
        self.assertEqual(config.gemini_url, "https://example.com")
        self.assertEqual(config.max_prompt_length, 5000)
        # Default values should be preserved
        self.assertEqual(config.browser_timeout, 30)
    
    def test_to_dict(self):
        """Test configuration conversion to dictionary"""
        config = AppConfig(max_prompt_length=7500)
        config_dict = config.to_dict()
        
        self.assertIsInstance(config_dict, dict)
        self.assertEqual(config_dict["max_prompt_length"], 7500)
        self.assertIn("gemini_url", config_dict)
    
    def test_validate_valid_config(self):
        """Test validation of valid configuration"""
        config = AppConfig()
        self.assertTrue(config.validate())
    
    def test_validate_invalid_prompt_length(self):
        """Test validation with invalid prompt length"""
        config = AppConfig(max_prompt_length=0)
        
        with self.assertRaises(ValueError) as cm:
            config.validate()
        
        self.assertIn("max_prompt_length must be positive", str(cm.exception))
    
    def test_validate_invalid_timeout(self):
        """Test validation with invalid timeout"""
        config = AppConfig(browser_timeout=-1)
        
        with self.assertRaises(ValueError) as cm:
            config.validate()
        
        self.assertIn("browser_timeout must be positive", str(cm.exception))
    
    def test_validate_empty_encoding(self):
        """Test validation with empty encoding"""
        config = AppConfig(encoding="")
        
        with self.assertRaises(ValueError) as cm:
            config.validate()
        
        self.assertIn("encoding cannot be empty", str(cm.exception))


class TestPlatform(unittest.TestCase):
    """Test Platform enum functionality"""
    
    @patch('sys.platform', 'win32')
    def test_current_windows(self):
        """Test platform detection on Windows"""
        self.assertEqual(Platform.current(), Platform.WINDOWS)
    
    @patch('sys.platform', 'darwin')
    def test_current_macos(self):
        """Test platform detection on macOS"""
        self.assertEqual(Platform.current(), Platform.MACOS)
    
    @patch('sys.platform', 'linux')
    def test_current_linux(self):
        """Test platform detection on Linux"""
        self.assertEqual(Platform.current(), Platform.LINUX)
    
    @patch('sys.platform', 'unknown')
    def test_current_unknown(self):
        """Test platform detection on unknown platform"""
        self.assertEqual(Platform.current(), Platform.LINUX)


class TestConfigLoader(unittest.TestCase):
    """Test ConfigLoader functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.config_file = self.temp_dir / "config.json"
    
    def tearDown(self):
        """Clean up test fixtures"""
        if self.config_file.exists():
            self.config_file.unlink()
        self.temp_dir.rmdir()
    
    def test_load_nonexistent_config(self):
        """Test loading when config file doesn't exist"""
        loader = ConfigLoader(self.config_file)
        config = loader.load()
        
        self.assertIsInstance(config, AppConfig)
        # Should return default config
        self.assertEqual(config.gemini_url, "https://aistudio.google.com/prompts/new_chat")
    
    def test_load_valid_config(self):
        """Test loading valid configuration file"""
        test_config = {
            "gemini_url": "https://test.example.com",
            "max_prompt_length": 8000,
            "browser_timeout": 45
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(test_config, f)
        
        loader = ConfigLoader(self.config_file)
        config = loader.load()
        
        self.assertEqual(config.gemini_url, "https://test.example.com")
        self.assertEqual(config.max_prompt_length, 8000)
        self.assertEqual(config.browser_timeout, 45)
    
    def test_load_invalid_json(self):
        """Test loading invalid JSON file"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            f.write("invalid json content")
        
        loader = ConfigLoader(self.config_file)
        config = loader.load()
        
        # Should return default config
        self.assertIsInstance(config, AppConfig)
        self.assertEqual(config.gemini_url, "https://aistudio.google.com/prompts/new_chat")
    
    def test_load_invalid_config_values(self):
        """Test loading config with invalid values"""
        test_config = {
            "max_prompt_length": -100,  # Invalid
            "browser_timeout": 0,       # Invalid
            "encoding": ""              # Invalid
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(test_config, f)
        
        loader = ConfigLoader(self.config_file)
        config = loader.load()
        
        # Should return default config due to validation failure
        self.assertIsInstance(config, AppConfig)
        self.assertEqual(config.max_prompt_length, 10000)  # Default value


if __name__ == '__main__':
    unittest.main()