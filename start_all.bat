@echo off
REM Start ALL Components in separate windows
echo ========================================
echo MUSIC AGENTS - START ALL COMPONENTS
echo ========================================
echo.
echo This will open:
echo  1. Orchestrator (Training Mode)
echo  2. Dashboard Backend
echo  3. Integration Tests
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo [1/3] Starting Orchestrator in new window...
start "Orchestrator - Stats" cmd /k "%~dp0start_orchestrator.bat stats"

timeout /t 2 /nobreak >nul

echo [2/3] Starting Dashboard Backend in new window...
start "Dashboard Backend" cmd /k "%~dp0start_backend.bat"

timeout /t 2 /nobreak >nul

echo [3/3] Starting Integration Tests in new window...
start "Integration Tests" cmd /k "%~dp0start_tests.bat"

echo.
echo ========================================
echo [SUCCESS] All components started!
echo ========================================
echo.
echo Check the opened windows for status.
echo Close this window when done.
pause
