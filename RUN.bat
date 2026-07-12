@echo off
setlocal EnableExtensions

chcp 65001 >nul
title Product Import Pipeline - Execution Mode
color 0B

set "ROOT_DIR=%~dp0"
cd /d "%ROOT_DIR%"

:MENU
cls
echo.
echo ============================================================================
echo                  Product Import Pipeline - Execution Mode
echo ============================================================================
echo.
echo   Choose how you want to run the pipeline:
echo.
echo   [1] Step-by-Step Mode   (open the interactive menu, run stages manually)
echo   [2] Automatic Mode      (run the whole pipeline from start to finish)
echo   [0] Exit
echo.
echo ============================================================================
echo.
set /p "choice=Select an option (0-2): "

if "%choice%"=="1" goto STEP_BY_STEP
if "%choice%"=="2" goto AUTOMATIC
if "%choice%"=="0" goto EXIT

echo.
echo Invalid choice. Please select 0, 1 or 2.
timeout /t 2 >nul
goto MENU

:STEP_BY_STEP
cls
echo.
echo ============================================================================
echo Launching Step-by-Step Mode...
echo ============================================================================
echo.
call "%ROOT_DIR%run_pipeline.bat"
goto EXIT

:AUTOMATIC
cls
echo.
echo ============================================================================
echo Running Automatic Mode - Full Pipeline (no prompts)
echo ============================================================================
echo.
echo This runs, from start to finish:
echo   1. Scrape Product Links
echo   2. Scrape Product Specifications (fresh) + Standardize
echo   3. Download and Process Images
echo   4. Build Import Files (WooCommerce CSV)
echo.
pushd product_extraction
python main.py auto
popd
echo.
echo ============================================================================
echo Automatic pipeline finished. Press any key to exit...
echo ============================================================================
pause >nul
goto EXIT

:EXIT
cls
echo.
echo ============================================================================
echo Exiting Product Import Pipeline
echo ============================================================================
echo.
timeout /t 2 >nul
endlocal
exit /b 0
