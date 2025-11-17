"""Configurazioni per il sistema di scraping."""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ScraperConfig:
    """Configurazione per lo scraper."""

    # Rate limiting
    requests_per_second: float = 0.5  # Max 1 richiesta ogni 2 secondi
    min_delay: float = 2.0  # Delay minimo tra richieste (secondi)
    max_delay: float = 5.0  # Delay massimo tra richieste (secondi)

    # Retry logic
    max_retries: int = 3
    retry_delay: float = 5.0  # Delay tra retry (secondi)
    backoff_factor: float = 2.0  # Moltiplicatore per exponential backoff

    # Timeout
    request_timeout: int = 30  # Timeout richieste HTTP (secondi)

    # Headers HTTP
    user_agents: List[str] = field(default_factory=lambda: [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
    ])

    default_headers: Dict[str, str] = field(default_factory=lambda: {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    })

    # Parsing
    parser: str = 'html.parser'  # 'html.parser', 'lxml', o 'html5lib'

    # Output
    save_html: bool = False  # Salva HTML raw per debugging
    save_json: bool = True
    output_dir: str = 'output'

    # Logging
    log_level: str = 'INFO'  # DEBUG, INFO, WARNING, ERROR
    log_file: str = 'scraper.log'

    # Subito.it specifico
    subito_base_url: str = 'https://www.subito.it'

    def __post_init__(self):
        """Validazione configurazione."""
        if self.requests_per_second <= 0:
            raise ValueError("requests_per_second deve essere > 0")
        if self.min_delay < 0:
            raise ValueError("min_delay deve essere >= 0")
        if self.max_retries < 0:
            raise ValueError("max_retries deve essere >= 0")


# Configurazione di default
DEFAULT_CONFIG = ScraperConfig()
