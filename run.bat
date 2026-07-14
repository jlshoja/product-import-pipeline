@echo off
REM run.bat - wrapper to run the automatic pipeline with safe defaults
REM Usage: run.bat [timeout_seconds] [subprocess_retries] [no-resume]

IF "%~1"=="" (
  SET TIMEOUT=3600
) ELSE (
  SET TIMEOUT=%~1
)

IF "%~2"=="" (
  SET RETRIES=1
) ELSE (
  SET RETRIES=%~2
)

SET PROCESS_TIMEOUT=%TIMEOUT%
SET PROCESS_SUBPROCESS_RETRY=%RETRIES%

ECHO PROCESS_TIMEOUT=%PROCESS_TIMEOUT%
ECHO PROCESS_SUBPROCESS_RETRY=%PROCESS_SUBPROCESS_RETRY%

IF /I "%~3"=="no-resume" (
  ECHO AUTO_RESUME disabled (will prompt if previous run incomplete)
  SET RESUME_ARG=no-resume
) ELSE (
  ECHO AUTO_RESUME=1 (will resume previous incomplete runs)
  SET RESUME_ARG=auto
)

python product_extraction\main.py %RESUME_ARG%
IF %ERRORLEVEL% NEQ 0 (
  ECHO.
  ECHO Pipeline failed. Check logs for details.
  PAUSE
  EXIT /B 1
)

ECHO.
ECHO Pipeline execution completed.
PAUSE
