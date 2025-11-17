@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

echo.
echo ========================================
echo 🚀 Avvio Sistema Completo - Windows 10
echo ========================================
echo.

REM ============================================
REM 1. VERIFICA PYTHON
REM ============================================
echo 1️⃣  Verifico Python...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python non trovato
    echo.
    echo 📖 Installa Python da: https://www.python.org/downloads/
    echo    Consigliato: Python 3.11 o 3.12
    echo    IMPORTANTE: Spunta "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

REM Ottieni versione Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python installato: Python %PYTHON_VERSION%

REM Controlla se è Python 3.13
echo %PYTHON_VERSION% | findstr /C:"3.13" >nul
if %errorlevel% equ 0 (
    echo.
    echo ⚠️  WARNING: Python 3.13 rilevato
    echo    Alcune dipendenze potrebbero richiedere compilazione.
    echo    Consigliato: Python 3.11 o 3.12 per Windows
    echo.
    echo    Continuo comunque... ^(ho aggiornato i pacchetti^)
    timeout /t 3 >nul
)

REM ============================================
REM 2. VERIFICA NODE.JS
REM ============================================
echo.
echo 2️⃣  Verifico Node.js...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js non trovato
    echo.
    echo 📖 Installa Node.js da: https://nodejs.org/
    echo    Usa la versione LTS ^(Long Term Support^)
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node --version 2^>^&1') do set NODE_VERSION=%%i
echo ✅ Node.js installato: %NODE_VERSION%

REM ============================================
REM 3. SETUP VIRTUAL ENVIRONMENT
REM ============================================
echo.
echo 3️⃣  Setup Python virtual environment...

REM Controlla se esiste venv
if exist venv\ (
    echo ✅ Virtual environment già presente
) else (
    echo 📦 Creo nuovo virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Errore creazione virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment creato
)

REM Attiva virtual environment
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Errore attivazione virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment attivato

REM ============================================
REM 4. INSTALLA DIPENDENZE PYTHON
REM ============================================
echo.
echo 4️⃣  Installo dipendenze Python...

REM Aggiorna pip per sicurezza
python -m pip install --upgrade pip --quiet 2>nul

REM Installa dipendenze
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo.
    echo ❌ Errore installazione dipendenze Python
    echo.
    echo 🔧 POSSIBILI SOLUZIONI:
    echo.
    echo    1. Prova a pulire e reinstallare:
    echo       ^> rmdir /s /q venv
    echo       ^> start.bat
    echo.
    echo    2. Se hai Python 3.13, installa Python 3.11 o 3.12:
    echo       ^> https://www.python.org/downloads/
    echo.
    echo    3. Installa Microsoft C++ Build Tools:
    echo       ^> https://visualstudio.microsoft.com/visual-cpp-build-tools/
    echo.
    echo 📖 Guida completa: WINDOWS_SETUP.md
    echo.
    pause
    exit /b 1
)
echo ✅ Dipendenze Python installate

REM ============================================
REM 5. VERIFICA FRONTEND
REM ============================================
echo.
echo 5️⃣  Verifico frontend...
if not exist frontend\ (
    echo ❌ Directory frontend non trovata
    pause
    exit /b 1
)

cd frontend
if %errorlevel% neq 0 (
    echo ❌ Impossibile accedere a directory frontend
    cd ..
    pause
    exit /b 1
)

REM ============================================
REM 6. INSTALLA DIPENDENZE FRONTEND
REM ============================================
echo.
echo 6️⃣  Installo dipendenze frontend ^(potrebbe richiedere qualche minuto^)...

