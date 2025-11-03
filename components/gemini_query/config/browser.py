"""Browser automation configuration settings."""

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .legacy import BrowserType


class BrowserConfig(BaseSettings):
    """Browser automation configuration settings.

    This configuration handles browser detection, paths, and
    automation-specific settings.
    """

    model_config = SettingsConfigDict(
        env_prefix="GEMINI_BROWSER_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="forbid"
    )

    # Browser paths
    browser_path: str = Field(
        default="",
        description="Path to browser executable"
    )

    firefox_path: str = Field(
        default="",
        description="Legacy Firefox path for backward compatibility"
    )

    # Browser selection
    supported_browsers: list[str] = Field(
        default_factory=lambda: [
            BrowserType.FIREFOX.value,
            BrowserType.CHROME.value,
            BrowserType.CHROME_GOOGLE.value,
            BrowserType.EDGE.value,
            BrowserType.EDGE_MS.value
        ],
        description="List of supported browser names"
    )

    # Browser behavior
    headless_mode: bool = Field(
        default=False,
        description="Run browser in headless mode"
    )

    auto_detect_browser: bool = Field(
        default=True,
        description="Automatically detect available browsers"
    )

    # User script settings
    userscript_enabled: bool = Field(
        default=True,
        description="Enable userscript injection"
    )

    userscript_path: str = Field(
        default="gemini_auto_input.user.js",
        description="Path to userscript file"
    )

    @field_validator("browser_path", "firefox_path", mode="after")
    @classmethod
    def validate_browser_paths(cls, v: str) -> str:
        """Validate browser paths if provided."""
        if v and not Path(v).exists():
            # Don't raise error, just log warning - browser auto-detection will handle
            pass
        return v

    @field_validator("userscript_path", mode="after")
    @classmethod
    def validate_userscript_path(cls, v: str) -> str:
        """Validate userscript path."""
        if v and not Path(v).exists():
            # Don't raise error for now, but log warning
            pass
        return v
