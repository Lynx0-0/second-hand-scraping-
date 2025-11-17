@echo off
REM Script per fermare l'intero sistema su Windows 10

echo 🛑 Fermando il sistema...
echo.

REM Ferma tutti i processi uvicorn (Backend)
echo Fermando Backend API...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *uvicorn*" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Backend fermato
) else (
    echo ℹ Backend non in esecuzione
)

REM Ferma processi Node/Vite (Frontend)
echo Fermando Frontend React...
taskkill /F /IM node.exe /FI "WINDOWTITLE eq *vite*" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Frontend fermato
) else (
    echo ℹ Frontend non in esecuzione
)

REM Alternativa: cerca per porta
echo.
echo Verifico porte...

REM Libera porta 8000 (Backend)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    echo Termino processo sulla porta 8000 (PID: %%a)
    taskkill /F /PID %%a >nul 2>&1
)

REM Libera porta 5173 (Frontend)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5173 ^| findstr LISTENING') do (
    echo Termino processo sulla porta 5173 (PID: %%a)
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo ✓ Sistema fermato
echo.
echo Per riavviare: start.bat
pause