if not exist node_modules\ (
    echo 📦 Installazione pacchetti npm...
    call npm install --silent
    if !errorlevel! neq 0 (
        echo.
        echo ❌ Errore installazione dipendenze frontend
        echo.
        echo 🔧 SOLUZIONI:
        echo    1. Pulisci cache npm:
        echo       ^> npm cache clean --force
        echo       ^> npm install
        echo.
        echo    2. Usa amministratore:
        echo       - Click destro su Prompt → "Esegui come amministratore"
        echo       - Riprova: start.bat
        echo.
        cd ..
        pause
        exit /b 1
    )
    echo ✅ Dipendenze frontend installate
) else (
    echo ✅ Dipendenze frontend già installate
)

cd ..

REM ============================================
REM 7. VERIFICA PORTE DISPONIBILI
REM ============================================
echo.
echo 7️⃣  Verifico porte disponibili...

REM Controlla porta 8000 (Backend)
netstat -ano | findstr ":8000" | findstr "LISTENING" >nul
if %errorlevel% equ 0 (
    echo ⚠️  Porta 8000 già in uso
    echo    Provo a liberarla...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
        taskkill /F /PID %%a >nul 2>&1
    )
    timeout /t 2 >nul
)

REM Controlla porta 5173 (Frontend)
netstat -ano | findstr ":5173" | findstr "LISTENING" >nul
if %errorlevel% equ 0 (
    echo ⚠️  Porta 5173 già in uso
    echo    Provo a liberarla...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5173 ^| findstr LISTENING') do (
        taskkill /F /PID %%a >nul 2>&1
    )
    timeout /t 2 >nul
)

echo ✅ Porte verificate

REM ============================================
REM 8. CREA DIRECTORY LOGS
REM ============================================
echo.
echo 8️⃣  Setup directory logs...
if not exist logs mkdir logs
echo ✅ Directory logs pronta

REM ============================================
REM 9. AVVIA BACKEND
REM ============================================
echo.
echo 9️⃣  Avvio Backend FastAPI ^(porta 8000^)...

REM Attiva venv e avvia backend in background
start "Backend-FastAPI" /B cmd /c "call venv\Scripts\activate.bat && python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 > logs\backend.log 2>&1"

if %errorlevel% neq 0 (
    echo ❌ Errore avvio backend
    pause
    exit /b 1
)

echo ✅ Backend avviato in background
timeout /t 3 >nul

REM ============================================
REM 10. AVVIA FRONTEND
REM ============================================
echo.
echo 🔟  Avvio Frontend React ^(porta 5173^)...

cd frontend
start "Frontend-React-Vite" /B cmd /c "npm run dev > ..\logs\frontend.log 2>&1"

if !errorlevel! neq 0 (
    echo ❌ Errore avvio frontend
    cd ..
    pause
    exit /b 1
)

echo ✅ Frontend avviato in background
cd ..

REM ============================================
REM 11. ATTESA AVVIO SERVIZI
REM ============================================
echo.
echo 📡 Attendo che i servizi si avviino...
timeout /t 8 /nobreak >nul

REM ============================================
REM 12. APERTURA BROWSER
REM ============================================
echo.
echo 🌐 Apro il browser...
timeout /t 2 >nul

start http://localhost:5173

REM ============================================
REM SISTEMA AVVIATO
REM ============================================
echo.
echo ========================================
echo ✅ SISTEMA AVVIATO CON SUCCESSO!
echo ========================================
echo.
echo 📊 SERVIZI ATTIVI:
echo    • Backend API:  http://localhost:8000
echo    • Frontend UI:  http://localhost:5173
echo    • API Docs:     http://localhost:8000/docs
echo.
echo 📝 LOGS:
echo    • Backend:  logs\backend.log
echo    • Frontend: logs\frontend.log
echo.
echo 🛑 Per fermare il sistema:
echo    • Esegui: stop.bat
echo    • Oppure chiudi questa finestra
echo.
echo 💡 TIP: Se non vedi l'interfaccia, aspetta 10 secondi
echo         e aggiorna il browser ^(F5^)
echo.
echo ========================================
echo.
echo Premi un tasto per chiudere questa finestra...
echo ^(Il sistema continuerà a funzionare in background^)
echo.
pause >nul

exit /b 0
