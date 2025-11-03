# Testing Guide

This document provides comprehensive testing procedures for the Gemini Auto Query project, including manual testing, automated testing, and troubleshooting procedures.

## 🧪 Testing Overview

### Testing Philosophy
- **Multi-layer testing**: Unit, integration, and end-to-end tests
- **Cross-platform validation**: Windows, macOS, and Linux
- **Browser compatibility**: Firefox (primary), Chrome, Edge
- **Failure mode testing**: Test what happens when things go wrong
- **User experience testing**: Real-world usage scenarios

### Test Categories

1. **Unit Tests**: Individual component functionality
2. **Integration Tests**: Component interaction testing
3. **End-to-End Tests**: Complete workflow validation
4. **Performance Tests**: Speed and resource usage
5. **Security Tests**: Permission and data handling
6. **Compatibility Tests**: Cross-platform and cross-browser

## 🔧 Pre-Test Setup

### Environment Preparation

```bash
# 1. Ensure Python environment
python --version  # Should be 3.7+

# 2. Verify project structure
ls -la  # Should show all main files

# 3. Check configuration
cat config.json  # Verify paths and settings

# 4. Install browser extension
# Open Tampermonkey and install gemini_auto_input.user.js
```

### Browser Setup Verification

```javascript
// In browser console at https://aistudio.google.com/prompts/new_chat
// 1. Check script loading
typeof window.geminiDebug  // Should not be 'undefined'

// 2. Check permissions
window.geminiDebug.checkPermissions()
// Should show ✅ for GM_xmlhttpRequest, GM_getValue, GM_setValue

// 3. Test debug interface
window.geminiDebug.help()  // Should show command list
```

## 🧪 Unit Tests

### Python Component Tests

#### 1. Configuration Loading Test
```bash
python -c "
from gemini_query import GeminiQueryCLI
cli = GeminiQueryCLI()
print('Config loaded:', cli.config is not None)
print('Firefox path:', cli.config.get('firefox_path', 'Not set'))
"
```

#### 2. HTTP Server Test
```bash
# Test standalone HTTP server
python debug_test.py

# Expected output:
# ✅ データ書き込み成功
# ✅ HTTP経由でのアクセス成功
```

#### 3. Data Bridge Test
```bash
# Test data writing and reading
python -c "
import sys
sys.path.insert(0, 'src')
from src.data_bridge import DataBridge
from src.config_manager import ConfigManager

config = ConfigManager().load_config()
bridge = DataBridge(config)
success = bridge.write_temp_data('Test data')
print('Data bridge test:', 'PASS' if success else 'FAIL')
"
```

### JavaScript Component Tests

#### 1. Debug Interface Test
```javascript
// In browser console
// Test all debug functions
const functions = ['help', 'checkPermissions', 'showInfo', 'test', 'setTestData', 'forceInput'];
functions.forEach(func => {
    try {
        console.log(`${func}:`, typeof window.geminiDebug[func] === 'function' ? 'PASS' : 'FAIL');
    } catch (e) {
        console.log(`${func}: ERROR -`, e.message);
    }
});
```

#### 2. Element Detection Test
```javascript
// Test UI element detection
const textarea = document.querySelector('textarea[aria-label*="Type something"]');
const button = document.querySelector('button[aria-label*="Run"]');

console.log('Textarea found:', !!textarea);
console.log('Button found:', !!button);
console.log('Button disabled:', button?.disabled);
```

#### 3. Data Transfer Test
```javascript
// Test each data transfer method
async function testDataTransfer() {
    const methods = [
        'HTTP Server',
        'URL Parameters', 
        'localStorage',
        'sessionStorage'
    ];
    
    // Test localStorage
    localStorage.setItem('gemini_auto_input_data', 'test data');
    const localData = localStorage.getItem('gemini_auto_input_data');
    console.log('localStorage test:', localData === 'test data' ? 'PASS' : 'FAIL');
    
    // Test HTTP server
    try {
        const response = await fetch('http://localhost:8765/temp/gemini_input.txt');
        const httpData = await response.text();
        console.log('HTTP server test:', httpData ? 'PASS' : 'FAIL');
    } catch (e) {
        console.log('HTTP server test: FAIL -', e.message);
    }
}

testDataTransfer();
```

## 🔗 Integration Tests

### 1. Python-to-Browser Integration
```bash
# Test complete data flow
echo "Integration test data" | python gemini_query.py "Test integration"

# Expected behavior:
# 1. Python script starts HTTP server
# 2. Browser opens with Gemini URL
# 3. Greasemonkey script detects data
# 4. Text is filled automatically
# 5. Submit button is clicked (if enabled)
```

