# Architecture Guide

## Overview

Gemini Auto Query uses a **Polylith-based modular architecture** designed for maintainability, testability, and extensibility.

## Architecture Pattern: Polylith

### What is Polylith?

Polylith is an architecture pattern that organizes code into reusable components and bases:

- **Components**: Reusable business logic modules
- **Bases**: Application entry points
- **Projects**: Deployable artifacts

### Benefits

- ✅ **Modularity**: Clear separation of concerns
- ✅ **Reusability**: Components can be shared across projects
- ✅ **Testability**: Each component can be tested independently
- ✅ **Maintainability**: Changes are isolated to specific components

## Project Structure

```
gemini-auto-query/
├── components/           # Reusable business logic components
│   └── gemini_query/
│       ├── browser/      # Browser automation logic
│       ├── config/       # Configuration management
│       ├── di/           # Dependency injection
│       ├── logging/      # Logging infrastructure
│       ├── query/        # Query processing
│       └── utils/        # Utility functions
├── bases/                # Application entry points
│   └── gemini_query/
│       └── cli_app/      # CLI application base
├── projects/             # Deployable projects (future)
├── development/          # Development utilities
├── tests/                # Test suites
├── scripts/              # Utility scripts
│   ├── userscripts/      # Browser userscripts
│   └── *.bat             # Windows batch files
├── configs/              # Configuration files
├── docs/                 # Documentation
└── pyproject.toml        # Project configuration
```

## Component Architecture

### 1. Browser Component (`components/gemini_query/browser/`)

**Purpose**: Manages browser automation and interaction

**Key Modules:**
- `interface.py`: Browser service interface (Protocol)
- `service.py`: Browser service implementation
- `strategies.py`: Browser launch strategies

**Responsibilities:**
- Browser detection and configuration
- Browser process management
- URL generation and navigation

**Dependencies:**
- `config` component (browser configuration)
- `logging` component (error logging)

### 2. Config Component (`components/gemini_query/config/`)

**Purpose**: Centralized configuration management

**Key Modules:**
- `application.py`: Application-wide settings
- `browser.py`: Browser-specific settings
- `network.py`: Network and server settings
- `unified.py`: Unified configuration container
- `factory.py`: Configuration factory
- `legacy.py`: Legacy config compatibility

**Features:**
- Pydantic-based validation
- Environment variable support
- Type-safe configuration
- Backward compatibility

### 3. Query Component (`components/gemini_query/query/`)

**Purpose**: Query processing and input handling

**Key Modules:**
- `interface.py`: Query service interface
- `service.py`: Query service implementation
- `input_processor.py`: Input processing logic
- `url_generator.py`: URL generation
- `async_service.py`: Async query processing

**Responsibilities:**
- Command-line argument parsing
- Piped input processing
- Query formatting
- Data transfer coordination

**Dependencies:**
- `config` component (query settings)
- `browser` component (browser interaction)
- `utils` component (error handling)

### 4. Logging Component (`components/gemini_query/logging/`)

**Purpose**: Structured logging infrastructure

**Key Modules:**
- `setup.py`: Logging configuration
- `dependency_injection.py`: Logger DI integration

**Features:**
- Structured logging with `structlog`
- Multiple output formats
- Log rotation
- Debug mode support

### 5. DI Component (`components/gemini_query/di/`)

**Purpose**: Dependency injection container

**Key Modules:**
- `container.py`: DI container configuration

**Benefits:**
- Loose coupling
- Easy testing (mock injection)
- Configuration centralization

### 6. Utils Component (`components/gemini_query/utils/`)

**Purpose**: Shared utilities and helpers

**Key Modules:**
- `errors.py`: Custom exception classes
- `logging.py`: Logging utilities
- `structured_logging.py`: Structured logging helpers

## CLI Application Base (`bases/gemini_query/cli_app/`)

**Purpose**: Application entry point

**Key Modules:**
- `core.py`: Typer CLI application
- `__init__.py`: Version and exports

**Responsibilities:**
- Command-line interface definition
- User interaction
- Component orchestration
- Error handling

**Entry Points:**
- `gemini-query`: Main command
- `gq`: Short alias

## System Architecture

### Data Flow

