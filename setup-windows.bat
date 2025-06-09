@echo off
echo ========================================
echo Flash Arbitrage Bot - Windows Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

REM Check if pip is available
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip is not available
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

echo Pip version:
python -m pip --version
echo.

REM Upgrade pip, setuptools, and wheel first
echo Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel
if %errorlevel% neq 0 (
    echo WARNING: Failed to upgrade pip/setuptools/wheel, continuing anyway...
)
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist "venv" (
    echo Virtual environment already exists, removing old one...
    rmdir /s /q venv
)

python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo Virtual environment created successfully
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Virtual environment activated
echo.

REM Upgrade pip in virtual environment
echo Upgrading pip in virtual environment...
python -m pip install --upgrade pip setuptools wheel
echo.

REM Install dependencies with Windows-compatible versions
echo Installing Windows-compatible dependencies...
python -m pip install --no-cache-dir -r requirements-windows.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install some dependencies
    echo Trying alternative installation method...
    
    REM Try installing packages one by one
    python -m pip install flask==2.3.3
    python -m pip install flask-cors==4.0.0
    python -m pip install requests==2.31.0
    python -m pip install numpy==1.24.3
    python -m pip install python-dotenv==1.0.0
    
    echo Basic dependencies installed, some advanced features may not work
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To start the bot:
echo 1. Make sure you're in the project directory
echo 2. Run: venv\Scripts\activate.bat
echo 3. Run: python app.py
echo 4. Open browser to: http://localhost:5000
echo.
echo Your wallet is configured as: 68Jxdxbe2GC86GoJGBwNeaRAqun1ttyEEntUSnBsokMK
echo.
pause

