@echo off
REM Script per avviare l'intero sistema su Windows 10

setlocal EnableDelayedExpansion

echo ========================================
echo 🚀 Avvio Sistema Completo - Windows 10
echo ========================================
echo.

REM Directory root del progetto
set "PROJECT_ROOT=%~dp0"
cd /d "%PROJECT_ROOT%"

REM 1. Verifica Python
echo 1️⃣  Verifico Python...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ Python non trovato. Scaricalo da https://www.python.org/downloads/
    echo   IMPORTANTE: Spunta "Add Python to PATH" durante l'installazione
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ Python installato: %PYTHON_VERSION%

REM 2. Verifica Node.js
echo.
echo 2️⃣  Verifico Node.js...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ Node.js non trovato. Scaricalo da https://nodejs.org/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
echo ✓ Node.js installato: %NODE_VERSION%

REM 3. Crea e attiva virtual environment Python
echo.
echo 3️⃣  Setup Python virtual environment...
if not exist "venv" (
    echo ℹ Creo virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat
echo ✓ Virtual environment attivato

REM 4. Installa dipendenze Python
echo.
echo 4️⃣  Installo dipendenze Python...
pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ✗ Errore installazione dipendenze Python
    pause
    exit /b 1
)
echo ✓ Dipendenze Python installate

REM 5. Installa dipendenze Frontend
echo.
echo 5️⃣  Installo dipendenze Frontend...
cd frontend

if not exist "node_modules" (
    echo ℹ Installo dipendenze Node.js (potrebbe richiedere qualche minuto)...
    call npm install
    if !errorlevel! neq 0 (
        echo ✗ Errore installazione dipendenze Frontend
        cd ..
        pause
        exit /b 1
    )
    echo ✓ Dipendenze Frontend installate
) else (
    echo ✓ Dipendenze Frontend già installate
)

cd ..

REM 6. Verifica Redis (opzionale)
echo.
echo 6️⃣  Verifico Redis...
where redis-cli >nul 2>&1
if %errorlevel% neq 0 (
    echo ℹ Redis non trovato. L'API funzionerà senza cache.
    echo   Per installare Redis su Windows: https://github.com/microsoftarchive/redis/releases
) else (
    redis-cli ping >nul 2>&1
    if !errorlevel! equ 0 (
        echo ✓ Redis già in esecuzione
    ) else (
        echo ℹ Redis installato ma non in esecuzione
        echo   Avvia Redis manualmente se vuoi usare la cache
    )
)

REM 7. Crea directory necessarie
echo.
echo 7️⃣  Creo directory necessarie...
if not exist "data" mkdir data
if not exist "output" mkdir output
if not exist "logs" mkdir logs
echo ✓ Directory create

REM 8. Configura variabili d'ambiente
echo.
echo 8️⃣  Verifico configurazione...
if not exist ".env" (
    echo ℹ Copio .env.example in .env
    copy .env.example .env >nul
)
echo ✓ Configurazione verificata

REM 9. Avvia Backend API
echo.
echo 9️⃣  Avvio Backend API...
echo.
echo ℹ Backend sarà disponibile su: http://localhost:8000
echo ℹ Docs interattive: http://localhost:8000/docs

REM Avvia in background e salva PID
start /B python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 > logs\backend.log 2>&1

REM Attendi che il backend sia pronto
echo ℹ Attendo che il backend sia pronto...
timeout /t 5 /nobreak >nul

REM Verifica che il backend risponda (max 30 secondi)
set /a counter=0
:wait_backend
set /a counter+=1
if %counter% gtr 30 goto backend_timeout

curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% neq 0 (
    timeout /t 1 /nobreak >nul
    goto wait_backend
)

echo ✓ Backend avviato correttamente!
goto backend_ok

:backend_timeout
echo ⚠️ Backend non risponde dopo 30 secondi
echo ℹ Controlla logs\backend.log per dettagli

:backend_ok

REM 10. Avvia Frontend
echo.
echo 🔟  Avvio Frontend React...
echo.
echo ℹ Frontend sarà disponibile su: http://localhost:5173

cd frontend

REM Avvia in background
start /B cmd /c "npm run dev > ..\logs\frontend.log 2>&1"

cd ..

REM Attendi che il frontend sia pronto
echo ℹ Attendo che il frontend sia pronto...
timeout /t 8 /nobreak >nul

REM 11. Riepilogo
echo.
echo ========================================
echo ✅ Sistema Avviato con Successo!
echo ========================================
echo.
echo 📍 LINK UTILI:
echo    • Frontend:     http://localhost:5173
echo    • Backend API:  http://localhost:8000
echo    • API Docs:     http://localhost:8000/docs
echo.
echo 📁 LOG FILES:
echo    • Backend:  logs\backend.log
echo    • Frontend: logs\frontend.log
echo.
echo 🛑 PER FERMARE:
echo    stop.bat
echo.
echo 💡 SUGGERIMENTI:
echo    1. Apri http://localhost:5173 nel browser
echo    2. Prova a cercare: "iPhone 13", "MacBook", "Bicicletta"
echo    3. Usa i filtri per raffinare la ricerca
echo    4. Clicca sul badge rosso per info sulle truffe
echo.
echo ========================================
echo.

REM Apri automaticamente il browser
echo ℹ Apro il browser...
timeout /t 2 /nobreak >nul
start http://localhost:5173

echo.
echo ✓ Sistema avviato! Premi un tasto per chiudere questa finestra.
echo   (Il sistema continuerà a funzionare in background)
pause >nul
