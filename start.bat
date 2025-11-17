@echo off
echo.
echo ========================================
echo Avvio Sistema Subito Scraper
echo ========================================
echo.

REM Salva directory corrente
set "PROJECT_DIR=%CD%"

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

echo [1/7] Verifiche completate
echo.

REM Crea virtual environment se non esiste
if not exist venv (
    echo [2/7] Creo virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERRORE: Impossibile creare virtual environment!
        pause
        exit /b 1
    )
) else (
    echo [2/7] Virtual environment trovato
)

REM Attiva virtual environment e installa dipendenze Python
echo [3/7] Installo dipendenze Python...
call venv\Scripts\activate.bat
pip install -q --upgrade pip
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
    echo.
    echo SOLUZIONI:
    echo 1. Elimina la cartella venv: rmdir /s /q venv
    echo 2. Se hai Python 3.13, installa Python 3.11 o 3.12
    echo 3. Controlla logs\backend.log per dettagli
    echo.
    echo SOLUZIONE: Elimina cartella venv e riprova
    echo   rmdir /s /q venv
    pause
    exit /b 1
)

REM Installa dipendenze frontend
echo [4/7] Installo dipendenze frontend...
cd frontend
if not exist node_modules (
    echo    Installazione npm in corso (puo richiedere tempo)...
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
) else (
    echo    Dipendenze frontend gia installate
)
cd ..

REM Crea directory logs e data
echo [5/7] Preparo directory...
    cd ..
)

REM Crea directory necessarie
if not exist logs mkdir logs
if not exist data mkdir data
if not exist output mkdir output

REM Verifica file .env
if not exist .env (
    echo ATTENZIONE: File .env non trovato!
    echo Copio da .env.example...
    copy .env.example .env >nul
)

if not exist frontend\.env (
    echo ATTENZIONE: File frontend\.env non trovato!
    echo Copio da frontend\.env.example...
    copy frontend\.env.example frontend\.env >nul
)

REM Avvia backend
echo [6/7] Avvio Backend API (porta 8000)...
start "Backend-API" cmd /c "cd /d "%PROJECT_DIR%" && call venv\Scripts\activate.bat && python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 2>&1 | tee logs\backend.log"

REM Aspetta backend
echo    Attendo avvio backend...
timeout /t 5 /nobreak >nul

REM Verifica backend
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo    ATTENZIONE: Backend potrebbe non essere partito
    echo    Controlla logs\backend.log
) else (
    echo    Backend ATTIVO!
)

REM Avvia frontend
echo [7/7] Avvio Frontend UI (porta 5173)...
start "Frontend-UI" cmd /c "cd /d "%PROJECT_DIR%\frontend" && npm run dev 2>&1 | tee ..\logs\frontend.log"

REM Aspetta frontend
echo    Attendo avvio frontend...
timeout /t 8 /nobreak >nul
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
echo Logs:
echo   - logs\backend.log
echo   - logs\frontend.log
echo.
echo FINESTRE APERTE:
echo   - Backend-API  (porta 8000)
echo   - Frontend-UI  (porta 5173)
echo.
echo Per fermare: esegui stop.bat
echo            o chiudi le finestre Backend-API e Frontend-UI
echo.

REM Apri browser
echo Apro browser tra 3 secondi...
timeout /t 3 /nobreak >nul
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
