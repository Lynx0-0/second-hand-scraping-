"""Esempio base di utilizzo dello scraper per Subito.it."""

import sys
from pathlib import Path

# Aggiungi parent directory al path per importare i moduli
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraper.subito_scraper import SubitoScraper
from src.config.settings import ScraperConfig
from src.utils.logger import setup_logger
import json


def main():
    """Esempio base di scraping."""

    # Setup logger
    logger = setup_logger(name='example', level='INFO')

    # Configura lo scraper
    config = ScraperConfig(
        requests_per_second=0.5,  # Max 1 richiesta ogni 2 secondi
        min_delay=2.0,
        max_delay=4.0,
        max_retries=3,
        save_html=False,  # Impostare True per salvare HTML
        save_json=True
    )

    # Crea lo scraper
    with SubitoScraper(config) as scraper:
        logger.info("=== Esempio 1: Scraping da URL specifica ===")

        # URL di esempio (sostituire con URL reale)
        # url = "https://www.subito.it/annunci-italia/vendita/usato/"

        # Per questo esempio, usiamo il metodo search
        logger.info("\n=== Esempio 2: Ricerca per query ===")

        # Cerca "iphone" nella categoria elettronica
        listings = scraper.search(
            query="iphone",
            category="telefonia",
            max_pages=1  # Cerca solo prima pagina
        )

        logger.info(f"\nTrovati {len(listings)} annunci")

        # Mostra i primi 5 annunci
        for i, listing in enumerate(listings[:5], 1):
            print(f"\n--- Annuncio {i} ---")
            print(f"Titolo: {listing.title}")
            print(f"Prezzo: {listing.price_text or listing.price}")
            print(f"Link: {listing.link}")
            print(f"Foto: {len(listing.photos)} immagine/i")
            if listing.location:
                print(f"Località: {listing.location}")

        # Estrai dettagli completi per il primo annuncio
        if listings:
            logger.info("\n=== Esempio 3: Estrazione dettagli completi ===")

            first_listing = listings[0]
            detailed_listing = scraper.scrape_listing_details(first_listing)

            print(f"\n--- Dettagli completi ---")
            print(f"Titolo: {detailed_listing.title}")
            print(f"Prezzo: {detailed_listing.price_text or detailed_listing.price}")
            print(f"Descrizione: {detailed_listing.description[:200] if detailed_listing.description else 'N/A'}...")
            print(f"Foto: {len(detailed_listing.photos)}")
            print(f"Link: {detailed_listing.link}")

        # Salva risultati in JSON
        if config.save_json:
            output_dir = Path(config.output_dir)
            output_dir.mkdir(exist_ok=True)

            output_file = output_dir / 'listings.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(
                    [listing.to_dict() for listing in listings],
                    f,
                    ensure_ascii=False,
                    indent=2
                )
            logger.info(f"\nRisultati salvati in: {output_file}")

        # Mostra statistiche
        stats = scraper.get_stats()
        print("\n=== Statistiche ===")
        print(f"Richieste totali: {stats['requests']}")
        print(f"Richieste riuscite: {stats['successful']}")
        print(f"Richieste fallite: {stats['failed']}")
        print(f"Annunci trovati: {stats['listings_found']}")


if __name__ == "__main__":
    main()
