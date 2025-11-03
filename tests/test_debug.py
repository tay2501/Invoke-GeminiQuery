#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug test script for Gemini Auto Query
Tests basic functionality and connection
"""

import sys
import os
import json
from pathlib import Path

# Windows環境での文字コード設定
if sys.platform == "win32":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
    os.environ['PYTHONIOENCODING'] = 'utf-8'


def test_python_version():
    """Test Python version compatibility."""
    print("Testing Python version...")
    version = sys.version_info
    if version >= (3, 10):
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} - Requires 3.10+")
        return False


def test_configuration():
    """Test configuration file."""
    print("Testing configuration...")
    config_path = Path("../config.json")
    
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print("✓ Configuration file loaded successfully")
            
            # Check required keys
            required_keys = ['gemini_url', 'firefox_path', 'temp_file_path']
            missing_keys = [key for key in required_keys if key not in config]
            
            if missing_keys:
                print(f"✗ Missing configuration keys: {missing_keys}")
                return False
            else:
                print("✓ All required configuration keys present")
                return True
                
        except json.JSONDecodeError as e:
            print(f"✗ Configuration file has invalid JSON: {e}")
            return False
        except Exception as e:
            print(f"✗ Error reading configuration: {e}")
            return False
    else:
        print("⚠ Configuration file not found (will use defaults)")
        return True


def test_temp_directory():
    """Test temporary directory creation."""
    print("Testing temporary directory...")
    temp_dir = Path("../temp")
    
    try:
        temp_dir.mkdir(exist_ok=True)
        print("✓ Temporary directory created/verified")
        
        # Test file creation
        test_file = temp_dir / "test.txt"
        test_file.write_text("test", encoding='utf-8')
        content = test_file.read_text(encoding='utf-8')
        test_file.unlink()
        
        if content == "test":
            print("✓ File read/write test successful")
            return True
        else:
            print("✗ File read/write test failed")
            return False
            
    except Exception as e:
        print(f"✗ Temporary directory test failed: {e}")
        return False


def test_main_script():
    """Test main script existence."""
    print("Testing main script...")
    # Check both old and new main scripts
    old_script = Path("../gemini_query.py")
    new_script = Path("../gemini_query_new.py")
    
    found_scripts = []
    if old_script.exists():
        found_scripts.append("gemini_query.py")
    if new_script.exists():
        found_scripts.append("gemini_query_new.py")
    
    if found_scripts:
        print(f"✓ Main script(s) found: {', '.join(found_scripts)}")
        return True
    else:
        print("✗ No main scripts found")
        return False


def test_browser_script():
    """Test browser script existence."""
    print("Testing browser script...")
    browser_script = Path("../gemini_auto_input.user.js")
    
    if browser_script.exists():
        print("✓ Browser script (gemini_auto_input.user.js) found")
        return True
    else:
        print("✗ Browser script (gemini_auto_input.user.js) not found")
        return False


def test_browser_availability():
    """Test browser availability."""
    print("Testing browser availability...")
    
    import subprocess
    browsers_found = []
    
    # Test common browser paths on Windows
    if sys.platform == "win32":
        common_paths = [
            ("Firefox", r"C:\Program Files\Mozilla Firefox\firefox.exe"),
            ("Firefox (x86)", r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"),
            ("Chrome", r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
            ("Chrome (x86)", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
            ("Edge", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
            ("Edge (64bit)", r"C:\Program Files\Microsoft\Edge\Application\msedge.exe")
        ]
        
        for name, path in common_paths:
            if os.path.exists(path):
                browsers_found.append(f"{name}: {path}")
                print(f"✓ {name} found at: {path}")
    
    # Test system commands
    system_commands = []
    if sys.platform == "win32":
        system_commands = ["start"]
    elif sys.platform == "darwin":
        system_commands = ["open"]
    else:
        system_commands = ["xdg-open"]
    
    for cmd in system_commands:
        try:
            result = subprocess.run([cmd], capture_output=True, timeout=1)
            print(f"✓ System command '{cmd}' available")
            browsers_found.append(f"System command: {cmd}")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print(f"✗ System command '{cmd}' not available")
    
    if browsers_found:
        print(f"✓ Found {len(browsers_found)} browser option(s)")
        return True
    else:
        print("✗ No browsers found")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Gemini Auto Query - Debug Test")
    print("=" * 60)
    print()
    
    tests = [
        test_python_version,
        test_configuration,
        test_temp_directory,
        test_main_script,
        test_browser_script,
        test_browser_availability
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
        print()
    
    print("=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! System appears to be working correctly.")
        return 0
    else:
        print("⚠ Some tests failed. Please check the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())