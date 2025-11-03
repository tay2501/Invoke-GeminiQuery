#!/usr/bin/env python3
"""
Configuration factory for Gemini Auto Query.

This module implements the Factory pattern to create different
configuration profiles for various environments and use cases.
"""

import contextlib
import os
from abc import ABC, abstractmethod
from pathlib import Path

from .config import AppConfig, ConfigLoader
from .logging_config import get_application_logger


class ConfigProfile(ABC):
    """Abstract base class for configuration profiles"""

    @abstractmethod
    def create_config(self) -> AppConfig:
        """Create configuration for this profile"""
        pass

    @abstractmethod
    def get_profile_name(self) -> str:
        """Get profile name"""
        pass


class DefaultConfigProfile(ConfigProfile):
    """Default configuration profile"""

    def create_config(self) -> AppConfig:
        """Create default configuration"""
        return AppConfig()

    def get_profile_name(self) -> str:
        return "default"


class FileConfigProfile(ConfigProfile):
    """Configuration profile that loads from file"""

    def __init__(self, config_path: Path | None = None):
        self.config_path = config_path

    def create_config(self) -> AppConfig:
        """Load configuration from file"""
        loader = ConfigLoader(self.config_path)
        return loader.load()

    def get_profile_name(self) -> str:
        return f"file:{self.config_path or 'config.json'}"


class TestConfigProfile(ConfigProfile):
    """Configuration profile optimized for testing"""

    def create_config(self) -> AppConfig:
        """Create test configuration with short timeouts and small limits"""
        return AppConfig(
            gemini_url="http://localhost:8080/test",
            browser_timeout=1,
            max_prompt_length=100,
            browser_path="echo",  # Use echo for testing
            temp_file_path="temp/test_gemini_input.txt"
        )

    def get_profile_name(self) -> str:
        return "test"


class DevelopmentConfigProfile(ConfigProfile):
    """Configuration profile for development"""

    def create_config(self) -> AppConfig:
        """Create development configuration with debug settings"""
        return AppConfig(
            browser_timeout=60,  # Longer timeout for debugging
            max_prompt_length=50000,  # Larger prompts for testing
            temp_file_path="temp/dev_gemini_input.txt"
        )

    def get_profile_name(self) -> str:
        return "development"


class ProductionConfigProfile(ConfigProfile):
    """Configuration profile for production"""

    def create_config(self) -> AppConfig:
        """Create production configuration with optimized settings"""
        # Load from file but with production overrides
        base_config = FileConfigProfile().create_config()

        # Production optimizations
        return AppConfig(
            gemini_url=base_config.gemini_url,
            browser_path=base_config.browser_path,
            firefox_path=base_config.firefox_path,
            temp_file_path="temp/prod_gemini_input.txt",
            localhost_port=base_config.localhost_port,
            log_retention_days=30,  # Shorter retention for production
            encoding=base_config.encoding,
            max_prompt_length=20000,  # Conservative limit
            browser_timeout=15,  # Faster timeout for production
            supported_browsers=base_config.supported_browsers
        )

    def get_profile_name(self) -> str:
        return "production"


class EnvironmentConfigProfile(ConfigProfile):
    """Configuration profile that adapts based on environment variables"""

    def create_config(self) -> AppConfig:
        """Create configuration based on environment variables"""
        # Start with file config as base
        base_config = FileConfigProfile().create_config()

        # Override with environment variables
        overrides = {}

        if os.getenv('GEMINI_URL'):
            overrides['gemini_url'] = os.getenv('GEMINI_URL')

        if os.getenv('GEMINI_MAX_PROMPT_LENGTH'):
            with contextlib.suppress(ValueError):
                overrides['max_prompt_length'] = int(os.getenv('GEMINI_MAX_PROMPT_LENGTH'))

        if os.getenv('GEMINI_BROWSER_PATH'):
            overrides['browser_path'] = os.getenv('GEMINI_BROWSER_PATH')

        if os.getenv('GEMINI_BROWSER_TIMEOUT'):
            with contextlib.suppress(ValueError):
                overrides['browser_timeout'] = int(os.getenv('GEMINI_BROWSER_TIMEOUT'))

        # Create new config with overrides
        base_dict = base_config.to_dict()
        base_dict.update(overrides)

        return AppConfig.from_dict(base_dict)

    def get_profile_name(self) -> str:
        return "environment"


