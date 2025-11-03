"""Unified configuration combining all modular components."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .application import ApplicationConfig
from .browser import BrowserConfig
from .network import NetworkConfig


class AppConfig(BaseSettings):
    """Unified application configuration combining all modular components.

    This is the main configuration class that brings together all
    specialized configuration modules for easy access and validation.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="forbid"
    )

    # Modular configuration components
    application: ApplicationConfig = Field(
        default_factory=ApplicationConfig,
        description="Application-wide settings"
    )

    browser: BrowserConfig = Field(
        default_factory=BrowserConfig,
        description="Browser automation settings"
    )

    network: NetworkConfig = Field(
        default_factory=NetworkConfig,
        description="Network and server settings"
    )

    # Legacy property access for backward compatibility
    @property
    def gemini_url(self) -> str:
        """Legacy access to Gemini URL."""
        return self.application.gemini_url

    @property
    def browser_path(self) -> str:
        """Legacy access to browser path."""
        return self.browser.browser_path

    @property
    def localhost_port(self) -> int:
        """Legacy access to localhost port."""
        return self.network.localhost_port

    @property
    def browser_timeout(self) -> int:
        """Legacy access to browser timeout."""
        return self.network.browser_timeout

    @property
    def max_prompt_length(self) -> int:
        """Legacy access to max prompt length."""
        return self.application.max_prompt_length

    @property
    def encoding(self) -> str:
        """Legacy access to encoding."""
        return self.application.encoding

    @property
    def temp_file_path(self) -> str:
        """Legacy access to temp file path."""
        return self.application.temp_file_path

    @property
    def supported_browsers(self) -> list[str]:
        """Legacy access to supported browsers."""
        return self.browser.supported_browsers
