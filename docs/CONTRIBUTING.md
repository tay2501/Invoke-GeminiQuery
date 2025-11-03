# Contributing to Gemini Auto Query

Thank you for your interest in contributing to Gemini Auto Query! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

1. **Check existing issues** first to avoid duplicates
2. **Use the issue template** when creating new issues
3. **Provide detailed information**:
   - Operating system and version
   - Python version (`python --version`)
   - Browser and version
   - Steps to reproduce the issue
   - Expected vs actual behavior
   - Output from `python debug_test.py`

### Suggesting Features

1. **Open a feature request** issue
2. **Describe the use case** and why it would be valuable
3. **Provide examples** of how the feature would work
4. **Consider implementation complexity** and maintenance burden

### Code Contributions

#### Development Setup

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/gemini-auto-query.git
cd gemini-auto-query

# 3. Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# 4. Install development dependencies
pip install -r requirements-dev.txt  # If exists

# 5. Run setup and tests
python setup.py
python debug_test.py
```

#### Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Follow coding standards**:
   - **Python**: PEP 8 compliance with type hints
   - **JavaScript**: ES6+ with JSDoc comments
   - **Batch files**: Clear comments and error handling
   - **Documentation**: Clear, concise, and up-to-date

3. **Test your changes**:
   ```bash
   # Run diagnostic tests
   python debug_test.py
   
   # Test interactive mode
   test_interactive.bat  # Windows
   
   # Test actual functionality
   python gemini_query.py "test question"
   ```

4. **Update documentation** if needed:
   - Update README.md for user-facing changes
   - Update DEVELOPMENT.md for technical changes
   - Add entries to TESTING.md for new test procedures

#### Code Style Guidelines

##### Python Code
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module docstring describing the purpose.
"""

import sys
from typing import Optional, List

def function_name(param: str) -> bool:
    """
    Function docstring with clear description.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When parameter is invalid
    """
    # Implementation with clear comments
    pass
```

##### JavaScript Code
```javascript
/**
 * Function description
 * @param {string} param - Parameter description
 * @returns {boolean} Return value description
 */
function functionName(param) {
    // Clear implementation with error handling
    try {
        // Main logic
        return true;
    } catch (error) {
        console.error(`Error in functionName: ${error.message}`);
        return false;
    }
}
```

##### Batch File Code
```batch
@echo off
REM Clear description of what this script does
REM Author: Your Name
REM Version: 1.0.0

setlocal enabledelayedexpansion

REM Set UTF-8 encoding for Windows
chcp 65001 >nul 2>&1

REM Main logic with error handling
if exist "file.txt" (
    echo [INFO] File found
) else (
    echo [ERROR] File not found
    exit /b 1
)
```

#### Commit Guidelines

1. **Use clear commit messages**:
   ```
   feat: add browser auto-detection feature
   fix: resolve character encoding issue on Windows
   docs: update installation instructions
   test: add browser availability tests
   refactor: improve error handling in main script
   ```

2. **Keep commits focused**: One logical change per commit

3. **Include tests** for new features and bug fixes

#### Pull Request Process

1. **Ensure all tests pass**:
   ```bash
   python debug_test.py
   python test_interactive.bat  # Windows
   ```

2. **Update documentation** as needed

3. **Create a pull request** with:
   - Clear title and description
   - Reference to related issues
   - Screenshots for UI changes
   - Test results

4. **Respond to feedback** promptly and professionally

## 🧪 Testing Guidelines

### Required Tests

Before submitting a pull request, ensure:

1. **System diagnostic tests pass**:
   ```bash
   python debug_test.py
   ```

2. **Interactive mode works**:
   ```bash
   # Windows
   test_interactive.bat
   
   # Manual test
   gemini-query.bat
   ```

3. **Core functionality works**:
   ```bash
   python gemini_query.py "test question"
   ```

4. **Browser detection works**:
   ```bash
   python fix_browser_config.py
   ```

### Cross-Platform Testing

If possible, test on multiple platforms:
- **Windows 10/11**: Primary target platform
- **macOS**: Secondary support
- **Linux**: Secondary support

### Browser Testing

Test with multiple browsers:
- **Firefox**: Primary target browser
- **Chrome**: Secondary support
- **Edge**: Secondary support

## 📋 Issue Labels

We use the following labels to categorize issues:

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements or additions to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `question`: Further information is requested
- `wontfix`: This will not be worked on
- `duplicate`: This issue or pull request already exists
- `invalid`: This doesn't seem right

## 🔒 Security

If you discover a security vulnerability, please:

1. **Do NOT open a public issue**
2. **Email the maintainers** directly
3. **Provide detailed information** about the vulnerability
4. **Allow time** for the issue to be addressed before public disclosure

## 📝 Documentation

### Documentation Standards

- **Clear and concise**: Avoid unnecessary jargon
- **Examples included**: Show practical usage
- **Up-to-date**: Keep documentation current with code changes
- **Accessible**: Consider users with different skill levels

### Documentation Types

1. **User Documentation** (README.md):
   - Installation instructions
   - Usage examples
   - Troubleshooting guides

2. **Developer Documentation** (DEVELOPMENT.md):
   - Architecture overview
   - API documentation
   - Development setup

3. **Testing Documentation** (TESTING.md):
   - Test procedures
   - Quality assurance guidelines

## 🎯 Development Priorities

### High Priority
- Bug fixes for critical functionality
- Security improvements
- Cross-platform compatibility
- Performance optimizations

### Medium Priority
- New features that enhance usability
- Documentation improvements
- Additional browser support
- Enhanced error handling

### Low Priority
- Code refactoring (without functional changes)
- Minor UI improvements
- Additional debugging tools

## 🏆 Recognition

Contributors will be recognized in:
- README.md acknowledgments section
- CONTRIBUTORS.md file (if created)
- Release notes for significant contributions

## 📞 Getting Help

If you need help with contributing:

1. **Check existing documentation** first
2. **Search closed issues** for similar questions
3. **Open a discussion** or issue for guidance
4. **Be patient and respectful** when asking for help

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project maintainers. All complaints will be reviewed and investigated promptly and fairly.

---

Thank you for contributing to Gemini Auto Query! Your efforts help make this tool better for everyone. 🚀