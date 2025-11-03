# Troubleshooting Guide

## Common Issues and Solutions

### Character Encoding Issues (Windows)

#### 文字化けが発生する場合

**Command Prompt:**
```bash
# Enable UTF-8 encoding
chcp 65001

# Set Python encoding
set PYTHONIOENCODING=utf-8

# Run the application
gemini-query "質問内容"
```

**PowerShell (推奨):**
```powershell
# Set encoding environment variable
$env:PYTHONIOENCODING="utf-8"

# Run the application
gemini-query "質問内容"
```

**Batch File (自動設定):**
```bash
# Use the batch file (automatically sets UTF-8)
scripts\gemini-query.bat
```

### Installation Issues

#### Python Version Errors

```bash
# Check Python version (must be 3.12+)
python --version

# Install specific version with uv
uv python install 3.12

# List available Python versions
uv python list
```

#### Dependency Installation Fails

```bash
# Clear uv cache
uv cache clean

# Reinstall dependencies
uv sync --reinstall

# Install with dev dependencies
uv sync --group dev
```

#### Virtual Environment Issues

```bash
# Remove existing virtual environment
rm -rf .venv  # Linux/macOS
rmdir /s .venv  # Windows

# Recreate virtual environment
uv venv

# Sync dependencies
uv sync
```

### Browser Issues

#### Browser Doesn't Open

**Automatic Fix:**
```bash
# Run browser configuration script
uv run python scripts/fix_browser_config.py
```

**Manual Configuration:**

Edit `configs/config.json`:
```json
{
  "firefox_path": "C:\\Program Files\\Mozilla Firefox\\firefox.exe"  // Windows
}
```

**Verify Browser Path:**
```bash
# Test browser manually
firefox "https://aistudio.google.com/prompts/new_chat"

# Check if browser executable exists
ls "C:\Program Files\Mozilla Firefox\firefox.exe"  # Windows
```

#### Browser Opens But Script Doesn't Run

1. **Check Tampermonkey Installation:**
   - Open Tampermonkey dashboard
   - Verify script is enabled
   - Check script matches location

2. **Verify Permissions:**
   ```javascript
   // In browser console (F12)
   window.geminiDebug.checkPermissions()
   ```

3. **Expected Output:**
   ```
   ✅ GM_xmlhttpRequest: 利用可能
   ✅ GM_getValue: 利用可能
   ✅ GM_setValue: 利用可能
   ```

#### Wrong Browser Opens

Update `configs/config.json` with your preferred browser:

```json
{
  "firefox_path": "/path/to/your/browser",
  "browser_type": "firefox"  // or "chrome", "edge"
}
```

### Greasemonkey/Tampermonkey Issues

#### Script Not Loading

**Verify Installation:**
```javascript
// In browser console
typeof window.geminiDebug  // Should not be 'undefined'
```

**If Undefined:**
```javascript
// Try emergency interface
window.geminiDebugEmergency.test()
```

**Check Script Matches:**
- Navigate to: `https://aistudio.google.com/prompts/new_chat`
- Open Tampermonkey menu
- Verify script is active (green indicator)

#### Permission Errors

**Check Permissions:**
```javascript
// In browser console
window.geminiDebug.checkPermissions()
```

**Fix Permissions:**
1. Open Tampermonkey dashboard
2. Click on script name
3. Go to Settings tab
4. Verify these grants are enabled:
   - `GM_xmlhttpRequest`
   - `GM_getValue`
   - `GM_setValue`
5. Verify these connections are allowed:
   - `localhost`
   - `127.0.0.1`
   - `*` (all domains)

**Automatic Fix:**
```javascript
window.geminiDebug.fixPermissions()
```

#### Data Not Transferred

**Test Data Sources:**
```javascript
// Test localStorage
localStorage.setItem('gemini_auto_input_data', 'test data')
window.geminiDebug.test()

// Test HTTP server
fetch('http://localhost:8765/temp/gemini_input.txt')
  .then(r => r.text())
  .then(console.log)
  .catch(console.error)
```

**Force Input:**
```javascript
window.geminiDebug.forceInput("test question")
```

#### Submit Button Not Working

**Check Button State:**
```javascript
const button = document.querySelector('button[aria-label*="Run"]')
console.log('Button exists:', !!button)
console.log('Button disabled:', button?.disabled)
```

**Force Submit:**
```javascript
window.geminiDebug.forceInput("test question")
```

### Network Issues

#### HTTP Server Not Starting

**Check Port Availability:**
```bash
# Linux/macOS
netstat -an | grep 8765

# Windows
netstat -an | findstr 8765
```

**Change Port:**

Edit `configs/config.json`:
```json
{
  "localhost_port": 9000  // Use different port
}
```

#### Connection Refused

1. **Check Firewall:**
   - Allow `python.exe` through firewall
   - Allow localhost connections

2. **Check Antivirus:**
   - Some antivirus software blocks localhost servers
   - Add exception for project directory

3. **Test Manually:**
   ```bash
   # Start simple HTTP server
   python -m http.server 8765
   ```

