"""Network and server configuration settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class NetworkConfig(BaseSettings):
    """Network and server related configuration settings.

    This configuration handles all network-related settings including
    server ports, timeouts, and connection parameters.
    """

    model_config = SettingsConfigDict(
        env_prefix="GEMINI_NET_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="forbid"
    )

    # Server settings
    localhost_port: int = Field(
        default=8765,
        ge=1024,
        le=65535,
        description="Port for HTTP server (must match userscript)"
    )

    # Timeout settings
    browser_timeout: int = Field(
        default=30,
        ge=1,
        description="Browser operation timeout in seconds"
    )

    connection_timeout: int = Field(
        default=10,
        ge=1,
        description="Network connection timeout in seconds"
    )

    # Retry settings
    max_retries: int = Field(
        default=3,
        ge=0,
        description="Maximum number of retry attempts"
    )

    retry_delay: float = Field(
        default=1.0,
        ge=0.1,
        description="Delay between retry attempts in seconds"
    )
