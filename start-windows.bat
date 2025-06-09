@echo off
title Flash Arbitrage Bot - Windows Launcher

echo ========================================
echo Flash Arbitrage Bot - Windows Launcher
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found!
    echo Please run setup-windows.bat first
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    echo Please run setup-windows.bat to recreate it
    pause
    exit /b 1
)

echo Virtual environment activated
echo.

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo Flask not found, installing basic dependencies...
    python -m pip install flask flask-cors requests
)

echo Starting Flash Arbitrage Bot...
echo.
echo Dashboard will be available at: http://localhost:5000
echo Your wallet: 68Jxdxbe2GC86GoJGBwNeaRAqun1ttyEEntUSnBsokMK
echo.
echo Press Ctrl+C to stop the bot
echo ========================================
echo.

REM Start the Windows-compatible version
python app-windows.py

echo.
echo Bot stopped.
pause

