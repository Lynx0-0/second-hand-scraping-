# 🛡️ Modifiche Anti-Blocco per Subito.it

## 📋 Panoramica

Questo documento descrive le modifiche implementate per evitare blocchi da parte di Subito.it durante lo scraping.

## ⚠️ Problema

Subito.it implementa misure anti-bot sofisticate che rilevano e bloccano richieste automatizzate basandosi su:
- Pattern di richieste troppo regolari
- User agent sospetti o limitati
- Headers HTTP incompleti o non realistici
- Mancanza di cookies o sessioni
- Velocità di richieste troppo elevata

## ✅ Soluzioni Implementate

### 1. **Delay Aumentati**
**File modificato:** `src/config/settings.py`, `api/core/config.py`

- ❌ **Prima:** 2-5 secondi tra richieste
- ✅ **Dopo:** 5-15 secondi tra richieste
- **Rationale:** Pattern più umano e meno prevedibile

```python
requests_per_second: 0.2  # 1 richiesta ogni 5 secondi (prima: 0.5)
min_delay: 5.0  # Minimo 5 secondi (prima: 2.0)
max_delay: 15.0  # Massimo 15 secondi (prima: 5.0)
```

### 2. **Pool User Agents Espanso**
**File modificato:** `src/config/settings.py`

- ❌ **Prima:** 5 user agents
- ✅ **Dopo:** 23 user agents
- **Include:** Chrome, Firefox, Safari, Edge, Opera su Windows, Mac, Linux
- **Rationale:** Maggiore varietà simula traffico reale da dispositivi diversi

### 3. **Headers HTTP Migliorati**
**File modificato:** `src/config/settings.py`

Aggiunti header moderni e realistici:
```python
'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120"'
'Sec-Ch-Ua-Mobile': '?0'
'Sec-Ch-Ua-Platform': '"Windows"'
'Sec-Fetch-User': '?1'
'Referer': 'https://www.subito.it/'  # CRITICO!
```

**Rationale:** Headers Referer e Sec-Ch-* sono richiesti dai browser moderni

### 4. **Gestione Cookies Migliorata**
**File modificato:** `src/scraper/base_scraper.py`

```python
session.cookies.set_policy(None)  # Accetta tutti i cookies
```

**Rationale:** Mantiene sessione persistente e cookies di tracking

### 5. **Gestione Errori HTTP Potenziata**
**File modificato:** `src/scraper/base_scraper.py`

Rilevamento specifico per codici di blocco:
```python
if status_code in [403, 429, 503]:
    # Attesa 30-60 secondi invece di retry normale
    wait_time = random.uniform(30.0, 60.0)
```

**HTTP Codes:**
- **403 Forbidden:** IP bloccato temporaneamente
- **429 Too Many Requests:** Rate limit superato
- **503 Service Unavailable:** Server sovraccarico o protezione anti-bot attiva

## 🧪 Come Testare

### Test Rapido
```bash
python3 test_scraper.py
```

Questo script:
1. Esegue una ricerca base
2. Esegue una ricerca con filtri
3. Mostra statistiche e risultati
4. Fornisce suggerimenti in caso di problemi

### Test Manuale
```python
from src.scraper.subito_scraper import SubitoScraper
from src.config.settings import ScraperConfig

config = ScraperConfig()
with SubitoScraper(config) as scraper:
    listings = scraper.search("iphone", max_pages=1)
    print(f"Trovati {len(listings)} annunci")
```

## 📊 Parametri Raccomandati

### Per Uso Normale
```python
max_pages = 1-2  # Non più di 2 pagine per ricerca
pausa_tra_ricerche = 60  # 1 minuto tra ricerche diverse
```

### Se Continui ad Essere Bloccato

1. **Aumenta i delay:**
   ```python
   # In settings.py
   min_delay: 10.0
   max_delay: 20.0
   ```

2. **Riduci frequenza:**
   ```python
   max_pages = 1  # Solo 1 pagina
   requests_per_second = 0.1  # 1 ogni 10 secondi
   ```

3. **Usa proxy/VPN:**
   - Considera l'uso di servizi proxy rotanti
   - Alterna tra diversi IP
   - Usa VPN per cambiare regione

4. **Attendi blocco temporaneo:**
   - Blocchi solitamente durano 1-6 ore
   - Non fare richieste durante il blocco
   - Riprovare dopo alcune ore

## 🚨 Segni di Blocco

Se vedi questi pattern, sei probabilmente bloccato:

### Nei Log
```
HTTP 403 Forbidden
HTTP 429 Too Many Requests
HTTP 503 Service Unavailable
ConnectionError / Timeout frequenti
```

### Nel Comportamento
- Tutte le richieste falliscono improvvisamente
- Pagine vuote o HTML minimale
- Redirect a pagine CAPTCHA
- Risposte sempre identiche (cached error page)

## 💡 Best Practices

### ✅ DA FARE
- Limitare a 1-2 pagine per ricerca
- Attendere 1-2 minuti tra ricerche diverse
- Usare la cache Redis quando possibile
- Monitorare i log per errori HTTP
- Variare le query di ricerca
- Fare scraping durante orari di basso traffico (notte)

### ❌ DA EVITARE
- Scraping massiccio (100+ pagine)
- Richieste troppo frequenti (<5 secondi)
- Stessa query ripetuta continuamente
- Ignorare errori HTTP 429/403
- Retry aggressivi dopo blocchi

## 🔧 Troubleshooting

### Problema: "Nessun annuncio trovato"
**Possibili cause:**
1. Struttura HTML di Subito.it cambiata
2. Selettori CSS obsoleti
3. JavaScript-rendered content

**Soluzione:**
- Verifica URL nel browser
- Controlla HTML della pagina
- Considera uso di Selenium per pagine JS

### Problema: "Timeout continui"
**Possibili cause:**
1. Connessione internet lenta
2. Firewall/proxy aziendale
3. Rate limiting severo

**Soluzione:**
- Aumenta `request_timeout` in settings.py
- Verifica connessione
- Usa VPN se dietro firewall

### Problema: "403 Forbidden persistente"
**Possibili cause:**
1. IP bloccato per abuso
2. Mancanza di header critici
3. Pattern riconosciuto come bot

**Soluzione:**
- Attendi 6-12 ore
- Cambia IP (VPN/proxy/riavvio router)
- Verifica headers siano corretti
- Riduci ulteriormente frequenza richieste

## 📈 Metriche di Successo

Monitora queste metriche per valutare l'efficacia:

```python
stats = scraper.get_stats()
success_rate = stats['successful'] / stats['requests'] * 100

# Target ideale
assert success_rate > 90  # Almeno 90% di richieste riuscite
assert stats['failed'] < 2  # Massimo 1-2 fallimenti
```

## ⚖️ Note Legali

**IMPORTANTE:**
- Rispetta i Terms of Service di Subito.it
- Usa questo strumento solo per scopi educativi/personali
- Non fare scraping commerciale senza autorizzazione
- Rispetta robots.txt
- Non sovraccaricare i server di Subito.it

## 📞 Supporto

Se continui ad avere problemi:

1. **Controlla i log dettagliati:**
   ```bash
   tail -f scraper.log
   ```

2. **Abilita debug logging:**
   ```python
   config.log_level = 'DEBUG'
   ```

3. **Testa connessione manuale:**
   ```bash
   curl -A "Mozilla/5.0..." https://www.subito.it
   ```

---

**Ultima modifica:** 2024-11-17
**Versione:** 2.0
