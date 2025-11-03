# Development Guide

This document provides comprehensive information for developers who want to understand, modify, or extend the Gemini Auto Query project. It includes architecture details, development patterns, testing strategies, and critical insights gained during development.

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Core Components](#core-components)
3. [Development Environment](#development-environment)
4. [Testing Strategies](#testing-strategies)
5. [Debugging Guide](#debugging-guide)
6. [Extension Points](#extension-points)
7. [Performance Considerations](#performance-considerations)
8. [Security Considerations](#security-considerations)
9. [Deployment Guide](#deployment-guide)
10. [Critical Development Insights](#critical-development-insights)

## 🏗️ Architecture Overview

### System Components (v4.4 Architecture)

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Command Line  │───▶│  Python Script   │───▶│     Browser         │
│   Interface     │    │  + HTTP Server   │    │  + Greasemonkey     │
│   + Pipe Input  │    │  + Data Bridge   │    │  + Debug Interface  │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
                                │                          │
                                ▼                          ▼
                       ┌──────────────────┐    ┌─────────────────────┐
                       │  Multi-Method    │    │   Smart Auto-Fill   │
                       │  Data Transfer   │    │   + Submit System   │
                       │  (7 Fallbacks)   │    │   (6 Click Methods) │
                       └──────────────────┘    └─────────────────────┘
```

### Component Interaction Matrix

| Component | Reads From | Writes To | Communicates With |
|-----------|------------|-----------|-------------------|
| `gemini_query.py` | stdin, args, config.json | temp/gemini_input.txt, logs/ | HTTP server, Firefox |
| `HTTP Server` | temp/gemini_input.txt | HTTP responses | Greasemonkey script |
| `gemini_auto_input.user.js` | localhost:8765, URL params, localStorage | Browser DOM, console | Debug interface |
| `Debug Interface` | User input, localStorage | Browser console, DOM | Main script functions |

### Data Flow

1. **Input Collection**: CLI collects arguments and stdin
2. **URL Generation**: Python creates Gemini URL with encoded prompt
3. **Browser Launch**: System opens browser with generated URL
4. **Parameter Detection**: Greasemonkey script reads URL parameters
5. **Auto-Fill**: Script fills textarea with prompt text
6. **Auto-Submit**: Script clicks submit button when ready

## 🔧 Core Components

### 1. Python CLI Application (`gemini_query.py`)

**Purpose**: Main application logic and browser interface

**Key Classes**:
- `GeminiQueryCLI`: Main application class with configuration and execution logic

**Key Methods**:
- `_load_configuration()`: Loads and validates config.json
- `_get_input_data()`: Processes command line and stdin input
- `_create_gemini_url()`: Generates properly encoded URLs
- `_launch_browser()`: Cross-platform browser launching

**Design Patterns**:
- **Single Responsibility**: Each method has one clear purpose
- **Error Handling**: Comprehensive exception handling with user-friendly messages
- **Configuration**: External JSON configuration with sensible defaults
- **Logging**: Structured logging for debugging and monitoring

### 2. Greasemonkey Script (`gemini_auto_input.user.js`)

**Purpose**: Browser automation for Gemini AI interface

**Key Functions**:
- `initializeScript()`: Main entry point and orchestration
- `extractPromptFromURL()`: URL parameter parsing and validation
- `findElement()`: Generic element finder with timeout handling
- `fillAndSubmitPrompt()`: Core automation logic

**Design Patterns**:
- **Promise-based**: Async operations with proper error handling
- **Modular Functions**: Clear separation of concerns
- **Configuration Object**: Centralized constants and settings
- **Debug Interface**: Comprehensive debugging and testing tools

### 3. Configuration System (`config.json`)

**Purpose**: Centralized configuration management

**Structure**:
```json
{
  "gemini_url": "Base URL with optional parameters",
  "browser_path": "Preferred browser command",
  "max_prompt_length": "Character limit for prompts",
  "browser_timeout": "Timeout for browser operations",
  "supported_browsers": ["List of fallback browsers"]
}
```

## 🧪 Testing Strategy

### Unit Testing

**URL Generation Testing** (`tests/test_url_generation.py`):
- Tests URL encoding with various character sets
- Validates parameter handling
- Checks truncation logic

**Browser Parameter Testing** (`tests/test_url_params.html`):
- Visual testing of URL parameter detection
- Greasemonkey script validation
- Debug interface testing

### Integration Testing

**Manual Testing Workflow**:
1. Run `python gemini_query.py "test question"`
2. Verify browser opens with correct URL
3. Check browser console for script logs
4. Confirm textarea is filled automatically
5. Verify submit button is clicked

**Automated Testing**:
```bash
# Test URL generation
python tests/test_url_generation.py

# Test with various inputs
echo "test content" | python gemini_query.py "test question"
python gemini_query.py "unicode test: 日本語 🚀"
```

## 🔍 Debugging Guide

### Python Application Debugging

**Enable Debug Logging**:
```python
# Modify _setup_logging() method
logging.basicConfig(level=logging.DEBUG)
```

**Common Debug Points**:
- Configuration loading issues
- Input processing problems
- URL generation errors
- Browser launch failures

**Debug Commands**:
```bash
# Test configuration loading
python -c "from gemini_query import GeminiQueryCLI; print(GeminiQueryCLI()._load_configuration())"

# Test URL generation
python tests/test_url_generation.py
```

### Greasemonkey Script Debugging

**Browser Console Commands**:
```javascript
// Check script status
window.geminiDebug.help()

// Manual test
window.geminiDebug.test("debug question")

// View configuration
window.geminiDebug.getConfig()

// Check URL parameters
new URLSearchParams(window.location.search).get('prompt')
```

**Common Issues**:
- Script not loading: Check Tampermonkey installation
- Parameters not detected: Verify URL format
- Elements not found: Check Gemini UI changes
- Timing issues: Adjust delay constants

### Network Debugging

**URL Validation**:
```bash
# Check generated URL format
python tests/test_url_generation.py

# Manual URL test
# Copy generated URL and open in browser manually
```

## 🚀 Extension Points

### Adding New Browsers

**In Python** (`gemini_query.py`):
```python
# Add to supported_browsers in config.json
"supported_browsers": [
    "firefox",
    "chrome",
    "safari",      # New browser
    "your-browser" # Custom browser
]
```

### Adding New URL Parameters

**In Python**:
```python
def _create_gemini_url(self, prompt: str) -> str:
    # Add new parameters
    encoded_prompt = urllib.parse.quote(prompt, safe='')
    timestamp = int(time.time())
    final_url = f"{base_url}{separator}prompt={encoded_prompt}&ts={timestamp}"
```

**In Greasemonkey**:
```javascript
function extractPromptFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    // Add new parameter names
    const paramNames = ['prompt', 'q', 'data', 'text', 'query'];
    // ... rest of function
}
```

### Adding New Input Sources

**Example: File Input**:
```python
def _get_file_input(self, file_path: str) -> str:
    """Read input from file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except IOError as error:
        self.logger.error(f"Could not read file {file_path}: {error}")
        return ''
```

### Custom Element Selectors

**In Greasemonkey**:
```javascript
// Add new selectors for different Gemini UI versions
const buttonSelectors = [
    'button:has(.run-button-content)',
    'button[aria-label*="Run"]',
    'button.new-submit-class',        // New selector
    'input[type="submit"]'            // Alternative element
];
```

## 📊 Performance Considerations

### Python Application

**Optimization Points**:
- Configuration caching
- Browser detection caching
- Input processing efficiency
- Error handling overhead

**Memory Usage**:
- Minimal memory footprint
- No persistent state
- Efficient string handling

### Greasemonkey Script

**Optimization Points**:
- Element search timeouts
- Event listener efficiency
- DOM manipulation performance
- Memory leak prevention

**Best Practices**:
- Use `const` for immutable values
- Implement proper cleanup
- Avoid global variable pollution
- Use efficient selectors

## 🔒 Security Considerations

### Input Validation

**Python Side**:
- URL encoding prevents injection
- Input length limits
- Configuration validation

**Browser Side**:
- No eval() or innerHTML usage
- Proper event handling
- Limited DOM access

### Data Handling

**Sensitive Data**:
- No persistent storage of prompts
- URL parameters are temporary
- No network requests to external servers

## 📝 Code Style Guidelines

### Python Code Style

**Follow PEP 8**:
- 4 spaces for indentation
- Line length limit: 88 characters
- Type hints for all functions
- Comprehensive docstrings

**Example**:
```python
def _create_gemini_url(self, prompt: str) -> str:
    """
    Create a properly formatted Gemini URL with the prompt parameter.
    
    Args:
        prompt: The question/prompt to send to Gemini
        
    Returns:
        Complete URL with encoded prompt parameter
        
    Raises:
        ValueError: If prompt is empty
    """
```

### JavaScript Code Style

**ES6+ Standards**:
- Use `const`/`let` instead of `var`
- Arrow functions for callbacks
- Template literals for strings
- Proper error handling

**Example**:
```javascript
/**
 * Extract prompt from URL parameters
 * @returns {string|null} The prompt text or null if not found
 */
function extractPromptFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    // Implementation...
}
```

## 🔄 Release Process

### Version Management

**Semantic Versioning**:
- Major: Breaking changes
- Minor: New features
- Patch: Bug fixes

**Update Locations**:
- `gemini_query.py`: `__doc__` string
- `gemini_auto_input.user.js`: `@version` header
- `README.md`: Version references

### Testing Checklist

- [ ] Python script runs without errors
- [ ] Greasemonkey script loads correctly
- [ ] URL generation works with various inputs
- [ ] Browser launching works on target platforms
- [ ] Auto-fill and submit work in Gemini interface
- [ ] Configuration loading handles edge cases
- [ ] Error messages are user-friendly

### Deployment

1. Update version numbers
2. Run full test suite
3. Update documentation
4. Create release notes
5. Tag release in git
6. Update distribution files

## 🧠 Critical Development Insights

### Lessons Learned During Development

#### 1. **Browser Security Evolution**
**Challenge**: Modern browsers increasingly restrict cross-origin requests and localhost access.
**Solution**: Implemented multiple fallback methods with GM_xmlhttpRequest as primary.
**Key Insight**: Always plan for browser security changes - what works today may not work tomorrow.

#### 2. **Framework Compatibility Issues**
**Challenge**: Modern web frameworks (Angular, React) don't detect programmatic DOM changes.
**Solution**: Fire comprehensive event sets including keyboard events with proper key codes.
**Key Insight**: Test with actual framework applications, not just static HTML.

#### 3. **Permission Management Complexity**
**Challenge**: Greasemonkey permissions are complex and browser-dependent.
**Solution**: Implemented permission checking and repair functions.
**Key Insight**: Provide clear diagnostic tools for users to troubleshoot permission issues.

#### 4. **UI Element Detection Fragility**
**Challenge**: Web UI selectors break frequently with updates.
**Solution**: Use multiple selector strategies and graceful degradation.
**Key Insight**: Build robustness into element detection from day one.

#### 5. **Data Transfer Reliability**
**Challenge**: Single-method data transfer is unreliable across different environments.
**Solution**: Implemented 7-layer fallback system.
**Key Insight**: Redundancy is essential for production reliability.

### Development Anti-Patterns to Avoid

#### 1. **Single Point of Failure**
```javascript
// ❌ Bad: Only one way to transfer data
const data = getFromURL();

// ✅ Good: Multiple fallback methods
const data = await getFromHTTP() || 
             getFromURL() || 
             getFromStorage() || 
             promptUser();
```

#### 2. **Hardcoded Selectors**
```javascript
// ❌ Bad: Brittle selector
const textarea = document.querySelector('textarea.specific-class');

// ✅ Good: Multiple selector strategy
const selectors = ['textarea[aria-label*="Type"]', 'textarea', '[contenteditable]'];
const textarea = selectors.map(s => document.querySelector(s)).find(el => el);
```

#### 3. **Synchronous Operations**
```javascript
// ❌ Bad: Blocking operations
element.click();
checkIfWorked();

// ✅ Good: Async with proper waiting
element.click();
await waitForStateChange();
checkIfWorked();
```

### Performance Optimization Strategies

#### 1. **Lazy Loading**
- Load debug interfaces only when needed
- Initialize HTTP server only when required
- Cache configuration data

#### 2. **Resource Management**
- Automatic cleanup of temporary files
- HTTP server shutdown on completion
- Memory leak prevention in long-running scripts

#### 3. **Efficient Polling**
- Use exponential backoff for retries
- Implement maximum retry limits
- Provide early exit conditions

### Testing Philosophy

#### 1. **Test Pyramid Approach**
```
    /\
   /  \     E2E Tests (Few, High-Value)
  /____\    
 /      \   Integration Tests (Some)
/________\  Unit Tests (Many, Fast)
```

#### 2. **Failure Mode Testing**
- Test with permissions disabled
- Test with network failures
- Test with UI changes
- Test with invalid inputs

#### 3. **Cross-Environment Testing**
- Multiple browsers (Firefox, Chrome, Edge)
- Multiple operating systems (Windows, macOS, Linux)
- Multiple Python versions (3.7+)

### Debugging Strategies

#### 1. **Layered Debug Interfaces**
```javascript
// Layer 1: Emergency interface (always available)
window.geminiDebugEmergency

// Layer 2: Full interface (when script loads properly)
window.geminiDebug

// Layer 3: Force creation (when primary fails)
window.geminiDebugEmergency.forceDebugInterface()
```

#### 2. **Comprehensive Logging**
```python
# Python: Structured logging
logger.info(f"Data transfer: {method} -> {status}")

# JavaScript: Prefixed console logging
console.log('[GEMINI-AUTO] [DEBUG] Operation completed');
```

#### 3. **State Inspection Tools**
```javascript
// Provide tools to inspect current state
window.geminiDebug.showInfo()  // System state
window.geminiDebug.checkPermissions()  // Permission state
```

## 🚀 Future Development Roadmap

### Short-term Improvements (v4.5)
- [ ] **WebSocket server**: Real-time bidirectional communication
- [ ] **Configuration UI**: Browser-based configuration interface
- [ ] **Plugin system**: Extensible architecture for custom handlers
- [ ] **Performance metrics**: Built-in performance monitoring

### Medium-term Features (v5.0)
- [ ] **Multi-AI support**: Support for Claude, ChatGPT, etc.
- [ ] **Session management**: Persistent conversation handling
- [ ] **Template system**: Reusable prompt templates
- [ ] **Batch processing**: Multiple queries in sequence

### Long-term Vision (v6.0+)
- [ ] **Native app**: Electron-based desktop application
- [ ] **API server**: RESTful API for integration
- [ ] **Cloud sync**: Configuration and history synchronization
- [ ] **AI model switching**: Dynamic model selection

## 📚 Additional Resources

### Essential Reading
- [Greasemonkey API Documentation](https://wiki.greasespot.net/Greasemonkey_Manual:API)
- [Tampermonkey Documentation](https://www.tampermonkey.net/documentation.php)
- [CORS and Security](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Browser Extension Security](https://developer.chrome.com/docs/extensions/mv3/security/)

### Development Tools
- **Browser DevTools**: Essential for debugging DOM interactions
- **Python Debugger**: `pdb` for step-through debugging
- **Network Monitoring**: Monitor HTTP requests and responses
- **Performance Profiling**: Browser performance tools

### Community Resources
- **Greasemonkey Community**: [GreasyFork](https://greasyfork.org/)
- **Python CLI Tools**: [Click](https://click.palletsprojects.com/) and [Typer](https://typer.tiangolo.com/)
- **Browser Automation**: [Selenium](https://selenium.dev/) for reference

---

This development guide represents the collective knowledge gained through extensive development, testing, and debugging. It should serve as a comprehensive resource for anyone working on this project or similar browser automation tools.

**Remember**: The key to successful browser automation is redundancy, robustness, and comprehensive error handling. Always assume things will fail and plan accordingly.