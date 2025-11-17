# 🚀 Quick Start - Windows 10/11

Guida rapida in 3 passi per Windows.

## 📦 Passo 1: Installa Requisiti

### Python 3.9+

1. Vai su https://www.python.org/downloads/
2. **Scarica Python 3.11 o 3.12** (consigliato per Windows)
   - ⚠️ Python 3.13 potrebbe avere problemi con alcuni pacchetti su Windows
3. **IMPORTANTE:** Spunta ✅ "Add Python to PATH"
4. Clicca "Install Now"

### Node.js 18+

1. Vai su https://nodejs.org/
2. Scarica versione **LTS** (Long Term Support)
3. Installa con impostazioni predefinite
4. Riavvia Prompt dei Comandi

**Verifica installazione:**
```cmd
python --version
node --version
```

---

## 🎯 Passo 2: Avvia il Sistema

### Opzione A: Doppio Click (Più Semplice)

1. Apri la cartella del progetto
2. **Doppio click** su `start.bat`
3. Attendi 10-15 secondi
4. Il browser si aprirà automaticamente

### Opzione B: Da Prompt dei Comandi

```cmd
cd C:\percorso\del\progetto\second-hand-scraping-
start.bat
```

### Cosa fa start.bat?

Lo script automaticamente:
- ✅ Verifica Python e Node.js
- ✅ Crea virtual environment Python
- ✅ Installa dipendenze Python
- ✅ Installa dipendenze frontend (npm)
- ✅ Avvia Backend (porta 8000)
- ✅ Avvia Frontend (porta 5173)
- ✅ Apre browser su http://localhost:5173

**Tempi stimati:**
- Prima esecuzione: 2-5 minuti (installa tutto)
- Successive: 10-15 secondi (già installato)

---

## 🎨 Passo 3: Usa l'Interfaccia

Dopo l'avvio vedrai:

### 1. Barra di Ricerca
- Cerca prodotti (es: "iPhone 13")
- Usa filtri: categoria, prezzo max, regione

### 2. Risultati
- Griglia con foto anteprime
- Prezzi e località
- Badge colorati:
  - 🔴 **Rosso** = Rischio truffa alto (score > 70%)
  - 🟡 **Giallo** = Rischio medio (40-70%)
  - 🟢 **Verde** = Rischio basso (< 40%)

### 3. Dettagli Truffe
- Click su badge rosso/giallo
- Vedi motivi sospetti
- Leggi consigli sicurezza
- Segnala annuncio

### 4. Link Diretti
- Click "Vedi su Subito"
- Apre annuncio originale

---

## 🛑 Fermare il Sistema

### Opzione A: Script Stop
```cmd
stop.bat
```

### Opzione B: Manuale
Chiudi le finestre:
- `Backend-FastAPI`
- `Frontend-React-Vite`

---

## 🔄 Reset Sistema (In caso di problemi)

Se hai errori di installazione o dipendenze corrotte:

```cmd
reset.bat
```

Questo script:
- 🛑 Arresta tutti i servizi
- 🗑️ Rimuove virtual environment
- 🧹 Pulisce cache Python
- 🔄 Opzionalmente rimuove node_modules
- ✨ Resetta sistema a stato iniziale

Dopo il reset:
```cmd
start.bat
```

---

## 📡 URL Utili

Dopo l'avvio:

| Servizio | URL | Descrizione |
|----------|-----|-------------|
| **Frontend** | http://localhost:5173 | Interfaccia utente |
| **Backend** | http://localhost:8000 | API REST |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **ReDoc** | http://localhost:8000/redoc | Documentazione API |

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

### ❌ Errore pydantic-core / Rust

**Errore:**
```
error: metadata-generation-failed
× Encountered error while generating package metadata.
╰─> pydantic-core
```

**Soluzione:**
```cmd
REM 1. Usa lo script di reset
reset.bat

REM 2. Riavvia
start.bat
```

**Se persiste:** Usa Python 3.11 o 3.12 invece di 3.13
- Vai su https://www.python.org/downloads/
- Scarica Python 3.11.x o 3.12.x
- Reinstalla e riprova

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

### ❌ Browser non si apre automaticamente

**Soluzione:**

Apri manualmente: **http://localhost:5173**

Se non vedi l'interfaccia:
1. Attendi 15 secondi
2. Aggiorna (F5)
3. Controlla logs:
   - `logs\backend.log`
   - `logs\frontend.log`

### ❌ Pagina bianca / Errori JavaScript

**Soluzione:**
```cmd
REM 1. Ferma sistema
stop.bat

REM 2. Pulisci frontend
cd frontend
rd /s /q node_modules
npm cache clean --force
cd ..

REM 3. Riavvia
start.bat
```

### ❌ "ModuleNotFoundError" Python

**Soluzione:**
```cmd
REM 1. Ferma sistema
stop.bat

REM 2. Rimuovi venv
rd /s /q venv

REM 3. Riavvia (reinstalla tutto)
start.bat
```

---

## 🛠️ Script Disponibili

| Script | Descrizione | Quando usarlo |
|--------|-------------|---------------|
| **start.bat** | Avvia sistema completo | Uso quotidiano |
| **stop.bat** | Ferma tutti i servizi | Quando finisci di lavorare |
| **reset.bat** | Reset completo sistema | Problemi di installazione |

---

## 📖 Documentazione Completa

Per problemi più complessi o configurazioni avanzate:

- **[WINDOWS_SETUP.md](WINDOWS_SETUP.md)** - Setup dettagliato Windows
- **[README.md](README.md)** - Documentazione generale
- **[INTERFACE_PREVIEW.md](INTERFACE_PREVIEW.md)** - Anteprima interfaccia

---

## 💡 Tips

1. **Prima esecuzione lenta?**
   - È normale, installa tutte le dipendenze
   - Esecuzioni successive saranno veloci

2. **Errori strani?**
   - Prova `reset.bat` per ricominciare da capo

3. **Python 3.13 problemi?**
   - Usa Python 3.11 o 3.12 per massima compatibilità

4. **Redis non necessario**
   - Il sistema funziona anche senza Redis
   - Cache disabilitata automaticamente se Redis non disponibile

5. **Logs utili**
   - Backend: `logs\backend.log`
   - Frontend: `logs\frontend.log`
   - Controlla in caso di errori

---

## 🎯 Checklist Prima Esecuzione

- [ ] Python 3.11/3.12 installato con "Add to PATH"
- [ ] Node.js 18+ LTS installato
- [ ] Terminali/Prompt chiusi e riaperti
- [ ] `python --version` funziona
- [ ] `node --version` funziona
- [ ] Antivirus non blocca Python/Node
- [ ] Sei nella directory del progetto
- [ ] Doppio click su `start.bat`
- [ ] Attendi 2-5 minuti (prima volta)
- [ ] Browser aperto su http://localhost:5173

---

**🚀 Pronto! Buon utilizzo!**

Per supporto: consulta [WINDOWS_SETUP.md](WINDOWS_SETUP.md) per troubleshooting dettagliato.
