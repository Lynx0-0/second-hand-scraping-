"""Router per endpoint di ricerca."""

import time
import uuid
from datetime import datetime
from typing import List
import logging

from fastapi import APIRouter, Depends, HTTPException, status
import redis

from api.models.requests import SearchRequest, PlatformEnum
from api.models.responses import SearchResponse, ListingResponse
from api.core.dependencies import get_redis_client
from api.core.config import settings
from api.services.cache import CacheService
from src.scraper.subito_scraper import SubitoScraper
from src.scraper.ebay_scraper import EbayScraper
from src.config.settings import ScraperConfig
from src.models.listing import Listing


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["search"])


def _create_scraper(platform: PlatformEnum):
    """
    Crea l'istanza dello scraper corretto in base alla piattaforma.

    Args:
        platform: Piattaforma richiesta

    Returns:
        Scraper instance (SubitoScraper o EbayScraper)
    """
    config = ScraperConfig(
        requests_per_second=settings.SCRAPER_REQUESTS_PER_SECOND,
        min_delay=settings.SCRAPER_MIN_DELAY,
        max_delay=settings.SCRAPER_MAX_DELAY,
        max_retries=settings.SCRAPER_MAX_RETRIES,
        request_timeout=settings.SCRAPER_TIMEOUT,
        log_level=settings.LOG_LEVEL
    )

    if platform == PlatformEnum.EBAY:
        return EbayScraper(config)
    else:  # Default: Subito
        return SubitoScraper(config)


def _filter_by_price(listings: List[Listing], max_price: float) -> List[Listing]:
    """
    Filtra annunci per prezzo massimo.

    Args:
        listings: Lista annunci
        max_price: Prezzo massimo

    Returns:
        Lista filtrata
    """
    filtered = []
    for listing in listings:
        if listing.price is not None:
            if listing.price <= max_price:
                filtered.append(listing)
        else:
            # Include annunci senza prezzo (es. "Gratis", "Contattami")
            filtered.append(listing)

    return filtered


def _convert_listing_to_response(listing: Listing) -> ListingResponse:
    """
    Converte Listing model in ListingResponse.

    Args:
        listing: Listing object

    Returns:
        ListingResponse object
    """
    return ListingResponse(
        listing_id=listing.listing_id,
        title=listing.title,
        price=listing.price,
        price_text=listing.price_text,
        description=listing.description,
        link=listing.link,
        photos=listing.photos,
        location=listing.location,
        category=listing.category,
        posted_date=listing.posted_date,
        seller_name=listing.seller_name,
        seller_type=listing.seller_type,
        scraped_at=listing.scraped_at
    )


@router.post(
    "/search",
    response_model=SearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Cerca annunci su Subito.it",
    description="""
    Cerca annunci su Subito.it con filtri opzionali.

    I risultati vengono automaticamente cachati per migliorare le performance.
    Le ricerche identiche restituiscono risultati dalla cache per 1 ora.

    **Parametri:**
    - **query**: Parola chiave di ricerca (obbligatorio, 2-100 caratteri)
    - **categoria**: Categoria specifica (opzionale)
    - **prezzo_max**: Prezzo massimo in euro (opzionale)
    - **regione**: Regione geografica (opzionale)
    - **max_pages**: Numero di pagine da scansionare, max 5 (default: 1)

    **Note:**
    - Il rate limiting limita le richieste a 10 al minuto per IP
    - Rispetta le policy di Subito.it e usa delay appropriati
    """
)
async def search_listings(
    request: SearchRequest,
    redis_client: redis.Redis = Depends(get_redis_client),
    scraper: SubitoScraper = Depends(get_scraper)
):
    """Endpoint per cercare annunci."""
    start_time = time.time()

    logger.info(
        f"Ricerca richiesta: query='{request.query}', "
        f"categoria={request.categoria}, prezzo_max={request.prezzo_max}"
    )

    # Inizializza cache service
    cache = CacheService(redis_client)

    # Prova a recuperare da cache
    cached_results = cache.get_search_results(
        query=request.query,
        categoria=request.categoria.value if request.categoria else None,
        prezzo_max=request.prezzo_max,
        regione=request.regione
    )

    if cached_results:
        logger.info("Risultati recuperati da cache")
        execution_time = (time.time() - start_time) * 1000

        # Marca come cached
        cached_results['cached'] = True
        cached_results['execution_time_ms'] = execution_time

        return SearchResponse(**cached_results)

    # Non in cache, esegui scraping
    try:
        logger.info("Esecuzione scraping...")

        # Esegui ricerca
        listings = scraper.search(
            query=request.query,
            category=request.categoria.value if request.categoria else None,
            region=request.regione,
            max_pages=request.max_pages
        )

        logger.info(f"Trovati {len(listings)} annunci")

        # Filtra per prezzo se richiesto
        if request.prezzo_max is not None:
            original_count = len(listings)
            listings = _filter_by_price(listings, request.prezzo_max)
            logger.info(
                f"Filtrati per prezzo: {original_count} -> {len(listings)} annunci"
            )

        # Converti in response model
        listing_responses = [
            _convert_listing_to_response(listing)
            for listing in listings
        ]

        # Genera ID univoco per la ricerca
        search_id = str(uuid.uuid4())

        # Prepara risposta
        response_data = {
            "search_id": search_id,
            "query": request.query,
            "categoria": request.categoria.value if request.categoria else None,
            "total_results": len(listing_responses),
            "results": [resp.dict() for resp in listing_responses],
            "cached": False,
            "scraped_at": datetime.now(),
            "execution_time_ms": (time.time() - start_time) * 1000
        }

        # Salva in cache
        cache.set_search_results(
            results=response_data,
            query=request.query,
            categoria=request.categoria.value if request.categoria else None,
            prezzo_max=request.prezzo_max,
            regione=request.regione
        )

        # Salva anche i singoli listing in cache
        for listing in listings:
            if listing.listing_id:
                cache.set_listing(
                    listing_id=listing.listing_id,
                    listing_data=listing.to_dict()
                )

        logger.info(f"Ricerca completata in {response_data['execution_time_ms']:.2f}ms")

        return SearchResponse(**response_data)

    except Exception as e:
        logger.error(f"Errore durante scraping: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "ScrapingError",
                "message": "Errore durante l'estrazione degli annunci",
                "detail": str(e)
            }
        )