```
┌─────────────────────┐
│   User Input        │
│  (CLI/Pipe/File)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Input Processor    │
│  (Query Component)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  URL Generator      │
│  (Query Component)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Browser Service    │
│ (Browser Component) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Browser + Script   │
│  (Tampermonkey)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Gemini AI         │
└─────────────────────┘
```

### Component Interaction

```
┌──────────────────────────────────────────┐
│           CLI Application                 │
│         (bases/cli_app)                   │
└─────────┬───────────┬──────────┬─────────┘
          │           │          │
          ▼           ▼          ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐
    │ Browser │ │  Query  │ │ Config  │
    │Component│ │Component│ │Component│
    └────┬────┘ └────┬────┘ └────┬────┘
         │           │           │
         └───────────┴───────────┘
                     │
                     ▼
              ┌─────────────┐
              │   Logging   │
              │  Component  │
              └─────────────┘
```

## Design Patterns

### 1. Dependency Injection

**Pattern**: Constructor injection via `dependency-injector`

**Benefits:**
- Testability: Easy to inject mocks
- Flexibility: Runtime configuration
- Decoupling: Components don't know about each other

**Example:**
```python
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    config = providers.Singleton(UnifiedConfig.from_env)
    browser_service = providers.Factory(
        BrowserService,
        config=config.provided.browser
    )
```

### 2. Protocol-Based Interfaces

**Pattern**: Python Protocols for type-safe interfaces

**Benefits:**
- Type safety without inheritance
- Duck typing with type hints
- Easy to mock in tests

**Example:**
```python
from typing import Protocol

class BrowserServiceProtocol(Protocol):
    def launch(self, url: str) -> None: ...
```

### 3. Factory Pattern

**Pattern**: Configuration factory for creating instances

**Benefits:**
- Encapsulates creation logic
- Supports multiple creation strategies
- Easy to extend

**Example:**
```python
class ConfigFactory:
    @staticmethod
    def from_env() -> UnifiedConfig:
        return UnifiedConfig(
            application=ApplicationConfig(),
            browser=BrowserConfig(),
            network=NetworkConfig()
        )
```

### 4. Strategy Pattern

**Pattern**: Browser launch strategies

**Benefits:**
- Multiple browser support
- Platform-specific logic
- Easy to add new strategies

**Example:**
```python
class BrowserStrategy(ABC):
    @abstractmethod
    def launch(self, url: str) -> None: ...

class FirefoxStrategy(BrowserStrategy):
    def launch(self, url: str) -> None: ...
```

## Data Transfer Architecture

### Multi-Method Fallback System

```
┌─────────────────────────────────────────┐
│        Python Application                │
└────────────┬────────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌─────────┐      ┌──────────┐
│  HTTP   │      │   URL    │
│ Server  │      │Parameters│
└────┬────┘      └─────┬────┘
     │                 │
     └────────┬────────┘
              │
              ▼
     ┌─────────────────┐
     │   Browser       │
     │ + Greasemonkey  │
     └────────┬────────┘
              │
     ┌────────┴────────────┐
     │                     │
     ▼                     ▼
┌──────────┐        ┌─────────────┐
│GM_xhr    │        │localStorage │
│(Primary) │        │ (Fallback)  │
└────┬─────┘        └──────┬──────┘
     │                     │
     └─────────┬───────────┘
               │
               ▼
        ┌─────────────┐
        │Manual Input │
        │(Last Resort)│
        └─────────────┘
```

### Priority Order

1. **GM_xmlhttpRequest**: CORS-free HTTP request (Primary)
2. **URL Parameters**: Query string encoding
3. **localStorage**: Browser storage
4. **sessionStorage**: Session storage
5. **Manual Input**: User prompt (Last resort)

## Browser Automation Architecture

### Greasemonkey/Tampermonkey Script

**Location**: `scripts/userscripts/gemini_auto_input.user.js`

**Key Features:**
- Early execution (`@run-at document-start`)
- Multiple UI detection methods
- Smart input simulation
- Comprehensive event firing
- Debug interface

**Permissions:**
```javascript
// @grant        GM_xmlhttpRequest
// @grant        GM_setValue
// @grant        GM_getValue
// @connect      localhost
// @connect      127.0.0.1
// @connect      *
```

### Event Flow

