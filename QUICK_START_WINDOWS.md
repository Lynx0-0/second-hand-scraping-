# ⚡ Quick Start per Windows 10/11

Guida rapida in 3 passi per Windows.

## 📦 Passo 1: Installa Requisiti

### Python 3.9+

1. Vai su https://www.python.org/downloads/
2. Scarica l'installer Windows
3. **IMPORTANTE:** Spunta ✅ "Add Python to PATH"
4. Clicca "Install Now"

### Node.js 18+

1. Vai su https://nodejs.org/
2. Scarica versione "LTS" (Long Term Support)
3. Esegui installer
4. Accetta tutte le opzioni di default

### Verifica Installazione

Apri **Prompt dei Comandi** (cerca "cmd" nel menu Start):

```cmd
python --version
node --version
```

Se vedi i numeri di versione, sei pronto! ✅

---

## 🚀 Passo 2: Avvia il Sistema

### Metodo Facile (Doppio Click)

1. Vai nella cartella del progetto
2. **Doppio click su `start.bat`**
3. Aspetta 10-15 secondi
4. Il browser si apre automaticamente

### Metodo Command Line

Apri **Prompt dei Comandi** nella cartella progetto:

```cmd
start.bat
```

**Cosa Succede:**
```
========================================
🚀 Avvio Sistema Completo - Windows 10
========================================

1️⃣  Verifico Python...
✓ Python installato: Python 3.11.0

2️⃣  Verifico Node.js...
✓ Node.js installato: v18.17.0

3️⃣  Setup Python virtual environment...
✓ Virtual environment attivato

4️⃣  Installo dipendenze Python...
✓ Dipendenze Python installate

5️⃣  Installo dipendenze Frontend...
✓ Dipendenze Frontend installate

8️⃣  Verifico configurazione...
✓ Configurazione verificata

9️⃣  Avvio Backend API...
✓ Backend avviato correttamente!

🔟  Avvio Frontend React...

========================================
✅ Sistema Avviato con Successo!
========================================

📍 LINK UTILI:
   • Frontend:     http://localhost:5173
   • Backend API:  http://localhost:8000

🛑 PER FERMARE:
   stop.bat

ℹ Apro il browser...
```

---

## 💻 Passo 3: Usa l'Interfaccia

Il browser si apre automaticamente su **http://localhost:5173**

### Prima Ricerca:

1. **Scrivi nella barra:** `iPhone 13`
2. **Clicca:** 🔍 Cerca
3. **Aspetta 2-5 secondi**
4. **Vedi la griglia** con risultati e foto

### Con Filtri:

1. **Clicca:** ⚙️ (icona filtri)
2. **Seleziona:**
   - Categoria: Telefonia
   - Prezzo max: 500
   - Regione: Lazio
3. **Clicca:** 🔍 Cerca
4. **Vedi risultati filtrati**

### Badge Truffe:

Se vedi **🔴 ATTENZIONE TRUFFA (85)** su un annuncio:

1. **Clicca il badge rosso**
2. Si apre **modal** con:
   - Score di rischio (es. 85/100)
   - Motivi specifici (prezzo basso, poche foto, etc.)
   - 5 consigli di sicurezza
   - Form per segnalare
3. **Leggi i consigli** prima di contattare il venditore!

---

## 🛑 Fermare il Sistema

### Metodo 1: Doppio Click

**Doppio click su `stop.bat`**

### Metodo 2: Command Line

```cmd
stop.bat
```

Output:
```
🛑 Fermando il sistema...

Fermando Backend API...
✓ Backend fermato

Fermando Frontend React...
✓ Frontend fermato

✓ Sistema fermato

Per riavviare: start.bat
```

---

## 🐛 Problemi Comuni

### ❌ Python non trovato

**Errore:**
```
✗ Python non trovato
```

**Soluzione:**
1. Reinstalla Python
2. Spunta "Add Python to PATH"
3. Riavvia Prompt dei Comandi

### ❌ Porta 8000 occupata

**Errore:**
```
Error: Port 8000 is already in use
```

**Soluzione:**
```cmd
stop.bat
start.bat
```

Se persiste:
```cmd
REM Trova processo
netstat -ano | findstr :8000

REM Termina processo (sostituisci 1234 con PID trovato)
taskkill /F /PID 1234
```

### ❌ npm install fallisce

**Errore:**
```
npm ERR! network
```

**Soluzione:**
```cmd
cd frontend
npm cache clean --force
npm install
cd ..
```

### ❌ Browser non si apre

**Soluzione:**
Apri manualmente: http://localhost:5173

### ❌ "Access is denied"

**Soluzione:**
Esegui come Amministratore:
1. Click destro su `start.bat`
2. "Esegui come amministratore"

---

## 📂 Cosa Crea lo Script

Dopo il primo avvio, troverai:

```
second-hand-scraping-\
├── venv\                ← Virtual environment Python
├── frontend\
│   └── node_modules\    ← Dipendenze Node.js (2-300 MB)
├── logs\
│   ├── backend.log      ← Log API
│   └── frontend.log     ← Log React
├── data\                ← Database segnalazioni
└── output\              ← Risultati export
```

---

## ⏱️ Tempi di Esecuzione

| Operazione | Prima Volta | Successivi |
|------------|-------------|------------|
| Installazione dipendenze | 3-5 minuti | - |
| Avvio sistema | 15 secondi | 10 secondi |
| Prima ricerca | 2-5 secondi | - |
| Ricerche successive | 1-2 secondi | (con cache) |

---

## 💡 Tips Windows

### Collegamento Desktop

Per avviare con doppio click dal desktop:

1. Click destro su `start.bat`
2. "Invia a" → "Desktop (crea collegamento)"
3. Rinomina "🔍 Avvia Subito Scraper"

### Apri Prompt Comandi Veloce

Nella cartella progetto:
1. **Shift + Click destro** su spazio vuoto
2. "Apri finestra PowerShell qui"
3. Digita `start.bat`

### Verifica Log

Se qualcosa non funziona:

```cmd
REM Vedi log backend
type logs\backend.log

REM Vedi log frontend
type logs\frontend.log
```

---

## ✅ Checklist Prima Volta

- [ ] Python installato (con "Add to PATH")
- [ ] Node.js installato
- [ ] Internet connesso
- [ ] Almeno 2GB spazio disco
- [ ] Windows Defender non blocca Python/Node
- [ ] Doppio click su `start.bat`
- [ ] Aspetto messaggio "Sistema Avviato"
- [ ] Browser aperto su localhost:5173
- [ ] Prima ricerca funzionante

---

## 🎉 Pronto!

**Ora hai:**
- ✅ Interfaccia grafica funzionante
- ✅ Ricerca annunci con foto
- ✅ Rilevamento truffe automatico
- ✅ Badge colorati per sicurezza
- ✅ Link diretti a Subito.it

**Comando completo:**
```cmd
start.bat
```

**Poi cerca:** "iPhone 13", "MacBook", "Bicicletta"

**📖 [Guida completa Windows →](WINDOWS_SETUP.md)**
