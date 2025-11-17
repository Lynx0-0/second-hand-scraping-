@echo off
echo.
echo Avvio Sistema Subito Scraper
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Python non trovato!
    pause
    exit /b 1
)

where node >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Node.js non trovato!
    pause
    exit /b 1
)

echo [1/3] Verifiche OK
echo.

if not exist venv (
    echo [2/3] Creo virtual environment...
    python -m venv venv
)

echo [2/3] Installo dipendenze Python...
call venv\Scripts\activate.bat
pip install -q -r requirements.txt

echo [3/3] Installo dipendenze frontend...
if not exist frontend\node_modules (
    cd frontend
    call npm install
    cd ..
)

if not exist logs mkdir logs
if not exist data mkdir data
if not exist .env copy .env.example .env >nul 2>&1
if not exist frontend\.env copy frontend\.env.example frontend\.env >nul 2>&1

echo.
echo Avvio servizi...
echo.

start "Backend-API" cmd /c "cd /d %CD% && call venv\Scripts\activate.bat && python -m uvicorn api.main:app --host 0.0.0.0 --port 8000"
timeout /t 3 >nul

start "Frontend-UI" cmd /c "cd /d %CD%\frontend && npm run dev"
timeout /t 5 >nul

echo.
echo SISTEMA AVVIATO!
echo Frontend: http://localhost:5173
echo Backend: http://localhost:8000
echo.
timeout /t 3 >nul
start http://localhost:5173
pause