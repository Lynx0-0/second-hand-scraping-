# Frontend React - Subito Scraper

Interfaccia web React per il sistema di scraping annunci con rilevamento truffe automatico.

## 🚀 Caratteristiche

### Interfaccia Utente
- **Barra di ricerca avanzata** con filtri multipli
- **Griglia responsive** di prodotti (1-4 colonne)
- **Cards prodotti** con foto, prezzo, località
- **Badge truffe** rosso per annunci sospetti (score > 70)
- **Modal informativo** con dettagli sicurezza

### Sistema Anti-Truffa
- **Scoring automatico** (0-100) basato su:
  - Analisi prezzo (troppo basso, sospetto)
  - Parole chiave nel titolo (urgente, affare)
  - Descrizione (pagamento anticipato, metodi non tracciabili)
  - Numero foto (poche = sospetto)
  - Località generica
  - Nome venditore

- **Badge colorati**:
  - 🔴 Rosso (score > 70): ATTENZIONE TRUFFA
  - 🟡 Giallo (score 40-70): SOSPETTO
  - 🟢 Verde (score < 40): Verificato

### Segnalazioni
- **Form segnalazione** integrato nel modal
- Invio automatico al backend
- Tracking report con conferma visiva

## 📦 Installazione

```bash
# Dalla directory frontend
npm install

# Copia configurazione
cp .env.example .env

# Modifica .env se necessario (default: http://localhost:8000)
```

## 🏃 Avvio

### Development

```bash
npm run dev
```

L'app sarà disponibile su: http://localhost:5173

### Build Production

```bash
npm run build
npm run preview
```

## 🏗️ Struttura Progetto

```
frontend/
├── src/
│   ├── components/
│   │   ├── SearchBar.jsx        # Barra ricerca con filtri
│   │   ├── ProductCard.jsx      # Card singolo prodotto
│   │   ├── ProductGrid.jsx      # Griglia responsive
│   │   ├── ScamBadge.jsx        # Badge rischio truffa
│   │   └── ScamModal.jsx        # Modal info sicurezza
│   ├── services/
│   │   └── api.js               # Client API (axios)
│   ├── utils/
│   │   └── scamDetector.js      # Sistema scoring truffe
│   ├── App.jsx                  # Componente principale
│   ├── main.jsx                 # Entry point
│   └── index.css                # Stili Tailwind
├── public/
├── package.json
├── vite.config.js
├── tailwind.config.js
└── README.md
```

## 🔌 Integrazione API

L'app si connette al backend FastAPI. Assicurati che il backend sia attivo:

```bash
# Dalla root del progetto
./run_api.sh
```

### Endpoint Utilizzati

**POST /api/v1/search**
```javascript
await api.search({
  query: "iphone 13",
  categoria: "telefonia",
  prezzo_max: 500,
  regione: "lazio",
  max_pages: 2
});
```

**POST /api/v1/report-scam**
```javascript
await api.reportScam({
  listing_id: "123456",
  listing_url: "https://www.subito.it/...",
  reason: "Prezzo sospetto"
});
```

## 🧠 Sistema Scoring Truffe

Lo scoring automatico analizza ogni annuncio assegnando un punteggio 0-100:

- **Score > 70**: 🔴 ATTENZIONE TRUFFA (badge rosso animato)
- **Score 40-70**: 🟡 SOSPETTO (badge giallo)
- **Score < 40**: 🟢 Verificato (nessun badge)

### Criteri Analizzati

1. **Prezzo** (peso 25-40): Confronto con valori di mercato
2. **Titolo** (peso 5-10): Parole chiave sospette
3. **Descrizione** (peso 15-40): Red flags (pagamenti, contatti esterni)
4. **Foto** (peso 10-20): Numero e qualità
5. **Località** (peso 10-12): Genericità
6. **Venditore** (peso 8-12): Nome e tipo account

## 🎨 Responsive Design

Breakpoints:
- Mobile: 1 colonna
- Tablet (768px+): 2 colonne
- Desktop (1024px+): 3 colonne
- Large (1280px+): 4 colonne

## 🔧 Troubleshooting

### API non raggiungibile

```bash
# Verifica backend
curl http://localhost:8000/health

# Avvia backend
cd ..
./run_api.sh
```

### CORS Errors

Verifica `.env` del backend:
```bash
CORS_ORIGINS=["http://localhost:5173"]
```

## 📄 Licenza

Progetto educativo - fornito "as is".
