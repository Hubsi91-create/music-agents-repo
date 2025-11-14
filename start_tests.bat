@echo off
REM Run Integration Tests
echo ========================================
echo MUSIC AGENTS - INTEGRATION TESTS
echo ========================================
echo.

cd /d "%~dp0"

if not exist "test_all_agents_local.py" (
    echo ERROR: test_all_agents_local.py not found!
    pause
    exit /b 1
)

echo [START] Running Integration Tests...
echo.

python -m pytest test_all_agents_local.py -v --tb=short

echo.
echo ========================================
echo [DONE] Exit Code: %ERRORLEVEL%
echo ========================================
pause
