# 🔍 Subito Scraper - Guida Rapida Italiana

Sistema completo di web scraping per Subito.it con interfaccia grafica React e rilevamento truffe automatico.

---

## 🚀 AVVIO VELOCE (Windows 10/11)

### 1. Prima volta - Installazione

**Requisiti:**
- Python 3.11 o 3.12 ([Download](https://www.python.org/downloads/))
- Node.js 18+ LTS ([Download](https://nodejs.org/))

**⚠️ IMPORTANTE:** Durante installazione Python, spunta ✅ "Add Python to PATH"

### 2. Avvia il Sistema

Apri la cartella del progetto e **doppio click** su:

```
start.bat
```

**Prima esecuzione:** 2-5 minuti (installa tutto)  
**Esecuzioni successive:** 10-15 secondi

### 3. Usa l'Interfaccia

Dopo l'avvio si apre automaticamente il browser su: **http://localhost:5173**

---

## 🎯 Come Funziona

### Interfaccia Principale

1. **Barra di Ricerca**
   - Inserisci cosa cerchi (es: "iPhone 13", "MacBook Pro")
   - Usa filtri: categoria, prezzo max, regione
   - Clicca 🔍 Cerca

2. **Risultati**
   - Griglia con foto anteprime
   - Prezzi e località
   - **Badge colorati** per rilevamento truffe:
     - 🔴 **Rosso** = Rischio ALTO (>70%)
     - 🟡 **Giallo** = Rischio MEDIO (40-70%)
     - 🟢 **Verde** = Rischio BASSO (<40%)

3. **Dettagli Truffe**
   - Click su badge rosso/giallo
   - Vedi motivi sospetti
   - Leggi consigli sicurezza
   - Segnala annuncio

4. **Vai all'Annuncio**
   - Click "Vedi su Subito"
   - Apre annuncio originale

---

## 🛠️ Script Disponibili

| Script | Descrizione | Quando Usarlo |
|--------|-------------|---------------|
| **start.bat** | Avvia sistema completo | Uso quotidiano |
| **stop.bat** | Ferma tutti i servizi | Fine lavoro |
| **check-logs.bat** | Mostra ultimi logs | Problemi/debug |
| **test-system.bat** | Verifica configurazione | Prima installazione |

---

## 📡 URL Sistema

Dopo l'avvio:

| Servizio | URL | Descrizione |
|----------|-----|-------------|
| **Frontend** | http://localhost:5173 | Interfaccia utente |
| **Backend** | http://localhost:8000 | API REST |
| **API Docs** | http://localhost:8000/docs | Documentazione API Swagger |
| **Health** | http://localhost:8000/health | Verifica stato backend |

---

## 🐛 Risoluzione Problemi

### ❌ "Python non trovato"

**Soluzione:**
1. Installa Python 3.11 o 3.12
2. Durante installazione spunta ✅ "Add Python to PATH"
3. Riavvia Prompt dei Comandi

**Verifica:**
```cmd
python --version
```

### ❌ Errore "pydantic-core" / Rust

**Causa:** Python 3.13 troppo recente per Windows

**Soluzione:**
```cmd
REM 1. Elimina virtual environment
rmdir /s /q venv

REM 2. Riprova (ho aggiornato requirements.txt)
start.bat
```

**Se persiste:** Usa Python 3.11 o 3.12 (più stabile)

### ❌ Pagina bianca / Errore connessione

**Soluzione 1 - Verifica Backend:**
```cmd
REM Apri nel browser:
http://localhost:8000/health
```

Dovrebbe mostrare: `{"status": "healthy"}`

Se non funziona:
```cmd
REM Controlla logs
check-logs.bat
```

**Soluzione 2 - Verifica Frontend:**
```cmd
REM Controlla che sia partito
check-logs.bat
```

**Soluzione 3 - Riavvio Completo:**
```cmd
stop.bat
timeout /t 5
start.bat
```

### ❌ Porta 8000 o 5173 occupata

**Soluzione:**
```cmd
stop.bat
start.bat
```

Se persiste:
```cmd
REM Trova processo su porta 8000
netstat -ano | findstr :8000

REM Termina processo (sostituisci 1234 con PID)
taskkill /F /PID 1234
```

### ❌ npm install fallisce

**Soluzione:**
```cmd
cd frontend
npm cache clean --force
npm install
cd ..
start.bat
```

---

## 📋 Struttura Progetto

```
second-hand-scraping-/
├── start.bat              ← Avvia sistema
├── stop.bat               ← Ferma sistema  
├── check-logs.bat         ← Mostra logs
├── test-system.bat        ← Test configurazione
│
├── api/                   ← Backend FastAPI
│   ├── main.py            ← Applicazione principale
│   ├── routers/           ← Endpoint API
│   ├── services/          ← Logica business
│   └── models/            ← Modelli dati
│
├── frontend/              ← Frontend React
│   ├── src/
│   │   ├── components/    ← Componenti UI
│   │   ├── services/      ← API client
│   │   └── utils/         ← Rilevamento truffe
│   └── .env               ← Config frontend
│
├── src/                   ← Core scraping
│   ├── scraper/           ← Scraper Subito.it
│   ├── models/            ← Modelli listing
│   └── utils/             ← Rate limiting
│
├── logs/                  ← Log files
│   ├── backend.log        ← Log backend
│   └── frontend.log       ← Log frontend
│
├── data/                  ← Database segnalazioni
├── output/                ← Output scraping
├── .env                   ← Config backend
└── requirements.txt       ← Dipendenze Python
```

---

## ⚙️ Configurazione

### File .env (Backend)

Configurazione principale del backend (già creato):

```env
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS (permette frontend di comunicare)
CORS_ENABLED=True
CORS_ORIGINS=["http://localhost:5173"]

# Rate Limiting
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_PERIOD=60

# Logging
LOG_LEVEL=INFO
```

### File frontend/.env (Frontend)

Configurazione frontend (già creato):

```env
# URL del backend
VITE_API_URL=http://localhost:8000
```

---

## 🔍 Funzionalità Rilevamento Truffe

Il sistema analizza automaticamente ogni annuncio con **6 criteri**:

### 1. Analisi Prezzo (peso: 25-40)
- Confronto con prezzi medi di mercato
- Rileva prezzi sospettosamente bassi
- Categorie specifiche (elettronica, veicoli, immobili)

### 2. Parole Chiave nel Titolo (peso: 20)
- "urgente", "affare", "occasione"
- "ultimo prezzo", "non perderti"
- Uso eccessivo di emoji o maiuscole

### 3. Descrizione Sospetta (peso: 30)
- Richiesta pagamenti esterni (Western Union, MoneyGram)
- Contatti fuori piattaforma (WhatsApp, Telegram)
- Frasi tipiche truffe ("sono all'estero", "acconto urgente")
- Link esterni sospetti

### 4. Numero Foto (peso: 10)
- 0 foto = molto sospetto
- 1-2 foto = sospetto
- 3+ foto = normale

### 5. Località Generica (peso: 10)
- "Italia", "Tutta Italia" = sospetto
- Città specifica = normale

### 6. Nome Venditore (peso: 10)
- Pattern casuali (es: "user123456")
- Nomi generici non realistici
- Account nuovi

### Score Finale

- **0-39**: 🟢 Rischio Basso
- **40-69**: 🟡 Rischio Medio  
- **70-100**: 🔴 Rischio Alto

---

## 💡 Suggerimenti d'Uso

### Ricerche Efficaci

✅ **Buone ricerche:**
- "iPhone 13 128GB"
- "MacBook Pro 2020"
- "Bicicletta mountain bike"
- "PlayStation 5"

❌ **Evita:**
- Ricerche troppo generiche ("telefono")
- Parole troppo corte (meno di 3 lettere)

### Filtri Utili

- **Categoria:** Raffina la ricerca
- **Prezzo Max:** Elimina annunci troppo costosi
- **Regione:** Cerca nella tua zona

### Interpretare Badge

- 🔴 **Rosso (>70%):** ATTENZIONE! Alta probabilità truffa
  - Non pagare anticipi
  - Diffida di prezzi troppo bassi
  - Verifica identità venditore

- 🟡 **Giallo (40-70%):** SOSPETTO - Massima cautela
  - Controlla attentamente descrizione
  - Verifica foto (cerca immagini duplicate online)
  - Richiedi info aggiuntive al venditore

- 🟢 **Verde (<40%):** Probabile annuncio legittimo
  - Comunque usa buon senso
  - Incontra in luoghi pubblici
  - Paga solo con metodi sicuri

---

## 🔒 Consigli Sicurezza

### Mai Fare:
- ❌ Pagare con Western Union, MoneyGram, ricariche
- ❌ Inviare acconti a sconosciuti
- ❌ Comunicare fuori dalla piattaforma prima dell'incontro
- ❌ Dare dati personali (carta credito, password, documenti)

### Sempre Fare:
- ✅ Incontrare di persona in luoghi pubblici
- ✅ Verificare il prodotto prima di pagare
- ✅ Usare PayPal con protezione acquirenti (se online)
- ✅ Diffidare di prezzi troppo bassi
- ✅ Controllare profilo venditore (feedback, data iscrizione)

---

## 📖 Documentazione Completa

- **README.md** - Documentazione tecnica completa
- **QUICK_START_WINDOWS.md** - Guida rapida Windows
- **WINDOWS_SETUP.md** - Setup dettagliato Windows
- **API_README.md** - Documentazione API

---

## 🆘 Supporto

Se hai problemi:

1. **Controlla logs:**
   ```cmd
   check-logs.bat
   ```

2. **Testa sistema:**
   ```cmd
   test-system.bat
   ```

3. **Riavvio completo:**
   ```cmd
   stop.bat
   rmdir /s /q venv
   start.bat
   ```

4. **Verifica requisiti:**
   - Python 3.11 o 3.12 (NON 3.13)
   - Node.js 18+ LTS
   - Windows 10/11

---

## ⚠️ Note Legali

- Questo è un **progetto educativo**
- Non affiliato con Subito.it
- Usa in modo responsabile
- Rispetta i Termini di Servizio di Subito.it
- Il rilevamento truffe è automatico e può avere falsi positivi
- Usa sempre il buon senso negli acquisti

---

## 🎯 Quick Reference

```cmd
# Avvia sistema
start.bat

# Ferma sistema
stop.bat

# Mostra logs
check-logs.bat

# Test configurazione
test-system.bat

# Apri interfaccia (dopo avvio)
start http://localhost:5173

# Apri API docs (dopo avvio)
start http://localhost:8000/docs
```

---

**🚀 Pronto! Buon utilizzo!**