```
Page Load
    │
    ▼
Wait for UI Ready
    │
    ▼
Detect Textarea (multiple selectors)
    │
    ▼
Fetch Data (multiple methods)
    │
    ▼
Simulate Input (chunked typing)
    │
    ▼
Fire Events (framework compatibility)
    │
    ▼
Enable Submit Button (multiple attempts)
    │
    ▼
Click Submit (6 different methods)
    │
    ▼
Monitor Success
```

## Configuration Architecture

### Configuration Hierarchy

```
Environment Variables (.env)
          │
          ▼
  Application Config
  ┌─────────┴─────────┐
  │                   │
  ▼                   ▼
Browser Config    Network Config
  │                   │
  └─────────┬─────────┘
            │
            ▼
    Unified Config
            │
            ▼
    DI Container
            │
            ▼
      Components
```

### Configuration Loading

1. **Default Values**: Hardcoded defaults
2. **Config File**: `configs/config.json`
3. **Environment Variables**: `.env` file
4. **CLI Arguments**: Command-line overrides

### Type Safety

All configuration uses Pydantic models:
```python
class BrowserConfig(BaseModel):
    firefox_path: str = Field(default="firefox")
    timeout: int = Field(default=30, ge=1)
```

## Testing Architecture

### Test Structure

```
tests/
├── unit/                 # Unit tests (fast)
├── integration/          # Integration tests
├── browser/              # Browser automation tests
└── fixtures/             # Test fixtures
```

### Test Markers

```python
@pytest.mark.unit          # Fast unit tests
@pytest.mark.integration   # Integration tests
@pytest.mark.browser       # Browser automation tests
@pytest.mark.network       # Network-dependent tests
@pytest.mark.slow          # Slow tests
```

### Testing Strategies

1. **Unit Tests**: Test individual components in isolation
2. **Integration Tests**: Test component interactions
3. **Browser Tests**: Test browser automation (Playwright)
4. **Mock Testing**: Use DI to inject mocks

## Error Handling Architecture

### Exception Hierarchy

```
GeminiQueryError (Base)
    │
    ├── ConfigurationError
    │   ├── MissingConfigError
    │   └── InvalidConfigError
    │
    ├── BrowserError
    │   ├── BrowserNotFoundError
    │   └── BrowserLaunchError
    │
    ├── QueryError
    │   ├── InputError
    │   └── ProcessingError
    │
    └── NetworkError
        ├── ServerError
        └── ConnectionError
```

### Error Recovery

1. **Graceful Degradation**: Fallback to simpler methods
2. **Retry Logic**: Automatic retries with backoff
3. **User Feedback**: Clear error messages
4. **Logging**: Comprehensive error logging

## Performance Considerations

### Optimization Strategies

1. **Lazy Loading**: Components loaded on demand
2. **Connection Pooling**: Reuse HTTP connections
3. **Caching**: Cache configuration and browser paths
4. **Async I/O**: Async operations where possible

### Resource Management

1. **Temporary Files**: Auto-cleanup after use
2. **Log Rotation**: Automatic log file rotation
3. **Memory Management**: Efficient data structures
4. **Process Management**: Clean browser process termination

## Security Architecture

### Security Principles

1. **Localhost Only**: No external network access
2. **Temporary Storage**: Sensitive data deleted after use
3. **No Credentials**: No API keys or passwords stored
4. **Sandboxing**: Browser runs in normal sandbox

### Data Flow Security

```
User Input → Sanitization → Processing → Browser → Gemini AI
             ↓
        Validation
             ↓
        Temp File (Auto-deleted)
             ↓
        HTTP Server (Localhost only)
```

## Future Architecture Considerations

### Planned Enhancements

1. **Plugin System**: Support for custom components
2. **Multiple Projects**: Support for different deployment targets
3. **API Mode**: REST API interface
4. **Cloud Integration**: Optional cloud storage support

### Scalability

- Component-based design allows easy addition of new features
- Polylith architecture supports multiple projects from same codebase
- DI container makes configuration and testing straightforward

## See Also

- [Development Guide](development.md) - Contributing and development setup
- [Testing Guide](development.md#testing) - Testing strategies
- [Configuration Guide](usage.md#configuration) - Configuration options
