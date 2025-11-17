"""Servizio caching Redis."""

import json
import hashlib
import logging
from typing import Optional, Any, Dict
import redis

from api.core.config import settings


logger = logging.getLogger(__name__)


class CacheService:
    """Gestisce il caching con Redis."""

    def __init__(self, redis_client: Optional[redis.Redis] = None):
        """
        Inizializza il servizio cache.

        Args:
            redis_client: Client Redis (opzionale)
        """
        self.redis = redis_client
        self.enabled = redis_client is not None

        if not self.enabled:
            logger.warning("Cache Redis non disponibile, funzionerà senza cache")

    def _generate_key(self, prefix: str, **kwargs) -> str:
        """
        Genera chiave cache univoca.

        Args:
            prefix: Prefisso della chiave
            **kwargs: Parametri per generare la chiave

        Returns:
            Chiave cache
        """
        # Ordina i parametri per consistenza
        params_str = json.dumps(kwargs, sort_keys=True)
        # Hash MD5 dei parametri
        params_hash = hashlib.md5(params_str.encode()).hexdigest()
        return f"{prefix}:{params_hash}"

    def get(self, key: str) -> Optional[Any]:
        """
        Recupera valore dalla cache.

        Args:
            key: Chiave cache

        Returns:
            Valore deserializzato o None
        """
        if not self.enabled:
            return None

        try:
            value = self.redis.get(key)
            if value:
                logger.debug(f"Cache HIT: {key}")
                return json.loads(value)
            else:
                logger.debug(f"Cache MISS: {key}")
                return None
        except Exception as e:
            logger.error(f"Errore recupero cache: {e}")
            return None

    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """
        Salva valore in cache.

        Args:
            key: Chiave cache
            value: Valore da salvare
            ttl: Time to live in secondi

        Returns:
            True se salvato con successo
        """
        if not self.enabled:
            return False

        try:
            serialized = json.dumps(value, default=str)
            if ttl:
                self.redis.setex(key, ttl, serialized)
            else:
                self.redis.set(key, serialized)

            logger.debug(f"Cache SET: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Errore salvataggio cache: {e}")
            return False

    def delete(self, key: str) -> bool:
        """
        Elimina valore dalla cache.

        Args:
            key: Chiave cache

        Returns:
            True se eliminato con successo
        """
        if not self.enabled:
            return False

        try:
            self.redis.delete(key)
            logger.debug(f"Cache DELETE: {key}")
            return True
        except Exception as e:
            logger.error(f"Errore eliminazione cache: {e}")
            return False

    def clear_pattern(self, pattern: str) -> int:
        """
        Elimina tutte le chiavi che matchano un pattern.

        Args:
            pattern: Pattern da matchare (es. "search:*")

        Returns:
            Numero di chiavi eliminate
        """
        if not self.enabled:
            return 0

        try:
            keys = self.redis.keys(pattern)
            if keys:
                deleted = self.redis.delete(*keys)
                logger.info(f"Cache CLEAR: {deleted} chiavi eliminate per pattern '{pattern}'")
                return deleted
            return 0
        except Exception as e:
            logger.error(f"Errore pulizia cache: {e}")
            return 0

    def get_search_results(self, query: str, categoria: Optional[str] = None,
                          prezzo_max: Optional[float] = None,
                          regione: Optional[str] = None) -> Optional[Dict]:
        """
        Recupera risultati ricerca dalla cache.

        Args:
            query: Query di ricerca
            categoria: Categoria
            prezzo_max: Prezzo massimo
            regione: Regione

        Returns:
            Risultati cached o None
        """
        key = self._generate_key(
            "search",
            query=query,
            categoria=categoria,
            prezzo_max=prezzo_max,
            regione=regione
        )
        return self.get(key)

    def set_search_results(self, results: Dict, query: str,
                          categoria: Optional[str] = None,
                          prezzo_max: Optional[float] = None,
                          regione: Optional[str] = None) -> bool:
        """
        Salva risultati ricerca in cache.

        Args:
            results: Risultati da salvare
            query: Query di ricerca
            categoria: Categoria
            prezzo_max: Prezzo massimo
            regione: Regione

        Returns:
            True se salvato con successo
        """
        key = self._generate_key(
            "search",
            query=query,
            categoria=categoria,
            prezzo_max=prezzo_max,
            regione=regione
        )
        return self.set(key, results, ttl=settings.CACHE_TTL_SEARCH)

    def get_listing(self, listing_id: str) -> Optional[Dict]:
        """
        Recupera dettagli listing dalla cache.

        Args:
            listing_id: ID listing

        Returns:
            Listing cached o None
        """
        key = f"listing:{listing_id}"
        return self.get(key)

    def set_listing(self, listing_id: str, listing_data: Dict) -> bool:
        """
        Salva dettagli listing in cache.

        Args:
            listing_id: ID listing
            listing_data: Dati listing

        Returns:
            True se salvato con successo
        """
        key = f"listing:{listing_id}"
        return self.set(key, listing_data, ttl=settings.CACHE_TTL_LISTING)

    def ping(self) -> bool:
        """
        Verifica connessione Redis.

        Returns:
            True se connesso
        """
        if not self.enabled:
            return False

        try:
            return self.redis.ping()
        except Exception as e:
            logger.error(f"Redis ping fallito: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """
        Ottiene statistiche cache.

        Returns:
            Dict con statistiche
        """
        if not self.enabled:
            return {
                "enabled": False,
                "connected": False
            }

        try:
            info = self.redis.info()
            return {
                "enabled": True,
                "connected": True,
                "keys": self.redis.dbsize(),
                "used_memory_human": info.get('used_memory_human', 'N/A'),
                "uptime_seconds": info.get('uptime_in_seconds', 0)
            }
        except Exception as e:
            logger.error(f"Errore recupero stats: {e}")
            return {
                "enabled": True,
                "connected": False,
                "error": str(e)
            }
