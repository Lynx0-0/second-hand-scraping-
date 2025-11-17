@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

echo.
echo ========================================
echo 🛑 Arresto Sistema - Windows 10
echo ========================================
echo.

REM ============================================
REM 1. TERMINA PROCESSI PYTHON (BACKEND)
REM ============================================
echo 1️⃣  Termino processi Backend Python...

REM Trova e termina processi uvicorn/python
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe" >NUL
if "%ERRORLEVEL%"=="0" (
    echo 📦 Trovati processi Python, termino...

    REM Termina processi con window title Backend
    taskkill /F /FI "WINDOWTITLE eq Backend-FastAPI*" >nul 2>&1

    REM Backup: termina tutti i python.exe (se necessario)
    REM taskkill /F /IM python.exe >nul 2>&1

    echo ✅ Processi Backend terminati
) else (
    echo ℹ️  Nessun processo Backend attivo
)

REM ============================================
REM 2. TERMINA PROCESSI NODE (FRONTEND)
REM ============================================
echo.
echo 2️⃣  Termino processi Frontend Node.js...

REM Trova e termina processi node
tasklist /FI "IMAGENAME eq node.exe" 2>NUL | find /I /N "node.exe" >NUL
if "%ERRORLEVEL%"=="0" (
    echo 📦 Trovati processi Node.js, termino...

    REM Termina processi con window title Frontend
    taskkill /F /FI "WINDOWTITLE eq Frontend-React-Vite*" >nul 2>&1

    REM Backup: termina node processi vite
    REM taskkill /F /IM node.exe >nul 2>&1

    echo ✅ Processi Frontend terminati
) else (
    echo ℹ️  Nessun processo Frontend attivo
)

REM ============================================
REM 3. LIBERA PORTA 8000 (BACKEND)
REM ============================================
echo.
echo 3️⃣  Libero porta 8000 ^(Backend^)...

set PORT_8000_FREED=0
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING 2^>nul') do (
    echo 🔓 Libero porta 8000 ^(PID: %%a^)...
    taskkill /F /PID %%a >nul 2>&1
    set PORT_8000_FREED=1
)

if !PORT_8000_FREED! equ 1 (
    echo ✅ Porta 8000 liberata
) else (
    echo ℹ️  Porta 8000 già libera
)

REM ============================================
REM 4. LIBERA PORTA 5173 (FRONTEND)
REM ============================================
echo.
echo 4️⃣  Libero porta 5173 ^(Frontend^)...

set PORT_5173_FREED=0
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5173 ^| findstr LISTENING 2^>nul') do (
    echo 🔓 Libero porta 5173 ^(PID: %%a^)...
    taskkill /F /PID %%a >nul 2>&1
    set PORT_5173_FREED=1
)

if !PORT_5173_FREED! equ 1 (
    echo ✅ Porta 5173 liberata
) else (
    echo ℹ️  Porta 5173 già libera
)

REM ============================================
REM 5. VERIFICA FINALE
REM ============================================
echo.
echo 5️⃣  Verifica finale...
timeout /t 2 >nul

REM Controlla se ci sono ancora processi attivi
set STILL_RUNNING=0

netstat -ano | findstr ":8000" | findstr "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️  Porta 8000 ancora occupata
    set STILL_RUNNING=1
)

netstat -ano | findstr ":5173" | findstr "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️  Porta 5173 ancora occupata
    set STILL_RUNNING=1
)

if !STILL_RUNNING! equ 0 (
    echo ✅ Tutti i servizi arrestati correttamente
) else (
    echo.
    echo ⚠️  ATTENZIONE: Alcuni servizi potrebbero essere ancora attivi
    echo.
    echo 🔧 SOLUZIONI:
    echo    1. Riavvia il computer
    echo    2. Usa Task Manager ^(Ctrl+Shift+Esc^) per terminare manualmente:
    echo       - python.exe
    echo       - node.exe
    echo    3. Oppure usa questi comandi:
    echo       ^> taskkill /F /IM python.exe
    echo       ^> taskkill /F /IM node.exe
    echo.
)

REM ============================================
REM 6. CLEANUP OPZIONALE
REM ============================================
echo.
echo ========================================
echo 🧹 OPZIONI CLEANUP ^(Opzionale^)
echo ========================================
echo.
echo Vuoi pulire anche i file temporanei? ^(s/N^)
echo.
echo • s = Rimuove __pycache__, .pyc, logs
echo • N = Mantieni tutto ^(default^)
echo.
set /p CLEANUP="Scelta [s/N]: "

if /i "!CLEANUP!"=="s" (
    echo.
    echo 🧹 Pulizia in corso...

    REM Rimuovi cache Python
    if exist __pycache__ (
        rd /s /q __pycache__ >nul 2>&1
        echo ✅ Rimosso __pycache__
    )

    REM Rimuovi file .pyc
    for /r %%f in (*.pyc) do (
        del /q "%%f" >nul 2>&1
    )
    echo ✅ Rimossi file .pyc

    REM Rimuovi logs (opzionale)
    if exist logs (
        del /q logs\*.log >nul 2>&1
        echo ✅ Logs puliti
    )

    echo ✅ Cleanup completato
) else (
    echo ℹ️  Cleanup saltato
)

REM ============================================
REM SISTEMA ARRESTATO
REM ============================================
echo.
echo ========================================
echo ✅ SISTEMA ARRESTATO
echo ========================================
echo.
echo 🔄 Per riavviare il sistema:
echo    • Esegui: start.bat
echo.
echo 📖 Guide disponibili:
echo    • QUICK_START_WINDOWS.md
echo    • WINDOWS_SETUP.md
echo.
echo ========================================
echo.
pause

exit /b 0
