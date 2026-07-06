@echo off
chcp 65001 >nul
title Product Scraper Web Panel - Starting...
color 0A

echo.
echo ================================================================================
echo                      Product Scraper Web Panel v2.2
echo ================================================================================
echo.
echo Starting web server...
echo.
echo Your browser will open automatically at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.
echo ================================================================================
echo.

REM Wait 2 seconds then open browser
start /B timeout /t 2 /nobreak >nul
start http://localhost:5000

REM Start web panel
python web_panel_interactive.py

pause