### 2. Multi-Method Fallback Test
```javascript
// In browser console, test fallback chain
async function testFallbacks() {
    // Disable primary method
    const originalGM = window.GM_xmlhttpRequest;
    window.GM_xmlhttpRequest = undefined;
    
    // Set fallback data
    localStorage.setItem('gemini_auto_input_data', 'Fallback test data');
    
    // Run test
    window.geminiDebug.test();
    
    // Restore
    window.GM_xmlhttpRequest = originalGM;
}

testFallbacks();
```

### 3. Permission Repair Test
```javascript
// Test permission repair functionality
window.geminiDebug.fixPermissions();

// Should either:
// 1. Prompt for page reload
// 2. Show configuration instructions
// 3. Attempt automatic repair
```

## 🌐 End-to-End Tests

### Test Scenarios

#### Scenario 1: Basic Question
```bash
# Test: Simple question input
python gemini_query.py "What is the capital of Japan?"

# Expected:
# ✅ Browser opens
# ✅ Text appears in textarea
# ✅ Submit button is clicked (if enabled)
# ✅ Gemini responds
```

#### Scenario 2: Piped Input
```bash
# Test: Piped content
echo "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)" | python gemini_query.py "Explain this code"

# Expected:
# ✅ Combined prompt with code and question
# ✅ Proper text formatting
# ✅ Successful submission
```

#### Scenario 3: Long Input
```bash
# Test: Long input handling
python gemini_query.py "$(cat README.md) Please summarize this documentation"

# Expected:
# ✅ Input length validation
# ✅ Truncation if necessary
# ✅ Manual input prompt if too long
```

#### Scenario 4: Error Recovery
```bash
# Test: Error handling
# 1. Stop HTTP server manually
# 2. Run: python gemini_query.py "Test error recovery"

# Expected:
# ✅ Fallback to URL parameters
# ✅ Or manual input prompt
# ✅ User-friendly error messages
```

#### Scenario 5: Permission Issues
```javascript
// In browser: Disable GM permissions
// Then run: python gemini_query.py "Test permission fallback"

// Expected:
// ✅ Fallback to localStorage
// ✅ Debug interface shows permission issues
// ✅ Repair suggestions provided
```

## 🚀 Performance Tests

### 1. Startup Time Test
```bash
# Measure startup time
time python gemini_query.py "Performance test"

# Target: < 3 seconds total
# Breakdown:
# - Python startup: < 1 second
# - HTTP server start: < 0.5 seconds
# - Browser launch: < 2 seconds
```

### 2. Memory Usage Test
```bash
# Monitor memory usage
# Windows:
tasklist | findstr python
tasklist | findstr firefox

# Linux/macOS:
ps aux | grep python
ps aux | grep firefox

# Target: < 50MB Python, reasonable browser usage
```

### 3. Data Transfer Speed Test
```javascript
// In browser console
async function speedTest() {
    const start = performance.now();
    
    try {
        const response = await fetch('http://localhost:8765/temp/gemini_input.txt');
        const data = await response.text();
        const end = performance.now();
        
        console.log(`Data transfer: ${end - start}ms for ${data.length} characters`);
        console.log(`Speed: ${(data.length / (end - start) * 1000).toFixed(0)} chars/second`);
    } catch (e) {
        console.log('Speed test failed:', e.message);
    }
}

speedTest();
```

## 🔒 Security Tests

### 1. Data Isolation Test
```bash
# Verify data doesn't persist
python gemini_query.py "Sensitive test data"

# Check:
# 1. temp/gemini_input.txt is cleaned up
# 2. No data in browser storage after use
# 3. HTTP server shuts down properly
```

### 2. Permission Scope Test
```javascript
// Verify script permissions are minimal
console.log('Script permissions:');
console.log('GM_xmlhttpRequest:', typeof GM_xmlhttpRequest !== 'undefined');
console.log('GM_getValue:', typeof GM_getValue !== 'undefined');
console.log('GM_setValue:', typeof GM_setValue !== 'undefined');

// Should NOT have:
console.log('GM_deleteValue:', typeof GM_deleteValue !== 'undefined');  // Should be false
console.log('GM_listValues:', typeof GM_listValues !== 'undefined');    // Should be false
```

### 3. Network Security Test
```bash
# Verify no external network requests
# Monitor network traffic while running:
python gemini_query.py "Network security test"

# Should only see:
# ✅ localhost:8765 requests
# ✅ aistudio.google.com requests
# ❌ No other external requests
```

## 🌍 Cross-Platform Tests

### Windows Testing
```cmd
REM Test Windows-specific functionality
python gemini_query.py "Windows test"

REM Check Windows-specific paths
type config.json | findstr firefox_path

REM Test batch file
gemini-query.bat "Batch file test"
```

### macOS Testing
```bash
# Test macOS-specific functionality
python3 gemini_query.py "macOS test"

# Check macOS Firefox path
grep firefox_path config.json

# Test with different browsers
# Update config.json to point to Chrome or Safari
```

