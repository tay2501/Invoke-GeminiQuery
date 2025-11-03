# Gemini Query

🚀 **Advanced Command Line Interface for Google Gemini AI** - Send queries to Google Gemini AI directly from your command line with intelligent browser automation, robust error handling, and modular architecture.

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](LICENSE)
[![uv](https://img.shields.io/badge/package_manager-uv-orange.svg)](https://github.com/astral-sh/uv)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()
[![Architecture](https://img.shields.io/badge/architecture-Polylith-green.svg)](https://polylith.gitbook.io/)
[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/gemini-query/gemini-query)

---

## 📚 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### Core Functionality
- **Multi-Method Data Transfer**: HTTP server, localStorage, URL parameters, and manual input fallbacks
- **Intelligent Browser Automation**: Advanced userscript with multiple UI detection methods
- **Cross-Platform Support**: Works on Windows, macOS, and Linux
- **Flexible Input Methods**: Direct arguments, piped input, file input, and interactive prompts
- **Robust Error Handling**: Comprehensive fallback mechanisms and user-friendly error messages

### Advanced Features
- **Polylith Architecture**: Modular, maintainable, and testable component-based design
- **Dependency Injection**: Clean separation of concerns with DI container
- **Modern Python**: Type hints, async/await, dataclasses, and Pydantic validation
- **Performance Monitoring**: Built-in performance tracking and optimization
- **Structured Logging**: Comprehensive logging with `structlog`
- **Automatic Cleanup**: Intelligent temporary file and resource management

---

## 🏗️ Architecture

### Polylith Architecture

This project uses **Polylith architecture** for superior modularity and maintainability:

```
gemini-query/
├── bases/gemini_query/
│   └── cli_app/              # CLI entry point (Typer application)
│       ├── core.py           # Main CLI commands
│       └── __init__.py       # Version and exports
│
├── components/gemini_query/  # Reusable components
│   ├── browser/              # Browser automation strategies
│   ├── config/               # Configuration management (Pydantic)
│   ├── di/                   # Dependency injection container
│   ├── logging/              # Structured logging setup
│   ├── query/                # Query processing and input handling
│   └── utils/                # Shared utilities
│
├── scripts/                  # Helper scripts
│   ├── gemini-query.bat      # Windows interactive launcher
│   ├── fix_browser_config.py # Browser auto-detection
│   └── userscripts/
│       └── gemini_auto_input.user.js  # Browser userscript (v1.0.0)
│
├── configs/                  # Configuration files
│   ├── config.json           # User configuration
│   └── config.sample.json    # Sample configuration
│
├── development/              # Development entry point
│   └── main.py               # Development CLI
│
├── tests/                    # Test suite
├── docs/                     # Documentation
└── pyproject.toml            # Project metadata (uv/hatch)
```

### Why Polylith?

- **Modularity**: Components are independent and reusable
- **Testability**: Each component can be tested in isolation
- **Maintainability**: Clear boundaries reduce coupling
- **Scalability**: Easy to add new components or bases
- **Development Speed**: Hot-reload and fast feedback loops

Learn more: [Polylith Documentation](https://polylith.gitbook.io/)

---

## 🔧 Installation

### Prerequisites

- **Python 3.12+** - [Download here](https://www.python.org/downloads/)
- **uv** - Modern Python package manager ([Installation Guide](https://docs.astral.sh/uv/))
- **Web Browser** - Firefox (recommended), Chrome, Edge, or Safari
- **Tampermonkey/Greasemonkey** - Browser extension for userscripts

### Step 1: Install uv (Modern Python Package Manager)

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Step 2: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/gemini-query/gemini-query.git
cd gemini-query

# Install Python 3.12+ (if not already installed)
uv python install 3.12

# Install project dependencies
uv sync

# Configure settings (optional - auto-created on first run)
cp configs/config.sample.json configs/config.json
```

### Step 3: Install Browser Extension

1. **Install Extension**:
   - [Tampermonkey](https://www.tampermonkey.net/) (recommended) or [Greasemonkey](https://www.greasespot.net/)

2. **Install Userscript**:
   - Open Tampermonkey dashboard
   - Click "Create a new script"
   - Copy and paste the contents of `scripts/userscripts/gemini_auto_input.user.js`
   - Save the script

3. **Verify Installation**:
   - Navigate to [Gemini AI](https://aistudio.google.com/prompts/new_chat)
   - Open browser console (F12)
   - Type `window.geminiDebug.help()` - should show available commands

---

## 🚀 Quick Start

### Option 1: Windows Interactive Mode (Easiest)

**Double-click `scripts\gemini-query.bat`** for the easiest experience:

```
╔══════════════════════════════════════════════════════════════╗
║                 Gemini Auto Query - Interactive Mode         ║
╚══════════════════════════════════════════════════════════════╝

🤖 Welcome to Gemini AI Command Line Interface!

📝 Usage Instructions:
   • Enter your question below
   • Press Enter to submit
   • Type 'help' for more options
   • Type 'exit' to quit

────────────────────────────────────────────────────────────────
💬 Your question: What is Python programming?
```

### Option 2: Command Line (All Platforms)

```bash
# Basic usage with uv
uv run gemini-query "What is Python?"

# Short alias
uv run gq "What is Python?"

# With piped input
echo "def hello(): print('world')" | uv run gemini-query "Explain this code"

# File content
cat file.txt | uv run gemini-query "Summarize this content"

# Development mode (if in virtual environment)
uv shell
gemini-query "Hello, Gemini!"
```

### Option 3: Development Mode

```bash
# Use development entry point
cd development
python main.py --help
python main.py "Your question here"
```

---

## 💡 Usage

### Basic Commands

```bash
# Direct question
uv run gemini-query "What is Python?"

# With verbose output
uv run gemini-query --verbose "Explain async/await"

# Custom config file
uv run gemini-query --config path/to/config.json "Question"

# Help
uv run gemini-query --help
```

### Advanced Examples

```bash
# Code review
git diff | uv run gemini-query "Review these changes"

# Documentation generation
uv run gemini-query "Write comprehensive documentation for a REST API"

# Multi-line input
cat <<EOF | uv run gemini-query "Analyze this code"
def fibonacci(n):
    if n <= 1: return n
    return fibonacci(n-1) + fibonacci(n-2)
EOF
```

### Data Transfer Methods

The system uses multiple fallback methods for reliable data transfer:

1. **HTTP Server** (Primary): CORS-free localhost server
2. **URL Parameters**: Direct URL encoding
3. **localStorage**: Browser storage fallback
4. **sessionStorage**: Additional browser storage
5. **Manual Input**: Interactive prompt as last resort

### Browser Debug Commands

```javascript
// Check system status
window.geminiDebug.help()

// Test permissions
window.geminiDebug.checkPermissions()

// Manual input test
window.geminiDebug.forceInput("Test question")

// Set test data
window.geminiDebug.setTestData("Test data")
```

---

## ⚙️ Configuration

Edit `configs/config.json` to customize behavior:

```json
{
  "gemini_url": "https://aistudio.google.com/prompts/new_chat?model=gemini-2.5-pro-exp-03-25",
  "browser_path": "D:\\Applications\\MozillaFirefox\\firefox.exe",
  "temp_file_path": "temp/gemini_input.txt",
  "localhost_port": 8765,
  "log_retention_days": 365,
  "encoding": "utf-8",
  "max_prompt_length": 10000,
  "browser_timeout": 30,
  "supported_browsers": [
    "firefox",
    "chrome",
    "google-chrome",
    "microsoft-edge",
    "msedge"
  ]
}
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `gemini_url` | Base URL for Gemini AI with model parameters | See config |
| `browser_path` | Full path to browser executable (auto-detected if not specified) | Auto |
| `temp_file_path` | Path for temporary data files | `temp/gemini_input.txt` |
| `localhost_port` | Port for HTTP server | `8765` |
| `log_retention_days` | How long to keep log files | `365` |
| `encoding` | Text encoding for file operations | `utf-8` |
| `max_prompt_length` | Maximum characters in prompt | `10000` |
| `browser_timeout` | Browser startup timeout in seconds | `30` |

### Platform-Specific Browser Paths

**Windows**:
```json
{
  "browser_path": "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
}
```

**macOS**:
```json
{
  "browser_path": "/Applications/Firefox.app/Contents/MacOS/firefox"
}
```

**Linux**:
```json
{
  "browser_path": "/usr/bin/firefox"
}
```

---

## 📁 Project Structure

### Polylith Components

```
components/gemini_query/
├── browser/
│   ├── interface.py          # Browser automation interface
│   ├── service.py            # Browser service implementation
│   └── strategies.py         # Browser detection strategies
│
├── config/
│   ├── application.py        # Application configuration
│   ├── browser.py            # Browser configuration
│   ├── factory.py            # Configuration factory
│   ├── network.py            # Network configuration
│   └── unified.py            # Unified config model
│
├── di/
│   └── container.py          # Dependency injection container
│
├── logging/
│   └── setup.py              # Structured logging configuration
│
├── query/
│   ├── async_service.py      # Async query service
│   ├── input_processor.py    # Input processing
│   └── interface.py          # Query service interface
│
└── utils/
    └── errors.py             # Custom exceptions
```

### Key Files

| File | Purpose |
|------|---------|
| `bases/gemini_query/cli_app/core.py` | Main CLI application (Typer) |
| `components/gemini_query/di/container.py` | DI container setup |
| `components/gemini_query/config/unified.py` | Unified configuration model |
| `scripts/gemini-query.bat` | Windows interactive launcher |
| `scripts/userscripts/gemini_auto_input.user.js` | Browser automation script |
| `pyproject.toml` | Project metadata and dependencies |

---

## 🛠️ Development

### Development Environment Setup

```bash
# Clone repository
git clone https://github.com/gemini-query/gemini-query.git
cd gemini-query

# Install Python 3.12+ with uv
uv python install 3.12

# Install all dependencies (including dev)
uv sync --all-extras

# Activate virtual environment
uv shell

# Install pre-commit hooks (optional)
pre-commit install
```

### Development Tools

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=components --cov=bases --cov-report=html

# Type checking
uv run mypy components/ bases/

# Linting
uv run ruff check .

# Formatting
uv run black .

# Run all checks
uv run pytest && uv run mypy components/ bases/ && uv run ruff check .
```

### Development Entry Point

```bash
# Use development CLI
cd development
python main.py --help
python main.py "Test question"
```

### Adding New Components

1. Create component in `components/gemini_query/your_component/`
2. Add to `pyproject.toml` under `[tool.polylith.bricks]`
3. Import in relevant bases or other components
4. Add tests in `tests/test_your_component.py`

### Code Style and Standards

- **Python**: PEP 8 compliant with type hints and comprehensive docstrings
- **Type Hints**: Full type coverage enforced by mypy
- **Linting**: Ruff with strict configuration
- **Testing**: pytest with 80%+ coverage target
- **Documentation**: Sphinx with autodoc for API documentation

---

## 🔧 Troubleshooting

### Common Issues

#### Character Encoding Issues (Windows)

**文字化けが発生する場合**
```bash
# Windows 11日本語環境での対処法
# 1. コマンドプロンプトでUTF-8を有効化
chcp 65001

# 2. 環境変数を設定
set PYTHONIOENCODING=utf-8

# 3. バッチファイルを使用（自動的にUTF-8設定）
scripts\gemini-query.bat
```

#### Browser doesn't open

```bash
# Automatic fix (recommended)
uv run python scripts/fix_browser_config.py

# Or use interactive mode
scripts\gemini-query.bat
# Then type: fix
```

#### Module Not Found Errors

```bash
# Ensure dependencies are installed
uv sync

# If still failing, try reinstalling
rm -rf .venv
uv sync

# Or use development mode
cd development
python main.py --help
```

#### HTTP Server Issues

```bash
# Check port availability
netstat -an | grep 8765  # Linux/macOS
netstat -an | findstr 8765  # Windows

# Try different port in configs/config.json
"localhost_port": 8766
```

### Greasemonkey Script Issues

**Script not loading**
```javascript
// Check in browser console
typeof window.geminiDebug  // Should not be 'undefined'
```

**Permission errors**
```javascript
// Check permissions
window.geminiDebug.checkPermissions()

// Expected output should show:
// ✅ All permissions available
```

**Data not transferred**
```javascript
// Test data sources manually
localStorage.setItem('gemini_auto_input_data', 'test data')
window.geminiDebug.test()
```

### Getting Help

1. **Check browser console** for error messages
2. **Run with verbose flag**: `uv run gemini-query --verbose "Question"`
3. **Check logs**: `logs/gemini_query_YYYY-MM-DD.log`
4. **Test with simple input** to isolate problems
5. **Verify configuration**: `configs/config.json`
6. **Check GitHub Issues**: [Issue Tracker](https://github.com/gemini-query/gemini-query/issues)

---

## 📝 Contributing

### Development Workflow

1. **Fork and Clone**
```bash
git clone https://github.com/your-fork/gemini-query.git
cd gemini-query
```

2. **Create Development Environment**
```bash
uv sync --all-extras
uv shell
```

3. **Create Feature Branch**
```bash
git checkout -b feature/your-feature-name
```

4. **Make Changes**
- Follow existing code style and patterns
- Add comprehensive error handling
- Include debug logging
- Test with multiple browsers
- Add/update tests

5. **Test Thoroughly**
```bash
# Run all tests
uv run pytest

# Type checking
uv run mypy components/ bases/

# Linting
uv run ruff check .

# Format code
uv run black .
```

6. **Submit Pull Request**
- Include detailed description of changes
- Provide test results from multiple environments
- Update documentation if needed

### Code Review Checklist

- [ ] **Error Handling**: Comprehensive exception handling
- [ ] **Type Hints**: Full type coverage
- [ ] **Tests**: New tests for new functionality
- [ ] **Documentation**: Updated docstrings and README
- [ ] **Polylith**: Components remain independent
- [ ] **Performance**: No significant performance regressions
- [ ] **Cross-Platform**: Works on Windows, macOS, and Linux

---

## 📄 License

**AGPL-3.0-or-later** - see [LICENSE](LICENSE) file for details.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

---

## 🙏 Acknowledgments

- **Polylith Community**: For the excellent architecture pattern
- **Greasemonkey/Tampermonkey Communities**: For robust browser automation frameworks
- **Python Community**: For excellent cross-platform libraries and tools
- **Google Gemini Team**: For creating an accessible AI interface
- **Open Source Contributors**: For inspiration and best practices

---

## 🔄 Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

### v2.0.0 (Current - Polylith Edition)
- 🏗️ **Polylith Architecture**: Complete rewrite with modular component-based design
- 📦 **Modern Tooling**: Migration to `uv` for package management
- 🔧 **Dependency Injection**: Clean separation with DI container
- 📊 **Enhanced Logging**: Structured logging with `structlog`
- ⚡ **Performance**: Improved startup time and resource usage
- 🧪 **Better Testing**: Component isolation for easier testing

---

**Made with ❤️ for developers who love the command line and clean architecture**

*"The best tools are invisible until you need them, then they work flawlessly."*

**Star ⭐ this project if it helps you! Your support motivates continued development.**