### Application Errors

#### Command Not Found

**After Installation:**
```bash
# Verify installation
uv run gemini-query --help

# If command not found, use full path
uv run python -m gemini_query.cli_app.core
```

**Activate Virtual Environment:**
```bash
# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# Then run directly
gemini-query "test"
```

#### Import Errors

**ModuleNotFoundError:**
```bash
# Reinstall dependencies
uv sync --reinstall

# Check installed packages
uv pip list
```

**Version Conflicts:**
```bash
# Check dependency tree
uv tree

# Update specific package
uv pip install --upgrade <package-name>
```

#### Configuration Errors

**Config File Not Found:**
```bash
# Create from sample
cp configs/config.sample.json configs/config.json  # Linux/macOS
copy configs\config.sample.json configs\config.json  # Windows
```

**Invalid JSON:**
```bash
# Validate JSON
python -m json.tool configs/config.json
```

### Performance Issues

#### Slow Response Times

1. **Check Network:**
   ```bash
   # Test localhost connection
   curl http://localhost:8765
   ```

2. **Check Temp Files:**
   ```bash
   # Clear temp directory
   rm -rf temp/*  # Linux/macOS
   del /q temp\*  # Windows
   ```

3. **Monitor Logs:**
   ```bash
   # Check recent logs
   tail -f logs/gemini_query_$(date +%Y-%m-%d).log  # Linux/macOS
   ```

#### High Memory Usage

1. **Check Browser:**
   - Close unused tabs
   - Clear browser cache
   - Restart browser

2. **Check Python Process:**
   ```bash
   # Linux/macOS
   ps aux | grep python

   # Windows
   tasklist | findstr python
   ```

3. **Clean Up:**
   ```bash
   # Remove logs older than 30 days
   find logs/ -name "*.log" -mtime +30 -delete  # Linux/macOS
   ```

## Debug Mode

### Enable Debug Logging

Edit `configs/config.json`:
```json
{
  "log_level": "DEBUG"
}
```

### Browser Debug Mode

```javascript
// Enable debug mode
localStorage.setItem('gemini_debug_mode', 'true')
window.location.reload()

// View debug logs
console.log(localStorage.getItem('gemini_debug_logs'))
```

## Debug Commands Reference

### Browser Console Commands

```javascript
// System Information
window.geminiDebug.help()                    // Show all commands
window.geminiDebug.showInfo()               // Show system info
window.geminiDebug.checkPermissions()        // Check permissions

// Testing
window.geminiDebug.test()                    // Run test
window.geminiDebug.setTestData("test")       // Set test data
window.geminiDebug.forceInput("test")        // Force input

// Troubleshooting
window.geminiDebug.fixPermissions()         // Fix permissions
window.geminiDebug.toggleDebug()            // Toggle debug mode

// Emergency
window.geminiDebugEmergency.test()          // Emergency test
window.geminiDebugEmergency.forceDebugInterface()  // Force debug UI
```

## FAQ

### Q: Why does the manual input prompt appear?

**A:** This happens when all automatic data transfer methods fail. It's a fallback mechanism.

**Solutions:**
1. Check HTTP server is running
2. Verify Greasemonkey permissions
3. Check browser console for errors

### Q: Can I use browsers other than Firefox?

**A:** Yes, but Firefox is recommended.

**To use Chrome/Edge:**
```json
{
  "firefox_path": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "browser_type": "chrome"
}
```

### Q: How do I update the Greasemonkey script?

**A:**
1. Open Tampermonkey dashboard
2. Click script name
3. Replace content with `scripts/userscripts/gemini_auto_input.user.js`
4. Save

### Q: What if Gemini's UI changes?

**A:** The script uses multiple selectors for robustness. If it breaks:
1. Check browser console for errors
2. Update selectors in userscript
3. Report issue on GitHub

### Q: Is my data secure?

**A:** Yes. Data is:
- Stored temporarily in local files
- Transferred via localhost only
- No external servers involved
- Automatically cleaned up

## Getting Additional Help

### Before Reporting Issues

1. **Check logs:**
   ```bash
   cat logs/gemini_query_$(date +%Y-%m-%d).log | tail -n 50
   ```

2. **Run debug commands:**
   ```javascript
   window.geminiDebug.showInfo()
   ```

3. **Test with simple input:**
   ```bash
   gemini-query "test"
   ```

### Bug Report Information

When reporting issues, include:

- **Operating System:** Windows/macOS/Linux version
- **Python Version:** `python --version`
- **Browser:** Name and version
- **Error Messages:** Full error text
- **Console Output:** Browser console errors (F12)
- **Log Files:** Recent log entries
- **Steps to Reproduce:** What you did before the error

### Create GitHub Issue

Visit: [GitHub Issues](https://github.com/gemini-query/gemini-query/issues)

Include:
- Clear description
- Environment details
- Error messages
- Steps to reproduce
- Expected vs actual behavior

## See Also

- [Installation Guide](installation.md)
- [Usage Guide](usage.md)
- [Architecture Guide](architecture.md)
- [Development Guide](development.md)
