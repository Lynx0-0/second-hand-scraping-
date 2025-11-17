"""Router per segnalazioni annunci sospetti."""

from datetime import datetime
import logging

from fastapi import APIRouter, HTTPException, status

from api.models.requests import ReportScamRequest
from api.models.responses import ReportScamResponse
from api.services.reports import ReportService
from api.core.config import settings


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["reports"])

# Istanza globale del servizio segnalazioni
report_service = ReportService(settings.REPORTS_DB_PATH)


@router.post(
    "/report-scam",
    response_model=ReportScamResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Segnala un annuncio sospetto",
    description="""
    Permette di segnalare annunci potenzialmente fraudolenti o sospetti.

    **Parametri richiesti:**
    - **listing_id**: ID univoco dell'annuncio da segnalare
    - **listing_url**: URL completo dell'annuncio (deve essere di subito.it)
    - **reason**: Motivo della segnalazione (min 10 caratteri)

    **Parametri opzionali:**
    - **reporter_email**: Email del segnalante per follow-up
    - **additional_info**: Informazioni aggiuntive sulla segnalazione

    **Esempi di motivi validi:**
    - "Prezzo troppo basso rispetto al mercato, probabile truffa"
    - "Il venditore chiede pagamento anticipato su carta prepagata"
    - "Le foto sono rubate da altri siti web"
    - "Annuncio duplicato con dati contraddittori"

    **Note:**
    - Tutte le segnalazioni vengono registrate e revisionate
    - Non abusare del sistema con segnalazioni false
    """
)
async def report_scam(request: ReportScamRequest):
    """Endpoint per segnalare annunci sospetti."""
    logger.info(
        f"Nuova segnalazione ricevuta per listing_id: {request.listing_id}"
    )

    try:
        # Verifica se l'annuncio è già stato segnalato
        existing_reports = report_service.get_reports_by_listing(request.listing_id)

        if len(existing_reports) >= 5:
            logger.warning(
                f"Listing {request.listing_id} già segnalato {len(existing_reports)} volte"
            )
            # Permettiamo comunque la segnalazione ma informiamo l'utente
            # In produzione, potresti voler limitare o bloccare

        # Crea la segnalazione
        report = report_service.create_report(
            listing_id=request.listing_id,
            listing_url=str(request.listing_url),
            reason=request.reason,
            reporter_email=request.reporter_email,
            additional_info=request.additional_info
        )

        logger.info(f"Segnalazione creata con successo: {report['report_id']}")

        # Prepara risposta
        response = ReportScamResponse(
            report_id=report['report_id'],
            listing_id=report['listing_id'],
            status=report['status'],
            message="Segnalazione ricevuta e registrata correttamente. Grazie per il contributo!",
            created_at=datetime.fromisoformat(report['created_at'])
        )

        return response

    except Exception as e:
        logger.error(f"Errore creazione segnalazione: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "ReportCreationError",
                "message": "Impossibile creare la segnalazione",
                "detail": str(e)
            }
        )


@router.get(
    "/reports/{report_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Recupera una segnalazione per ID",
    description="""
    Recupera i dettagli di una segnalazione specifica.

    **Parametri:**
    - **report_id**: ID univoco della segnalazione

    **Note:**
    - Restituisce 404 se la segnalazione non esiste
    """
)
async def get_report(report_id: str):
    """Endpoint per recuperare una segnalazione."""
    logger.info(f"Richiesta dettagli segnalazione: {report_id}")

    report = report_service.get_report(report_id)

    if not report:
        logger.warning(f"Segnalazione non trovata: {report_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "NotFound",
                "message": f"Segnalazione non trovata: {report_id}"
            }
        )

    return report


@router.get(
    "/reports/listing/{listing_id}",
    response_model=list,
    status_code=status.HTTP_200_OK,
    summary="Recupera tutte le segnalazioni per un annuncio",
    description="""
    Recupera tutte le segnalazioni relative a uno specifico annuncio.

    **Parametri:**
    - **listing_id**: ID dell'annuncio

    **Restituisce:**
    - Lista di segnalazioni (può essere vuota se l'annuncio non è mai stato segnalato)
    """
)
async def get_reports_by_listing(listing_id: str):
    """Endpoint per recuperare segnalazioni per un annuncio."""
    logger.info(f"Richiesta segnalazioni per listing: {listing_id}")

    reports = report_service.get_reports_by_listing(listing_id)

    logger.info(f"Trovate {len(reports)} segnalazioni per listing {listing_id}")

    return reports


@router.get(
    "/reports",
    response_model=list,
    status_code=status.HTTP_200_OK,
    summary="Recupera tutte le segnalazioni",
    description="""
    Recupera tutte le segnalazioni registrate nel sistema.

    **Query Parameters:**
    - **status**: Filtra per status (opzionale)
    - **limit**: Numero massimo di risultati (default: 100, max: 500)

    **Note:**
    - Le segnalazioni sono ordinate per data (più recenti prima)
    """
)
async def get_all_reports(
    status_filter: str = None,
    limit: int = 100
):
    """Endpoint per recuperare tutte le segnalazioni."""
    if limit > 500:
        limit = 500

    logger.info(f"Richiesta tutte le segnalazioni (status={status_filter}, limit={limit})")

    reports = report_service.get_all_reports(
        status=status_filter,
        limit=limit
    )

    logger.info(f"Trovate {len(reports)} segnalazioni")

    return reports


@router.get(
    "/reports/stats",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Ottieni statistiche segnalazioni",
    description="""
    Restituisce statistiche aggregate sulle segnalazioni.

    **Restituisce:**
    - Numero totale di segnalazioni
    - Distribuzione per status
    """
)
async def get_reports_stats():
    """Endpoint per statistiche segnalazioni."""
    logger.info("Richiesta statistiche segnalazioni")

    stats = report_service.get_stats()

    return stats
