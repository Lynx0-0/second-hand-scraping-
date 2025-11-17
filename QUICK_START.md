# 🚀 QUICK START - Interfaccia Grafica Funzionante

Guida rapida per avviare l'intero sistema e vedere l'interfaccia grafica in azione.

## ⚡ Avvio Rapido (1 comando)

```bash
./start.sh
```

Questo script:
1. ✅ Verifica dipendenze (Python, Node.js)
2. ✅ Installa dipendenze backend e frontend
3. ✅ Avvia Redis (se disponibile)
4. ✅ Avvia Backend API su porta 8000
5. ✅ Avvia Frontend React su porta 5173
6. ✅ Apre automaticamente il browser

**Dopo ~10 secondi** vedrai l'interfaccia su: **http://localhost:5173**

## 🎯 Come Usare l'Interfaccia

### 1. Fai una Ricerca

Nella barra di ricerca principale, inserisci una query:
```
iPhone 13
MacBook Pro
Bicicletta elettrica
PlayStation 5
```

### 2. Usa i Filtri (Opzionale)

Clicca sull'icona filtri per aprire:
- **Categoria**: Scegli tra 14 categorie (Telefonia, Informatica, etc.)
- **Prezzo Max**: Inserisci budget massimo (es. 500)
- **Regione**: Seleziona regione italiana

### 3. Vedi i Risultati

Dopo la ricerca vedrai una **griglia di card** con:

```
┌─────────────────────────────┐
│  [FOTO ANTEPRIMA]          │ ← Foto principale prodotto
│  🔴 ATTENZIONE TRUFFA      │ ← Badge se sospetto (score > 70)
├─────────────────────────────┤
│ iPhone 13 128GB Nero       │ ← Titolo
│ €450.00                    │ ← Prezzo grande
│ 📍 Roma • Oggi 10:30       │ ← Località e data
│ Ottime condizioni...       │ ← Anteprima descrizione
│ 👤 Mario Rossi (privato)   │ ← Venditore
├─────────────────────────────┤
│ [Vedi su Subito.it] [🛡️]   │ ← Bottoni azione
└─────────────────────────────┘
```

### 4. Badge Truffe

Se vedi il **badge rosso animato** "ATTENZIONE TRUFFA":

1. **Clicca sul badge** → Si apre modal informativo
2. Vedi **score di rischio** (es. 75/100)
3. Leggi **motivi specifici**:
   - "Prezzo sospettosamente basso per iPhone (€150)"
   - "Descrizione molto breve"
   - "Solo una foto disponibile"
4. Leggi **5 consigli di sicurezza**
5. Puoi **segnalare** l'annuncio compilando il form

### 5. Apri Annuncio Originale

Clicca **"Vedi su Subito.it"** per aprire il link originale in nuova tab.

## 📱 Layout Responsive

- **Mobile**: 1 colonna verticale
- **Tablet**: 2 colonne
- **Desktop**: 3 colonne
- **Large Screen**: 4 colonne

## 🛑 Fermare il Sistema

```bash
./stop.sh
```

## 📊 Esempio Completo

### Ricerca iPhone

```bash
# 1. Avvia
./start.sh

# 2. Aspetta messaggio "Sistema Avviato"

# 3. Apri browser: http://localhost:5173

# 4. Nella barra di ricerca scrivi:
"iPhone 13"

# 5. Clicca filtri e imposta:
Categoria: Telefonia
Prezzo max: 500

# 6. Clicca "Cerca"

# 7. Vedrai griglia con risultati come:
```

