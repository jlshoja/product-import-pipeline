@echo off
chcp 65001 >nul
title Product Scraper v2.2 - Main Menu
color 0B

:MENU
cls
echo.
echo ================================================================================
echo                        Product Scraper v2.2 - Main Menu
echo ================================================================================
echo.
echo   [1] Start Web Panel (Interactive Mode)
echo   [2] Scrape Links (Extract Product URLs)
echo   [3] Scrape Specs (Extract Product Details)
echo   [4] Compare Scans (Product Changes)
echo   [5] Track Prices (Compare Prices)
echo   [6] Generate Dashboard
echo   [7] Run Full Pipeline
echo   [8] Run Tests
echo   [9] Open Reports Folder
echo   [A] View Price History
  [0] Exit
echo.
echo ================================================================================
echo.
set /p choice="Select an option (0-9): "

if "%choice%"=="1" goto WEB_PANEL
if "%choice%"=="2" goto SCRAPE_LINKS
if "%choice%"=="3" goto SCRAPE_SPECS
if "%choice%"=="4" goto COMPARE_SCANS
if "%choice%"=="5" goto TRACK_PRICES
if "%choice%"=="6" goto DASHBOARD
if "%choice%"=="7" goto FULL_PIPELINE
if "%choice%"=="8" goto TESTS
if "%choice%"=="9" goto OPEN_REPORTS
if "%choice%"=="0" goto EXIT
if /i "%choice%"=="A" goto VIEW_HISTORY

echo Invalid choice! Please select 0-9.
timeout /t 2 >nul
goto MENU

:WEB_PANEL
cls
echo.
echo ================================================================================
echo                         Starting Web Panel...
echo ================================================================================
echo.
echo Your browser will open at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
echo ================================================================================
echo.
timeout /t 2 /nobreak >nul
start http://localhost:5000
python web_panel_interactive.py
goto MENU

:SCRAPE_LINKS
cls
echo.
echo ================================================================================
echo                         Scraping Product Links...
echo ================================================================================
echo.
python main.py scrape-links
echo.
echo ================================================================================
echo Completed! Press any key to return to menu...
pause >nul
goto MENU

:SCRAPE_SPECS
cls
echo.
echo ================================================================================
echo                      Scraping Product Specifications...
echo ================================================================================
echo.
python main.py scrape-specs
echo.
echo ================================================================================
echo Completed! Press any key to return to menu...
pause >nul
goto MENU

:TRACK_PRICES
cls
echo.
echo ================================================================================
echo                          Tracking Prices...
echo ================================================================================
echo.
python main.py track
echo.
echo ================================================================================
echo Completed! Press any key to return to menu...
pause >nul
goto MENU

:DASHBOARD
cls
echo.
echo ================================================================================
echo                       Generating Dashboard...
echo ================================================================================
echo.
python main.py dashboard
echo.
echo ================================================================================
echo Completed! Press any key to return to menu...
pause >nul
goto MENU

:FULL_PIPELINE
cls
echo.
echo ================================================================================
echo                      Running Full Pipeline...
echo ================================================================================
echo.
echo This will run all steps:
echo 1. Scrape Links
echo 2. Scrape Specs
echo 3. Track Prices
echo 4. Generate Dashboard
echo.
set /p confirm="Continue? (y/n): "
if /i not "%confirm%"=="y" goto MENU
echo.
python main.py full
echo.
echo ================================================================================
echo Completed! Press any key to return to menu...
pause >nul
goto MENU

:TESTS
cls
echo.
echo ================================================================================
echo                           Running Tests...
echo ================================================================================
echo.
python main.py test
echo.
echo ================================================================================
echo Completed! Press any key to return to menu...
pause >nul
goto MENU

:OPEN_REPORTS
cls
echo.
echo Opening reports folder...
start "" "reports"
timeout /t 1 >nul
goto MENU

:VIEW_HISTORY
cls
echo.
echo ================================================================================
echo                          Price History
echo ================================================================================
echo.
if exist "reports\price_history.xlsx" (
    echo Opening price_history.xlsx...
    start "" "reports\price_history.xlsx"
) else (
    echo Price history file not found!
    echo Run "Track Prices" first to generate history.
)
echo.
echo Press any key to return to menu...
pause >nul
goto MENU

:COMPARE_SCANS
cls
echo.
echo ================================================================================
echo                     Comparing Scans (Product Changes)...
echo ================================================================================
echo.
echo This will compare the two latest scans in the reports folder
echo and generate product_changes.xlsx with all differences.
echo.
python trackers\compare_scans.py
echo.
echo ================================================================================
echo Completed! Press any key to return to menu...
pause >nul
goto MENU

:EXIT
cls
echo.
echo ================================================================================
echo                            Goodbye!
echo ================================================================================
echo.
timeout /t 2 >nul
exit
