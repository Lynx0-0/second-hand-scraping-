@echo off
echo.
echo ========================================
echo Test Sistema Subito Scraper
echo ========================================
echo.

echo [1/5] Test Python...
python --version
if errorlevel 1 (
    echo ERRORE: Python non funziona!
    pause
    exit /b 1
)
echo OK
echo.

echo [2/5] Test Node.js...
node --version
if errorlevel 1 (
    echo ERRORE: Node.js non funziona!
    pause
    exit /b 1
)
echo OK
echo.

echo [3/5] Test Virtual Environment...
if exist venv\Scripts\python.exe (
    echo OK - Virtual environment trovato
) else (
    echo ATTENZIONE: Virtual environment non trovato
    echo Verra creato al primo avvio
)
echo.

echo [4/5] Test Frontend...
if exist frontend\node_modules (
    echo OK - Dipendenze frontend installate
) else (
    echo ATTENZIONE: Dipendenze frontend non installate
    echo Verranno installate al primo avvio
)
echo.

echo [5/5] Test File Configurazione...
if exist .env (
    echo OK - .env trovato
) else (
    echo ATTENZIONE: .env mancante
)

if exist frontend\.env (
    echo OK - frontend\.env trovato
) else (
    echo ATTENZIONE: frontend\.env mancante
)
echo.

echo ========================================
echo Test Porte
echo ========================================
echo.

netstat -ano | findstr ":8000" | findstr "LISTENING" >nul 2>&1
if errorlevel 1 (
    echo Backend (porta 8000): NON attivo
) else (
    echo Backend (porta 8000): ATTIVO
)

netstat -ano | findstr ":5173" | findstr "LISTENING" >nul 2>&1
if errorlevel 1 (
    echo Frontend (porta 5173): NON attivo
) else (
    echo Frontend (porta 5173): ATTIVO
)
echo.

echo ========================================
echo RIEPILOGO
echo ========================================
echo.
echo Se tutto OK, esegui: start.bat
echo.
pause
