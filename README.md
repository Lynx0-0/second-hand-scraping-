# Sistema di Web Scraping Modulare per Subito.it

Sistema modulare e robusto per il web scraping di annunci da Subito.it. Estrae titolo, prezzo, foto, descrizione e link degli annunci con gestione intelligente del rate limiting e retry logic.

## 🚀 Caratteristiche

- **Architettura Modulare**: Struttura organizzata e facilmente estensibile
- **Rate Limiting Intelligente**: Rispetta i server con delay randomizzati e configura bili
- **Retry Logic**: Gestione automatica degli errori con exponential backoff
- **Estrazione Dati Completa**:
  - Titolo
  - Prezzo (numerico e testo)
  - Link annuncio
  - Foto (tutte le immagini disponibili)
  - Descrizione completa
  - Località
  - Info venditore
  - Categoria
  - Data pubblicazione
- **Export Multipli**: JSON e CSV
- **Logging Completo**: Debug e monitoring delle operazioni
- **User-Agent Rotation**: Simula diversi browser
- **Context Manager**: Gestione automatica delle risorse

## 📁 Struttura Progetto

```
second-hand-scraping-/
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py          # Configurazioni sistema
│   ├── models/
│   │   ├── __init__.py
│   │   └── listing.py           # Modello dati annuncio
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── base_scraper.py      # Scraper base astratto
│   │   └── subito_scraper.py    # Scraper specifico Subito.it
│   └── utils/
│       ├── __init__.py
│       ├── rate_limiter.py      # Gestione rate limiting
│       └── logger.py            # Configurazione logging
├── examples/
│   ├── basic_scraping.py        # Esempio base
│   └── advanced_scraping.py     # Esempi avanzati
├── tests/
├── output/                       # Output generato
├── requirements.txt
├── .gitignore
└── README.md
```

## 🛠️ Installazione

### 1. Clona il repository

```bash
git clone <repository-url>
cd second-hand-scraping-
```

### 2. Crea virtual environment (consigliato)

```bash
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
```

### 3. Installa dipendenze

```bash
pip install -r requirements.txt
```

## 📖 Utilizzo

### Esempio Base

```python
from src.scraper.subito_scraper import SubitoScraper
from src.config.settings import ScraperConfig
from src.utils.logger import setup_logger

# Setup logger
logger = setup_logger(name='scraper', level='INFO')

# Configura scraper
config = ScraperConfig(
    requests_per_second=0.5,  # Max 1 richiesta ogni 2 secondi
    min_delay=2.0,
    max_delay=4.0,
    max_retries=3
)

# Usa lo scraper
with SubitoScraper(config) as scraper:
    # Cerca annunci
    listings = scraper.search(
        query="iphone",
        category="telefonia",
        max_pages=2
    )

    # Mostra risultati
    for listing in listings:
        print(f"{listing.title} - €{listing.price}")
        print(f"Link: {listing.link}\n")

    # Estrai dettagli completi
    if listings:
        detailed = scraper.scrape_listing_details(listings[0])
        print(f"Descrizione: {detailed.description}")
        print(f"Foto: {len(detailed.photos)}")
```

### Esegui Esempi

```bash
# Esempio base
python examples/basic_scraping.py

# Esempi avanzati
python examples/advanced_scraping.py
```

## ⚙️ Configurazione

### ScraperConfig - Parametri Principali

```python
from src.config.settings import ScraperConfig

config = ScraperConfig(
    # Rate Limiting
    requests_per_second=0.5,      # Richieste al secondo
    min_delay=2.0,                 # Delay minimo (sec)
    max_delay=5.0,                 # Delay massimo (sec)

    # Retry Logic
    max_retries=3,                 # Numero tentativi
    retry_delay=5.0,               # Delay tra retry (sec)
    backoff_factor=2.0,            # Moltiplicatore backoff

    # Timeout
    request_timeout=30,            # Timeout richieste (sec)

    # Parser
    parser='html.parser',          # 'lxml' per performance migliori

    # Output
    save_html=False,               # Salva HTML per debug
    save_json=True,                # Salva risultati JSON
    output_dir='output',           # Directory output

    # Logging
    log_level='INFO',              # DEBUG, INFO, WARNING, ERROR
    log_file='scraper.log'
)
```

## 🔍 API Principale

### SubitoScraper

#### Metodi

**`search(query, category=None, region=None, max_pages=1)`**
Cerca annunci per query e filtri.

```python
listings = scraper.search(
    query="bicicletta",
    category="biciclette",
    region="lazio",
    max_pages=3
)
```

**`scrape_listings(url, max_pages=1)`**
Scrape annunci da URL specifica.

```python
listings = scraper.scrape_listings(
    url="https://www.subito.it/annunci-italia/vendita/usato/",
    max_pages=2
)
```

