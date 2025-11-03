# Usage Guide

## Quick Start

### Interactive Mode (Windows)

Double-click `scripts\gemini-query.bat` for the easiest experience:

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

**Interactive Features:**
- **User-friendly prompts**: Clear instructions and visual feedback
- **Built-in help system**: Type `help` for commands and examples
- **Connection testing**: Type `test` to verify setup
- **Configuration access**: Type `config` to edit settings
- **Multiple questions**: Continue asking without restarting
- **Error recovery**: Helpful troubleshooting suggestions

## Command Line Usage

### Basic Usage

```bash
# Direct question
uv run gemini-query "What is Python?"
uv run gq "What is Python?"

# Windows batch file (command line mode)
scripts\gemini-query.bat "What is Python?"

# After activating virtual environment
gemini-query "What is Python?"
gq "What is Python?"
```

### Input Methods

#### 1. Direct Question

```bash
gemini-query "Explain quantum computing"
```

#### 2. Piped Input

```bash
# From echo
echo "def hello(): print('world')" | gemini-query "Explain this code"

# From file
cat file.txt | gemini-query "Summarize this content"    # Linux/macOS
type file.txt | gemini-query "Summarize this content"   # Windows
```

#### 3. Combined Input

```bash
# Question + piped code
cat my_script.py | gemini-query "Review this code and suggest improvements"
```

## Advanced Examples

### Code Review

```bash
# Review git changes
git diff | gemini-query "Review these changes"

# Review specific file
cat src/main.py | gemini-query "Analyze this code for security issues"
```

### Documentation Generation

```bash
# Generate API documentation
cat api.py | gemini-query "Write comprehensive API documentation"

# Create README
ls -la | gemini-query "Create a README for this project structure"
```

### Data Analysis

```bash
# Analyze logs
tail -n 100 application.log | gemini-query "Identify errors and patterns"

# Process CSV data
cat data.csv | gemini-query "Analyze this data and suggest insights"
```

### Translation and Formatting

```bash
# Translate code comments
cat legacy_code.py | gemini-query "Translate all comments to English"

# Format output
echo "raw data" | gemini-query "Format this as a Markdown table"
```

## Data Transfer Methods

The system uses multiple fallback methods for reliable data transfer:

1. **HTTP Server** (Primary): CORS-free localhost server
2. **URL Parameters**: Direct URL encoding
3. **localStorage**: Browser storage fallback
4. **sessionStorage**: Additional browser storage
5. **Manual Input**: Interactive prompt as last resort

## Browser Debug Commands

Access these commands in the browser console (F12):

### System Status

```javascript
// Show all available commands
window.geminiDebug.help()

// Show detailed system information
window.geminiDebug.showInfo()
```

### Testing

```javascript
// Test permissions
window.geminiDebug.checkPermissions()

// Run auto-input test
window.geminiDebug.test()

// Set test data
window.geminiDebug.setTestData("Test data")

// Force input directly
window.geminiDebug.forceInput("Test question")
```

### Troubleshooting

```javascript
// Attempt permission repair
window.geminiDebug.fixPermissions()

// Toggle debug mode
window.geminiDebug.toggleDebug()
```

### Emergency Access

```javascript
// Emergency test interface
window.geminiDebugEmergency.test()

// Force debug interface creation
window.geminiDebugEmergency.forceDebugInterface()
```

## Configuration Options

Edit `configs/config.json` to customize behavior:

### Available Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `gemini_url` | Gemini AI URL with model parameters | `https://aistudio.google.com/...` |
| `firefox_path` | Path to browser executable | Auto-detected |
| `temp_file_path` | Path for temporary data files | `temp/gemini_input.txt` |
| `localhost_port` | Port for HTTP server | `8765` |
| `log_retention_days` | Log file retention period | `365` |
| `encoding` | Text encoding for file operations | `utf-8` |
| `max_prompt_length` | Maximum characters in prompt | `10000` |

### Character Encoding (Windows)

For Japanese or other non-ASCII characters:

```bash
# Command Prompt
chcp 65001
set PYTHONIOENCODING=utf-8

# Or use batch file (automatic UTF-8 setup)
scripts\gemini-query.bat

# PowerShell
$env:PYTHONIOENCODING="utf-8"
gemini-query "質問内容"
```

## Best Practices

### 1. Use Piped Input for Long Content

```bash
# Good: Pipe file content
cat long_document.txt | gemini-query "Summarize"

# Avoid: Very long command-line arguments
gemini-query "Very long text that spans multiple lines..."
```

### 2. Combine with Shell Tools

```bash
# Use grep to filter before sending
grep "ERROR" application.log | gemini-query "Analyze these errors"

# Use head/tail for specific sections
tail -n 50 debug.log | gemini-query "What's the root cause?"
```

### 3. Save Output for Later

```bash
# Redirect output
gemini-query "Explain Docker" > docker_explanation.txt

# Append to existing file
gemini-query "More info" >> notes.txt
```

### 4. Use Aliases for Convenience

```bash
# Add to ~/.bashrc or ~/.zshrc
alias gq='gemini-query'
alias gqr='git diff | gemini-query "Review these changes"'

# Then use
gq "Quick question"
gqr  # Review current git changes
```

## Tips and Tricks

### 1. Multi-line Input

```bash
# Using heredoc
gemini-query <<EOF
Explain the following concepts:
1. Async programming
2. Dependency injection
3. Test-driven development
EOF
```

### 2. Environment Variables

```bash
# Set default model
export GEMINI_MODEL="gemini-2.5-pro-exp-03-25"

# Set custom config path
export GEMINI_CONFIG="$HOME/.config/gemini-query/config.json"
```

### 3. Batch Processing

```bash
# Process multiple files
for file in *.py; do
    cat "$file" | gemini-query "Document this file" > "docs/$file.md"
done
```

## Next Steps

- See [Troubleshooting Guide](troubleshooting.md) for common issues
- See [Architecture Guide](architecture.md) to understand internals
- See [Development Guide](development.md) to contribute
