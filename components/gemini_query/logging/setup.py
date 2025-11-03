"""Structured logging configuration using structlog.

This module provides a simplified, production-ready logging setup using structlog,
following industry best practices for structured logging.
"""

import sys
from typing import Any

import structlog
from structlog.types import Processor


def configure_structlog(
    log_level: str = "INFO",
    use_json: bool = False,
) -> None:
    """Configure structlog for the application.

    Args:
        log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        use_json: If True, output JSON logs; otherwise use colored console output

    Example:
        >>> configure_structlog(log_level="DEBUG", use_json=False)
        >>> logger = get_logger(__name__)
        >>> logger.info("application_started", version="1.0.0")
    """
    # Shared processors for all log entries
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    # Choose renderer based on environment
    if use_json or not sys.stderr.isatty():
        # JSON output for production/containers
        renderer: Processor = structlog.processors.JSONRenderer()
    else:
        # Colored console output for development
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=shared_processors
        + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Configure standard library logging for structlog integration
    import logging.config

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "structlog": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processors": [
                        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                        renderer,
                    ],
                    "foreign_pre_chain": shared_processors,
                },
            },
            "handlers": {
                "default": {
                    "level": log_level,
                    "class": "logging.StreamHandler",
                    "formatter": "structlog",
                },
            },
            "loggers": {
                "": {
                    "handlers": ["default"],
                    "level": log_level,
                    "propagate": True,
                },
            },
        }
    )


def get_logger(name: str) -> Any:
    """Get a structlog logger instance.

    Args:
        name: Logger name, typically __name__

    Returns:
        Configured structlog BoundLogger instance

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("user_login", user_id=123, ip="192.168.1.1")
    """
    return structlog.get_logger(name)


def reset_logging() -> None:
    """Reset structlog configuration to defaults.

    Useful for testing or reconfiguration scenarios.
    """
    structlog.reset_defaults()