**Risultato Visivo:**
```
╔══════════════════════════════════════════════════════════╗
║          🔍 Subito Scraper                               ║
║          Cerca annunci usati con rilevamento truffe      ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  [iPhone 13    ] [📦 Telefonia ▼] [€ 500] [🔍 Cerca]   ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  Query: iPhone 13 | Categoria: telefonia | 15 risultati  ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   ║
║  │[📷]     │  │[📷]     │  │[📷]     │  │[📷]     │   ║
║  │🔴Truffa │  │         │  │🟡Sosp   │  │         │   ║
║  │iPhone13 │  │iPhone13 │  │iPhone13 │  │iPhone13 │   ║
║  │€150❌   │  │€450✓    │  │€280     │  │€520✓    │   ║
║  │Roma     │  │Milano   │  │Napoli   │  │Torino   │   ║
║  │[Vedi]   │  │[Vedi]   │  │[Vedi]   │  │[Vedi]   │   ║
║  └─────────┘  └─────────┘  └─────────┘  └─────────┘   ║
║                                                          ║
║  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   ║
║  │ ... altre card ...                                   ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

## 🐛 Troubleshooting

### "API non raggiungibile"

```bash
# Verifica backend
curl http://localhost:8000/health

# Se non risponde, riavvia
./stop.sh
./start.sh
```

### "Porta già in uso"

```bash
# Ferma processi esistenti
./stop.sh

# Oppure cambia porte in .env:
PORT=8001  # Backend
# E in frontend/.env:
VITE_API_URL=http://localhost:8001
```

### "Nessun risultato"

L'API fa scraping reale da Subito.it. Se non trovi risultati:
1. Prova query diverse
2. Rimuovi filtri troppo restrittivi
3. Verifica log: `tail -f logs/backend.log`

### "Foto non si caricano"

Alcune foto potrebbero non caricarsi per:
- Protezioni CORS di Subito.it
- Link foto scaduti
- Il placeholder "No Image" viene mostrato automaticamente

## 📁 Struttura Visualizzata

```
Frontend (React)          Backend (FastAPI)          Subito.it
     │                           │                        │
     │  1. Ricerca "iPhone"      │                        │
     ├──────────────────────────>│                        │
     │                           │  2. Scraping           │
     │                           ├───────────────────────>│
     │                           │<───────────────────────┤
     │                           │  3. HTML risultati     │
     │                           │                        │
     │                           │  4. Parse + Score      │
     │                           │     Truffe ✓          │
     │  5. JSON risultati        │                        │
     │<──────────────────────────┤                        │
     │                           │                        │
     │  6. Render Cards          │                        │
     │     con Badge Truffe      │                        │
     │                           │                        │
```

## 💡 Funzionalità Complete

### ✅ Ricerca
- Input con validazione
- 14 categorie
- Filtro prezzo
- 20 regioni italiane
- Loading states
- Cache Redis (risultati instantanei se già cercati)

### ✅ Visualizzazione Risultati
- Griglia responsive
- Card con foto anteprima
- Titolo, prezzo, località
- Descrizione preview
- Info venditore
- Contatore foto (se multiple)

### ✅ Sistema Anti-Truffa
- Score automatico 0-100
- Badge colorati (rosso/giallo/verde)
- Modal con dettagli
- 6 criteri di analisi
- Segnalazione truffe

### ✅ Link Esterni
- "Vedi su Subito.it" apre annuncio originale
- Nuovo tab con noopener (sicurezza)
- Icon esterno

## 🎨 Personalizzazione

### Cambia Colori

Modifica `frontend/tailwind.config.js`:
```javascript
colors: {
  'scam-red': '#dc2626',  // Cambia colore badge truffe
  'subito-blue': '#0066ff', // Cambia colore principale
}
```

### Cambia Soglie Score

Modifica `frontend/src/utils/scamDetector.js`:
```javascript
// Linea ~50
if (score >= 80) {  // Era 70
  riskLevel = 'high';
}
```

## 📞 Supporto

- Log Backend: `tail -f logs/backend.log`
- Log Frontend: `tail -f logs/frontend.log`
- API Docs: http://localhost:8000/docs
- GitHub Issues: [link repository]

---

**🎉 Buon utilizzo! Ricorda: questo è un progetto educativo.**