class ConfigFactory:
    """Factory for creating configuration instances"""

    _profiles: dict[str, ConfigProfile] = {}
    _logger = get_application_logger("config_factory")

    @classmethod
    def register_profile(cls, name: str, profile: ConfigProfile) -> None:
        """Register a configuration profile"""
        cls._profiles[name] = profile
        cls._logger.info("Registered configuration profile", profile_name=name)

    @classmethod
    def create_config(cls, profile_name: str = "auto") -> AppConfig:
        """
        Create configuration using the specified profile.

        Args:
            profile_name: Name of the profile to use ("auto", "default", "test", etc.)

        Returns:
            AppConfig instance
        """
        cls._logger.debug("Creating configuration", requested_profile=profile_name)

        # Auto-detect profile if not specified
        if profile_name == "auto":
            profile_name = cls._detect_profile()
            cls._logger.info("Auto-detected configuration profile", detected_profile=profile_name)

        # Get or create profile
        profile = cls._get_or_create_profile(profile_name)

        # Create configuration
        config = profile.create_config()

        cls._logger.info(
            "Configuration created successfully",
            profile_name=profile.get_profile_name(),
            max_prompt_length=config.max_prompt_length,
            browser_timeout=config.browser_timeout
        )

        return config

    @classmethod
    def _detect_profile(cls) -> str:
        """Auto-detect which profile to use based on environment"""
        # Check for test environment
        if os.getenv('PYTEST_CURRENT_TEST') or 'pytest' in os.getenv('_', ''):
            return "test"

        # Check for development environment
        if os.getenv('ENVIRONMENT') == 'development' or os.getenv('DEBUG') == '1':
            return "development"

        # Check for production environment
        if os.getenv('ENVIRONMENT') == 'production':
            return "production"

        # Check for environment variable overrides
        if any(key.startswith('GEMINI_') for key in os.environ):
            return "environment"

        # Default to file-based configuration
        return "file"

    @classmethod
    def _get_or_create_profile(cls, profile_name: str) -> ConfigProfile:
        """Get registered profile or create built-in profile"""
        if profile_name in cls._profiles:
            return cls._profiles[profile_name]

        # Create built-in profiles
        built_in_profiles = {
            "default": DefaultConfigProfile(),
            "file": FileConfigProfile(),
            "test": TestConfigProfile(),
            "development": DevelopmentConfigProfile(),
            "production": ProductionConfigProfile(),
            "environment": EnvironmentConfigProfile(),
        }

        if profile_name in built_in_profiles:
            return built_in_profiles[profile_name]

        cls._logger.warning(f"Unknown profile '{profile_name}', using default")
        return DefaultConfigProfile()

    @classmethod
    def list_profiles(cls) -> dict[str, str]:
        """List all available profiles"""
        built_in = {
            "default": "Default configuration with hardcoded values",
            "file": "Load configuration from config.json",
            "test": "Testing configuration with short timeouts",
            "development": "Development configuration with debug settings",
            "production": "Production configuration with optimized settings",
            "environment": "Configuration with environment variable overrides",
            "auto": "Auto-detect profile based on environment",
        }

        registered = {
            name: f"Custom profile: {profile.get_profile_name()}"
            for name, profile in cls._profiles.items()
        }

        return {**built_in, **registered}


# Convenience function for easy configuration creation
def create_config(profile: str = "auto") -> AppConfig:
    """Create configuration using the factory"""
    return ConfigFactory.create_config(profile)
