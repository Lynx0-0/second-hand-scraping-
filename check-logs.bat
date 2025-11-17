@echo off
echo.
echo ========================================
echo Controllo Logs Sistema
echo ========================================
echo.

if not exist logs (
    echo ATTENZIONE: Directory logs non trovata!
    echo Il sistema non e' stato ancora avviato.
    echo.
    echo Directory logs non trovata!
    echo Il sistema non e stato ancora avviato.
    pause
    exit /b 1
)

echo Ultimi 30 righe BACKEND LOG:
echo ----------------------------------------
if exist logs\backend.log (
    powershell -Command "Get-Content logs\backend.log -Tail 30"
echo.
echo ======== BACKEND LOG ========
echo.
if exist logs\backend.log (
    type logs\backend.log
) else (
    echo File backend.log non trovato
)

echo.
echo.
echo Ultimi 30 righe FRONTEND LOG:
echo ----------------------------------------
if exist logs\frontend.log (
    powershell -Command "Get-Content logs\frontend.log -Tail 30"
echo ======== FRONTEND LOG ========
echo.
if exist logs\frontend.log (
    type logs\frontend.log
) else (
    echo File frontend.log non trovato
)

echo.
echo ========================================
echo.
echo Per vedere file completi:
echo   - logs\backend.log
echo   - logs\frontend.log
echo.
pause
