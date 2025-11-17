"""Core modules per API."""

from .config import settings
from .dependencies import get_redis_client, get_scraper

__all__ = ['settings', 'get_redis_client', 'get_scraper']
