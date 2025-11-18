@echo off
REM Script per avviare l'API FastAPI su Windows

echo ========================================
echo Subito.it Scraper API - Avvio
echo ========================================

REM Crea directory necessarie
if not exist "data" mkdir data
if not exist "output" mkdir output
if not exist "logs" mkdir logs

echo.
echo Avvio API su http://localhost:8000
echo Documentazione: http://localhost:8000/docs
echo.
echo Premi Ctrl+C per fermare il server
echo ========================================
echo.

REM Avvia con uvicorn (assicurati che Python e uvicorn siano installati)
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

pause
