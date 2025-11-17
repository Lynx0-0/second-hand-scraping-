"""Router per health check e status."""

import time
from datetime import datetime
import logging

from fastapi import APIRouter, Depends
import redis

from api.models.responses import HealthResponse
from api.core.dependencies import get_redis_client
from api.core.config import settings


logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])

# Timestamp di avvio dell'applicazione
_start_time = time.time()


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=200,
    summary="Health check",
    description="""
    Endpoint per verificare lo stato di salute dell'API.

    **Restituisce:**
    - Status del servizio (healthy/unhealthy)
    - Versione API
    - Stato connessione Redis
    - Uptime del servizio
    - Timestamp corrente

    **Note:**
    - Questo endpoint NON è soggetto a rate limiting
    - Utile per monitoring e load balancers
    """
)
async def health_check(redis_client: redis.Redis = Depends(get_redis_client)):
    """Health check endpoint."""

    # Verifica Redis
    redis_connected = False
    if redis_client:
        try:
            redis_connected = redis_client.ping()
        except Exception as e:
            logger.warning(f"Redis health check fallito: {e}")
            redis_connected = False

    # Calcola uptime
    uptime = time.time() - _start_time

    # Determina status generale
    status_value = "healthy" if True else "unhealthy"  # Potresti aggiungere più controlli

    response = HealthResponse(
        status=status_value,
        version=settings.API_VERSION,
        redis_connected=redis_connected,
        uptime_seconds=uptime,
        timestamp=datetime.now()
    )

    return response


@router.get(
    "/",
    summary="Root endpoint",
    description="Endpoint root che restituisce informazioni base sull'API"
)
async def root():
    """Root endpoint."""
    return {
        "name": settings.API_TITLE,
        "version": settings.API_VERSION,
        "description": "API per web scraping di annunci da Subito.it",
        "documentation": "/docs",
        "health": "/health",
        "endpoints": {
            "search": "POST /api/v1/search",
            "get_results": "GET /api/v1/results/{search_id}",
            "get_listing": "GET /api/v1/listing/{listing_id}",
            "report_scam": "POST /api/v1/report-scam",
            "get_report": "GET /api/v1/reports/{report_id}"
        }
    }
