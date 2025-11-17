"""FastAPI application principale."""

import sys
from pathlib import Path

# Aggiungi root al path per importare src
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import logging
from datetime import datetime

from api.core.config import settings
from api.core.dependencies import close_redis
from api.middleware.rate_limit import RateLimitMiddleware
from api.routers import search_router, reports_router, health_router
from api.models.responses import ErrorResponse
from src.utils.logger import setup_logger


# Setup logging
logger = setup_logger(
    name='api',
    level=settings.LOG_LEVEL,
    log_file='api.log',
    log_to_console=True
)


# Crea applicazione FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# CORS Middleware
if settings.CORS_ENABLED:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )
    logger.info("CORS abilitato")


# Rate Limiting Middleware
app.add_middleware(RateLimitMiddleware)


# Exception Handlers

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler per errori di validazione Pydantic."""
    logger.warning(f"Errore validazione: {exc.errors()}")

    errors = []
    for error in exc.errors():
        field = " -> ".join(str(x) for x in error['loc'])
        errors.append(f"{field}: {error['msg']}")

    error_response = ErrorResponse(
        error="ValidationError",
        message="I dati forniti non sono validi",
        detail="; ".join(errors),
        timestamp=datetime.now()
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.dict()
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handler per ValueError."""
    logger.warning(f"ValueError: {str(exc)}")

    error_response = ErrorResponse(
        error="ValueError",
        message="Valore non valido",
        detail=str(exc),
        timestamp=datetime.now()
    )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=error_response.dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handler per errori generici."""
    logger.error(f"Errore non gestito: {str(exc)}", exc_info=True)

    error_response = ErrorResponse(
        error="InternalServerError",
        message="Si è verificato un errore interno del server",
        detail=str(exc) if settings.DEBUG else "Contatta l'amministratore",
        timestamp=datetime.now()
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.dict()
    )


# Lifecycle Events

@app.on_event("startup")
async def startup_event():
    """Evento di avvio applicazione."""
    logger.info("="*60)
    logger.info(f"{settings.API_TITLE} v{settings.API_VERSION}")
    logger.info("="*60)
    logger.info(f"Environment: {'DEBUG' if settings.DEBUG else 'PRODUCTION'}")
    logger.info(f"Redis: {settings.REDIS_HOST}:{settings.REDIS_PORT}")
    logger.info(f"Rate Limiting: {'Enabled' if settings.RATE_LIMIT_ENABLED else 'Disabled'}")
    logger.info(f"CORS: {'Enabled' if settings.CORS_ENABLED else 'Disabled'}")
    logger.info("="*60)
    logger.info("Applicazione avviata con successo!")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento di chiusura applicazione."""
    logger.info("Chiusura applicazione...")
    close_redis()
    logger.info("Applicazione chiusa")


# Include Routers
app.include_router(health_router)
app.include_router(search_router)
app.include_router(reports_router)


# Main (per esecuzione diretta)
if __name__ == "__main__":
    import uvicorn

    logger.info(f"Avvio server su {settings.HOST}:{settings.PORT}")

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )
