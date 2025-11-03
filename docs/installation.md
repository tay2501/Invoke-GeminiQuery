# Installation Guide

## Prerequisites

- **Python 3.12+** - [Download here](https://www.python.org/downloads/)
- **Web Browser** - Firefox (recommended), Chrome, Edge, or Safari
- **Tampermonkey/Greasemonkey** - Browser extension for userscripts

## Step 1: Install Browser Extension

### 1.1 Install Extension

Install one of the following browser extensions:
- [Tampermonkey](https://www.tampermonkey.net/) (recommended)
- [Greasemonkey](https://www.greasespot.net/)

### 1.2 Install Userscript

1. Open Tampermonkey dashboard
2. Click "Create a new script"
3. Copy and paste the contents of `scripts/userscripts/gemini_auto_input.user.js`
4. **Important**: Ensure these permissions are enabled:
   ```javascript
   // @grant        GM_xmlhttpRequest
   // @grant        GM_setValue
   // @grant        GM_getValue
   // @connect      localhost
   // @connect      127.0.0.1
   // @connect      *
   ```
5. Save the script

### 1.3 Verify Installation

1. Navigate to [Gemini AI](https://aistudio.google.com/prompts/new_chat)
2. Open browser console (F12)
3. Type `window.geminiDebug.help()` - should show available commands

## Step 2: Install uv (Modern Python Package Manager)

Install uv package manager:

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

For more details, see [uv documentation](https://docs.astral.sh/uv/).

## Step 3: Download and Setup Project

```bash
# Clone the repository
git clone https://github.com/your-repo/gemini-auto-query.git
cd gemini-auto-query

# Install Python 3.12+ (if not already installed)
uv python install 3.12

# Install project dependencies
uv sync

# Optional: Install development dependencies
uv sync --group dev
```

## Step 4: Configuration

### 4.1 Create Configuration File

Copy the sample configuration:

```bash
# Windows
copy configs\config.sample.json configs\config.json

# Linux/macOS
cp configs/config.sample.json configs/config.json
```

### 4.2 Edit Configuration

Edit `configs/config.json` to customize behavior:

```json
{
  "gemini_url": "https://aistudio.google.com/prompts/new_chat?model=gemini-2.5-pro-exp-03-25",
  "firefox_path": "D:\\Applications\\MozillaFirefox\\firefox.exe",
  "temp_file_path": "temp/gemini_input.txt",
  "localhost_port": 8765,
  "log_retention_days": 365,
  "encoding": "utf-8",
  "max_prompt_length": 10000
}
```

### 4.3 Environment-Specific Configuration

**Windows:**
```json
{
  "firefox_path": "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
}
```

**macOS:**
```json
{
  "firefox_path": "/Applications/Firefox.app/Contents/MacOS/firefox"
}
```

**Linux:**
```json
{
  "firefox_path": "/usr/bin/firefox"
}
```

## Step 5: First Run and Verification

### Windows Users (Interactive Mode)

Double-click `scripts\gemini-query.bat` for interactive setup.

### All Platforms (Command Line)

```bash
# Run using uv
uv run gemini-query "Hello, this is a test"

# Or use the shorter alias
uv run gq "Hello, this is a test"

# Activate virtual environment for repeated use
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Then run directly
gemini-query "Hello, this is a test"
gq "Hello, this is a test"
```

### Test Debug Interface

In browser console:
```javascript
window.geminiDebug.checkPermissions()
```

## Troubleshooting Installation

### Python Version Issues

```bash
# Check Python version
python --version  # Should be 3.12+

# Install specific version with uv
uv python install 3.12
```

### Browser Path Issues

If browser doesn't open automatically:

```bash
# Run browser configuration script
uv run python scripts/fix_browser_config.py
```

### Permission Issues

If you encounter permission errors:

```javascript
// In browser console
window.geminiDebug.checkPermissions()
window.geminiDebug.fixPermissions()
```

## Next Steps

- See [Usage Guide](usage.md) for how to use the tool
- See [Troubleshooting Guide](troubleshooting.md) for common issues
- See [Development Guide](development.md) to contribute
