@echo off
chcp 65001 >nul 2>&1
REM ========================================================================
REM Gemini Query v2.0 - Interactive Command Line Interface for Google Gemini AI
REM ========================================================================
REM
REM This enhanced batch file provides both interactive and command-line
REM interfaces for the Gemini Query application using uv package manager.
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
REM   - Python 3.12+
REM   - uv package manager
REM   - Firefox browser (recommended)
REM   - Tampermonkey/Greasemonkey with gemini_auto_input.user.js
REM
REM Author: GeminiQuery Team
REM Version: 2.0.0 (Polylith Architecture Edition)

setlocal enabledelayedexpansion

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Change to the PROJECT ROOT directory (parent of scripts/)
cd /d "%SCRIPT_DIR%.."

REM Check if uv is available
uv --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo.
    echo ================================================================
    echo                           ERROR
    echo ================================================================
    echo.
    echo [ERROR] uv package manager is not installed or not in PATH
    echo [INFO] Please install uv and try again
    echo [INFO] Installation: https://docs.astral.sh/uv/
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

REM Check if project is set up
if not exist "pyproject.toml" (
    echo.
    echo ================================================================
    echo                           ERROR
    echo ================================================================
    echo.
    echo [ERROR] pyproject.toml not found
    echo [INFO] Please run this script from the project root
    echo [INFO] Current directory: %CD%
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

REM Set console properties for better display
title Gemini Query v2.0.0 - Interactive Edition

REM Display startup message
echo [INFO] Gemini Query v2.0.0 - Interactive Edition
echo [INFO] Launching query...

REM Check if arguments were provided
if "%~1"=="" (
    REM No arguments - Interactive mode
    call :interactive_mode
    set "EXIT_CODE=%ERRORLEVEL%"

) else (
    REM Arguments provided - Command line mode
    echo [INFO] Command line mode
    uv run gemini-query query %*
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

REM Exit with the same code as the application
exit /b %EXIT_CODE%

REM ========================================
REM Interactive Mode Function
REM ========================================
:interactive_mode
echo.
echo ================================================================
echo                Gemini Query - Interactive Mode
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

if /i "!USER_INPUT!"=="config" (
    echo [INFO] Opening configuration directory...
    if exist "configs\config.json" (
        notepad "configs\config.json"
    ) else (
        echo [ERROR] config.json not found in configs/
        echo [INFO] Copy configs/config.sample.json to configs/config.json
    )
    goto input_loop
)

if /i "!USER_INPUT!"=="fix" (
    echo [INFO] Running browser configuration fix...
    uv run python scripts/fix_browser_config.py
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

REM Run the application using uv
uv run gemini-query query "!USER_INPUT!"
set "APP_EXIT_CODE=%ERRORLEVEL%"

echo.
if %APP_EXIT_CODE% equ 0 (
    echo [SUCCESS] Query sent successfully!
    echo [INFO] Check your browser for Gemini's response
) else (
    echo [ERROR] Query failed with exit code %APP_EXIT_CODE%
    echo [INFO] Check the error messages above
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

echo [INFO] Thank you for using Gemini Query!
exit /b %APP_EXIT_CODE%

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
echo    config   - Open configuration file
echo    fix      - Fix browser configuration automatically
echo    exit     - Quit the application
echo.
echo Tips:
echo    - Ask questions in natural language
echo    - Be specific for better results
echo    - Use quotes for complex questions
echo.
echo Command Line Usage:
echo    uv run gemini-query query "Your question here"
echo    uv run gq query "Your question here"
echo.
echo Examples:
echo    "What is Python programming?"
echo    "Explain machine learning in simple terms"
echo    "Write a function to sort an array"
echo.
echo Useful Links:
echo    - Documentation: README.md
echo    - Userscript: scripts/userscripts/gemini_auto_input.user.js
echo.
exit /b 0
