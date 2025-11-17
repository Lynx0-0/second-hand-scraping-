"""Modelli Pydantic per validazione API."""

from .requests import SearchRequest, ReportScamRequest
from .responses import (
    SearchResponse,
    ListingResponse,
    ReportScamResponse,
    ErrorResponse,
    HealthResponse
)

__all__ = [
    'SearchRequest',
    'ReportScamRequest',
    'SearchResponse',
    'ListingResponse',
    'ReportScamResponse',
    'ErrorResponse',
    'HealthResponse'
]
