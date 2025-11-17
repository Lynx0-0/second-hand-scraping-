# 🪟 Guida Windows - Subito Scraper

Sistema completo di ricerca annunci Subito.it con rilevamento truffe automatico.

---

## 🚀 AVVIO RAPIDO

### 1. Requisiti

- **Python 3.11 o 3.12** ([Download](https://www.python.org/downloads/))
  - ⚠️ Durante installazione spunta ✅ **"Add Python to PATH"**
- **Node.js 18+** ([Download](https://nodejs.org/))

### 2. Avvia

Doppio click su:
```
start.bat
```

**Prima volta:** 2-5 minuti (installa tutto)
**Successive:** 10-15 secondi

### 3. Usa

Il browser si apre automaticamente su: **http://localhost:5173**

---

## 🎯 Come Funziona

### Interfaccia

1. **Barra Ricerca**
   - Inserisci prodotto (es: "iPhone 13")
   - Usa filtri (categoria, prezzo, regione)

2. **Risultati**
   - Badge colorati rilevamento truffe:
     - 🔴 **Rosso** = Rischio ALTO (>70%)
     - 🟡 **Giallo** = Rischio MEDIO (40-70%)
     - 🟢 **Verde** = Rischio BASSO (<40%)

3. **Dettagli**
   - Click su badge per vedere motivi
   - Segnala annunci sospetti

---

## 🛠️ Script Disponibili

| File | Cosa Fa |
|------|---------|
| **start.bat** | Avvia tutto |
| **stop.bat** | Ferma tutto |
| **test-system.bat** | Verifica configurazione |
| **check-logs.bat** | Mostra logs |

---

## 🐛 Problemi Comuni

### ❌ Errore Python 3.13

Se hai Python 3.13, potrebbero esserci problemi con alcuni pacchetti.

**Soluzione:**
1. Disinstalla Python 3.13
2. Installa Python 3.11 o 3.12
3. Elimina cartella `venv`
4. Riprova `start.bat`

### ❌ Porta 8000/5173 occupata

```cmd
stop.bat
start.bat
```

### ❌ npm install fallisce

```cmd
cd frontend
npm cache clean --force
npm install
cd ..
```

---

## 📡 URL Sistema

| Servizio | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

---

## 🔍 Rilevamento Truffe

Il sistema analizza automaticamente ogni annuncio con **6 criteri**:

1. **Prezzo** - Confronto con mercato
2. **Titolo** - Parole sospette ("urgente", "affare")
3. **Descrizione** - Richieste pagamenti strani
4. **Foto** - Numero di immagini
5. **Località** - Troppo generica
6. **Venditore** - Nome pattern casuali

**Score 0-100:**
- 0-39: Probabile OK
- 40-69: Sospetto
- 70-100: Alta probabilità truffa

---

## 🔒 Consigli Sicurezza

### Mai Fare:
- ❌ Pagare con Western Union, ricariche
- ❌ Inviare acconti prima di vedere prodotto
- ❌ Dare dati carta credito/documenti

### Sempre Fare:
- ✅ Incontrare di persona
- ✅ Verificare prodotto prima di pagare
- ✅ Diffidare di prezzi troppo bassi

---

## 📖 Documentazione

- **README.md** - Documentazione tecnica completa
- **API_README.md** - Documentazione API

---

## 🆘 Supporto

1. **Test sistema:**
   ```cmd
   test-system.bat
   ```

2. **Controlla logs:**
   ```cmd
   check-logs.bat
   ```

3. **Reset completo:**
   ```cmd
   stop.bat
   rmdir /s /q venv
   start.bat
   ```

---

## ⚠️ Note

- Progetto educativo
- Non affiliato con Subito.it
- Usa responsabilmente
- Rilevamento truffe automatico (possibili falsi positivi)

---

**🚀 Buon utilizzo!**
