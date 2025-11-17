@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

echo.
echo ========================================
echo 🔄 Reset Sistema - Windows 10
echo ========================================
echo.
echo ⚠️  ATTENZIONE: Questo script:
echo    • Arresta tutti i servizi
echo    • Rimuove virtual environment Python
echo    • Pulisce cache e file temporanei
echo    • Resetta il sistema alle condizioni iniziali
echo.
echo 💡 Usa questo script se:
echo    • Hai problemi con le dipendenze Python
echo    • L'installazione è corrotta
echo    • Vuoi ricominciare da capo
echo.
echo ========================================
echo.
set /p CONFIRM="Sei sicuro di voler procedere? [s/N]: "

if /i not "!CONFIRM!"=="s" (
    echo.
    echo ❌ Reset annullato
    echo.
    pause
    exit /b 0
)

echo.
echo 🚀 Avvio procedura di reset...
echo.

REM ============================================
REM 1. ARRESTA SISTEMA
REM ============================================
echo 1️⃣  Arresto sistema...
call stop.bat >nul 2>&1
timeout /t 2 >nul
echo ✅ Sistema arrestato

REM ============================================
REM 2. RIMUOVI VIRTUAL ENVIRONMENT
REM ============================================
echo.
echo 2️⃣  Rimuovo virtual environment Python...

if exist venv\ (
    echo 📦 Rimozione venv in corso...
    rd /s /q venv >nul 2>&1
    if exist venv\ (
        echo ⚠️  Impossibile rimuovere completamente venv
        echo    Prova a chiudere tutti i programmi Python e riprova
    ) else (
        echo ✅ Virtual environment rimosso
    )
) else (
    echo ℹ️  Virtual environment non presente
)

REM ============================================
REM 3. PULISCI CACHE PYTHON
REM ============================================
echo.
echo 3️⃣  Pulizia cache Python...

REM Rimuovi __pycache__
set PYCACHE_COUNT=0
for /d /r %%d in (__pycache__) do (
    rd /s /q "%%d" >nul 2>&1
    set /a PYCACHE_COUNT+=1
)
if !PYCACHE_COUNT! gtr 0 (
    echo ✅ Rimossi !PYCACHE_COUNT! directory __pycache__
) else (
    echo ℹ️  Nessuna cache Python da rimuovere
)

REM Rimuovi file .pyc
set PYC_COUNT=0
for /r %%f in (*.pyc) do (
    del /q "%%f" >nul 2>&1
    set /a PYC_COUNT+=1
)
if !PYC_COUNT! gtr 0 (
    echo ✅ Rimossi !PYC_COUNT! file .pyc
)

REM ============================================
REM 4. PULISCI NODE_MODULES (OPZIONALE)
REM ============================================
echo.
echo 4️⃣  Pulizia frontend...
echo.
echo    Vuoi rimuovere anche node_modules? ^(Richiede reinstallazione^)
set /p CLEAN_NODE="    [s/N]: "

if /i "!CLEAN_NODE!"=="s" (
    if exist frontend\node_modules\ (
        echo 📦 Rimozione node_modules ^(può richiedere tempo^)...
        cd frontend
        rd /s /q node_modules >nul 2>&1
        cd ..
        echo ✅ node_modules rimosso
    ) else (
        echo ℹ️  node_modules non presente
    )
) else (
    echo ℹ️  node_modules mantenuto
)

REM Pulisci cache npm
if /i "!CLEAN_NODE!"=="s" (
    echo 🧹 Pulizia cache npm...
    npm cache clean --force >nul 2>&1
    echo ✅ Cache npm pulita
)

REM ============================================
REM 5. PULISCI LOGS
REM ============================================
echo.
echo 5️⃣  Pulizia logs...

if exist logs\ (
    del /q logs\*.log >nul 2>&1
    echo ✅ Logs rimossi
) else (
    echo ℹ️  Nessun log da rimuovere
)

REM ============================================
REM 6. PULISCI OUTPUT E DATA (OPZIONALE)
REM ============================================
echo.
echo 6️⃣  Pulizia dati applicazione...
echo.
echo    Vuoi rimuovere anche output e dati salvati?
set /p CLEAN_DATA="    [s/N]: "

if /i "!CLEAN_DATA!"=="s" (
    if exist output\ (
        rd /s /q output >nul 2>&1
        echo ✅ Directory output rimossa
    )
    if exist data\ (
        rd /s /q data >nul 2>&1
        echo ✅ Directory data rimossa
    )
) else (
    echo ℹ️  Dati applicazione mantenuti
)

REM ============================================
REM RESET COMPLETATO
REM ============================================
echo.
echo ========================================
echo ✅ RESET COMPLETATO
echo ========================================
echo.
echo 📊 STATO SISTEMA:
if exist venv\ (
    echo    • Virtual Environment: ⚠️  Ancora presente
) else (
    echo    • Virtual Environment: ✅ Rimosso
)

if exist frontend\node_modules\ (
    echo    • Node Modules:        ✅ Presente
) else (
    echo    • Node Modules:        ⚠️  Da reinstallare
)

echo.
echo 🚀 PROSSIMI PASSI:
echo.
echo    1. Verifica requisiti di sistema:
echo       • Python 3.11 o 3.12 consigliato
echo       • Node.js 18+ LTS
echo.
echo    2. Avvia il sistema:
echo       ^> start.bat
echo.
echo    3. Il primo avvio reinstallerà tutto automaticamente
echo.
echo 📖 Guide di riferimento:
echo    • QUICK_START_WINDOWS.md - Guida rapida
echo    • WINDOWS_SETUP.md       - Setup completo
echo    • README.md              - Documentazione generale
echo.
echo ========================================
echo.
pause

exit /b 0
