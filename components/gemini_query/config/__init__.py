"""Modular configuration management for Gemini Query.

This module provides a clean separation of configuration concerns
into focused, testable components.
"""

from .application import ApplicationConfig
from .browser import BrowserConfig
from .legacy import BrowserType, Platform
from .network import NetworkConfig
from .unified import AppConfig

__all__ = [
    "AppConfig",
    "ApplicationConfig",
    "BrowserConfig",
    "BrowserType",
    "NetworkConfig",
    "Platform",
]
