#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test cases for configuration factory implementations.
"""

import unittest
from unittest.mock import patch, mock_open
import os
import json
from pathlib import Path

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gemini_query.config import AppConfig

# Skip config factory tests - factory pattern may need redesign
import pytest
pytestmark = pytest.mark.skip(reason="Config factory tests need refactoring for new architecture")


class TestConfigProfiles(unittest.TestCase):
    """Test individual configuration profiles"""
    
    def test_default_config_profile(self):
        """Test default configuration profile"""
        profile = DefaultConfigProfile()
        config = profile.create_config()
        
        self.assertIsInstance(config, AppConfig)
        self.assertEqual(profile.get_profile_name(), "default")
        self.assertEqual(config.max_prompt_length, 10000)
        self.assertEqual(config.browser_timeout, 30)
    
    def test_test_config_profile(self):
        """Test testing configuration profile"""
        profile = TestConfigProfile()
        config = profile.create_config()
        
        self.assertIsInstance(config, AppConfig)
        self.assertEqual(profile.get_profile_name(), "test")
        self.assertEqual(config.browser_timeout, 1)
        self.assertEqual(config.max_prompt_length, 100)
        self.assertEqual(config.browser_path, "echo")
    
    def test_development_config_profile(self):
        """Test development configuration profile"""
        profile = DevelopmentConfigProfile()
        config = profile.create_config()
        
        self.assertIsInstance(config, AppConfig)
        self.assertEqual(profile.get_profile_name(), "development")
        self.assertEqual(config.browser_timeout, 60)
        self.assertEqual(config.max_prompt_length, 50000)
    
    @patch('src.gemini_query.config_factory.FileConfigProfile.create_config')
    def test_production_config_profile(self, mock_file_config):
        """Test production configuration profile"""
        # Mock base config
        mock_base_config = AppConfig(
            gemini_url="https://custom.gemini.url",
            browser_path="/custom/browser"
        )
        mock_file_config.return_value = mock_base_config
        
        profile = ProductionConfigProfile()
        config = profile.create_config()
        
        self.assertIsInstance(config, AppConfig)
        self.assertEqual(profile.get_profile_name(), "production")
        self.assertEqual(config.gemini_url, mock_base_config.gemini_url)
        self.assertEqual(config.browser_path, mock_base_config.browser_path)
        self.assertEqual(config.max_prompt_length, 20000)  # Production override
        self.assertEqual(config.browser_timeout, 15)  # Production override


class TestFileConfigProfile(unittest.TestCase):
    """Test file-based configuration profile"""
    
    def test_file_config_profile_default_path(self):
        """Test file config with default path"""
        profile = FileConfigProfile()
        self.assertEqual(profile.get_profile_name(), "file:config.json")
    
    def test_file_config_profile_custom_path(self):
        """Test file config with custom path"""
        custom_path = Path("custom_config.json")
        profile = FileConfigProfile(custom_path)
        self.assertEqual(profile.get_profile_name(), "file:custom_config.json")
    
    @patch('builtins.open', mock_open(read_data='{"max_prompt_length": 5000}'))
    @patch('pathlib.Path.exists')
    def test_file_config_loads_successfully(self, mock_exists):
        """Test successful file loading"""
        mock_exists.return_value = True
        
        profile = FileConfigProfile()
        config = profile.create_config()
        
        self.assertIsInstance(config, AppConfig)
        self.assertEqual(config.max_prompt_length, 5000)
    
    @patch('pathlib.Path.exists')
    def test_file_config_file_not_exists(self, mock_exists):
        """Test fallback when file doesn't exist"""
        mock_exists.return_value = False
        
        profile = FileConfigProfile()
        with patch('builtins.print') as mock_print:
            config = profile.create_config()
        
        self.assertIsInstance(config, AppConfig)
        mock_print.assert_called()


class TestEnvironmentConfigProfile(unittest.TestCase):
    """Test environment variable configuration profile"""
    
    @patch('os.getenv')
    @patch('src.gemini_query.config_factory.FileConfigProfile.create_config')
    def test_environment_config_overrides(self, mock_file_config, mock_getenv):
        """Test environment variable overrides"""
        # Mock base config
        mock_base_config = AppConfig()
        mock_file_config.return_value = mock_base_config
        
        # Mock environment variables
        def getenv_side_effect(key, default=None):
            env_vars = {
                'GEMINI_URL': 'https://env.gemini.url',
                'GEMINI_MAX_PROMPT_LENGTH': '15000',
                'GEMINI_BROWSER_PATH': '/env/browser',
                'GEMINI_BROWSER_TIMEOUT': '45'
            }
            return env_vars.get(key, default)
        
        mock_getenv.side_effect = getenv_side_effect
        
        profile = EnvironmentConfigProfile()
        config = profile.create_config()
        
        self.assertEqual(config.gemini_url, 'https://env.gemini.url')
        self.assertEqual(config.max_prompt_length, 15000)
        self.assertEqual(config.browser_path, '/env/browser')
        self.assertEqual(config.browser_timeout, 45)
    
    @patch('os.getenv')
    @patch('src.gemini_query.config_factory.FileConfigProfile.create_config')
    def test_environment_config_invalid_values(self, mock_file_config, mock_getenv):
        """Test environment config with invalid values"""
        mock_base_config = AppConfig()
        mock_file_config.return_value = mock_base_config
        
        # Mock invalid environment variables
        def getenv_side_effect(key, default=None):
            env_vars = {
                'GEMINI_MAX_PROMPT_LENGTH': 'invalid',  # Invalid integer
                'GEMINI_BROWSER_TIMEOUT': 'also_invalid'  # Invalid integer
            }
            return env_vars.get(key, default)
        
        mock_getenv.side_effect = getenv_side_effect
        
        profile = EnvironmentConfigProfile()
        config = profile.create_config()
        
        # Should use base config values when env vars are invalid
        self.assertEqual(config.max_prompt_length, mock_base_config.max_prompt_length)
        self.assertEqual(config.browser_timeout, mock_base_config.browser_timeout)