**`scrape_listing_details(listing)`**
Estrae dettagli completi di un annuncio.

```python
detailed_listing = scraper.scrape_listing_details(listings[0])
```

**`get_stats()`**
Restituisce statistiche operazioni.

```python
stats = scraper.get_stats()
print(f"Richieste: {stats['requests']}")
print(f"Annunci trovati: {stats['listings_found']}")
```

### Listing Model

```python
@dataclass
class Listing:
    title: str                       # Titolo annuncio
    price: Optional[float]           # Prezzo numerico
    price_text: Optional[str]        # Prezzo come testo
    description: Optional[str]       # Descrizione completa
    link: Optional[str]              # URL annuncio
    photos: List[str]                # Lista URL foto
    location: Optional[str]          # Località
    category: Optional[str]          # Categoria
    posted_date: Optional[str]       # Data pubblicazione
    seller_name: Optional[str]       # Nome venditore
    seller_type: Optional[str]       # Tipo venditore
    listing_id: Optional[str]        # ID annuncio
    scraped_at: datetime             # Timestamp scraping
    metadata: Dict                   # Metadati extra
```

Metodi utili:
- `to_dict()` - Converte in dizionario
- `to_json()` - Converte in JSON
- `is_valid()` - Valida dati essenziali

## 🎯 Esempi Avanzati

### Scraping Multiple Query

```python
searches = [
    {"query": "macbook", "category": "informatica"},
    {"query": "playstation", "category": "console-videogiochi"},
]

with SubitoScraper(config) as scraper:
    for search in searches:
        listings = scraper.search(**search, max_pages=2)
        # Processa risultati...
```

### Export CSV

```python
import csv

def save_to_csv(listings, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'price', 'link'])
        writer.writeheader()
        for listing in listings:
            writer.writerow({
                'title': listing.title,
                'price': listing.price,
                'link': listing.link
            })
```

### Filtraggio Custom

```python
# Filtra per prezzo
affordable = [l for l in listings if l.price and l.price < 100]

# Filtra per località
local = [l for l in listings if l.location and 'Roma' in l.location]

# Filtra annunci con foto
with_photos = [l for l in listings if len(l.photos) > 0]
```

## ⚠️ Best Practices

### Rate Limiting
- **Rispetta i server**: usa delay appropriati (min 2-3 secondi)
- **Evita ban**: non fare troppe richieste consecutive
- **Ore di basso traffico**: preferisci scraping notturno

### Gestione Errori
```python
try:
    listings = scraper.search("query", max_pages=5)
except Exception as e:
    logger.error(f"Errore durante scraping: {e}")
    # Gestisci errore...
```

### Logging
```python
# Debug dettagliato
logger = setup_logger(level='DEBUG', log_file='debug.log')

# Solo errori
logger = setup_logger(level='ERROR')
```

### Context Manager
```python
# Usa sempre context manager per chiusura automatica sessione
with SubitoScraper(config) as scraper:
    # ... operazioni ...
# Sessione chiusa automaticamente
```

## 🔧 Troubleshooting

### Errore 403 Forbidden
- Aumenta delay tra richieste
- Verifica User-Agent sia valido
- Usa VPN se necessario

### Nessun annuncio trovato
- Verifica selettori HTML (possono cambiare)
- Abilita `save_html=True` per debug
- Controlla log per errori parsing

### Timeout richieste
- Aumenta `request_timeout` in config
- Controlla connessione internet
- Verifica proxy/VPN non blocchino connessione

## 📝 Note Legali

⚠️ **IMPORTANTE**: Questo progetto è solo per scopi educativi.

- Rispetta sempre i **Termini di Servizio** dei siti web
- Verifica il file **robots.txt** del sito
- Non sovraccaricare i server con troppe richieste
- Considera l'utilizzo di **API ufficiali** quando disponibili
- Alcuni siti potrebbero bloccare il web scraping

## 🤝 Contribuire

Contributi benvenuti! Per miglioramenti:

1. Fork del progetto
2. Crea branch feature (`git checkout -b feature/nuova-feature`)
3. Commit modifiche (`git commit -m 'Aggiunge nuova feature'`)
4. Push al branch (`git push origin feature/nuova-feature`)
5. Apri Pull Request

## 📄 Licenza

Questo progetto è fornito "as is" solo per scopi educativi.

## 🔗 Risorse Utili

- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Documentation](https://docs.python-requests.org/)
- [Web Scraping Best Practices](https://www.scrapingbee.com/blog/web-scraping-best-practices/)
- [robots.txt di Subito.it](https://www.subito.it/robots.txt)

---

**Nota**: Il web scraping deve essere effettuato in modo responsabile ed etico. Assicurati di avere il diritto di estrarre i dati che stai cercando.
