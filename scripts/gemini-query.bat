@echo off
chcp 65001 >nul 2>&1
REM ========================================================================
REM Gemini Auto Query - Interactive Command Line Interface for Google Gemini AI
REM ========================================================================
REM 
REM This enhanced batch file provides both interactive and command-line
REM interfaces for the Gemini Auto Query Python application.
REM 
REM Usage:
REM   Double-click: Interactive mode with prompts and help
REM   Command line: gemini-query.bat [question text]
REM 
REM Interactive Mode Features:
REM   - User-friendly prompts and menus
REM   - Built-in help and troubleshooting
REM   - Configuration file access
REM   - Connection testing
REM   - Multiple question support
REM 
REM Command Line Examples: 
REM   gemini-query.bat "What is Python?"
REM   echo "code here" | gemini-query.bat "Explain this code"
REM 
REM Requirements:
REM   - Python 3.7+
REM   - Firefox browser (recommended)
REM   - Tampermonkey/Greasemonkey with gemini_auto_input.user.js v4.4+
REM 
REM Author: GeminiAutoQuery Team
REM Version: 2.0.0 (Interactive Edition)

setlocal enabledelayedexpansion

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Change to the script directory
cd /d "%SCRIPT_DIR%"

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo.
    echo ================================================================
    echo                           ERROR
    echo ================================================================
    echo.
    echo [ERROR] Python is not installed or not in PATH
    echo [INFO] Please install Python 3.7+ and try again
    echo [INFO] Download from: https://www.python.org/downloads/
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

