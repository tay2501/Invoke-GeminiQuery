#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Browser manager tests for Gemini Auto Query.

Tests browser detection, command execution, and error handling.
"""

import sys
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gemini_query.browser import BrowserManager
from gemini_query.config import AppConfig


class TestBrowserManager(unittest.TestCase):
    """Test BrowserManager functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = AppConfig()
        self.manager = BrowserManager(self.config)
    
    def test_get_user_configured_paths_valid(self):
        """Test getting user-configured paths when they exist"""
        config = AppConfig(browser_path="/valid/path")
        manager = BrowserManager(config)
        
        with patch.object(Path, 'exists', return_value=True):
            paths = manager._get_user_configured_paths()
        
        self.assertIn("/valid/path", paths)
    
    def test_get_user_configured_paths_invalid(self):
        """Test getting user-configured paths when they don't exist"""
        config = AppConfig(browser_path="/invalid/path")
        manager = BrowserManager(config)
        
        with patch.object(Path, 'exists', return_value=False):
            paths = manager._get_user_configured_paths()
        
        self.assertEqual(paths, [])
    
    def test_get_user_configured_paths_firefox_backward_compatibility(self):
        """Test backward compatibility with firefox_path"""
        config = AppConfig(firefox_path="/firefox/path")
        manager = BrowserManager(config)
        
        with patch.object(Path, 'exists', return_value=True):
            paths = manager._get_user_configured_paths()
        
        self.assertIn("/firefox/path", paths)
    
    @patch('gemini_query.browser.Platform.current')
    def test_get_windows_paths(self, mock_platform):
        """Test Windows-specific browser path detection"""
        mock_platform.return_value = Platform.WINDOWS
        
        with patch.object(Path, 'exists', return_value=True):
            paths = self.manager._get_windows_paths()
        
        # Should contain some Windows paths
        self.assertTrue(any("firefox.exe" in path for path in paths))
        self.assertTrue(any("chrome.exe" in path for path in paths))
        self.assertTrue(any("msedge.exe" in path for path in paths))
    
    @patch('gemini_query.browser.Platform.current')
    def test_get_macos_paths(self, mock_platform):
        """Test macOS-specific browser path detection"""
        mock_platform.return_value = Platform.MACOS
        
        with patch.object(Path, 'exists', return_value=True):
            paths = self.manager._get_macos_paths()
        
        # Should contain some macOS paths
        self.assertTrue(any("firefox" in path for path in paths))
        self.assertTrue(any("Chrome" in path for path in paths))
        self.assertTrue(any("Safari" in path for path in paths))
    
    @patch('gemini_query.browser.Platform.current')
    def test_get_system_commands_windows(self, mock_platform):
        """Test system command detection on Windows"""
        mock_platform.return_value = Platform.WINDOWS
        
        commands = self.manager._get_system_commands()
        
        self.assertIn('start', commands)
        self.assertIn('firefox', commands)
        self.assertIn('chrome', commands)
    
    @patch('gemini_query.browser.Platform.current')
    def test_get_system_commands_macos(self, mock_platform):
        """Test system command detection on macOS"""
        mock_platform.return_value = Platform.MACOS
        
        commands = self.manager._get_system_commands()
        
        self.assertIn('open', commands)
        self.assertIn('firefox', commands)
        self.assertIn('chrome', commands)
    
    @patch('gemini_query.browser.Platform.current')
    def test_get_system_commands_linux(self, mock_platform):
        """Test system command detection on Linux"""
        mock_platform.return_value = Platform.LINUX
        
        commands = self.manager._get_system_commands()
        
        self.assertIn('xdg-open', commands)
        self.assertIn('firefox', commands)
        self.assertIn('google-chrome', commands)
    
    @patch('subprocess.run')
    def test_try_launch_command_success(self, mock_run):
        """Test successful browser command execution"""
        mock_run.return_value.returncode = 0
        
        result = self.manager._try_launch_command("firefox", "https://example.com")
        
        self.assertTrue(result)
        mock_run.assert_called_once()
    
    @patch('subprocess.run')
    def test_try_launch_command_failure(self, mock_run):
        """Test failed browser command execution"""
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "Error message"
        
        result = self.manager._try_launch_command("firefox", "https://example.com")
        
        self.assertFalse(result)
    
    @patch('subprocess.run', side_effect=FileNotFoundError())
    def test_try_launch_command_not_found(self, mock_run):
        """Test browser command not found"""
        result = self.manager._try_launch_command("nonexistent", "https://example.com")
        
        self.assertFalse(result)
    
    @patch('subprocess.run', side_effect=TimeoutError())
    def test_try_launch_command_timeout(self, mock_run):
        """Test browser command timeout"""
        result = self.manager._try_launch_command("slow_browser", "https://example.com")
        
        self.assertFalse(result)
    
    @patch('gemini_query.browser.Platform.current')
    @patch('subprocess.run')
    def test_execute_command_windows_start(self, mock_run, mock_platform):
        """Test Windows start command execution"""
        mock_platform.return_value = Platform.WINDOWS
        mock_run.return_value.returncode = 0
        
        result = self.manager._execute_command("start", "https://example.com")
        
        # Should use shell=True for start command
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        self.assertTrue(kwargs.get('shell', False))
    
    @patch('subprocess.run')
    def test_execute_command_system_default(self, mock_run):
        """Test system default command execution"""
        mock_run.return_value.returncode = 0
        
        result = self.manager._execute_command("xdg-open", "https://example.com")
        
        # Should use list format for system commands
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        self.assertEqual(args, ["xdg-open", "https://example.com"])
    
    @patch('subprocess.run')
    def test_execute_command_direct_browser(self, mock_run):
        """Test direct browser executable execution"""
        mock_run.return_value.returncode = 0
        
        result = self.manager._execute_command("/usr/bin/firefox", "https://example.com")
        
        # Should use list format for direct executables
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        self.assertEqual(args, ["/usr/bin/firefox", "https://example.com"])
    
    @patch.object(BrowserManager, '_try_webbrowser_fallback')
    @patch.object(BrowserManager, '_try_launch_command')
    def test_launch_success_first_command(self, mock_try_launch, mock_fallback):
        """Test successful launch with first command"""
        mock_try_launch.return_value = True
        
        result = self.manager.launch("https://example.com")
        
        self.assertTrue(result)
        mock_fallback.assert_not_called()
    
    @patch.object(BrowserManager, '_try_webbrowser_fallback')
    @patch.object(BrowserManager, '_try_launch_command')
    def test_launch_fallback_to_webbrowser(self, mock_try_launch, mock_fallback):
        """Test fallback to webbrowser module"""
        mock_try_launch.return_value = False
        mock_fallback.return_value = True
        
        result = self.manager.launch("https://example.com")
        
        self.assertTrue(result)
        mock_fallback.assert_called_once()
    
    @patch('webbrowser.open')
    def test_try_webbrowser_fallback_success(self, mock_open):
        """Test successful webbrowser module fallback"""
        result = self.manager._try_webbrowser_fallback("https://example.com")
        
        self.assertTrue(result)
        mock_open.assert_called_once_with("https://example.com")
    
    @patch('webbrowser.open', side_effect=Exception("Webbrowser failed"))
    def test_try_webbrowser_fallback_failure(self, mock_open):
        """Test failed webbrowser module fallback"""
        result = self.manager._try_webbrowser_fallback("https://example.com")
        
        self.assertFalse(result)
    
    def test_get_browser_commands_no_duplicates(self):
        """Test that browser commands list has no duplicates"""
        commands = self.manager._get_browser_commands()
        
        # Should not have duplicates
        self.assertEqual(len(commands), len(set(commands)))
    
    def test_get_browser_commands_order(self):
        """Test that browser commands are in correct priority order"""
        config = AppConfig(browser_path="/custom/browser")
        manager = BrowserManager(config)
        
        with patch.object(Path, 'exists', return_value=True):
            commands = manager._get_browser_commands()
        
        # User-configured path should be first
        self.assertEqual(commands[0], "/custom/browser")


if __name__ == '__main__':
    unittest.main()