"""Application-wide configuration settings."""

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApplicationConfig(BaseSettings):
    """Application-wide configuration settings.

    This configuration handles general application settings like
    logging, file paths, and operational parameters.
    """

    model_config = SettingsConfigDict(
        env_prefix="GEMINI_APP_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="forbid"
    )

    # URLs and paths
    gemini_url: str = Field(
        default="https://aistudio.google.com/prompts/new_chat",
        description="Base URL for Gemini AI interface"
    )

    temp_file_path: str = Field(
        default="temp/gemini_input.txt",
        description="Path for temporary data files"
    )

    # Logging settings
    log_retention_days: int = Field(
        default=365,
        ge=1,
        description="Days to keep log files"
    )

    log_level: str = Field(
        default="INFO",
        description="Default logging level"
    )

    # Text processing
    encoding: str = Field(
        default="utf-8",
        description="Text encoding for file operations"
    )

    max_prompt_length: int = Field(
        default=10000,
        ge=1,
        description="Maximum prompt length before manual input"
    )

    # Feature flags
    enable_rich_output: bool = Field(
        default=True,
        description="Enable rich console output"
    )

    enable_progress_bars: bool = Field(
        default=True,
        description="Enable progress indicators"
    )

    @field_validator("encoding", mode="after")
    @classmethod
    def validate_encoding(cls, v: str) -> str:
        """Validate text encoding."""
        if not v.strip():
            raise ValueError("Encoding cannot be empty")
        return v.strip().lower()

    @field_validator("gemini_url", mode="after")
    @classmethod
    def validate_gemini_url(cls, v: str) -> str:
        """Validate Gemini URL format."""
        if not v.startswith(("https://", "http://")):
            raise ValueError("Gemini URL must start with http:// or https://")
        return v

    @field_validator("temp_file_path", mode="after")
    @classmethod
    def validate_temp_path(cls, v: str) -> str:
        """Ensure temp directory exists."""
        temp_path = Path(v)
        temp_path.parent.mkdir(parents=True, exist_ok=True)
        return v

    @field_validator("log_level", mode="after")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        level = v.upper()
        if level not in valid_levels:
            raise ValueError(f"Log level must be one of: {', '.join(valid_levels)}")
        return level