REM Check if main Python script exists
if not exist "%SCRIPT_DIR%gemini_query.py" (
    echo.
    echo ================================================================
    echo                           ERROR
    echo ================================================================
    echo.
    echo [ERROR] gemini_query.py not found in current directory
    echo [INFO] Please ensure all files are in the same folder
    echo [INFO] Current directory: %SCRIPT_DIR%
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

REM Check if configuration exists, offer to create it
if not exist "%SCRIPT_DIR%config.json" (
    echo.
    echo ================================================================
    echo                          WARNING
    echo ================================================================
    echo.
    echo [WARNING] config.json not found
    echo [INFO] This is your first time running Gemini Auto Query
    echo.
    set /p "CREATE_CONFIG=Would you like to create a configuration file? (y/n): "
    if /i "!CREATE_CONFIG!"=="y" (
        echo [INFO] Running setup script...
        python "%SCRIPT_DIR%setup.py"
        if %ERRORLEVEL% neq 0 (
            echo [ERROR] Setup failed. Please check the error messages above.
            pause
            exit /b 1
        )
    ) else (
        echo [INFO] Continuing without configuration file...
        echo [INFO] Default settings will be used
    )
    echo.
)

REM Set console properties for better display
title Gemini Auto Query v2.0.0 - Interactive Edition

REM Display startup message
echo [INFO] Gemini Auto Query v2.0.0 - Interactive Edition
echo [INFO] Launching query...

REM Check if arguments were provided
if "%~1"=="" (
    REM No arguments - Interactive mode
    call :interactive_mode
    set "EXIT_CODE=%ERRORLEVEL%"
    
) else (
    REM Arguments provided - Command line mode
    echo [INFO] Command line mode
    python "%SCRIPT_DIR%gemini_query.py" %*
    set "EXIT_CODE=%ERRORLEVEL%"
)

REM Display completion message
echo.
if %EXIT_CODE% equ 0 (
    echo [SUCCESS] Query completed successfully!
    echo [INFO] Check your browser for Gemini's response
) else (
    echo [ERROR] Query failed with exit code %EXIT_CODE%
    echo [INFO] Please check the error messages above
)

echo.
echo Press any key to close this window...
pause >nul

REM Exit with the same code as the Python application
exit /b %EXIT_CODE%

REM ========================================
REM Interactive Mode Function
REM ========================================
:interactive_mode
echo.
echo ================================================================
echo                Gemini Auto Query - Interactive Mode
echo ================================================================
echo.
echo Welcome to Gemini AI Command Line Interface!
echo.
echo Usage Instructions:
echo    - Enter your question below
echo    - Press Enter to submit
echo    - Type 'help' for more options
echo    - Type 'exit' to quit
echo.

:input_loop
echo ----------------------------------------------------------------
set /p "USER_INPUT=Your question: "

REM Check for special commands
if /i "!USER_INPUT!"=="exit" (
    echo [INFO] Goodbye!
    exit /b 0
)

if /i "!USER_INPUT!"=="help" (
    call :show_help
    goto input_loop
)

if /i "!USER_INPUT!"=="test" (
    echo [INFO] Running connection test...
    python "%SCRIPT_DIR%debug_test.py"
    echo.
    goto input_loop
)

if /i "!USER_INPUT!"=="config" (
    echo [INFO] Opening configuration file...
    if exist "%SCRIPT_DIR%config.json" (
        notepad "%SCRIPT_DIR%config.json"
    ) else (
        echo [ERROR] config.json not found
        echo [INFO] Run setup.py to create configuration
    )
    goto input_loop
)

if /i "!USER_INPUT!"=="fix" (
    echo [INFO] Running browser configuration fix...
    python "%SCRIPT_DIR%fix_browser_config.py"
    echo.
    goto input_loop
)

REM Check if user entered a question
if "!USER_INPUT!"=="" (
    echo [WARNING] Please enter a question
    echo.
    goto input_loop
)

REM Process the question
echo.
echo [INFO] Sending question to Gemini AI...
echo [INFO] Question: !USER_INPUT!
echo [INFO] Opening browser...
echo.

REM Run the Python application
python "%SCRIPT_DIR%gemini_query.py" "!USER_INPUT!"
set "PYTHON_EXIT_CODE=%ERRORLEVEL%"

echo.
if %PYTHON_EXIT_CODE% equ 0 (
    echo [SUCCESS] Query sent successfully!
    echo [INFO] Check your browser for Gemini's response
) else (
    echo [ERROR] Query failed with exit code %PYTHON_EXIT_CODE%
    echo [INFO] Try typing 'test' to check your setup
)

echo.
echo Would you like to ask another question?
set /p "CONTINUE=Continue? (y/n): "
if /i "!CONTINUE!"=="y" (
    echo.
    goto input_loop
) else if /i "!CONTINUE!"=="yes" (
    echo.
    goto input_loop
)

echo [INFO] Thank you for using Gemini Auto Query!
exit /b %PYTHON_EXIT_CODE%

REM ========================================
REM Help Function
REM ========================================
:show_help
echo.
echo ================================================================
echo                           Help Menu
echo ================================================================
echo.
echo Available Commands:
echo    help     - Show this help menu
echo    test     - Test connection and setup
echo    config   - Open configuration file
echo    fix      - Fix browser configuration automatically
echo    exit     - Quit the application
echo.
echo Tips:
echo    - Ask questions in natural language
echo    - Be specific for better results
echo    - Use quotes for complex questions
echo.
echo Troubleshooting:
echo    - Type 'test' if queries aren't working
echo    - Check browser console (F12) for debug info
echo    - Ensure Greasemonkey script is installed
echo.
echo Examples:
echo    "What is Python programming?"
echo    "Explain machine learning in simple terms"
echo    "Write a function to sort an array"
echo    "Review this code: [paste your code here]"
echo.
echo Useful Links:
echo    - Project Documentation: README.md
echo    - Browser Script: gemini_auto_input.user.js
echo    - Test Interface: quick_test.html
echo.
exit /b 0

REM ========================================
REM Utility Functions
REM ========================================
:check_browser_script
REM This function could check if the browser script is installed
REM For now, it's a placeholder for future enhancement
exit /b 0

:open_documentation
if exist "%SCRIPT_DIR%README.md" (
    start "" "%SCRIPT_DIR%README.md"
) else (
    echo [INFO] README.md not found in current directory
)
exit /b 0