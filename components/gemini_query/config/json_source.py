"""Custom JSON configuration source for Pydantic Settings.

Allows unified.AppConfig to load from configs/config.json while maintaining
compatibility with environment variables and .env files.
"""

import json
from pathlib import Path
from typing import Any

from pydantic_settings import PydanticBaseSettingsSource


class JsonConfigSource(PydanticBaseSettingsSource):
    """Custom settings source that loads from JSON file with prefix mapping.

    This source reads from configs/config.json and maps flat JSON keys to
    nested Pydantic models using the env_prefix configuration.
    """

    def __init__(self, settings_cls: type, config_path: Path | str = "configs/config.json"):
        """Initialize JSON config source.

        Args:
            settings_cls: The Settings class using this source
            config_path: Path to JSON configuration file
        """
        super().__init__(settings_cls)
        self.config_path = Path(config_path)
        self._config_data: dict[str, Any] = {}
        self._loaded = False

        if self.config_path.exists():
            try:
                with open(self.config_path, encoding='utf-8') as f:
                    self._config_data = json.load(f)
                    self._loaded = True
            except (json.JSONDecodeError, OSError) as e:
                # Log warning but don't fail - fall back to other sources
                print(f"Warning: Could not load {self.config_path}: {e}")

    def get_field_value(
        self, field: Any, field_name: str
    ) -> tuple[Any, str, bool]:
        """Get field value from JSON config.

        Args:
            field: Field info from Pydantic
            field_name: Name of the field

        Returns:
            Tuple of (value, key, is_complex)
        """
        # For nested models (application, browser, network), create sub-dict
        if field_name in ("application", "browser", "network"):
            nested_data = self._get_nested_config(field_name)
            if nested_data:
                return nested_data, field_name, True
            return None, field_name, False

        # For top-level fields, return from config data
        if field_name in self._config_data:
            return self._config_data[field_name], field_name, False

        return None, field_name, False

    def _get_nested_config(self, section: str) -> dict[str, Any]:
        """Extract nested configuration for a section.

        Maps flat JSON keys to nested structure based on common prefixes.
        For example:
            - browser_path -> browser.browser_path
            - gemini_url -> application.gemini_url

        Args:
            section: Section name (application, browser, network)

        Returns:
            Dictionary of configuration values for the section
        """
        result = {}

        # Define mapping of JSON keys to section fields
        mappings = {
            "application": [
                "gemini_url",
                "temp_file_path",
                "log_retention_days",
                "log_level",
                "encoding",
                "max_prompt_length",
                "enable_rich_output",
                "enable_progress_bars"
            ],
            "browser": [
                "browser_path",
                "firefox_path",
                "supported_browsers",
                "headless_mode",
                "auto_detect_browser",
                "userscript_enabled",
                "userscript_path"
            ],
            "network": [
                "localhost_port",
                "browser_timeout",
                "connection_timeout",
                "max_retries",
                "retry_delay"
            ]
        }

        # Extract relevant keys for this section
        for key in mappings.get(section, []):
            if key in self._config_data:
                result[key] = self._config_data[key]

        return result

    def __call__(self) -> dict[str, Any]:
        """Return all configuration data mapped to nested structure.

        Returns:
            Dictionary of configuration values with nested models
        """
        if not self._loaded:
            return {}

        # Create nested structure for AppConfig
        return {
            "application": self._get_nested_config("application"),
            "browser": self._get_nested_config("browser"),
            "network": self._get_nested_config("network"),
        }


def create_json_source(config_path: Path | str = "configs/config.json"):
    """Factory function to create JsonConfigSource.

    Args:
        config_path: Path to JSON configuration file

    Returns:
        Function that creates JsonConfigSource instance
    """
    def _source(settings_cls: type) -> JsonConfigSource:
        return JsonConfigSource(settings_cls, config_path)
    return _source
