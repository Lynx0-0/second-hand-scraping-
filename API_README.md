# API Documentation - Subito.it Scraper

API REST completa per il web scraping di annunci da Subito.it con caching Redis, rate limiting e validazione input.

## 🚀 Quick Start

### 1. Installa Dipendenze

```bash
pip install -r requirements.txt
```

### 2. Avvia Redis

```bash
# Con Docker Compose (raccomandato)
docker-compose up -d redis

# Oppure installa Redis localmente
# macOS: brew install redis && redis-server
# Ubuntu: sudo apt install redis-server && sudo systemctl start redis
```

### 3. Configura Variabili d'Ambiente

```bash
cp .env.example .env
# Modifica .env se necessario
```

### 4. Avvia l'API

```bash
# Metodo 1: Script di avvio
./run_api.sh

# Metodo 2: Direttamente con uvicorn
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Metodo 3: Python
python -m api.main
```

L'API sarà disponibile su: http://localhost:8000

**Documentazione interattiva:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📡 Endpoints

### 🔍 POST /api/v1/search

Cerca annunci su Subito.it con filtri avanzati.

**Request Body:**
```json
{
  "query": "iphone 13",
  "categoria": "telefonia",
  "prezzo_max": 500.0,
  "regione": "lazio",
  "max_pages": 2
}
```

**Response:**
```json
{
  "search_id": "550e8400-e29b-41d4-a716-446655440000",
  "query": "iphone 13",
  "categoria": "telefonia",
  "total_results": 15,
  "results": [
    {
      "listing_id": "12345678",
      "title": "iPhone 13 128GB Nero",
      "price": 450.0,
      "price_text": "450 €",
      "description": "iPhone 13 in ottime condizioni...",
      "link": "https://www.subito.it/telefonia/...",
      "photos": ["https://..."],
      "location": "Roma",
      "category": "telefonia",
      "seller_name": "Mario Rossi",
      "scraped_at": "2025-11-17T10:00:00"
    }
  ],
  "cached": false,
  "scraped_at": "2025-11-17T10:00:00",
  "execution_time_ms": 1234.56
}
```

**Categorie disponibili:**
- `elettronica`
- `telefonia`
- `informatica`
- `arredamento-casalinghi`
- `console-videogiochi`
- `fotografia`
- `libri-riviste`
- `strumenti-musicali`
- `abbigliamento-accessori`
- `biciclette`
- `sport`
- `auto`
- `moto`
- `tutto`

### 📄 GET /api/v1/results/{search_id}

Recupera risultati di una ricerca precedente usando il search_id.

**Response:** Stesso formato di POST /search

### 🔗 GET /api/v1/listing/{listing_id}

Recupera dettagli di un singolo annuncio.

**Response:**
```json
{
  "listing_id": "12345678",
  "title": "iPhone 13 128GB",
  "price": 450.0,
  "description": "Descrizione completa...",
  "link": "https://www.subito.it/...",
  "photos": ["https://..."],
  "location": "Roma",
  "scraped_at": "2025-11-17T10:00:00"
}
```

### 🚨 POST /api/v1/report-scam

Segnala un annuncio sospetto o fraudolento.

**Request Body:**
```json
{
  "listing_id": "12345678",
  "listing_url": "https://www.subito.it/telefonia/iphone-13-roma-12345678.htm",
  "reason": "Il venditore chiede pagamento anticipato su carta prepagata, sospetto truffa",
  "reporter_email": "user@example.com",
  "additional_info": "L'annuncio ha foto rubate da altri siti"
}
```

**Response:**
```json
{
  "report_id": "rep_123456789",
  "listing_id": "12345678",
  "status": "received",
  "message": "Segnalazione ricevuta e registrata correttamente",
  "created_at": "2025-11-17T10:00:00"
}
```

### 📊 GET /api/v1/reports/{report_id}

Recupera dettagli di una segnalazione.

### 📋 GET /api/v1/reports/listing/{listing_id}

Recupera tutte le segnalazioni per un annuncio specifico.

### 📈 GET /api/v1/reports/stats

Ottiene statistiche sulle segnalazioni.

### ❤️ GET /health

