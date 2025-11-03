"""CLI Core - Main Typer application with commands."""

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Import from Polylith components - Absolute imports only
from gemini_query.di.container import Container, create_container
from gemini_query.logging import configure_structlog, get_logger
from gemini_query.utils.errors import ConfigurationError, GeminiQueryError

# Create the main Typer app
app = typer.Typer(
    name="gemini-query",
    help="Advanced CLI for Google Gemini AI with intelligent browser automation",
    rich_markup_mode="rich",
    context_settings={"help_option_names": ["-h", "--help"]},
    no_args_is_help=True,
)

# Create rich console for output
console = Console()

# Initialize logging (will be configured in main callback)
logger = get_logger(__name__)

# Create DI container
container: Container | None = None


def get_container() -> Container:
    """Get or create the DI container.

    Returns:
        Configured DI container
    """
    global container
    if container is None:
        container = create_container()
    return container

# Type aliases for cleaner code
VerboseOption = Annotated[
    bool,
    typer.Option("--verbose", "-v", help="Enable verbose output"),
]

ConfigOption = Annotated[
    Path | None,
    typer.Option(
        "--config",
        "-c",
        help="Path to configuration file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
]


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
        from . import __version__

        console.print(f"gemini-query version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    verbose: VerboseOption = False,
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            callback=version_callback,
            help="Show [bold blue]version[/bold blue] and exit",
        ),
    ] = None,
) -> None:
    """Advanced CLI for Google Gemini AI with intelligent browser automation.

    This tool provides a modern, type-safe command-line interface for interacting
    with [bold blue]Google Gemini AI[/bold blue] using browser automation and
    multiple data transfer methods.

    [bold green]Features:[/bold green]
    • Intelligent browser detection and automation
    • Cross-platform support (Windows, macOS, Linux)
    • Multiple data transfer methods with fallbacks
    • Rich console output and progress indicators
    • Comprehensive error handling and diagnostics
    """
    # Configure structlog based on verbosity
    log_level = "DEBUG" if verbose else "INFO"
    configure_structlog(log_level=log_level, use_json=False)

    if verbose:
        logger.debug("verbose_mode_enabled", log_level=log_level)


@app.command()
def query(
    prompt: Annotated[
        str, typer.Argument(help="Query text to send to [bold blue]Gemini AI[/bold blue]")
    ],
    max_length: Annotated[
        int | None,
        typer.Option(
            "--max-length",
            "-l",
            help="Maximum prompt length override",
            rich_help_panel="Query Options",
        ),
    ] = None,
    config: ConfigOption = None,
    verbose: VerboseOption = False,
) -> None:
    """Send a query to Gemini AI with intelligent browser automation.

    [bold green]Examples:[/bold green]

    • Basic query:
      [dim]$ gemini-query query "What is machine learning?"[/dim]

    • Query with length limit:
      [dim]$ gemini-query query "Long text..." --max-length 5000[/dim]

    • Verbose output:
      [dim]$ gemini-query query "Debug query" --verbose[/dim]
    """
    import asyncio

    from gemini_query.utils.errors import ConfigurationError, GeminiQueryError

    try:
        # Get DI container
        di_container = get_container()

        # Get query processor from container
        processor = di_container.query_processor()

        # Process the query asynchronously
        with console.status("[bold green]Processing query...[/bold green]"):
            # Run async function in event loop
            success = asyncio.run(processor.process_query(prompt, max_length))

        if success:
            console.print("[green]✓ Query sent successfully![/green]")
        else:
            console.print("[red]✗ Failed to send query[/red]")
            raise typer.Exit(1)

    except ConfigurationError as e:
        console.print(f"[red]⚙️  Configuration Error: {e}[/red]")
        raise typer.Exit(1)
    except GeminiQueryError as e:
        console.print(f"[red]🔥 Error: {e}[/red]")
        raise typer.Exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]⏹️  Operation cancelled by user[/yellow]")
        raise typer.Exit(130)


@app.command()
def setup(
    config: ConfigOption = None,
    force: Annotated[
        bool, typer.Option("--force", "-f", help="Overwrite existing configuration")
    ] = False,
) -> None:
    """Set up configuration for gemini-query."""
    try:
        console.print("[yellow]Setup command implementation pending[/yellow]")

    except GeminiQueryError as e:
        console.print(
            Panel(
                Text(f"Setup failed: {e}", style="bold red"),
                title="[bold red]Setup Error[/bold red]",
                expand=False,
            )
        )
        raise typer.Exit(1)


@app.command()
def validate(config: ConfigOption = None) -> None:
    """Validate configuration file."""
    try:
        console.print("[yellow]Validate command implementation pending[/yellow]")

    except ConfigurationError as e:
        console.print(
            Panel(
                Text(f"Configuration Error: {e}", style="bold red"),
                title="[bold red]Validation Failed[/bold red]",
                expand=False,
            )
        )
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
