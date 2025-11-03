"""Development entry point for Gemini Query CLI with Polylith architecture."""
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm
from rich.table import Table
from rich.text import Text

# Import from Polylith components
from gemini_query.logging.setup import get_logger, setup_logging
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
logger = get_logger()

# Global options
VerboseOption = Annotated[
    bool,
    typer.Option(
        "--verbose", "-v",
        help="Enable verbose output"
    )
]

ConfigOption = Annotated[
    Path | None,
    typer.Option(
        "--config", "-c",
        help="Path to configuration file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    )
]


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
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
            help="Show [bold blue]version[/bold blue] and exit"
        )
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
    # Set up logging based on verbosity
    log_level = "DEBUG" if verbose else "INFO"
    setup_logging(level=log_level, console=console)

    if verbose:
        logger.debug("Verbose mode enabled")


@app.command()
def query(
    prompt: Annotated[str, typer.Argument(
        help="Query text to send to [bold blue]Gemini AI[/bold blue]"
    )],
    max_length: Annotated[int | None, typer.Option(
        "--max-length", "-l",
        help="Maximum prompt length override",
        rich_help_panel="Query Options"
    )] = None,
    config: ConfigOption = None,
    verbose: VerboseOption = False,
) -> None:
    """Send a query to Gemini AI with intelligent browser automation.

    [bold green]Examples:[/bold green]

    • Basic query:
      [dim]$ gemini-query "What is machine learning?"[/dim]

    • Query with length limit:
      [dim]$ gemini-query "Long text..." --max-length 5000[/dim]

    • Verbose output:
      [dim]$ gemini-query "Debug query" --verbose[/dim]
    """
    try:
        # Determine profile based on config
        profile_name = "file" if config else "auto"

        # Show progress with modern spinner
        with Progress(
            SpinnerColumn(spinner_style="blue"),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task(
                "[bold blue]Initializing application...[/bold blue]",
                total=None
            )

            # Create CLI app with dependency injection
            from gemini_query.cli_app.core import create_app
            app_instance = create_app(profile_name)

            progress.update(
                task,
                description="[bold yellow]Processing query...[/bold yellow]"
            )

            # Execute query with injected services
            app_instance.run_query(prompt, interactive=verbose)

        # Enhanced success reporting
        console.print(Panel(
            Text("Query completed successfully! 🚀", style="bold green"),
            subtitle=(
                f"[dim]{prompt[:60]}...[/dim]"
                if len(prompt) > 60 else f"[dim]{prompt}[/dim]"
            ),
            title="[bold blue]✨ Gemini AI ✨[/bold blue]",
            expand=False,
            padding=(1, 2),
            border_style="green"
        ))

    except ConfigurationError as e:
        console.print(f"[red]⚙️  Configuration Error: {e}[/red]")
        if "not found" in str(e):
            if Confirm.ask("Would you like to create a sample configuration?"):
                setup_config()
        raise typer.Exit(1)
    except GeminiQueryError as e:
        console.print(f"[red]🔥 Error: {e}[/red]")
        raise typer.Exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]⏹️  Operation cancelled by user[/yellow]")
        raise typer.Exit(130)

