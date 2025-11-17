# 🪟 Guida Completa Windows 10

Guida step-by-step per installare e usare il sistema su Windows 10.

## 📋 Requisiti Windows

### Software Necessario

1. **Python 3.9+**
   - Download: https://www.python.org/downloads/
   - ⚠️ **IMPORTANTE**: Durante installazione, spunta "Add Python to PATH"

2. **Node.js 18+**
   - Download: https://nodejs.org/
   - Scarica versione LTS (Long Term Support)

3. **Git** (opzionale, per clonare repository)
   - Download: https://git-scm.com/download/win

4. **Redis** (opzionale, per cache)
   - Download: https://github.com/microsoftarchive/redis/releases
   - Oppure usa Docker Desktop per Windows

### Verifica Installazione

Apri **Prompt dei Comandi** (cmd) o **PowerShell** e verifica:

```cmd
python --version
node --version
npm --version
```

Se vedi i numeri di versione, sei pronto!

---

## 🚀 Installazione Rapida

### Metodo 1: Download ZIP (Più Semplice)

1. **Scarica il progetto** come ZIP
2. **Estrai** in una cartella (es. `C:\Progetti\subito-scraper`)
3. **Apri Prompt dei Comandi** in quella cartella:
   - Shift + Click destro nella cartella
   - "Apri finestra PowerShell qui" o "Apri Prompt dei comandi qui"

4. **Avvia il sistema:**
   ```cmd
   start.bat
   ```

### Metodo 2: Con Git

```cmd
cd C:\Progetti
git clone [URL-repository]
cd second-hand-scraping-
start.bat
```

---

## 💻 Avvio Sistema

### Prima Volta (Installazione Completa)

```cmd
start.bat
```

Questo script:
- ✅ Verifica Python e Node.js
- ✅ Crea virtual environment Python
- ✅ Installa tutte le dipendenze (può richiedere 2-5 minuti)
- ✅ Avvia backend e frontend
- ✅ Apre automaticamente il browser

**Tempo stimato:** 3-5 minuti la prima volta

### Avvii Successivi

```cmd
start.bat
```

**Tempo stimato:** 10-15 secondi

Il sistema ricorda le dipendenze installate!

---

## 🌐 Usare l'Interfaccia Grafica

Dopo `start.bat`, il browser si apre automaticamente su:
**http://localhost:5173**

### Cosa Vedrai:

```
╔════════════════════════════════════════════╗
║  🔍 Subito Scraper                         ║
║  ────────────────────────────────────      ║
║                                            ║
║  [Cerca iPhone 13_____] [🔍] [⚙️]          ║
║                                            ║
╠════════════════════════════════════════════╣
║                                            ║
║  📦 Card 1    📦 Card 2    📦 Card 3      ║
║  🔴 TRUFFA                 🟡 SOSPETTO    ║
║  iPhone 13    iPhone 13    iPhone 13      ║
║  €150 ❌      €450 ✓       €380           ║
║                                            ║
╚════════════════════════════════════════════╝
```

### Come Cercare:

1. **Inserisci query** (es. "iPhone 13")
2. **Clicca filtri** ⚙️ (opzionale):
   - Categoria
   - Prezzo massimo
   - Regione
3. **Clicca Cerca** 🔍
4. **Vedi risultati** con foto e prezzi
5. **Clicca badge rosso** 🔴 per info truffe
6. **Clicca link** per aprire su Subito.it

---

## 🛑 Fermare il Sistema

### Opzione 1: Script
```cmd
stop.bat
```

### Opzione 2: Manuale
Chiudi le finestre del Prompt dei Comandi

### Opzione 3: Task Manager
1. Ctrl + Shift + Esc
2. Cerca processi "python.exe" e "node.exe"
3. Termina processi

---

## 🐛 Risoluzione Problemi Windows

### ❌ "Python non è riconosciuto"

**Problema:** Python non è nel PATH

**Soluzione:**
1. Disinstalla Python
2. Reinstalla spuntando "Add Python to PATH"
3. Riavvia Prompt dei Comandi

**Verifica:**
```cmd
python --version
```

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

