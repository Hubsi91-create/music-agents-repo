@echo off
REM Start Dashboard Backend
echo ========================================
echo MUSIC AGENTS - DASHBOARD BACKEND
echo ========================================
echo.

cd /d "%~dp0dashboard\backend"

if not exist "database.py" (
    echo ERROR: database.py not found!
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo [START] Starting Flask Backend...
echo.

REM Check if app.py exists
if exist "app.py" (
    python app.py
) else if exist "main.py" (
    python main.py
) else if exist "server.py" (
    python server.py
) else (
    echo ERROR: No backend entry point found ^(app.py, main.py, or server.py^)
    echo Files in directory:
    dir /b *.py
    pause
    exit /b 1
)

pause