Health check del servizio.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "redis_connected": true,
  "uptime_seconds": 3600.0,
  "timestamp": "2025-11-17T10:00:00"
}
```

## 🛡️ Sicurezza & Rate Limiting

### Rate Limiting

L'API implementa rate limiting per IP:
- **Default:** 10 richieste per minuto
- **Header risposta:**
  - `X-RateLimit-Limit`: Limite totale
  - `X-RateLimit-Remaining`: Richieste rimanenti
  - `X-RateLimit-Reset`: Timestamp reset

**Errore 429 - Too Many Requests:**
```json
{
  "error": "RateLimitExceeded",
  "message": "Troppe richieste. Riprova tra 30 secondi.",
  "retry_after": 30,
  "limit": 10,
  "period": 60
}
```

### Validazione Input

Tutti gli endpoint validano automaticamente gli input:

**Errore 422 - Validation Error:**
```json
{
  "error": "ValidationError",
  "message": "I dati forniti non sono validi",
  "detail": "query: ensure this value has at least 2 characters",
  "timestamp": "2025-11-17T10:00:00"
}
```

## 💾 Caching Redis

### Strategia di Cache

- **Ricerche:** TTL 1 ora (3600s)
- **Listing singoli:** TTL 2 ore (7200s)
- **Chiavi automatiche** basate su hash dei parametri

### Gestione Cache

La cache è gestita automaticamente ma può essere configurata in `.env`:

```bash
CACHE_TTL_SEARCH=3600
CACHE_TTL_LISTING=7200
```

### Funzionamento Senza Redis

L'API funziona anche senza Redis:
- Cache disabilitata automaticamente
- Tutte le richieste eseguono scraping real-time
- Performance ridotte ma funzionalità completa

## 🔧 Configurazione

### Variabili d'Ambiente (.env)

```bash
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_PERIOD=60

# Scraper
SCRAPER_REQUESTS_PER_SECOND=0.5
SCRAPER_MIN_DELAY=2.0
SCRAPER_MAX_DELAY=5.0

# Logging
LOG_LEVEL=INFO
```

## 📦 Deployment

### Docker

```bash
# Build immagine
docker build -t subito-scraper-api .

# Avvia con Docker Compose
docker-compose up -d

# L'API sarà disponibile su http://localhost:8000
```

### Produzione

Per produzione, usa un server ASGI production-ready:

```bash
# Gunicorn + Uvicorn workers
pip install gunicorn

gunicorn api.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

## 📝 Esempi Uso

### cURL

```bash
# Ricerca base
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "macbook",
    "categoria": "informatica",
    "prezzo_max": 1000.0,
    "max_pages": 2
  }'

# Segnalazione
curl -X POST http://localhost:8000/api/v1/report-scam \
  -H "Content-Type: application/json" \
  -d '{
    "listing_id": "12345678",
    "listing_url": "https://www.subito.it/...",
    "reason": "Prezzo sospetto, probabile truffa"
  }'

# Health check
curl http://localhost:8000/health
```

### Python

```python
import requests

# Ricerca
response = requests.post(
    "http://localhost:8000/api/v1/search",
    json={
        "query": "bicicletta",
        "categoria": "biciclette",
        "prezzo_max": 300.0,
        "max_pages": 1
    }
)

data = response.json()
print(f"Trovati {data['total_results']} annunci")

for listing in data['results']:
    print(f"- {listing['title']}: {listing['price']}€")
```

### JavaScript/TypeScript

```javascript
// Ricerca
const response = await fetch('http://localhost:8000/api/v1/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'playstation 5',
    categoria: 'console-videogiochi',
    prezzo_max: 400,
    max_pages: 2
  })
});

const data = await response.json();
console.log(`Trovati ${data.total_results} annunci`);
```

## 🔍 Monitoring & Logging

### Log Files

- `api.log` - Log applicazione
- `scraper.log` - Log scraper

### Livelli di Log

```bash
# Debug dettagliato
LOG_LEVEL=DEBUG

# Info (default)
LOG_LEVEL=INFO

# Solo errori
LOG_LEVEL=ERROR
```

### Metriche

Usa l'endpoint `/health` per monitoring:

```bash
# Script monitoring
while true; do
  curl -s http://localhost:8000/health | jq
  sleep 30
done
```

## ⚠️ Limitazioni & Best Practices

### Rispetta i Server

- Non abusare dell'API con troppe richieste
- Usa la cache quando possibile
- Rispetta il rate limiting

### Scraping Responsabile

- L'API implementa delay tra richieste (2-5s)
- Max 5 pagine per ricerca
- Verifica robots.txt di Subito.it

### Note Legali

⚠️ Questo progetto è solo per scopi educativi:
- Rispetta i Termini di Servizio di Subito.it
- Non sovraccaricare i server
- Considera l'uso di API ufficiali quando disponibili

## 🤝 Supporto

Per problemi o domande:
1. Verifica la documentazione
2. Controlla i log (`api.log`)
3. Testa con `/health`
4. Apri una issue su GitHub

## 📄 Licenza

Fornito "as is" solo per scopi educativi.
