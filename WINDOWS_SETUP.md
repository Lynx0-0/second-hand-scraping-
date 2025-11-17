# 🪟 Setup Completo Windows 10/11

Guida dettagliata per installare e configurare il sistema su Windows.

---

## 📋 Indice

1. [Requisiti Sistema](#-requisiti-sistema)
2. [Installazione Python](#-installazione-python)
3. [Installazione Node.js](#-installazione-nodejs)
4. [Setup Progetto](#-setup-progetto)
5. [Script Automatici](#-script-automatici)
6. [Troubleshooting](#-troubleshooting)
7. [Redis (Opzionale)](#-redis-opzionale)
8. [Configurazione Avanzata](#-configurazione-avanzata)

---

## 💻 Requisiti Sistema

### Minimo

- **OS**: Windows 10 (64-bit) o Windows 11
- **RAM**: 4 GB
- **Disco**: 2 GB spazio libero
- **Internet**: Connessione attiva (per installazione)

### Consigliato

- **OS**: Windows 11 o Windows 10 (build 19041+)
- **RAM**: 8 GB o più
- **Disco**: 5 GB spazio libero (SSD consigliato)
- **CPU**: Dual core o superiore

---

## 🐍 Installazione Python

### Versione Consigliata

**Python 3.11.x** o **Python 3.12.x**

⚠️ **Evita Python 3.13** su Windows (alcuni pacchetti potrebbero richiedere compilazione)

### Procedura Installazione

1. **Scarica Python**
   - Vai su: https://www.python.org/downloads/
   - Click su "Download Python 3.11.x" (o 3.12.x)
   - Scarica installer Windows (64-bit)

2. **Esegui Installer**
   - Doppio click sul file `.exe`
   - ✅ **IMPORTANTE**: Spunta **"Add Python to PATH"**
   - Click "Install Now"
   - Attendi completamento

3. **Verifica Installazione**

   Apri **Prompt dei Comandi** (cmd):
   ```cmd
   python --version
   ```

   Output atteso:
   ```
   Python 3.11.x (o 3.12.x)
   ```

   Verifica anche pip:
   ```cmd
   pip --version
   ```

### Problemi Comuni

**"Python non riconosciuto"**
- Reinstalla Python
- Assicurati di spuntare "Add Python to PATH"
- Riavvia Prompt dei Comandi
- Riavvia computer (se necessario)

**Python nel PATH manualmente** (se dimenticato durante installazione):
1. Cerca "Variabili d'ambiente" in Windows
2. Click "Variabili d'ambiente"
3. In "Variabili di sistema" trova `Path`
4. Click "Modifica"
5. Aggiungi:
   - `C:\Users\TUO_UTENTE\AppData\Local\Programs\Python\Python311`
   - `C:\Users\TUO_UTENTE\AppData\Local\Programs\Python\Python311\Scripts`

---

## 📦 Installazione Node.js

### Versione Consigliata

**Node.js 18.x LTS** o **Node.js 20.x LTS**

### Procedura Installazione

1. **Scarica Node.js**
   - Vai su: https://nodejs.org/
   - Click su versione **LTS** (Long Term Support)
   - Scarica installer Windows (64-bit .msi)

2. **Esegui Installer**
   - Doppio click sul file `.msi`
   - Click "Next" con impostazioni predefinite
   - Attendi completamento
   - Riavvia Prompt dei Comandi

3. **Verifica Installazione**

   ```cmd
   node --version
   npm --version
   ```

   Output atteso:
   ```
   v18.x.x (o v20.x.x)
   9.x.x (o 10.x.x)
   ```

### Problemi Comuni

**"Node non riconosciuto"**
- Chiudi e riapri Prompt dei Comandi
- Riavvia computer
- Reinstalla Node.js

**npm lento su Windows**
- Normale, Windows Defender può rallentare npm
- Aggiungi eccezione antivirus per `node_modules`

---

## 🚀 Setup Progetto

### 1. Clona/Scarica Progetto

**Opzione A: Con Git**
```cmd
cd C:\Users\TUO_UTENTE\Desktop
git clone <repository-url>
cd second-hand-scraping-
```

**Opzione B: Download ZIP**
1. Scarica ZIP dal repository
2. Estrai in una cartella (es: `C:\Projects\second-hand-scraping-`)
3. Apri Prompt dei Comandi nella cartella

### 2. Avvio Automatico

```cmd
start.bat
```

Lo script farà automaticamente:
- ✅ Crea virtual environment
- ✅ Installa dipendenze Python
- ✅ Installa dipendenze frontend
- ✅ Avvia Backend e Frontend
- ✅ Apre browser

**Prima esecuzione**: 2-5 minuti (installa tutto)
**Successive**: 10-15 secondi

---

## 🛠️ Script Automatici

### start.bat - Avvio Sistema

**Uso:**
```cmd
start.bat
```

**Cosa fa:**
1. Verifica Python e Node.js installati
2. Controlla versione Python (avvisa se 3.13)
3. Crea/attiva virtual environment
4. Installa dipendenze Python da `requirements.txt`
5. Installa dipendenze frontend (npm)
6. Libera porte 8000 e 5173 se occupate
7. Avvia Backend su porta 8000
8. Avvia Frontend su porta 5173
9. Apre browser su http://localhost:5173

**Output:**
- Logs salvati in `logs\backend.log` e `logs\frontend.log`
- Processi in background con titoli:
  - `Backend-FastAPI`
  - `Frontend-React-Vite`

**Errori gestiti:**
- Python/Node.js mancanti → Mostra guida installazione
- Python 3.13 → Avviso compatibilità
- Dipendenze falliscono → Soluzioni dettagliate
- Porte occupate → Libera automaticamente

### stop.bat - Arresto Sistema

**Uso:**
```cmd
stop.bat
```

**Cosa fa:**
1. Termina processi Backend (Python/uvicorn)
2. Termina processi Frontend (Node.js/Vite)
3. Libera porta 8000 (Backend)
4. Libera porta 5173 (Frontend)
5. Verifica arresto corretto
6. *Opzionale*: Pulisce cache e logs

**Cleanup opzionale:**
- Rimuove `__pycache__`
- Rimuove file `.pyc`
- Pulisce logs

### reset.bat - Reset Completo

**Uso:**
```cmd
reset.bat
```

**⚠️ ATTENZIONE**: Questo script è "distruttivo" (cancella virtual environment e cache)

**Cosa fa:**
1. Arresta tutti i servizi (chiama `stop.bat`)
2. **Rimuove** virtual environment (`venv`)
3. **Pulisce** cache Python (`__pycache__`, `*.pyc`)
4. *Opzionale*: Rimuove `node_modules`
5. *Opzionale*: Pulisce `output` e `data`
6. Pulisce logs

**Quando usarlo:**
- Errori di installazione dipendenze
- Problemi con virtual environment corrotto
- Dopo upgrade Python
- "ModuleNotFoundError" persistenti
- Ripartire da zero

**Dopo il reset:**
```cmd
start.bat
```
Il sistema si reinstallerà automaticamente.

---

## 🐛 Troubleshooting

### ❌ "Python non trovato"

**Errore:**
```
✗ Python non trovato
```

**Soluzioni:**
1. Verifica installazione:
   ```cmd
   python --version
   ```

2. Se non funziona:
   - Reinstalla Python
   - Spunta "Add Python to PATH"
   - Riavvia Prompt

3. Verifica PATH:
   ```cmd
   echo %PATH%
   ```
   Deve contenere cartelle Python

### ❌ "Node non è riconosciuto"

**Problema:** Node.js non è nel PATH

**Soluzione:**
1. Reinstalla Node.js
2. Usa installer Windows (.msi)
3. Riavvia Prompt dei Comandi

**Verifica:**
```cmd
node --version
```

### ❌ Errore "pydantic-core" - Rust non trovato (Python 3.13)

**Problema:** `error: metadata-generation-failed` per `pydantic-core` con Python 3.13

**Causa:** Python 3.13 è molto recente e alcuni pacchetti non hanno wheel pre-compilati per Windows.

**✅ Soluzione 1 - Usa reset.bat (CONSIGLIATO):**

```cmd
REM Reset sistema
reset.bat

REM Riavvia (userà requirements.txt aggiornato)
start.bat
```

Ho aggiornato `requirements.txt` con versioni compatibili con Python 3.13.

**Soluzione 2 - Usa Python 3.11 o 3.12 (PIÙ STABILE):**

1. Disinstalla Python 3.13
   - Pannello di Controllo → Programmi → Python 3.13 → Disinstalla

2. Scarica **Python 3.11** o **3.12**
   - https://www.python.org/downloads/
   - Scarica installer 3.11.x o 3.12.x

3. Installa con "Add Python to PATH"

4. Verifica:
   ```cmd
   python --version
   ```

5. Reset e riavvia:
   ```cmd
   reset.bat
   start.bat
   ```

**Soluzione 3 - Installa Microsoft C++ Build Tools:**

Se preferisci continuare con Python 3.13:

1. Scarica da: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Installa "Desktop development with C++"
3. Riavvia PC
4. Riprova `start.bat`

**Versioni Python consigliate:**
- ✅ Python 3.11.x (LTS, massima compatibilità)
- ✅ Python 3.12.x (stabile, consigliato)
- ⚠️ Python 3.13.x (richiede pacchetti più recenti, possibili problemi)

### ❌ "ModuleNotFoundError" Python

**Problema:** Dipendenze Python non installate

**Soluzione:**
```cmd
REM Attiva venv
call venv\Scripts\activate.bat

REM Reinstalla dipendenze
pip install -r requirements.txt

REM Se fallisce, reset completo
reset.bat
start.bat
```

### ❌ "Porta 8000 già in uso"

**Problema:** Un altro programma usa la porta

**Soluzione 1 - Usa stop.bat:**
```cmd
stop.bat
start.bat
```

**Soluzione 2 - Trova e chiudi manualmente:**
```cmd
REM Trova processo su porta 8000
netstat -ano | findstr :8000

REM Termina processo (sostituisci 1234 con PID trovato)
taskkill /F /PID 1234
```

**Soluzione 3 - Cambia porta:**

Modifica `.env`:
```env
PORT=8001
```

E in `frontend\.env`:
```env
VITE_API_URL=http://localhost:8001
```

### ❌ "npm install" fallisce

**Problema:** Permessi o rete

**Soluzioni:**
```cmd
REM 1. Pulisci cache npm
npm cache clean --force

REM 2. Riprova installazione
cd frontend
npm install
cd ..

REM 3. Se fallisce ancora, usa amministratore
REM Click destro su Prompt → "Esegui come amministratore"
cd frontend
npm install
cd ..

REM 4. Alternativa: usa yarn
npm install -g yarn
cd frontend
yarn install
cd ..
```

**Windows Defender rallenta npm:**
- Aggiungi eccezione per `node_modules`
- Temporaneamente disabilita protezione in tempo reale
- Usa npm con `--prefer-offline`

### ❌ Pagina bianca / Frontend non carica

**Problema:** Errori JavaScript o build

**Soluzione:**
```cmd
REM 1. Ferma sistema
stop.bat

REM 2. Pulisci frontend
cd frontend
rd /s /q node_modules
rd /s /q dist
npm cache clean --force
cd ..

REM 3. Riavvia
start.bat
```

### ❌ Browser non si apre automaticamente

**Problema:** Windows blocca apertura automatica

**Soluzione:**

Apri manualmente: http://localhost:5173

**Se pagina non carica:**
1. Attendi 15-20 secondi
2. Aggiorna (F5)
3. Controlla logs:
   ```cmd
   type logs\backend.log
   type logs\frontend.log
   ```

### ❌ Errore CORS / API non risponde

**Problema:** Frontend non riesce a comunicare con Backend

**Verifica:**
1. Backend attivo:
   ```cmd
   curl http://localhost:8000/health
   ```

2. Frontend configurato correttamente:
   - File `frontend\.env` deve contenere:
     ```env
     VITE_API_URL=http://localhost:8000
     ```

3. CORS abilitato nel Backend (già configurato in `api\main.py`)

**Soluzione:**
```cmd
REM Riavvia sistema
stop.bat
start.bat
```

### ❌ Antivirus blocca Python/Node

**Problema:** Windows Defender o altri antivirus bloccano esecuzione

**Soluzione:**

1. **Aggiungi eccezione** per cartelle:
   - `C:\Users\TUO_UTENTE\AppData\Local\Programs\Python`
   - Cartella progetto: `C:\...\second-hand-scraping-`
   - `node_modules`

2. **Windows Defender:**
   - Impostazioni → Virus e minacce
   - Protezione da virus e minacce → Impostazioni
   - Esclusioni → Aggiungi esclusione
   - Aggiungi cartelle sopra

### ❌ "Access Denied" / Permessi

**Problema:** Permessi insufficienti

**Soluzione:**

1. **Esegui come Amministratore:**
   - Click destro su `cmd.exe`
   - "Esegui come amministratore"
   - Naviga nella cartella progetto
   - Esegui `start.bat`

2. **Cambia permessi cartella:**
   - Click destro su cartella progetto
   - Proprietà → Sicurezza
   - Modifica permessi

---

## 🔴 Redis (Opzionale)

Redis è **opzionale**. Il sistema funziona anche senza.

### Windows Redis

**Opzione 1 - Docker Desktop (Consigliato)**

1. Installa Docker Desktop per Windows
2. Avvia:
   ```cmd
   docker run -d -p 6379:6379 redis:alpine
   ```

**Opzione 2 - WSL2 + Ubuntu**

1. Installa WSL2
2. Installa Ubuntu dal Microsoft Store
3. In Ubuntu:
   ```bash
   sudo apt update
   sudo apt install redis-server
   sudo service redis-server start
   ```

**Opzione 3 - Redis non ufficiale Windows**

1. Scarica da: https://github.com/microsoftarchive/redis/releases
2. Estrai e avvia `redis-server.exe`

### Configurazione Redis

Se Redis installato, modifica `.env`:
```env
REDIS_ENABLED=true
REDIS_HOST=localhost
REDIS_PORT=6379
```

Se Redis **non** installato (default):
```env
REDIS_ENABLED=false
```

Il sistema rileva automaticamente se Redis è disponibile.

---

## ⚙️ Configurazione Avanzata

### File .env (Backend)

Crea `.env` nella root del progetto:

```env
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Redis Cache (opzionale)
REDIS_ENABLED=false
REDIS_HOST=localhost
REDIS_PORT=6379
CACHE_TTL_SEARCH=3600
CACHE_TTL_LISTING=7200

# Rate Limiting
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_PERIOD=60

# CORS
CORS_ORIGINS=["http://localhost:5173"]

# Logging
LOG_LEVEL=INFO
```

### File frontend\.env (Frontend)

Crea `frontend\.env`:

```env
VITE_API_URL=http://localhost:8000
```

### Variabili Ambiente Sistema

**Opzionale** - Per configurazioni globali:

1. Cerca "Variabili d'ambiente" in Windows
2. Click "Variabili d'ambiente"
3. Aggiungi variabili:
   - `REDIS_HOST=localhost`
   - `REDIS_PORT=6379`

---

## 📊 Struttura Directory

Dopo setup completo:

```
second-hand-scraping-/
├── venv/                     # Virtual environment Python
├── frontend/
│   ├── node_modules/         # Dipendenze npm
│   ├── src/                  # Codice frontend
│   ├── dist/                 # Build produzione
│   └── .env                  # Config frontend
├── api/                      # Backend FastAPI
├── src/                      # Core scraping
├── logs/                     # Log files
│   ├── backend.log
│   └── frontend.log
├── output/                   # Output scraping
├── data/                     # Database segnalazioni
├── requirements.txt          # Dipendenze Python
├── .env                      # Config backend
├── start.bat                 # 🚀 Avvio sistema
├── stop.bat                  # 🛑 Stop sistema
└── reset.bat                 # 🔄 Reset completo
```

---

## 🔍 Verifica Setup

### Checklist Completa

Dopo setup, verifica:

1. **Python:**
   ```cmd
   python --version
   where python
   ```
   ✅ Deve mostrare Python 3.11 o 3.12

2. **Node.js:**
   ```cmd
   node --version
   npm --version
   ```
   ✅ Deve mostrare v18.x o v20.x

3. **Virtual Environment:**
   ```cmd
   dir venv
   ```
   ✅ Directory `venv` deve esistere

4. **Dipendenze Python:**
   ```cmd
   call venv\Scripts\activate.bat
   pip list
   ```
   ✅ Deve mostrare fastapi, uvicorn, beautifulsoup4, etc.

5. **Dipendenze Frontend:**
   ```cmd
   dir frontend\node_modules
   ```
   ✅ Directory `node_modules` deve esistere

6. **Porte libere:**
   ```cmd
   netstat -ano | findstr :8000
   netstat -ano | findstr :5173
   ```
   ✅ Nessun output (porte libere)

7. **Backend:**
   ```cmd
   curl http://localhost:8000/health
   ```
   ✅ Dopo `start.bat`, deve rispondere `{"status":"healthy"}`

8. **Frontend:**
   Apri http://localhost:5173
   ✅ Deve mostrare interfaccia

---

## 💡 Best Practices Windows

### Performance

1. **SSD consigliato** - Molto più veloce per `node_modules`
2. **Antivirus eccezioni** - Aggiungi cartelle progetto
3. **Windows Defender** - Escludi `node_modules` e `venv`
4. **Disabilita indicizzazione** - Su cartella progetto

### Sicurezza

1. **Non eseguire sempre come Amministratore**
2. **Virtual Environment** - Sempre attivo per Python
3. **`.env` in `.gitignore`** - Non committare secrets
4. **Firewall** - Potrebbe chiedere permessi per Python/Node

### Manutenzione

1. **Aggiorna dipendenze periodicamente:**
   ```cmd
   pip install --upgrade -r requirements.txt
   cd frontend
   npm update
   cd ..
   ```

2. **Pulisci cache regolarmente:**
   ```cmd
   npm cache clean --force
   pip cache purge
   ```

3. **Logs sotto controllo:**
   - Svuota `logs\` periodicamente
   - Configura rotazione logs

---

## 📖 Risorse Aggiuntive

### Documentazione

- [Python.org](https://www.python.org/) - Documentazione Python
- [Node.js](https://nodejs.org/) - Documentazione Node.js
- [FastAPI](https://fastapi.tiangolo.com/) - Docs FastAPI
- [Vite](https://vitejs.dev/) - Docs Vite
- [React](https://react.dev/) - Docs React

### Tools Utili

- [Visual Studio Code](https://code.visualstudio.com/) - Editor consigliato
- [Windows Terminal](https://aka.ms/terminal) - Terminale moderno
- [Git for Windows](https://git-scm.com/download/win) - Version control
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) - Per Redis

---

## 🆘 Supporto

Se hai ancora problemi dopo aver seguito questa guida:

1. Controlla i logs:
   - `logs\backend.log`
   - `logs\frontend.log`

2. Prova reset completo:
   ```cmd
   reset.bat
   start.bat
   ```

3. Verifica requisiti sistema

4. Consulta issue su GitHub repository

---

**Fatto! Ora sei pronto per usare il sistema su Windows! 🚀**

Prossimo passo: [QUICK_START_WINDOWS.md](QUICK_START_WINDOWS.md)
