"""Scraper base con funzionalità comuni."""

import requests
import random
import time
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from bs4 import BeautifulSoup
import logging
from pathlib import Path

from ..config.settings import ScraperConfig
from ..models.listing import Listing
from ..utils.rate_limiter import RateLimiter


logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Classe base astratta per gli scraper."""

    def __init__(self, config: Optional[ScraperConfig] = None):
        """
        Inizializza lo scraper.

        Args:
            config: Configurazione dello scraper
        """
        self.config = config or ScraperConfig()
        self.rate_limiter = RateLimiter(
            requests_per_second=self.config.requests_per_second,
            min_delay=self.config.min_delay,
            max_delay=self.config.max_delay
        )
        self.session = self._create_session()

        # Statistiche
        self.stats = {
            'requests': 0,
            'successful': 0,
            'failed': 0,
            'listings_found': 0
        }

        logger.info(f"{self.__class__.__name__} inizializzato")

    def _create_session(self) -> requests.Session:
        """Crea una sessione requests con headers appropriati."""
        session = requests.Session()
        session.headers.update(self.config.default_headers)
        return session

    def _get_random_user_agent(self) -> str:
        """Restituisce un User-Agent casuale."""
        return random.choice(self.config.user_agents)

    def fetch_page(
        self,
        url: str,
        method: str = 'GET',
        **kwargs
    ) -> Optional[requests.Response]:
        """
        Effettua una richiesta HTTP con rate limiting e retry logic.

        Args:
            url: URL da richiedere
            method: Metodo HTTP (GET, POST, etc.)
            **kwargs: Argomenti aggiuntivi per requests

        Returns:
            Response object o None se fallisce
        """
        # Applica rate limiting
        self.rate_limiter.wait()

        # Imposta User-Agent casuale
        headers = kwargs.pop('headers', {})
        headers['User-Agent'] = self._get_random_user_agent()

        retries = 0
        last_exception = None

        while retries <= self.config.max_retries:
            try:
                self.stats['requests'] += 1

                logger.debug(f"Richiesta {method} a: {url} (tentativo {retries + 1})")

                response = self.session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    timeout=self.config.request_timeout,
                    **kwargs
                )

                response.raise_for_status()

                self.stats['successful'] += 1
                logger.debug(f"Richiesta riuscita: {url} (status: {response.status_code})")

                return response

            except requests.exceptions.RequestException as e:
                last_exception = e
                retries += 1

                if retries <= self.config.max_retries:
                    # Exponential backoff
                    wait_time = self.config.retry_delay * (self.config.backoff_factor ** (retries - 1))
                    logger.warning(
                        f"Errore richiesta {url}: {str(e)}. "
                        f"Retry {retries}/{self.config.max_retries} tra {wait_time}s"
                    )
                    time.sleep(wait_time)
                else:
                    logger.error(f"Richiesta fallita dopo {self.config.max_retries} retry: {url}")
                    logger.error(f"Errore: {str(e)}")

        self.stats['failed'] += 1
        return None

    def parse_html(self, html: str) -> BeautifulSoup:
        """
        Parse HTML con BeautifulSoup.

        Args:
            html: HTML da parsare

        Returns:
            Oggetto BeautifulSoup
        """
        return BeautifulSoup(html, self.config.parser)

    def save_html(self, html: str, filename: str):
        """
        Salva HTML raw per debugging.

        Args:
            html: Contenuto HTML
            filename: Nome file
        """
        if not self.config.save_html:
            return

        output_dir = Path(self.config.output_dir) / 'html'
        output_dir.mkdir(parents=True, exist_ok=True)

        filepath = output_dir / filename
        filepath.write_text(html, encoding='utf-8')
        logger.debug(f"HTML salvato: {filepath}")

    @abstractmethod
    def scrape_listings(self, url: str, max_pages: int = 1) -> List[Listing]:
        """
        Scrape annunci dalla URL specificata.

        Args:
            url: URL da cui estrarre gli annunci
            max_pages: Numero massimo di pagine da processare

        Returns:
            Lista di Listing
        """
        pass

    @abstractmethod
    def scrape_listing_details(self, listing: Listing) -> Listing:
        """
        Estrae dettagli completi di un singolo annuncio.

        Args:
            listing: Listing con almeno il link

        Returns:
            Listing con tutti i dettagli
        """
        pass

    def get_stats(self) -> Dict:
        """Restituisce le statistiche dello scraper."""
        return self.stats.copy()

    def reset_stats(self):
        """Resetta le statistiche."""
        self.stats = {
            'requests': 0,
            'successful': 0,
            'failed': 0,
            'listings_found': 0
        }
        logger.info("Statistiche resettate")

    def close(self):
        """Chiude la sessione."""
        self.session.close()
        logger.info("Sessione chiusa")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
