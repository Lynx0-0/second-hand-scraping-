"""Middleware per rate limiting."""

import time
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from typing import Dict, Tuple
import logging

from api.core.config import settings


logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware per limitare le richieste per IP."""

    def __init__(self, app, requests: int = None, period: int = None):
        """
        Inizializza il middleware.

        Args:
            app: FastAPI app
            requests: Numero massimo di richieste
            period: Periodo in secondi
        """
        super().__init__(app)
        self.requests = requests or settings.RATE_LIMIT_REQUESTS
        self.period = period or settings.RATE_LIMIT_PERIOD
        self.enabled = settings.RATE_LIMIT_ENABLED

        # Dizionario per tracciare richieste per IP
        # Struttura: {ip: [(timestamp1, timestamp2, ...)]}
        self.request_log: Dict[str, list] = defaultdict(list)

        logger.info(
            f"Rate limiting {'abilitato' if self.enabled else 'disabilitato'}: "
            f"{self.requests} richieste/{self.period}s"
        )

    def _get_client_ip(self, request: Request) -> str:
        """
        Estrae l'IP del client dalla richiesta.

        Args:
            request: Request object

        Returns:
            IP del client
        """
        # Controlla header X-Forwarded-For (per proxy/load balancers)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()

        # Altrimenti usa l'IP del client diretto
        return request.client.host if request.client else "unknown"

    def _clean_old_requests(self, ip: str, current_time: float):
        """
        Rimuove richieste vecchie dal log.

        Args:
            ip: IP del client
            current_time: Timestamp corrente
        """
        cutoff_time = current_time - self.period
        self.request_log[ip] = [
            timestamp for timestamp in self.request_log[ip]
            if timestamp > cutoff_time
        ]

    def _is_rate_limited(self, ip: str) -> Tuple[bool, int]:
        """
        Verifica se l'IP ha superato il rate limit.

        Args:
            ip: IP del client

        Returns:
            Tupla (is_limited, remaining_requests)
        """
        current_time = time.time()

        # Pulisci richieste vecchie
        self._clean_old_requests(ip, current_time)

        # Conta richieste nel periodo
        request_count = len(self.request_log[ip])

        # Calcola richieste rimanenti
        remaining = max(0, self.requests - request_count)

        # Verifica limite
        is_limited = request_count >= self.requests

        return is_limited, remaining

    def _log_request(self, ip: str):
        """
        Registra una richiesta per l'IP.

        Args:
            ip: IP del client
        """
        current_time = time.time()
        self.request_log[ip].append(current_time)

    def _get_retry_after(self, ip: str) -> int:
        """
        Calcola quando l'IP potrà fare la prossima richiesta.

        Args:
            ip: IP del client

        Returns:
            Secondi da attendere
        """
        if not self.request_log[ip]:
            return 0

        oldest_request = min(self.request_log[ip])
        wait_until = oldest_request + self.period
        retry_after = max(0, int(wait_until - time.time()))

        return retry_after

    async def dispatch(self, request: Request, call_next):
        """
        Processa la richiesta con rate limiting.

        Args:
            request: Request object
            call_next: Prossimo middleware/handler

        Returns:
            Response
        """
        # Escludi endpoint di health check dal rate limiting
        if request.url.path in ["/health", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Se rate limiting disabilitato, passa oltre
        if not self.enabled:
            return await call_next(request)

        # Ottieni IP del client
        client_ip = self._get_client_ip(request)

        # Verifica rate limit
        is_limited, remaining = self._is_rate_limited(client_ip)

        if is_limited:
            retry_after = self._get_retry_after(client_ip)

            logger.warning(
                f"Rate limit superato per IP {client_ip}. "
                f"Retry dopo {retry_after}s"
            )

            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "RateLimitExceeded",
                    "message": f"Troppe richieste. Riprova tra {retry_after} secondi.",
                    "retry_after": retry_after,
                    "limit": self.requests,
                    "period": self.period
                },
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(self.requests),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(time.time()) + retry_after)
                }
            )

        # Registra richiesta
        self._log_request(client_ip)

        # Processa richiesta
        response = await call_next(request)

        # Aggiungi header rate limit alla risposta
        _, remaining = self._is_rate_limited(client_ip)
        response.headers["X-RateLimit-Limit"] = str(self.requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(time.time() + self.period))

        return response

    def clear_ip(self, ip: str):
        """
        Pulisce il log per un IP specifico.

        Args:
            ip: IP da pulire
        """
        if ip in self.request_log:
            del self.request_log[ip]
            logger.info(f"Log pulito per IP: {ip}")

    def clear_all(self):
        """Pulisce tutti i log."""
        self.request_log.clear()
        logger.info("Tutti i log rate limit puliti")

    def get_stats(self) -> Dict:
        """
        Ottiene statistiche rate limiting.

        Returns:
            Dict con statistiche
        """
        return {
            "enabled": self.enabled,
            "limit": f"{self.requests} requests/{self.period}s",
            "tracked_ips": len(self.request_log),
            "total_recent_requests": sum(len(reqs) for reqs in self.request_log.values())
        }
