@echo off
echo.
echo ========================================
echo Avvio Sistema Subito Scraper
echo ========================================
echo.

REM Verifica Python
where python >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Python non trovato!
    echo Installa Python da: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Verifica Node
where node >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Node.js non trovato!
    echo Installa Node.js da: https://nodejs.org/
    pause
    exit /b 1
)

echo [1/6] Verifiche completate
echo.

REM Crea virtual environment se non esiste
if not exist venv (
    echo [2/6] Creo virtual environment...
    python -m venv venv
) else (
    echo [2/6] Virtual environment trovato
)

REM Attiva virtual environment e installa dipendenze Python
echo [3/6] Installo dipendenze Python...
call venv\Scripts\activate.bat
pip install -q --upgrade pip
pip install -q -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERRORE: Installazione dipendenze Python fallita!
    echo.
    echo SOLUZIONI:
    echo 1. Elimina la cartella venv e riprova
    echo 2. Se hai Python 3.13, installa Python 3.11 o 3.12
    echo.
    pause
    exit /b 1
)

REM Installa dipendenze frontend
echo [4/6] Installo dipendenze frontend...
cd frontend
if not exist node_modules (
    call npm install
    if errorlevel 1 (
        echo ERRORE: Installazione npm fallita!
        cd ..
        pause
        exit /b 1
    )
)
cd ..

REM Crea directory logs
if not exist logs mkdir logs

REM Avvia backend
echo [5/6] Avvio Backend (porta 8000)...
start "Backend-API" /MIN cmd /c "call venv\Scripts\activate.bat && python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 > logs\backend.log 2>&1"

REM Aspetta 3 secondi
timeout /t 3 /nobreak >nul

REM Avvia frontend
echo [6/6] Avvio Frontend (porta 5173)...
cd frontend
start "Frontend-UI" /MIN cmd /c "npm run dev > ..\logs\frontend.log 2>&1"
cd ..

REM Aspetta che i servizi si avviino
echo.
echo Attendo avvio servizi...
timeout /t 8 /nobreak >nul

REM Apri browser
echo Apro browser...
start http://localhost:5173

echo.
echo ========================================
echo SISTEMA AVVIATO!
echo ========================================
echo.
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Logs:
echo   - logs\backend.log
echo   - logs\frontend.log
echo.
echo Per fermare: esegui stop.bat
echo.
pause
