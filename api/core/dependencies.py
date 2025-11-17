"""Dipendenze FastAPI."""

import redis
from typing import Generator
from fastapi import Depends
import logging

from .config import settings
from src.scraper.subito_scraper import SubitoScraper
from src.config.settings import ScraperConfig


logger = logging.getLogger(__name__)

# Redis client globale
_redis_client = None


def get_redis_client() -> redis.Redis:
    """
    Dependency per ottenere Redis client.

    Returns:
        Redis client instance
    """
    global _redis_client

    if _redis_client is None:
        try:
            _redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
                decode_responses=settings.REDIS_DECODE_RESPONSES,
                max_connections=settings.REDIS_MAX_CONNECTIONS,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Test connessione
            _redis_client.ping()
            logger.info("Redis connesso con successo")
        except redis.ConnectionError as e:
            logger.warning(f"Redis non disponibile: {e}. Cache disabilitata.")
            _redis_client = None
        except Exception as e:
            logger.error(f"Errore connessione Redis: {e}")
            _redis_client = None

    return _redis_client


def get_scraper() -> Generator[SubitoScraper, None, None]:
    """
    Dependency per ottenere scraper instance.

    Yields:
        SubitoScraper instance
    """
    config = ScraperConfig(
        requests_per_second=settings.SCRAPER_REQUESTS_PER_SECOND,
        min_delay=settings.SCRAPER_MIN_DELAY,
        max_delay=settings.SCRAPER_MAX_DELAY,
        max_retries=settings.SCRAPER_MAX_RETRIES,
        request_timeout=settings.SCRAPER_TIMEOUT,
        log_level=settings.LOG_LEVEL
    )

    scraper = SubitoScraper(config)
    try:
        yield scraper
    finally:
        scraper.close()


def close_redis():
    """Chiude la connessione Redis."""
    global _redis_client
    if _redis_client:
        try:
            _redis_client.close()
            logger.info("Connessione Redis chiusa")
        except Exception as e:
            logger.error(f"Errore chiusura Redis: {e}")
        finally:
            _redis_client = None
