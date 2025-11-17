@echo off
echo.
echo ========================================
echo Controllo Logs Sistema
echo ========================================
echo.

if not exist logs (
    echo Directory logs non trovata!
    echo Il sistema non e stato ancora avviato.
    pause
    exit /b 1
)

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
pause
