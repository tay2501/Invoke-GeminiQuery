"""Dependency Injection Module

Provides container for managing application dependencies with clean separation.
"""

from .container import Container, create_container

__all__ = ["Container", "create_container"]
