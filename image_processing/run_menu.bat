@echo off
cd /d "%~dp0"

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found! Please install from https://www.python.org
    pause
    exit /b 1
)

if not exist "menu.py" (
    echo menu.py not found in this folder!
    pause
    exit /b 1
)

python menu.py

if %errorlevel% neq 0 (
    pause
)
