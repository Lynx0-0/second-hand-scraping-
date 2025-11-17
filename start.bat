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

echo [1/3] Verifiche OK
echo.

REM Crea virtual environment
if not exist venv (
    echo [2/3] Creo virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERRORE: Impossibile creare virtual environment
        pause
        exit /b 1
    )
)

REM Installa dipendenze Python
echo [2/3] Installo dipendenze Python...
call venv\Scripts\activate.bat
pip install -q -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERRORE: Installazione dipendenze Python fallita!
    echo SOLUZIONE: Elimina cartella venv e riprova
    echo   rmdir /s /q venv
    pause
    exit /b 1
)

REM Installa dipendenze frontend
echo [3/3] Installo dipendenze frontend...
if not exist frontend\node_modules (
    cd frontend
    call npm install
    if errorlevel 1 (
        echo ERRORE: Installazione npm fallita!
        cd ..
        pause
        exit /b 1
    )
    cd ..
)

REM Crea directory necessarie
if not exist logs mkdir logs
if not exist data mkdir data
if not exist output mkdir output

REM Copia .env se non esiste
if not exist .env copy .env.example .env >nul 2>&1
if not exist frontend\.env copy frontend\.env.example frontend\.env >nul 2>&1

echo.
echo ========================================
echo Avvio servizi...
echo ========================================
echo.

REM Avvia backend
echo Avvio Backend API (porta 8000)...
start "Backend-API" cmd /c "cd /d %CD% && call venv\Scripts\activate.bat && python -m uvicorn api.main:app --host 0.0.0.0 --port 8000"

REM Aspetta 3 secondi
timeout /t 3 >nul

REM Avvia frontend
echo Avvio Frontend UI (porta 5173)...
start "Frontend-UI" cmd /c "cd /d %CD%\frontend && npm run dev"

REM Aspetta 5 secondi
timeout /t 5 >nul

echo.
echo ========================================
echo SISTEMA AVVIATO!
echo ========================================
echo.
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo FINESTRE APERTE:
echo   - Backend-API  (non chiudere!)
echo   - Frontend-UI  (non chiudere!)
echo.
echo Per fermare: esegui stop.bat
echo.
echo Apro browser tra 3 secondi...
timeout /t 3 >nul

start http://localhost:5173

echo.
echo Premi un tasto per chiudere questa finestra
echo (Il sistema continuera a funzionare)
echo.
pause >nul