@app.command()
def query_async(
    prompt: Annotated[str, typer.Argument(
        help="Query text to send to [bold blue]Gemini AI[/bold blue] (async)"
    )],
    max_length: Annotated[int | None, typer.Option(
        "--max-length", "-l",
        help="Maximum prompt length override",
        rich_help_panel="Query Options"
    )] = None,
    batch_size: Annotated[int, typer.Option(
        "--batch-size", "-b",
        help="Number of concurrent queries (advanced)",
        rich_help_panel="Advanced Options"
    )] = 1,
    config: ConfigOption = None,
    verbose: VerboseOption = False,
) -> None:
    """Send a query to Gemini AI using asynchronous processing for better performance.
    
    [bold yellow]⚡ Async Version[/bold yellow] - Provides better performance and resource utilization.
    
    [bold green]Examples:[/bold green]
    
    • Basic async query:
      [dim]$ gemini-query query-async "What is machine learning?"[/dim]
    
    • Multiple concurrent queries:
      [dim]$ gemini-query query-async "Query text" --batch-size 3[/dim]
    """
    import asyncio

    async def _async_query_handler():
        try:
            # Load configuration
            config_loader = ConfigLoader(config)
            app_config = config_loader.load()

            # Show progress with modern spinner
            with Progress(
                SpinnerColumn(spinner_style="cyan"),
                TextColumn("[progress.description]{task.description}"),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task(
                    "[bold cyan]⚡ Processing async query...[/bold cyan]",
                    total=None
                )

                # Use async query processor
                from ..core.async_query import AsyncQueryProcessor

                async with AsyncQueryProcessor(app_config) as processor:
                    progress.update(
                        task,
                        description="[bold yellow]🔗 Connecting to Gemini (async)...[/bold yellow]"
                    )

                    if batch_size > 1:
                        # Process multiple queries for testing/benchmarking
                        queries = [prompt] * batch_size
                        results = await processor.process_multiple_queries(queries)
                        success = all(results)

                        console.print(f"[dim]Processed {batch_size} queries: {sum(results)} successful[/dim]")
                    else:
                        success = await processor.process_query_async(prompt, max_length)

            # Enhanced success/failure reporting
            if success:
                console.print(Panel(
                    Text("Async query sent successfully! ⚡🚀", style="bold green"),
                    subtitle=(
                        f"[dim]{prompt[:60]}...[/dim]"
                        if len(prompt) > 60 else f"[dim]{prompt}[/dim]"
                    ),
                    title="[bold cyan]⚡ Gemini AI (Async) ⚡[/bold cyan]",
                    expand=False,
                    padding=(1, 2),
                    border_style="cyan"
                ))
            else:
                console.print(Panel(
                    Text("Failed to send async query ❌", style="bold red"),
                    title="[bold red]🚫 Async Error[/bold red]",
                    expand=False,
                    border_style="red"
                ))

        except ConfigurationError as e:
            console.print(f"[red]⚙️  Configuration Error: {e}[/red]")
            if "not found" in str(e):
                if Confirm.ask("Would you like to create a sample configuration?"):
                    setup_config()
            raise typer.Exit(1)
        except GeminiQueryError as e:
            console.print(f"[red]🔥 Async Error: {e}[/red]")
            raise typer.Exit(1)
        except KeyboardInterrupt:
            console.print("\n[yellow]⏹️  Async operation cancelled by user[/yellow]")
            raise typer.Exit(130)

    # Run the async handler
    try:
        asyncio.run(_async_query_handler())
    except KeyboardInterrupt:
        console.print("\n[yellow]⏹️  Operation cancelled[/yellow]")
        raise typer.Exit(130)


@app.command()
def setup(
    config: ConfigOption = None,
    force: Annotated[
        bool,
        typer.Option("--force", "-f", help="Overwrite existing configuration")
    ] = False,
) -> None:
    """Set up configuration for gemini-query.
    
    Args:
        config: Path to configuration file
        force: Overwrite existing configuration if it exists
    """
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("Setting up configuration...", total=None)
            setup_config(config, force)

        console.print(Panel(
            Text("Configuration setup completed successfully!", style="bold green"),
            title="[bold blue]Setup Complete[/bold blue]",
            expand=False,
            padding=(1, 2)
        ))

    except GeminiQueryError as e:
        console.print(Panel(
            Text(f"Setup failed: {e}", style="bold red"),
            title="[bold red]Setup Error[/bold red]",
            expand=False
        ))
        raise typer.Exit(1)


@app.command()
def validate(
    config: ConfigOption = None,
) -> None:
    """Validate configuration file.
    
    Args:
        config: Path to configuration file
    """
    try:
        config_loader = ConfigLoader(config)
        app_config = config_loader.load()

        console.print(Panel(
            Text("Configuration is valid!", style="bold green"),
            title="[bold blue]Validation Result[/bold blue]",
            expand=False,
            padding=(1, 2)
        ))

        # Create a detailed configuration table
        config_table = Table(title="Configuration Details", show_header=True)
        config_table.add_column("Setting", style="cyan", no_wrap=True)
        config_table.add_column("Value", style="green")
        config_table.add_column("Source", style="dim")

        config_table.add_row("Gemini URL", app_config.gemini_url, "Config/Default")
        config_table.add_row("Browser Path", app_config.browser_path or "Auto-detect", "Config/Auto")
        config_table.add_row("Localhost Port", str(app_config.localhost_port), "Config/Default")
        config_table.add_row("Max Prompt Length", str(app_config.max_prompt_length), "Config/Default")
        config_table.add_row("Browser Timeout", f"{app_config.browser_timeout}s", "Config/Default")
        config_table.add_row("Encoding", app_config.encoding, "Config/Default")

        console.print(config_table)

    except ConfigurationError as e:
        console.print(Panel(
            Text(f"Configuration Error: {e}", style="bold red"),
            title="[bold red]Validation Failed[/bold red]",
            expand=False
        ))
        raise typer.Exit(1)


@app.command()
def doctor(
    config: ConfigOption = None,
    verbose: VerboseOption = False,
) -> None:
    """Run diagnostic checks for system health."""
    console.print(Panel(
        Text("Running system diagnostics...", style="bold blue"),
        title="[bold blue]System Doctor[/bold blue]",
        expand=False,
        padding=(1, 2)
    ))

    try:
        config_loader = ConfigLoader(config)
        app_config = config_loader.load()

        # Create diagnostics table
        diag_table = Table(title="System Diagnostics", show_header=True)
        diag_table.add_column("Check", style="cyan", no_wrap=True)
        diag_table.add_column("Status", style="green")
        diag_table.add_column("Details", style="dim")

        # Configuration check
        diag_table.add_row("Configuration", "[green]Valid[/green]", "All settings validated")

        # Browser availability check
        from ..core.browser import BrowserManager
        browser_manager = BrowserManager(app_config)
        browsers = browser_manager.get_available_commands()

        if browsers:
            diag_table.add_row("Browser Detection", "[green]OK[/green]", f"{len(browsers)} browsers found")
        else:
            diag_table.add_row("Browser Detection", "[yellow]Warning[/yellow]", "No browsers detected")

        # Network port check
        import socket
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                result = s.connect_ex(('localhost', app_config.localhost_port))
                if result == 0:
                    diag_table.add_row("Port Availability", "[yellow]Warning[/yellow]", f"Port {app_config.localhost_port} in use")
                else:
                    diag_table.add_row("Port Availability", "[green]Available[/green]", f"Port {app_config.localhost_port} free")
        except Exception:
            diag_table.add_row("Port Availability", "[red]Error[/red]", "Could not check port")

        # Temp directory check
        temp_path = Path(app_config.temp_file_path).parent
        if temp_path.exists() and temp_path.is_dir():
            diag_table.add_row("Temp Directory", "[green]Available[/green]", str(temp_path))
        else:
            diag_table.add_row("Temp Directory", "[yellow]Warning[/yellow]", "Temp directory missing")

        console.print(diag_table)

    except Exception as e:
        console.print(Panel(
            Text(f"Diagnostic failed: {e}", style="bold red"),
            title="[bold red]Error[/bold red]",
            expand=False
        ))
        raise typer.Exit(1)


@app.command()
def browser_test(
    url: Annotated[str, typer.Argument(help="URL to test browser with")] = "https://google.com",
    config: ConfigOption = None,
    verbose: VerboseOption = False,
) -> None:
    """Test browser launch functionality."""
    console.print(Panel(
        Text(f"Testing browser launch with: {url}", style="bold blue"),
        title="[bold blue]Browser Test[/bold blue]",
        expand=False,
        padding=(1, 2)
    ))

    try:
        config_loader = ConfigLoader(config)
        app_config = config_loader.load()

        from ..core.browser import BrowserManager
        browser_manager = BrowserManager(app_config)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("Launching browser...", total=None)
            success = browser_manager.launch(url)

        if success:
            console.print(Panel(
                Text("Browser launched successfully!", style="bold green"),
                title="[bold green]Test Passed[/bold green]",
                expand=False,
                padding=(1, 2)
            ))
        else:
            console.print(Panel(
                Text("Failed to launch browser", style="bold red"),
                title="[bold red]Test Failed[/bold red]",
                expand=False
            ))
            raise typer.Exit(1)

    except Exception as e:
        console.print(Panel(
            Text(f"Browser test failed: {e}", style="bold red"),
            title="[bold red]Error[/bold red]",
            expand=False
        ))
        raise typer.Exit(1)


def setup_config(
    config_path: Path | None = None,
    force: bool = False
) -> None:
    """Interactive configuration setup.
    
    Args:
        config_path: Path to configuration file
        force: Overwrite existing configuration
        
    Raises:
        ConfigurationError: When setup fails
    """
    config_loader = ConfigLoader(config_path)
    target_path = config_path or Path("config.json")

    # Check if config exists
    if target_path.exists() and not force:
        if not Confirm.ask(
            f"Configuration file {target_path} already exists. Overwrite?"
        ):
            console.print("[yellow]Setup cancelled[/yellow]")
            return

    try:
        # Create sample configuration
        sample_path = config_loader.create_sample()

        # Copy sample to target
        import shutil
        shutil.copy2(sample_path, target_path)

        console.print(f"[green]Created configuration file: {target_path}[/green]")
        console.print("\n[yellow]Next steps:[/yellow]")
        console.print("1. Edit the configuration file to customize settings")
        console.print("2. Install browser extensions (Tampermonkey/Greasemonkey)")
        console.print("3. Install the userscript from gemini_auto_input.user.js")
        console.print("4. Test with: gemini-query query 'Hello, this is a test'")

    except Exception as e:
        raise ConfigurationError(f"Failed to set up configuration: {e}") from e


if __name__ == "__main__":
    app()
