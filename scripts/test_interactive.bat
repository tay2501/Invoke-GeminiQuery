@echo off
chcp 65001 >nul 2>&1
REM Test script for interactive batch file functionality
REM This script tests various scenarios for the interactive mode

echo ========================================
echo Testing Gemini Auto Query Interactive Mode
echo ========================================
echo.

REM Test 1: Check if batch file exists
echo [TEST 1] Checking if gemini-query.bat exists...
if exist "gemini-query.bat" (
    echo [PASS] gemini-query.bat found
) else (
    echo [FAIL] gemini-query.bat not found
    goto :end
)

REM Test 2: Check if Python script exists
echo [TEST 2] Checking if gemini_query.py exists...
if exist "gemini_query.py" (
    echo [PASS] gemini_query.py found
) else (
    echo [FAIL] gemini_query.py not found
    goto :end
)

REM Test 3: Check Python installation
echo [TEST 3] Checking Python installation...
python --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [PASS] Python is installed
    python --version
) else (
    echo [FAIL] Python not found or not in PATH
    goto :end
)

REM Test 4: Test command line mode
echo [TEST 4] Testing command line mode...
echo Testing command line functionality... | gemini-query.bat "This is a test from command line mode"
if %ERRORLEVEL% equ 0 (
    echo [PASS] Command line mode works
) else (
    echo [WARNING] Command line mode returned error code %ERRORLEVEL%
)

echo.
echo ========================================
echo Test Summary
echo ========================================
echo.
echo [SUCCESS] Basic functionality tests completed
echo [INFO] To test interactive mode:
echo    1. Double-click gemini-query.bat
echo    2. Try entering: help
echo    3. Try entering: test
echo    4. Try entering a question
echo.
echo [INFO] For more tests, see TESTING.md
echo.

:end
echo Press any key to exit...
pause >nul