### Linux Testing
```bash
# Test Linux-specific functionality
python3 gemini_query.py "Linux test"

# Test with different shells
bash -c 'echo "Shell test" | python3 gemini_query.py "Test bash"'
zsh -c 'echo "Shell test" | python3 gemini_query.py "Test zsh"'
```

## 🔧 Browser Compatibility Tests

### Firefox (Primary)
```javascript
// Test Firefox-specific features
console.log('Browser:', navigator.userAgent);
console.log('GM functions available:', typeof GM_xmlhttpRequest !== 'undefined');

// Test Greasemonkey vs Tampermonkey
console.log('Extension type:', typeof GM_info !== 'undefined' ? GM_info.scriptHandler : 'Unknown');
```

### Chrome Testing
```javascript
// Update config.json to use Chrome
// Test Chrome-specific behavior
console.log('Chrome version:', navigator.userAgent.match(/Chrome\/(\d+)/)?.[1]);

// Test Tampermonkey compatibility
window.geminiDebug.checkPermissions();
```

### Edge Testing
```javascript
// Test Microsoft Edge compatibility
console.log('Edge version:', navigator.userAgent.match(/Edg\/(\d+)/)?.[1]);

// Test extension compatibility
window.geminiDebug.test();
```

## 📊 Test Results Documentation

### Test Report Template

```markdown
# Test Report - [Date]

## Environment
- OS: [Windows 10/macOS 12/Ubuntu 20.04]
- Python: [3.9.7]
- Browser: [Firefox 95.0]
- Extension: [Tampermonkey 4.14]

## Test Results

### Unit Tests
- [ ] Configuration loading: PASS/FAIL
- [ ] HTTP server: PASS/FAIL
- [ ] Data bridge: PASS/FAIL
- [ ] Debug interface: PASS/FAIL

### Integration Tests
- [ ] Python-to-browser: PASS/FAIL
- [ ] Fallback methods: PASS/FAIL
- [ ] Permission repair: PASS/FAIL

### End-to-End Tests
- [ ] Basic question: PASS/FAIL
- [ ] Piped input: PASS/FAIL
- [ ] Long input: PASS/FAIL
- [ ] Error recovery: PASS/FAIL

### Performance Tests
- [ ] Startup time: [X.X seconds]
- [ ] Memory usage: [XX MB]
- [ ] Data transfer: [XX ms]

## Issues Found
1. [Description of issue]
   - Severity: High/Medium/Low
   - Workaround: [If available]

## Recommendations
1. [Improvement suggestions]
```

## 🚨 Troubleshooting Test Failures

### Common Test Failures

#### 1. "HTTP server test: FAIL"
```bash
# Check port availability
netstat -an | grep 8765  # Linux/macOS
netstat -an | findstr 8765  # Windows

# Try different port
# Edit config.json: "localhost_port": 8766
```

#### 2. "GM_xmlhttpRequest: FAIL"
```javascript
// Check Tampermonkey settings
// 1. Open Tampermonkey dashboard
// 2. Edit script
// 3. Verify @grant and @connect directives
// 4. Save and reload page
```

#### 3. "Element detection: FAIL"
```javascript
// Check for UI changes
document.querySelectorAll('textarea').forEach((el, i) => {
    console.log(`Textarea ${i}:`, el.className, el.getAttribute('aria-label'));
});

document.querySelectorAll('button').forEach((el, i) => {
    console.log(`Button ${i}:`, el.textContent.trim(), el.getAttribute('aria-label'));
});
```

#### 4. "Data transfer: FAIL"
```bash
# Check file permissions
ls -la temp/
cat temp/gemini_input.txt

# Check HTTP server manually
curl http://localhost:8765/temp/gemini_input.txt
```

### Test Environment Reset

```bash
# Clean test environment
rm -rf temp/
rm -rf logs/
mkdir temp
mkdir logs

# Reset browser storage
# In browser console:
localStorage.clear();
sessionStorage.clear();

# Restart HTTP server
python debug_test.py server
```

## 📈 Continuous Testing

### Automated Testing Setup

```bash
# Create test runner script
cat > run_tests.sh << 'EOF'
#!/bin/bash
echo "Running Gemini Auto Query Tests..."

# Unit tests
echo "1. Unit Tests"
python debug_test.py

# Integration test
echo "2. Integration Test"
echo "Test data" | python gemini_query.py "Test question"

# Performance test
echo "3. Performance Test"
time python gemini_query.py "Performance test"

echo "Tests completed!"
EOF

chmod +x run_tests.sh
```

### Regular Testing Schedule

- **Daily**: Automated unit tests
- **Weekly**: Full integration tests
- **Monthly**: Cross-platform compatibility tests
- **Before releases**: Complete test suite

---

This testing guide provides comprehensive procedures for validating the Gemini Auto Query system. Regular testing ensures reliability and helps identify issues before they affect users.

**Remember**: Good testing is about finding problems before users do. Test early, test often, and test everything that can break.