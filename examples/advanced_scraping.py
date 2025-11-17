"""Esempio avanzato con configurazione custom e gestione errori."""

import sys
from pathlib import Path
import json
import csv

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraper.subito_scraper import SubitoScraper
from src.config.settings import ScraperConfig
from src.utils.logger import setup_logger


def save_to_csv(listings, filename: str):
    """Salva annunci in formato CSV."""
    if not listings:
        return

    output_path = Path('output') / filename
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['title', 'price', 'price_text', 'location', 'link', 'num_photos']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        for listing in listings:
            writer.writerow({
                'title': listing.title,
                'price': listing.price,
                'price_text': listing.price_text,
                'location': listing.location,
                'link': listing.link,
                'num_photos': len(listing.photos)
            })

    print(f"CSV salvato: {output_path}")


def scrape_multiple_queries():
    """Scrape per multiple query di ricerca."""

    logger = setup_logger(name='advanced_example', level='DEBUG')

    # Configurazione custom
    config = ScraperConfig(
        requests_per_second=0.33,  # ~1 richiesta ogni 3 secondi (più conservativo)
        min_delay=3.0,
        max_delay=6.0,
        max_retries=5,
        retry_delay=10.0,
        save_html=True,  # Salva HTML per debugging
        save_json=True
    )

    # Query da cercare
    searches = [
        {"query": "macbook", "category": "informatica"},
        {"query": "playstation 5", "category": "console-videogiochi"},
        {"query": "bicicletta", "category": "biciclette"},
    ]

    all_results = {}

    with SubitoScraper(config) as scraper:
        for search in searches:
            search_name = f"{search['query']}_{search['category']}"
            logger.info(f"\n{'='*60}")
            logger.info(f"Ricerca: {search_name}")
            logger.info(f"{'='*60}")

            try:
                listings = scraper.search(
                    query=search['query'],
                    category=search['category'],
                    max_pages=2  # Prime 2 pagine
                )

                all_results[search_name] = listings

                logger.info(f"Trovati {len(listings)} annunci per '{search_name}'")

                # Mostra alcuni risultati
                for i, listing in enumerate(listings[:3], 1):
                    print(f"\n{i}. {listing.title}")
                    print(f"   Prezzo: {listing.price_text or listing.price}")
                    print(f"   Link: {listing.link}")

                # Salva risultati in CSV
                save_to_csv(listings, f'{search_name}.csv')

            except Exception as e:
                logger.error(f"Errore durante ricerca '{search_name}': {e}")
                continue

        # Salva tutti i risultati in un unico JSON
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)

        all_listings_file = output_dir / 'all_listings.json'
        with open(all_listings_file, 'w', encoding='utf-8') as f:
            json_data = {
                name: [listing.to_dict() for listing in listings]
                for name, listings in all_results.items()
            }
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        logger.info(f"\n\nTutti i risultati salvati in: {all_listings_file}")

        # Statistiche finali
        stats = scraper.get_stats()
        print(f"\n{'='*60}")
        print("STATISTICHE FINALI")
        print(f"{'='*60}")
        print(f"Ricerche effettuate: {len(searches)}")
        print(f"Richieste HTTP totali: {stats['requests']}")
        print(f"Richieste riuscite: {stats['successful']}")
        print(f"Richieste fallite: {stats['failed']}")
        print(f"Annunci totali trovati: {stats['listings_found']}")
        print(f"Success rate: {(stats['successful']/stats['requests']*100):.1f}%")


def scrape_with_details():
    """Scrape con estrazione dettagli completi."""

    logger = setup_logger(name='detailed_scraping', level='INFO')

    config = ScraperConfig(
        requests_per_second=0.25,  # Molto conservativo per dettagli
        min_delay=4.0,
        max_delay=7.0
    )

    with SubitoScraper(config) as scraper:
        logger.info("Ricerca annunci...")

        # Cerca annunci
        listings = scraper.search(
            query="chitarra",
            category="strumenti-musicali",
            max_pages=1
        )

        logger.info(f"Trovati {len(listings)} annunci")

        # Estrai dettagli solo per i primi 5
        detailed_listings = []
        for i, listing in enumerate(listings[:5], 1):
            logger.info(f"\nEstrazione dettagli {i}/5: {listing.title[:50]}...")

            try:
                detailed = scraper.scrape_listing_details(listing)
                detailed_listings.append(detailed)

                print(f"\n{'='*60}")
                print(f"Annuncio {i}")
                print(f"{'='*60}")
                print(f"Titolo: {detailed.title}")
                print(f"Prezzo: {detailed.price_text or detailed.price}")
                print(f"Descrizione: {detailed.description[:150] if detailed.description else 'N/A'}...")
                print(f"Foto: {len(detailed.photos)}")
                print(f"Venditore: {detailed.seller_name or 'N/A'}")
                print(f"Località: {detailed.location or 'N/A'}")

            except Exception as e:
                logger.error(f"Errore estrazione dettagli: {e}")
                continue

        # Salva dettagli
        output_file = Path('output') / 'detailed_listings.json'
        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(
                [listing.to_dict() for listing in detailed_listings],
                f,
                ensure_ascii=False,
                indent=2
            )

        logger.info(f"\nDettagli salvati in: {output_file}")


if __name__ == "__main__":
    print("Seleziona esempio:")
    print("1. Scraping multiple query")
    print("2. Scraping con dettagli completi")

    choice = input("\nScelta (1 o 2): ").strip()

    if choice == "1":
        scrape_multiple_queries()
    elif choice == "2":
        scrape_with_details()
    else:
        print("Scelta non valida")
