#!/usr/bin/env python3
"""
Configuration management for Gemini Auto Query.

This module handles all configuration-related functionality including
loading settings from JSON files and providing platform-specific configurations.
"""

import json
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class Platform(Enum):
    """Supported platforms"""
    WINDOWS = "win32"
    MACOS = "darwin"
    LINUX = "linux"

    @classmethod
    def current(cls) -> 'Platform':
        """Get current platform"""
        match sys.platform:
            case "win32":
                return cls.WINDOWS
            case "darwin":
                return cls.MACOS
            case _:
                return cls.LINUX


class BrowserType(Enum):
    """Supported browser types"""
    FIREFOX = "firefox"
    CHROME = "chrome"
    CHROME_GOOGLE = "google-chrome"
    EDGE = "edge"
    EDGE_MS = "msedge"
    SAFARI = "safari"
    SYSTEM_DEFAULT = "system_default"


@dataclass(kw_only=True)
class AppConfig:
    """Application configuration with type safety and validation"""
    gemini_url: str = "https://aistudio.google.com/prompts/new_chat"
    browser_path: str = ""
    firefox_path: str = ""  # For backward compatibility
    temp_file_path: str = "temp/gemini_input.txt"
    localhost_port: int = 8765
    log_retention_days: int = 365
    encoding: str = "utf-8"
    max_prompt_length: int = 10000
    browser_timeout: int = 30
    supported_browsers: list[str] = field(default_factory=lambda: [
        "firefox", "chrome", "google-chrome", "microsoft-edge", "msedge"
    ])

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'AppConfig':
        """Create AppConfig from dictionary with validation"""
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)

    def to_dict(self) -> dict[str, Any]:
        """Convert AppConfig to dictionary"""
        return {
            field.name: getattr(self, field.name)
            for field in self.__dataclass_fields__.values()
        }

    def validate(self) -> bool:
        """Validate configuration values"""
        if self.max_prompt_length <= 0:
            raise ValueError("max_prompt_length must be positive")
        if self.browser_timeout <= 0:
            raise ValueError("browser_timeout must be positive")
        if not self.encoding:
            raise ValueError("encoding cannot be empty")
        return True


class ConfigLoader:
    """Configuration loader with fallback to defaults"""

    def __init__(self, config_path: Path | None = None):
        self.config_path = config_path or Path("config.json")

    def load(self) -> AppConfig:
        """
        Load configuration from file with fallback to defaults.

        Returns:
            AppConfig: Configuration instance
        """
        default_config = AppConfig()

        if not self.config_path.exists():
            print(f"No {self.config_path.name} found, using default configuration")
            return default_config

        try:
            with open(self.config_path, encoding='utf-8') as file:
                user_data = json.load(file)
                config_dict = default_config.to_dict()
                config_dict.update(user_data)
                config = AppConfig.from_dict(config_dict)
                config.validate()
                print(f"Configuration loaded from {self.config_path}")
                return config
        except json.JSONDecodeError as error:
            print(f"Warning: Could not parse {self.config_path.name}: {error}")
            print("Using default configuration")
        except ValueError as error:
            print(f"Warning: Invalid configuration: {error}")
            print("Using default configuration")
        except OSError as error:
            print(f"Warning: Could not read {self.config_path.name}: {error}")
            print("Using default configuration")

        return default_config
