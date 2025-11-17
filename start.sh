#!/bin/bash

# Script per avviare l'intero sistema (Backend + Frontend)

set -e  # Exit on error

echo "========================================"
echo "🚀 Avvio Sistema Completo"
echo "========================================"
echo ""

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directory root del progetto
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Funzione per stampare messaggi colorati
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# 1. Verifica dipendenze Python
echo "1️⃣  Verifico dipendenze Python..."
if ! command -v python3 &> /dev/null; then
    print_error "Python3 non trovato. Installalo prima di continuare."
    exit 1
fi
print_success "Python3 installato"

# 2. Verifica Node.js
echo ""
echo "2️⃣  Verifico Node.js..."
if ! command -v node &> /dev/null; then
    print_error "Node.js non trovato. Installalo prima di continuare."
    exit 1
fi
print_success "Node.js installato ($(node --version))"

# 3. Installa dipendenze Python se necessario
echo ""
echo "3️⃣  Verifico dipendenze Python..."
if [ ! -d "venv" ]; then
    print_info "Creo virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate || . venv/Scripts/activate  # Windows compatibility

print_info "Installo/aggiorno dipendenze Python..."
pip install -q -r requirements.txt
print_success "Dipendenze Python installate"

# 4. Installa dipendenze Frontend
echo ""
echo "4️⃣  Verifico dipendenze Frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    print_info "Installo dipendenze Node.js (potrebbe richiedere qualche minuto)..."
    npm install --silent
    print_success "Dipendenze Frontend installate"
else
    print_success "Dipendenze Frontend già installate"
fi

cd ..

# 5. Verifica/Avvia Redis
echo ""
echo "5️⃣  Verifico Redis..."
if command -v redis-cli &> /dev/null; then
    if redis-cli ping &> /dev/null; then
        print_success "Redis già in esecuzione"
    else
        print_info "Avvio Redis con Docker Compose..."
        docker-compose up -d redis 2>/dev/null || print_error "Docker non disponibile, Redis verrà eseguito localmente se possibile"
    fi
else
    print_info "Redis CLI non trovato. L'API funzionerà senza cache."
fi

# 6. Crea directory necessarie
echo ""
echo "6️⃣  Creo directory necessarie..."
mkdir -p data output logs
print_success "Directory create"

# 7. Configura variabili d'ambiente
echo ""
echo "7️⃣  Verifico configurazione..."
if [ ! -f ".env" ]; then
    print_info "Copio .env.example in .env"
    cp .env.example .env
fi
print_success "Configurazione verificata"

# 8. Avvia Backend API
echo ""
echo "8️⃣  Avvio Backend API..."
echo ""
print_info "Backend sarà disponibile su: http://localhost:8000"
print_info "Docs interattive: http://localhost:8000/docs"

# Avvia in background e salva PID
nohup python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 > logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > .backend.pid

# Attendi che il backend sia pronto
print_info "Attendo che il backend sia pronto..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        print_success "Backend avviato correttamente!"
        break
    fi
    sleep 1
done

# 9. Avvia Frontend
echo ""
echo "9️⃣  Avvio Frontend React..."
echo ""
print_info "Frontend sarà disponibile su: http://localhost:5173"

cd frontend

# Avvia in background
nohup npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../.frontend.pid

cd ..

# Attendi che il frontend sia pronto
print_info "Attendo che il frontend sia pronto..."
sleep 5

# 10. Riepilogo
echo ""
echo "========================================"
echo "✅ Sistema Avviato con Successo!"
echo "========================================"
echo ""
echo "📍 LINK UTILI:"
echo "   • Frontend:     http://localhost:5173"
echo "   • Backend API:  http://localhost:8000"
echo "   • API Docs:     http://localhost:8000/docs"
echo ""
echo "📁 LOG FILES:"
echo "   • Backend:  logs/backend.log"
echo "   • Frontend: logs/frontend.log"
echo ""
echo "🛑 PER FERMARE:"
echo "   ./stop.sh"
echo ""
echo "💡 SUGGERIMENTI:"
echo "   1. Apri http://localhost:5173 nel browser"
echo "   2. Prova a cercare: 'iPhone 13', 'MacBook', 'Bicicletta'"
echo "   3. Usa i filtri per raffinare la ricerca"
echo "   4. Clicca sul badge rosso per info sulle truffe"
echo ""
echo "========================================"

# Apri automaticamente il browser (opzionale)
if command -v xdg-open &> /dev/null; then
    sleep 2
    xdg-open http://localhost:5173 &> /dev/null &
elif command -v open &> /dev/null; then
    sleep 2
    open http://localhost:5173 &> /dev/null &
fi
