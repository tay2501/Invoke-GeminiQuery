#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Browser configuration fix script for Gemini Auto Query
Automatically detects and configures browser paths
"""

import sys
import os
import json
import subprocess
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Optional

# Windows環境での文字コード設定
if sys.platform == "win32":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
    os.environ['PYTHONIOENCODING'] = 'utf-8'


class Platform(Enum):
    """サポートされているプラットフォーム"""
    WINDOWS = "win32"
    MACOS = "darwin"
    LINUX = "linux"
    
    @classmethod
    def current(cls) -> 'Platform':
        """現在のプラットフォームを取得"""
        match sys.platform:
            case "win32":
                return cls.WINDOWS
            case "darwin":
                return cls.MACOS
            case _:
                return cls.LINUX


@dataclass(kw_only=True)
class BrowserInfo:
    """ブラウザ情報"""
    name: str
    path: str
    is_available: bool = True


def detect_browsers() -> dict[str, BrowserInfo]:
    """システム上で利用可能なブラウザを検出"""
    browsers = {}
    
    match Platform.current():
        case Platform.WINDOWS:
            browsers.update(_detect_windows_browsers())
        case Platform.MACOS:
            browsers.update(_detect_macos_browsers())
        case Platform.LINUX:
            browsers.update(_detect_linux_browsers())
    
    return browsers


def _detect_windows_browsers() -> dict[str, BrowserInfo]:
    """Windows用ブラウザ検出"""
    browsers = {}
    browser_paths = {
        "Firefox": [
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
        ],
        "Chrome": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ],
        "Edge": [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        ]
    }
    
    for browser_name, paths in browser_paths.items():
        for path in paths:
            if Path(path).exists():
                browsers[browser_name] = BrowserInfo(name=browser_name, path=path)
                break
    
    return browsers


def _detect_macos_browsers() -> dict[str, BrowserInfo]:
    """macOS用ブラウザ検出"""
    browsers = {}
    browser_paths = {
        "Firefox": "/Applications/Firefox.app/Contents/MacOS/firefox",
        "Chrome": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "Safari": "/Applications/Safari.app/Contents/MacOS/Safari"
    }
    
    for browser_name, path in browser_paths.items():
        if Path(path).exists():
            browsers[browser_name] = BrowserInfo(name=browser_name, path=path)
    
    return browsers


def _detect_linux_browsers() -> dict[str, BrowserInfo]:
    """Linux用ブラウザ検出"""
    browsers = {}
    browser_commands = {
        "Firefox": "firefox",
        "Chrome": "google-chrome",
        "Chromium": "chromium-browser"
    }
    
    for browser_name, command in browser_commands.items():
        try:
            result = subprocess.run(['which', command], capture_output=True, text=True)
            if result.returncode == 0:
                browsers[browser_name] = BrowserInfo(name=browser_name, path=command)
        except Exception:
            pass
    
    return browsers


def fix_config():
    """Fix browser configuration."""
    print("=" * 60)
    print("Browser Configuration Fix Tool")
    print("=" * 60)
    print()
    
    # Detect browsers
    print("Detecting available browsers...")
    browsers = detect_browsers()
    
    if not browsers:
        print("✗ No browsers detected")
        print("Please install Firefox, Chrome, or Edge and try again")
        return False
    
    print("✓ Found browsers:")
    for i, (name, browser_info) in enumerate(browsers.items(), 1):
        print(f"  {i}. {name}: {browser_info.path}")
    
    print()
    
    # Load current config
    config_path = Path("config.json")
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print("✓ Current configuration loaded")
        except:
            print("✗ Error loading config.json, creating new one")
            config = {}
    else:
        print("✓ Creating new configuration")
        config = {}
    
    # Choose browser
    if len(browsers) == 1:
        browser_name, browser_info = list(browsers.items())[0]
        browser_path = browser_info.path
        print(f"✓ Using detected browser: {browser_name}")
    else:
        print("Multiple browsers detected. Choose one:")
        browser_list = list(browsers.items())
        
        # Auto-select Firefox if available, otherwise first one
        if "Firefox" in browsers:
            browser_name = "Firefox"
            browser_path = browsers["Firefox"].path
            print(f"✓ Auto-selected Firefox: {browser_path}")
        else:
            browser_name, browser_info = browser_list[0]
            browser_path = browser_info.path
            print(f"✓ Auto-selected {browser_name}: {browser_path}")
    
    # Update configuration
    config.update({
        "gemini_url": "https://aistudio.google.com/prompts/new_chat?model=gemini-2.5-pro-exp-03-25",
        "browser_path": browser_path,
        "firefox_path": browser_path if browser_name == "Firefox" else "",
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
    })
    
    # Save configuration
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✓ Configuration saved to {config_path}")
        print(f"✓ Browser path set to: {browser_path}")
        return True
    except Exception as e:
        print(f"✗ Error saving configuration: {e}")
        return False


def main():
    """Main function."""
    if fix_config():
        print()
        print("=" * 60)
        print("Configuration fixed successfully!")
        print("You can now run: python gemini_query.py \"your question\"")
        print("Or double-click: gemini-query.bat")
        print("=" * 60)
        return 0
    else:
        print()
        print("=" * 60)
        print("Configuration fix failed!")
        print("Please check the error messages above")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())