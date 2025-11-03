"""Application Dependency Injection Container

Simple and focused container for managing core application dependencies.
"""

from dependency_injector import containers, providers

from gemini_query.browser.service import BrowserManager
from gemini_query.config.unified import AppConfig
from gemini_query.logging import get_logger
from gemini_query.query.service import QueryProcessor, URLGenerator


class Container(containers.DeclarativeContainer):
    """Main application container for dependency injection.

    Provides centralized dependency management with clear configuration.
    """

    # Configuration
    config = providers.Configuration()

    # Logging - Singleton to ensure single logger instance
    logger = providers.Singleton(get_logger)

    # Config instances - Singleton for application-wide settings
    app_config = providers.Singleton(AppConfig)

    # URL Generator - Factory for creating URL generators per request
    url_generator = providers.Factory(
        URLGenerator,
        config=app_config
    )

    # Browser Manager - Factory for browser automation
    browser_manager = providers.Factory(
        BrowserManager,
        config=app_config
    )

    # Query Processor - Factory for query processing workflow
    query_processor = providers.Factory(
        QueryProcessor,
        config=app_config
    )


def create_container(profile_name: str = "auto") -> Container:
    """Create and configure the application container.

    Args:
        profile_name: Configuration profile to use

    Returns:
        Configured container instance
    """
    container = Container()
    container.config.profile_name.from_value(profile_name)
    container.init_resources()
    return container
