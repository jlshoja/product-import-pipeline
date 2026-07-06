@echo off
chcp 65001 >nul
title Download Images - Advanced

echo ============================================================
echo           Download Images - Advanced Options
echo ============================================================
echo.

REM Check virtual environment
if not exist "imagetools_env" (
    echo [ERROR] Virtual environment not found!
    echo Please run 'install.bat' first.
    echo.
    pause
    exit
)

echo Activating virtual environment...
call imagetools_env\Scripts\activate.bat >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit
)
echo [OK] Virtual environment activated
echo.

REM Check Excel file
if not exist "extracted_products.xlsx" (
    echo [ERROR] 'extracted_products.xlsx' file not found!
    echo.
    echo Please place your Excel file in this folder.
    echo The file should have columns: Product Name, Product URL
    echo.
    pause
    exit
)

echo [OK] Excel file found: extracted_products.xlsx
echo.

REM Check for existing download state
if exist "download_state.json" (
    echo ============================================================
    echo Resume Download
    echo ============================================================
    echo.
    echo [INFO] Previous download state found!
    echo.
    set /p resume="Resume from last position? (y/n, default: y): "
    if "%resume%"=="" set resume=y
    
    if /i "%resume%"=="n" (
        echo.
        set /p confirm_reset="Delete progress and start fresh? (y/n): "
        if /i "%confirm_reset%"=="y" (
            del download_state.json 2>nul
            echo [OK] Progress reset. Starting from beginning.
        ) else (
            echo Cancelled.
            pause
            exit
        )
    ) else (
        echo [OK] Will resume from last position
    )
    echo.
) else (
    echo [INFO] No previous download found. Starting fresh.
    echo.
)

REM Check downloaded_images folder
if exist "downloaded_images" (
    echo [INFO] Output folder 'downloaded_images' exists
) else (
    echo [INFO] Will create 'downloaded_images' folder
)
echo.

echo ============================================================
echo Download Settings
echo ============================================================
echo.
echo - Method: Selenium (full browser simulation)
echo - Output folder: downloaded_images\
echo - Auto-retry: Yes (3 attempts per failed image)
echo - Resume support: Yes
echo.
echo Note: Download time depends on:
echo   - Number of products
echo   - Internet speed
echo   - Server response time
echo.
echo You can press Ctrl+C to stop - progress is saved!
echo.
echo ============================================================
echo.

set /p start="Begin download? (y/n): "
if /i not "%start%"=="y" (
    echo Cancelled.
    pause
    exit
)

echo.
echo ============================================================
echo Downloading... Please wait
echo ============================================================
echo.

REM Run downloader
python Fixed_Image_Downloader.py

if errorlevel 1 (
    echo.
    echo ============================================================
    echo [WARNING] Download interrupted or failed
    echo ============================================================
    echo.
    
    if exist "download_state.json" (
        echo Your progress has been saved in 'download_state.json'
        echo Run this batch file again to continue from where you stopped.
    ) else (
        echo No progress state found.
        echo Check the error messages above.
    )
    echo.
    pause
    exit
)

echo.
echo ============================================================
echo Download Successfully Completed!
echo ============================================================
echo.

REM Count results
if exist "downloaded_images" (
    for /f %%A in ('dir /b /a-d downloaded_images 2^>nul ^| find /c /v ""') do set final_count=%%A
    if defined final_count (
        echo Total files downloaded: %final_count%
    ) else (
        echo Total files downloaded: 0
    )
) else (
    echo Output folder not found
)
echo.

echo Output folder: downloaded_images\
echo.

echo ============================================================
echo Next Steps
echo ============================================================
echo.
echo 1. View downloaded images
echo 2. Process images (run process.bat)
echo 3. Process with options (run process_advanced.bat)
echo.

set /p action="What would you like to do? (1/2/3/Enter to exit): "

if "%action%"=="1" (
    start explorer "downloaded_images"
) else if "%action%"=="2" (
    echo.
    echo Starting image processing...
    echo.
    call process.bat
) else if "%action%"=="3" (
    echo.
    echo Starting advanced processing...
    echo.
    call process_advanced.bat
)

echo.
pause
