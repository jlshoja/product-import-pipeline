@echo off
chcp 65001 >nul
echo ========================================
echo 🚀 WooCommerce Generator v9.1 FIXED
echo ========================================
echo.

REM Check Python
echo [1/3] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo.
    echo Please install Python 3.8+ from:
    echo https://www.python.org/downloads/
    echo.
    echo ⚠️ Make sure to check "Add Python to PATH"
    pause
    exit /b 1
)
python --version
echo ✅ Python found!
echo.

REM Install packages
echo [2/3] Installing packages...
echo This may take a few minutes...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ⚠️ Some packages failed to install.
    echo Trying alternative method...
    python -m pip install --user -r requirements.txt
)
echo.
echo ✅ Packages installed!
echo.

REM Configuration check
echo [3/3] Checking configuration...
if not exist config_v9.py (
    echo ❌ config_v9.py not found!
    pause
    exit /b 1
)
echo ✅ Configuration found!
echo.

echo ========================================
echo 🎉 Installation Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Edit config_v9.py with your settings
echo   2. Run: start.bat
echo.
echo For help, read: README.md
echo.
pause
