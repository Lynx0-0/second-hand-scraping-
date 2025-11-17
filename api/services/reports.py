"""Servizio per gestione segnalazioni."""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
import logging
from threading import Lock

from api.core.config import settings


logger = logging.getLogger(__name__)


class ReportService:
    """Gestisce le segnalazioni di annunci sospetti."""

    def __init__(self, db_path: str = None):
        """
        Inizializza il servizio segnalazioni.

        Args:
            db_path: Path al file JSON per le segnalazioni
        """
        self.db_path = Path(db_path or settings.REPORTS_DB_PATH)
        self._lock = Lock()
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        """Crea il file database se non esiste."""
        try:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

            if not self.db_path.exists():
                self.db_path.write_text(json.dumps([], indent=2), encoding='utf-8')
                logger.info(f"Database segnalazioni creato: {self.db_path}")
        except Exception as e:
            logger.error(f"Errore creazione database segnalazioni: {e}")

    def _load_reports(self) -> List[Dict]:
        """
        Carica tutte le segnalazioni.

        Returns:
            Lista di segnalazioni
        """
        try:
            if self.db_path.exists():
                data = self.db_path.read_text(encoding='utf-8')
                return json.loads(data)
            return []
        except Exception as e:
            logger.error(f"Errore caricamento segnalazioni: {e}")
            return []

    def _save_reports(self, reports: List[Dict]) -> bool:
        """
        Salva le segnalazioni su file.

        Args:
            reports: Lista di segnalazioni

        Returns:
            True se salvato con successo
        """
        try:
            self.db_path.write_text(
                json.dumps(reports, indent=2, default=str),
                encoding='utf-8'
            )
            return True
        except Exception as e:
            logger.error(f"Errore salvataggio segnalazioni: {e}")
            return False

    def create_report(
        self,
        listing_id: str,
        listing_url: str,
        reason: str,
        reporter_email: Optional[str] = None,
        additional_info: Optional[str] = None
    ) -> Dict:
        """
        Crea una nuova segnalazione.

        Args:
            listing_id: ID dell'annuncio
            listing_url: URL dell'annuncio
            reason: Motivo della segnalazione
            reporter_email: Email del segnalante
            additional_info: Info aggiuntive

        Returns:
            Dict con i dati della segnalazione creata
        """
        with self._lock:
            reports = self._load_reports()

            # Genera ID univoco
            report_id = f"rep_{uuid.uuid4().hex[:12]}"

            # Crea segnalazione
            report = {
                "report_id": report_id,
                "listing_id": listing_id,
                "listing_url": listing_url,
                "reason": reason,
                "reporter_email": reporter_email,
                "additional_info": additional_info,
                "status": "received",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }

            reports.append(report)

            # Salva
            if self._save_reports(reports):
                logger.info(f"Segnalazione creata: {report_id} per listing {listing_id}")
                return report
            else:
                raise Exception("Impossibile salvare la segnalazione")

    def get_report(self, report_id: str) -> Optional[Dict]:
        """
        Recupera una segnalazione per ID.

        Args:
            report_id: ID della segnalazione

        Returns:
            Dict con la segnalazione o None
        """
        reports = self._load_reports()
        for report in reports:
            if report.get('report_id') == report_id:
                return report
        return None

    def get_reports_by_listing(self, listing_id: str) -> List[Dict]:
        """
        Recupera tutte le segnalazioni per un annuncio.

        Args:
            listing_id: ID dell'annuncio

        Returns:
            Lista di segnalazioni
        """
        reports = self._load_reports()
        return [r for r in reports if r.get('listing_id') == listing_id]

    def get_all_reports(
        self,
        status: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict]:
        """
        Recupera tutte le segnalazioni.

        Args:
            status: Filtra per status (opzionale)
            limit: Numero massimo di risultati

        Returns:
            Lista di segnalazioni
        """
        reports = self._load_reports()

        if status:
            reports = [r for r in reports if r.get('status') == status]

        # Ordina per data (più recenti prima)
        reports.sort(
            key=lambda x: x.get('created_at', ''),
            reverse=True
        )

        return reports[:limit]

    def update_report_status(
        self,
        report_id: str,
        new_status: str
    ) -> Optional[Dict]:
        """
        Aggiorna lo status di una segnalazione.

        Args:
            report_id: ID della segnalazione
            new_status: Nuovo status

        Returns:
            Segnalazione aggiornata o None
        """
        with self._lock:
            reports = self._load_reports()

            for report in reports:
                if report.get('report_id') == report_id:
                    report['status'] = new_status
                    report['updated_at'] = datetime.now().isoformat()

                    if self._save_reports(reports):
                        logger.info(f"Segnalazione {report_id} aggiornata: {new_status}")
                        return report
                    break

            return None

    def get_stats(self) -> Dict:
        """
        Ottiene statistiche sulle segnalazioni.

        Returns:
            Dict con statistiche
        """
        reports = self._load_reports()

        stats = {
            "total": len(reports),
            "by_status": {}
        }

        # Conta per status
        for report in reports:
            status = report.get('status', 'unknown')
            stats['by_status'][status] = stats['by_status'].get(status, 0) + 1

        return stats
