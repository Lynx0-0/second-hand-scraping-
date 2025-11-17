#!/bin/bash

# Script per fermare l'intero sistema

echo "🛑 Fermando il sistema..."

# Colori
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

# Ferma Backend
if [ -f ".backend.pid" ]; then
    BACKEND_PID=$(cat .backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID
        print_success "Backend fermato (PID: $BACKEND_PID)"
    fi
    rm .backend.pid
fi

# Ferma Frontend
if [ -f ".frontend.pid" ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID
        print_success "Frontend fermato (PID: $FRONTEND_PID)"
    fi
    rm .frontend.pid
fi

# Ferma eventuali processi rimasti
pkill -f "uvicorn api.main:app" 2>/dev/null
pkill -f "vite" 2>/dev/null

print_success "Sistema fermato"
echo ""
echo "Per riavviare: ./start.sh"
