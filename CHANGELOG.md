# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-01-XX

### Changed - Major Architecture Refactor

#### 🏗️ Architecture
- **Polylith Architecture**: Migrated to Polylith-based modular architecture
  - Components: `browser`, `config`, `logging`, `query`, `utils`
  - Bases: `cli_app`
  - Improved modularity, testability, and maintainability
- **Dependency Injection**: Implemented DI container with `dependency-injector`
- **Package Management**: Migrated from `pip` to `uv` for faster dependency management

#### 📦 Project Structure
- Reorganized codebase into `components/`, `bases/`, and `projects/` directories
- Moved configuration files to `configs/` directory
- Moved scripts to `scripts/` directory
- Userscripts moved to `scripts/userscripts/`

#### ⚙️ Configuration System
- Unified configuration with `pydantic-settings`
- Split configuration into domain-specific modules:
  - `ApplicationConfig`: Application settings
  - `BrowserConfig`: Browser-related settings
  - `NetworkConfig`: Network and server settings
- Environment variable support with `.env` file

#### 🧪 Testing Infrastructure
- Enhanced test coverage with `pytest` and `pytest-cov`
- Added async test support with `pytest-asyncio`
- Browser automation tests with `pytest-playwright`
- Test markers for unit, integration, browser, and network tests

#### 📝 Documentation
- Split README.md into modular documentation:
  - `docs/installation.md`: Installation guide
  - `docs/usage.md`: Usage guide
  - `docs/troubleshooting.md`: Troubleshooting guide
  - `docs/architecture.md`: Architecture documentation
  - `docs/development.md`: Development guide
- Added Sphinx documentation support
- Created comprehensive CHANGELOG.md

#### 🔧 Developer Experience
- Added `pyproject.toml` with modern Python packaging
- Code quality tools: `ruff`, `black`, `mypy`
- Pre-commit hooks support
- Development dependencies management

### Added

#### New Features
- **Async Support**: Asynchronous query processing with `httpx`
- **Structured Logging**: Advanced logging with `structlog`
- **Type Safety**: Full type hints with `mypy` strict mode
- **CLI Enhancement**: Improved CLI with `typer` and `rich` output

#### New Commands
- `gemini-query`: Main command (entry point)
- `gq`: Short alias for `gemini-query`

#### New Configuration Options
- Support for multiple browser strategies
- Configurable logging levels and formats
- Network timeout and retry settings

### Fixed
- Improved error handling and recovery
- Better cross-platform compatibility
- Enhanced character encoding support for Windows

### Removed
- `debug_test.py`: Removed standalone debug script
- `quick_test.html`: Removed browser test interface
- `setup.py`: Replaced with `pyproject.toml`
- `.kiro/`: Removed development artifacts

## [1.0.0] - Previous Version

### Features (Legacy)
- Basic CLI for Gemini AI queries
- Greasemonkey/Tampermonkey userscript (v4.4)
- Multiple data transfer methods
- Interactive Windows batch interface
- HTTP server for CORS-free communication
- Browser automation with multiple fallbacks

---

## Version Numbering

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes
- **MINOR**: Backwards-compatible functionality additions
- **PATCH**: Backwards-compatible bug fixes

## Links
- [GitHub Repository](https://github.com/gemini-query/gemini-query)
- [Documentation](https://gemini-query.readthedocs.io/)
- [Issue Tracker](https://github.com/gemini-query/gemini-query/issues)
