@echo off
chcp 65001 >nul

echo.
echo ========================================
echo    ARRESTO SISTEMA
echo ========================================
echo.

cd /d "%~dp0"

REM Ferma Python
echo Fermando Backend...
taskkill /F /IM python.exe >nul 2>&1
if exist logs\backend.pid del /Q logs\backend.pid
echo OK Backend fermato
echo.

REM Ferma Node.js
echo Fermando Frontend...
taskkill /F /IM node.exe >nul 2>&1
if exist logs\frontend.pid del /Q logs\frontend.pid
echo OK Frontend fermato
echo.

REM Pulizia processi su porte
echo Pulizia porte...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5173 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)
echo OK Porte liberate
echo.

echo ========================================
echo    SISTEMA ARRESTATO
echo ========================================
echo.
echo Per riavviare: start.bat
echo.
pause