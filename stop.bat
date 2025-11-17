@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo.
echo ========================================
echo    AVVIO SISTEMA - WINDOWS
echo ========================================
echo.

cd /d "%~dp0"

REM 1. Verifica Python
echo [1] Verifica Python...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRORE: Python non trovato
    echo Scarica da: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo OK Python trovato
echo.

REM 2. Verifica Node.js
echo [2] Verifica Node.js...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRORE: Node.js non trovato
    echo Scarica da: https://nodejs.org/
    pause
    exit /b 1
)
node --version
echo OK Node.js trovato
echo.

REM 3. Crea directory
echo [3] Creazione directory...
if not exist logs mkdir logs
if not exist data mkdir data
if not exist output mkdir output
echo OK Directory create
echo.

REM 4. Virtual environment Python
echo [4] Setup virtual environment...
if not exist venv (
    echo Creazione virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat
echo OK Virtual environment attivo
echo.

REM 5. Dipendenze Python
echo [5] Installazione dipendenze Python...
pip install -q --upgrade pip
pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ERRORE installazione dipendenze Python
    pause
    exit /b 1
)
echo OK Dipendenze Python installate
echo.

REM 6. Dipendenze Frontend
echo [6] Installazione dipendenze Frontend...
cd frontend
if not exist node_modules (
    echo Installazione npm - attendere 2-3 minuti...
    call npm install
    if !errorlevel! neq 0 (
        echo ERRORE installazione dipendenze Frontend
        cd ..
        pause
        exit /b 1
    )
)
echo OK Dipendenze Frontend installate
cd ..
echo.

REM 7. Avvio Backend
echo [7] Avvio Backend API...
echo Backend: http://localhost:8000
start "Subito Scraper - Backend" /MIN cmd /k "venv\Scripts\python.exe -m uvicorn api.main:app --host 0.0.0.0 --port 8000"
echo OK Backend avviato in finestra separata
echo.

REM Attesa backend
echo Attendo backend...
timeout /t 5 /nobreak >nul
set /a RETRY=0
:check_backend
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo OK Backend risponde
    goto backend_ok
)
set /a RETRY+=1
if %RETRY% lss 10 (
    echo Tentativo %RETRY%/10...
    timeout /t 2 /nobreak >nul
    goto check_backend
)
echo ATTENZIONE: Backend non risponde
echo Controlla finestra Backend
:backend_ok
echo.

REM 8. Avvio Frontend
echo [8] Avvio Frontend React...
echo Frontend: http://localhost:5173
cd frontend
start "Subito Scraper - Frontend" cmd /k "npm run dev"
cd ..
echo OK Frontend avviato in finestra separata
echo.

REM Attesa frontend
echo Attendo frontend...
timeout /t 8 /nobreak >nul
echo.

REM 9. Riepilogo
echo ========================================
echo    SISTEMA AVVIATO!
echo ========================================
echo.
echo Frontend:  http://localhost:5173
echo Backend:   http://localhost:8000
echo Docs API:  http://localhost:8000/docs
echo.
echo IMPORTANTE:
echo - Vedrai 2 finestre cmd separate
echo - NON chiuderle! Backend e Frontend sono li
echo - Per fermare: stop.bat oppure chiudi le finestre
echo.
echo ========================================
echo.

REM Apri browser
echo Apertura browser...
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo.
echo Sistema avviato!
echo Premi un tasto per chiudere SOLO questa finestra.
echo Le altre 2 finestre devono rimanere aperte!
pause >nul