### ❌ "Porta 8000 già in uso"

**Problema:** Un altro programma usa la porta

**Soluzione 1 - Trova e chiudi:**
```cmd
netstat -ano | findstr :8000
taskkill /F /PID [numero_PID]
```

**Soluzione 2 - Cambia porta:**
Modifica `.env`:
```
PORT=8001
```

E in `frontend\.env`:
```
VITE_API_URL=http://localhost:8001
```

### ❌ "npm install" fallisce

**Problema:** Permessi o rete

**Soluzioni:**
```cmd
REM Pulisci cache npm
npm cache clean --force

REM Prova con amministratore
REM Click destro sul Prompt → "Esegui come amministratore"
cd frontend
npm install

REM Oppure usa yarn (alternativa a npm)
npm install -g yarn
yarn install
```

### ❌ Errore "pydantic-core" - Rust non trovato (Python 3.13)

**Problema:** `error: metadata-generation-failed` per `pydantic-core` con Python 3.13

**Causa:** Python 3.13 è molto recente e alcuni pacchetti non hanno wheel pre-compilati per Windows.

**✅ Soluzione 1 - Aggiorna requirements.txt (CONSIGLIATO):**

Ho già aggiornato il file `requirements.txt` con versioni compatibili. Riprova:

```cmd
# Se eri nel mezzo dell'installazione, riparti da capo
stop.bat

# Elimina virtual environment
rmdir /s /q venv

# Riavvia (userà il nuovo requirements.txt)
start.bat
```

**Soluzione 2 - Usa Python 3.11 o 3.12:**

Se il problema persiste:

1. Disinstalla Python 3.13
2. Scarica **Python 3.11** o **3.12** da https://www.python.org/downloads/
3. Installa con "Add Python to PATH"
4. Riavvia e prova `start.bat`

**Soluzione 3 - Installa Microsoft C++ Build Tools:**

Se preferisci continuare con Python 3.13:

1. Scarica da: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Installa "Desktop development with C++"
3. Riavvia PC
4. Riprova `start.bat`

**Verifica versione Python:**
```cmd
python --version
```

Consigliato: **Python 3.11.x** o **3.12.x** per massima compatibilità Windows.

### ❌ "ModuleNotFoundError" Python

**Problema:** Dipendenze Python non installate

**Soluzione:**
```cmd
REM Attiva virtual environment
venv\Scripts\activate

REM Reinstalla dipendenze
pip install -r requirements.txt

REM Verifica
pip list
```

### ❌ Firewall blocca connessioni

**Problema:** Windows Defender blocca

**Soluzione:**
1. Quando appare popup Windows Defender
2. Clicca "Consenti accesso"
3. Oppure:
   - Pannello di controllo → Windows Defender Firewall
   - Consenti app → Aggiungi Python e Node.js

### ❌ "CORS Error" nel browser

**Problema:** Backend non raggiungibile da frontend

**Soluzione:**
Verifica `.env`:
```
CORS_ORIGINS=["http://localhost:5173"]
```

### ❌ Browser non si apre automaticamente

**Soluzione manuale:**
Apri manualmente: http://localhost:5173

---

## 📂 Percorsi Windows

### Directory Progetto
```
C:\Users\[TuoNome]\Documents\subito-scraper\
│
├── start.bat              ← Doppio click qui per avviare
├── stop.bat               ← Doppio click qui per fermare
│
├── venv\                  ← Virtual environment Python
│   └── Scripts\
│       └── activate.bat
│
├── frontend\
│   └── node_modules\      ← Dipendenze Node.js
│
├── logs\
│   ├── backend.log        ← Log API
│   └── frontend.log       ← Log React
│
└── data\                  ← Database segnalazioni
```

### File Configurazione

**Backend:** `.env`
```env
HOST=0.0.0.0
PORT=8000
REDIS_HOST=localhost
```

**Frontend:** `frontend\.env`
```env
VITE_API_URL=http://localhost:8000
```

---

## 🎯 Comandi Utili Windows

### Virtual Environment Python

```cmd
REM Attiva
venv\Scripts\activate

REM Disattiva
deactivate

REM Verifica attivazione (vedi "(venv)" nel prompt)
```

