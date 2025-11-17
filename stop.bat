@echo off
echo.
echo ========================================
echo Arresto Sistema Subito Scraper
echo ========================================
echo.

echo [1/3] Termino processi Backend...
taskkill /FI "WINDOWTITLE eq Backend-API*" /F >nul 2>&1

echo [2/3] Termino processi Frontend...
taskkill /FI "WINDOWTITLE eq Frontend-UI*" /F >nul 2>&1

echo [3/3] Libero porte...
REM Trova e termina processi su porta 8000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

REM Trova e termina processi su porta 5173
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5173 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo SISTEMA ARRESTATO
echo ========================================
echo.
echo Per riavviare: esegui start.bat
echo.
pause
