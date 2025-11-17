#!/bin/bash

# Script per avviare l'API FastAPI

echo "========================================"
echo "Subito.it Scraper API - Avvio"
echo "========================================"

# Verifica se Redis è in esecuzione
echo "Verifico Redis..."
if ! redis-cli ping > /dev/null 2>&1; then
    echo "⚠️  Redis non in esecuzione!"
    echo "Avvio Redis con Docker Compose..."
    docker-compose up -d redis
    sleep 2
fi

# Verifica di nuovo
if redis-cli ping > /dev/null 2>&1; then
    echo "✓ Redis connesso"
else
    echo "⚠️  Redis non disponibile. L'API funzionerà senza cache."
fi

# Crea directory necessarie
mkdir -p data output logs

# Carica variabili d'ambiente se .env esiste
if [ -f .env ]; then
    echo "✓ Carico variabili da .env"
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️  File .env non trovato, uso valori di default"
fi

# Avvia l'API
echo ""
echo "Avvio API su http://localhost:8000"
echo "Documentazione: http://localhost:8000/docs"
echo ""
echo "Premi Ctrl+C per fermare il server"
echo "========================================"
echo ""

# Avvia con uvicorn
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