### Gestione Processi

```cmd
REM Vedi processi Python
tasklist | findstr python

REM Vedi processi Node
tasklist | findstr node

REM Termina processo
taskkill /F /PID [numero]

REM Vedi porte in uso
netstat -ano | findstr LISTENING
```

### Dipendenze

```cmd
REM Python
pip list
pip install [pacchetto]
pip uninstall [pacchetto]

REM Node.js
npm list
npm install [pacchetto]
npm uninstall [pacchetto]
```

### Log

```cmd
REM Leggi log backend
type logs\backend.log

REM Leggi log frontend
type logs\frontend.log

REM Monitora log in tempo reale (PowerShell)
Get-Content logs\backend.log -Wait
```

---

## 🔧 Configurazione Redis su Windows

### Opzione 1: Redis Nativo Windows

1. Download: https://github.com/microsoftarchive/redis/releases
2. Scarica `Redis-x64-[versione].msi`
3. Installa
4. Redis si avvia automaticamente come servizio

**Verifica:**
```cmd
redis-cli ping
```
Dovresti vedere: `PONG`

### Opzione 2: Docker Desktop

1. Installa Docker Desktop: https://www.docker.com/products/docker-desktop/
2. Avvia Docker Desktop
3. Nel progetto:
   ```cmd
   docker-compose up -d redis
   ```

### Opzione 3: Nessun Redis

Il sistema funziona anche senza Redis:
- ✅ Tutte le funzionalità attive
- ❌ Nessuna cache (ricerche più lente)
- ℹ️ Perfetto per test/sviluppo

---

## 📝 Script Personalizzati Windows

### Creare Collegamento Desktop

1. Click destro su `start.bat`
2. "Crea collegamento"
3. Trascina su Desktop
4. Rinomina "Avvia Subito Scraper"

**Ora doppio click dal desktop avvia tutto!**

### Avvio Automatico con Windows

1. Win + R
2. Digita: `shell:startup`
3. Copia collegamento `start.bat` in quella cartella

**Il sistema si avvia con Windows!**

---

## 💡 Tips Windows

### Performance

- **Antivirus:** Aggiungi cartella progetto alle esclusioni
- **Windows Defender:** Consenti Python e Node.js
- **Disco:** Usa SSD per dipendenze Node.js (più veloce)

### Editor Consigliati

- **VS Code:** https://code.visualstudio.com/
- **Notepad++:** https://notepad-plus-plus.org/
- **PyCharm Community:** https://www.jetbrains.com/pycharm/

### Terminal Migliori

- **Windows Terminal:** https://aka.ms/terminal (Microsoft Store)
- **PowerShell 7:** https://github.com/PowerShell/PowerShell
- **Git Bash:** Incluso con Git per Windows

---

## ✅ Checklist Pre-Avvio

Prima di `start.bat`, verifica:

- [ ] Python installato e nel PATH
- [ ] Node.js installato
- [ ] Connessione internet attiva
- [ ] Firewall non blocca porte 8000 e 5173
- [ ] Almeno 2GB spazio disco libero
- [ ] Antivirus non blocca Python/Node
- [ ] Prompt dei Comandi aperto nella directory progetto

---

## 🆘 Supporto

### Log Debugging

Se qualcosa non funziona:

1. Apri `logs\backend.log`
2. Apri `logs\frontend.log`
3. Cerca errori (righe con "ERROR" o "Exception")
4. Copia l'errore per cercare soluzione

### Browser Console

Nel browser (F12):
- Tab "Console" per errori JavaScript
- Tab "Network" per errori API

---

## 🎉 Quick Start Windows

```cmd
REM 1. Apri Prompt dei Comandi nella cartella progetto
cd C:\path\to\second-hand-scraping-

REM 2. Avvia tutto
start.bat

REM 3. Aspetta messaggio "Sistema Avviato"

REM 4. Browser si apre automaticamente

REM 5. Cerca "iPhone 13" e vedi risultati!

REM 6. Per fermare:
stop.bat
```

**È tutto pronto per Windows 10!** 🪟✨