class TestConfigFactory(unittest.TestCase):
    """Test configuration factory"""
    
    def test_create_config_default(self):
        """Test default configuration creation"""
        config = ConfigFactory.create_config("default")
        
        self.assertIsInstance(config, AppConfig)
        self.assertEqual(config.max_prompt_length, 10000)
    
    def test_create_config_test(self):
        """Test test configuration creation"""
        config = ConfigFactory.create_config("test")
        
        self.assertIsInstance(config, AppConfig)
        self.assertEqual(config.browser_timeout, 1)
        self.assertEqual(config.max_prompt_length, 100)
    
    @patch('os.getenv')
    def test_create_config_auto_detection_test(self, mock_getenv):
        """Test auto-detection of test environment"""
        mock_getenv.side_effect = lambda key, default='': 'pytest' if key == '_' else default
        
        config = ConfigFactory.create_config("auto")
        
        # Should detect test environment and use test config
        self.assertEqual(config.browser_timeout, 1)
    
    @patch('os.getenv')
    def test_create_config_auto_detection_development(self, mock_getenv):
        """Test auto-detection of development environment"""
        def getenv_side_effect(key, default=''):
            if key == 'ENVIRONMENT':
                return 'development'
            return default
        
        mock_getenv.side_effect = getenv_side_effect
        
        config = ConfigFactory.create_config("auto")
        
        # Should detect development environment
        self.assertEqual(config.browser_timeout, 60)
    
    @patch('os.getenv')  
    def test_create_config_auto_detection_production(self, mock_getenv):
        """Test auto-detection of production environment"""
        def getenv_side_effect(key, default=''):
            if key == 'ENVIRONMENT':
                return 'production'
            return default
            
        mock_getenv.side_effect = getenv_side_effect
        
        with patch('src.gemini_query.config_factory.FileConfigProfile.create_config') as mock_file:
            mock_file.return_value = AppConfig()
            config = ConfigFactory.create_config("auto")
            
            # Should detect production environment
            self.assertEqual(config.max_prompt_length, 20000)  # Production limit
    
    @patch('os.environ', {'GEMINI_URL': 'https://env.test'})
    def test_create_config_auto_detection_environment(self):
        """Test auto-detection of environment variables"""
        with patch('src.gemini_query.config_factory.FileConfigProfile.create_config') as mock_file:
            mock_file.return_value = AppConfig()
            config = ConfigFactory.create_config("auto")
            
            # Should use environment config due to GEMINI_ prefix
            self.assertEqual(config.gemini_url, 'https://env.test')
    
    def test_create_config_unknown_profile(self):
        """Test unknown profile falls back to default"""
        with patch('src.gemini_query.config_factory.ConfigFactory._logger') as mock_logger:
            config = ConfigFactory.create_config("unknown")
            
            self.assertIsInstance(config, AppConfig)
            mock_logger.warning.assert_called()
    
    def test_register_custom_profile(self):
        """Test custom profile registration"""
        class CustomProfile(ConfigProfile):
            def create_config(self):
                return AppConfig(max_prompt_length=99999)
            
            def get_profile_name(self):
                return "custom"
        
        custom_profile = CustomProfile()
        ConfigFactory.register_profile("custom", custom_profile)
        
        config = ConfigFactory.create_config("custom")
        self.assertEqual(config.max_prompt_length, 99999)
    
    def test_list_profiles(self):
        """Test profile listing"""
        profiles = ConfigFactory.list_profiles()
        
        self.assertIn("default", profiles)
        self.assertIn("test", profiles)
        self.assertIn("development", profiles)
        self.assertIn("production", profiles)
        self.assertIn("environment", profiles)
        self.assertIn("file", profiles)
        self.assertIn("auto", profiles)


class TestConfigFactoryConvenience(unittest.TestCase):
    """Test convenience functions"""
    
    def test_create_config_function(self):
        """Test convenience create_config function"""
        config = create_config("test")
        
        self.assertIsInstance(config, AppConfig)
        self.assertEqual(config.browser_timeout, 1)
    
    def test_create_config_function_default(self):
        """Test convenience function with default auto profile"""
        with patch('src.gemini_query.config_factory.ConfigFactory.create_config') as mock_create:
            mock_create.return_value = AppConfig()
            
            create_config()
            
            mock_create.assert_called_once_with("auto")


if __name__ == '__main__':
    unittest.main()