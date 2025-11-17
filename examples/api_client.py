"""Esempio client per interagire con l'API."""

import requests
import json
from typing import Optional, Dict, List


class SubitoScraperClient:
    """Client Python per l'API Subito Scraper."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Inizializza il client.

        Args:
            base_url: URL base dell'API
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    def search(
        self,
        query: str,
        categoria: Optional[str] = None,
        prezzo_max: Optional[float] = None,
        regione: Optional[str] = None,
        max_pages: int = 1
    ) -> Dict:
        """
        Cerca annunci.

        Args:
            query: Query di ricerca
            categoria: Categoria
            prezzo_max: Prezzo massimo
            regione: Regione
            max_pages: Numero pagine

        Returns:
            Dict con i risultati
        """
        url = f"{self.base_url}/api/v1/search"

        payload = {
            "query": query,
            "max_pages": max_pages
        }

        if categoria:
            payload["categoria"] = categoria
        if prezzo_max:
            payload["prezzo_max"] = prezzo_max
        if regione:
            payload["regione"] = regione

        response = self.session.post(url, json=payload)
        response.raise_for_status()

        return response.json()

    def get_results(self, search_id: str) -> Dict:
        """
        Recupera risultati per search_id.

        Args:
            search_id: ID della ricerca

        Returns:
            Dict con i risultati
        """
        url = f"{self.base_url}/api/v1/results/{search_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_listing(self, listing_id: str) -> Dict:
        """
        Recupera dettagli listing.

        Args:
            listing_id: ID dell'annuncio

        Returns:
            Dict con i dettagli
        """
        url = f"{self.base_url}/api/v1/listing/{listing_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def report_scam(
        self,
        listing_id: str,
        listing_url: str,
        reason: str,
        reporter_email: Optional[str] = None,
        additional_info: Optional[str] = None
    ) -> Dict:
        """
        Segnala annuncio sospetto.

        Args:
            listing_id: ID annuncio
            listing_url: URL annuncio
            reason: Motivo segnalazione
            reporter_email: Email segnalante
            additional_info: Info aggiuntive

        Returns:
            Dict con conferma
        """
        url = f"{self.base_url}/api/v1/report-scam"

        payload = {
            "listing_id": listing_id,
            "listing_url": listing_url,
            "reason": reason
        }

        if reporter_email:
            payload["reporter_email"] = reporter_email
        if additional_info:
            payload["additional_info"] = additional_info

        response = self.session.post(url, json=payload)
        response.raise_for_status()

        return response.json()

    def health_check(self) -> Dict:
        """
        Verifica stato API.

        Returns:
            Dict con status
        """
        url = f"{self.base_url}/health"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()


def main():
    """Esempi di utilizzo del client."""

    # Crea client
    client = SubitoScraperClient("http://localhost:8000")

    print("="*60)
    print("Client API - Subito.it Scraper")
    print("="*60)

    # 1. Health check
    print("\n1. Health Check")
    print("-"*60)
    try:
        health = client.health_check()
        print(f"Status: {health['status']}")
        print(f"Version: {health['version']}")
        print(f"Redis: {'✓ Connesso' if health['redis_connected'] else '✗ Non connesso'}")
    except Exception as e:
        print(f"Errore: {e}")
        return

    # 2. Ricerca annunci
    print("\n2. Ricerca Annunci")
    print("-"*60)
    print("Cercando 'iPhone 13' in categoria 'telefonia'...")

    try:
        results = client.search(
            query="iphone 13",
            categoria="telefonia",
            prezzo_max=600.0,
            max_pages=1
        )

        print(f"✓ Trovati {results['total_results']} annunci")
        print(f"  Cached: {results['cached']}")
        print(f"  Tempo: {results['execution_time_ms']:.2f}ms")

        # Mostra primi 3 risultati
        print("\nPrimi 3 risultati:")
        for i, listing in enumerate(results['results'][:3], 1):
            print(f"\n  {i}. {listing['title']}")
            print(f"     Prezzo: {listing['price_text'] or listing['price']}")
            print(f"     Località: {listing['location'] or 'N/A'}")
            print(f"     Link: {listing['link']}")

        # 3. Segnalazione (esempio - NON eseguire su annunci reali)
        if results['results']:
            print("\n3. Esempio Segnalazione")
            print("-"*60)
            print("(Esempio - non viene effettivamente inviata)")

            first_listing = results['results'][0]
            print(f"Segnalazione per: {first_listing['title']}")

            # Decommenta per testare realmente
            # report = client.report_scam(
            #     listing_id=first_listing['listing_id'],
            #     listing_url=first_listing['link'],
            #     reason="Test segnalazione da API client",
            #     reporter_email="test@example.com"
            # )
            # print(f"✓ Segnalazione creata: {report['report_id']}")

    except requests.exceptions.HTTPError as e:
        print(f"Errore HTTP: {e}")
        if e.response.status_code == 429:
            print("Rate limit superato! Attendi prima di riprovare.")
        else:
            print(f"Response: {e.response.text}")
    except Exception as e:
        print(f"Errore: {e}")

    print("\n" + "="*60)
    print("Test completato!")
    print("="*60)


if __name__ == "__main__":
    main()
