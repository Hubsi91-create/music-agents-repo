@echo off
REM Start Orchestrator with correct path
REM Usage: start_orchestrator.bat [command] [args]
REM Examples:
REM   start_orchestrator.bat train
REM   start_orchestrator.bat stats
REM   start_orchestrator.bat enhanced-train 100
REM   start_orchestrator.bat electro uplifting

echo ========================================
echo MUSIC AGENTS - ORCHESTRATOR
echo ========================================
echo.

cd /d "%~dp0orchestrator"

if "%1"=="" (
    echo ERROR: No command specified!
    echo.
    python orchestrator.py
    pause
    exit /b 1
)

echo [START] Running: python orchestrator.py %*
echo.

python orchestrator.py %*

echo.
echo ========================================
echo [DONE] Exit Code: %ERRORLEVEL%
echo ========================================
pause
