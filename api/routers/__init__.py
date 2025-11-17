"""Routers API."""

from .search import router as search_router
from .reports import router as reports_router
from .health import router as health_router

__all__ = ['search_router', 'reports_router', 'health_router']
