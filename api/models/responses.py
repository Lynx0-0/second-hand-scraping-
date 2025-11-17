"""Modelli Pydantic per le risposte API."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ListingResponse(BaseModel):
    """Modello per un singolo annuncio nella risposta."""

    listing_id: Optional[str] = Field(None, description="ID dell'annuncio")
    title: str = Field(..., description="Titolo dell'annuncio")
    price: Optional[float] = Field(None, description="Prezzo numerico")
    price_text: Optional[str] = Field(None, description="Prezzo come testo")
    description: Optional[str] = Field(None, description="Descrizione completa")
    link: Optional[str] = Field(None, description="URL dell'annuncio")
    photos: List[str] = Field(default_factory=list, description="Lista URL foto")
    location: Optional[str] = Field(None, description="Località")
    category: Optional[str] = Field(None, description="Categoria")
    posted_date: Optional[str] = Field(None, description="Data pubblicazione")
    seller_name: Optional[str] = Field(None, description="Nome venditore")
    seller_type: Optional[str] = Field(None, description="Tipo venditore")
    source: str = Field(default="subito", description="Piattaforma di origine (subito/ebay)")
    condition: Optional[str] = Field(None, description="Condizione articolo (nuovo/usato)")
    shipping: Optional[str] = Field(None, description="Info spedizione")
    scraped_at: datetime = Field(..., description="Timestamp scraping")

    class Config:
        """Configurazione Pydantic."""
        schema_extra = {
            "example": {
                "listing_id": "12345678",
                "title": "iPhone 13 128GB Nero",
                "price": 450.0,
                "price_text": "450 €",
                "description": "iPhone 13 in ottime condizioni...",
                "link": "https://www.subito.it/telefonia/iphone-13-roma-12345678.htm",
                "photos": ["https://example.com/photo1.jpg"],
                "location": "Roma",
                "category": "telefonia",
                "posted_date": "Oggi alle 10:30",
                "seller_name": "Mario Rossi",
                "seller_type": "privato",
                "scraped_at": "2025-11-17T10:00:00"
            }
        }


class SearchResponse(BaseModel):
    """Modello per risposta di ricerca."""

    search_id: str = Field(..., description="ID univoco della ricerca")
    query: str = Field(..., description="Query di ricerca")
    categoria: Optional[str] = Field(None, description="Categoria ricercata")
    platform: str = Field(default="subito", description="Piattaforma cercata (subito/ebay/all)")
    total_results: int = Field(..., description="Numero totale di risultati")
    results: List[ListingResponse] = Field(..., description="Lista annunci trovati")
    cached: bool = Field(False, description="Se i risultati provengono da cache")
    scraped_at: datetime = Field(..., description="Timestamp della ricerca")
    execution_time_ms: float = Field(..., description="Tempo di esecuzione in millisecondi")

    class Config:
        """Configurazione Pydantic."""
        schema_extra = {
            "example": {
                "search_id": "550e8400-e29b-41d4-a716-446655440000",
                "query": "iphone 13",
                "categoria": "telefonia",
                "total_results": 15,
                "results": [],
                "cached": False,
                "scraped_at": "2025-11-17T10:00:00",
                "execution_time_ms": 1234.56
            }
        }


class ReportScamResponse(BaseModel):
    """Modello per risposta di segnalazione."""

    report_id: str = Field(..., description="ID univoco della segnalazione")
    listing_id: str = Field(..., description="ID dell'annuncio segnalato")
    status: str = Field(..., description="Stato della segnalazione")
    message: str = Field(..., description="Messaggio di conferma")
    created_at: datetime = Field(..., description="Timestamp della segnalazione")

    class Config:
        """Configurazione Pydantic."""
        schema_extra = {
            "example": {
                "report_id": "rep_123456789",
                "listing_id": "12345678",
                "status": "received",
                "message": "Segnalazione ricevuta e registrata correttamente",
                "created_at": "2025-11-17T10:00:00"
            }
        }


class ErrorResponse(BaseModel):
    """Modello per risposta di errore."""

    error: str = Field(..., description="Tipo di errore")
    message: str = Field(..., description="Messaggio descrittivo")
    detail: Optional[str] = Field(None, description="Dettagli aggiuntivi")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp dell'errore")

    class Config:
        """Configurazione Pydantic."""
        schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "I dati forniti non sono validi",
                "detail": "Il campo 'query' è obbligatorio",
                "timestamp": "2025-11-17T10:00:00"
            }
        }


class HealthResponse(BaseModel):
    """Modello per health check."""

    status: str = Field(..., description="Stato del servizio")
    version: str = Field(..., description="Versione API")
    redis_connected: bool = Field(..., description="Stato connessione Redis")
    uptime_seconds: float = Field(..., description="Uptime in secondi")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp")

    class Config:
        """Configurazione Pydantic."""
        schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "redis_connected": True,
                "uptime_seconds": 3600.0,
                "timestamp": "2025-11-17T10:00:00"
            }
        }
