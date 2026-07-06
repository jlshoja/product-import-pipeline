@echo off
chcp 65001 >nul
echo ========================================
echo 🌐 Starting WooCommerce Web Panel
echo ========================================
echo.

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Check if web panel exists
if not exist web_panel_v12.py (
    echo ❌ web_panel_v12.py not found!
    echo Please run install.bat first.
    pause
    exit /b 1
)

echo ✅ Starting server...
echo.
echo 🌐 Open in browser:
echo    http://localhost:5000
echo.
echo 🛑 Press Ctrl+C to stop
echo.
echo ========================================
echo.

python web_panel_v12.py

pause
