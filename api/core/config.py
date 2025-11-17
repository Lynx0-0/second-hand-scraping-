"""Configurazione API."""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Configurazione API con variabili d'ambiente."""

    # API Info
    API_TITLE: str = "Subito.it Scraper API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = """
    API per il web scraping di annunci da Subito.it

    ## Caratteristiche

    * **Ricerca annunci** con filtri avanzati
    * **Caching Redis** per performance ottimali
    * **Rate limiting** per protezione
    * **Validazione input** completa
    * **Segnalazione annunci sospetti**
    """

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    RELOAD: bool = False

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    REDIS_DECODE_RESPONSES: bool = True
    REDIS_MAX_CONNECTIONS: int = 10

    # Cache TTL (Time To Live)
    CACHE_TTL_SEARCH: int = 3600  # 1 ora
    CACHE_TTL_LISTING: int = 7200  # 2 ore

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 10  # Richieste
    RATE_LIMIT_PERIOD: int = 60  # Per periodo in secondi (10 richieste/minuto)

    # Scraper - Parametri aumentati per evitare blocchi da Subito.it
    SCRAPER_REQUESTS_PER_SECOND: float = 0.2  # 1 richiesta ogni 5 secondi
    SCRAPER_MIN_DELAY: float = 5.0  # Minimo 5 secondi tra richieste
    SCRAPER_MAX_DELAY: float = 15.0  # Massimo 15 secondi tra richieste
    SCRAPER_MAX_RETRIES: int = 3
    SCRAPER_TIMEOUT: int = 30

    # CORS
    CORS_ENABLED: bool = True
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # Database per segnalazioni (file JSON per semplicità)
    REPORTS_DB_PATH: str = "data/reports.json"

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        """Configurazione Pydantic Settings."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Istanza globale settings
settings = Settings()