@router.get(
    "/results/{search_id}",
    response_model=SearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Recupera risultati ricerca per ID",
    description="""
    Recupera i risultati di una ricerca precedente usando il search_id.

    **Parametri:**
    - **search_id**: ID univoco della ricerca (UUID)

    **Note:**
    - I risultati sono disponibili per 1 ora dalla ricerca originale
    - Restituisce 404 se i risultati non sono più in cache
    """
)
async def get_search_results(
    search_id: str,
    redis_client: redis.Redis = Depends(get_redis_client)
):
    """Endpoint per recuperare risultati ricerca per ID."""
    logger.info(f"Richiesta risultati per search_id: {search_id}")

    cache = CacheService(redis_client)

    # Cerca in cache con chiave specifica
    key = f"search_result:{search_id}"
    cached_data = cache.get(key)

    if cached_data:
        logger.info(f"Risultati trovati per search_id: {search_id}")
        cached_data['cached'] = True
        return SearchResponse(**cached_data)

    # Non trovato
    logger.warning(f"Risultati non trovati per search_id: {search_id}")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "error": "NotFound",
            "message": f"Risultati non trovati per search_id: {search_id}",
            "detail": "I risultati potrebbero essere scaduti (TTL: 1 ora)"
        }
    )


@router.get(
    "/listing/{listing_id}",
    response_model=ListingResponse,
    status_code=status.HTTP_200_OK,
    summary="Recupera dettagli annuncio per ID",
    description="""
    Recupera i dettagli completi di un annuncio specifico.

    **Parametri:**
    - **listing_id**: ID univoco dell'annuncio

    **Note:**
    - I dettagli sono disponibili in cache per 2 ore
    - Se non in cache, viene eseguito scraping real-time (più lento)
    """
)
async def get_listing_details(
    listing_id: str,
    redis_client: redis.Redis = Depends(get_redis_client),
    scraper: SubitoScraper = Depends(get_scraper)
):
    """Endpoint per recuperare dettagli annuncio."""
    logger.info(f"Richiesta dettagli per listing_id: {listing_id}")

    cache = CacheService(redis_client)

    # Prova cache
    cached_listing = cache.get_listing(listing_id)

    if cached_listing:
        logger.info(f"Listing trovato in cache: {listing_id}")
        return ListingResponse(**cached_listing)

    # Non in cache, bisognerebbe fare scraping della singola pagina
    # Per ora ritorniamo 404
    logger.warning(f"Listing non trovato in cache: {listing_id}")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "error": "NotFound",
            "message": f"Annuncio non trovato: {listing_id}",
            "detail": "Esegui prima una ricerca per popolare la cache"
        }
    )
