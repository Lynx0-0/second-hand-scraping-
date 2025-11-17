#!/usr/bin/env python3
"""Script di test per verificare il funzionamento dello scraper."""

import sys
import logging
from pathlib import Path

# Aggiungi src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from scraper.subito_scraper import SubitoScraper
from config.settings import ScraperConfig

# Configura logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_basic_search():
    """Test ricerca base."""
    logger.info("=" * 80)
    logger.info("TEST 1: Ricerca base - 1 pagina")
    logger.info("=" * 80)

    # Configurazione con delay aumentati
    config = ScraperConfig()

    logger.info(f"Configurazione:")
    logger.info(f"  - Delay minimo: {config.min_delay}s")
    logger.info(f"  - Delay massimo: {config.max_delay}s")
    logger.info(f"  - User agents disponibili: {len(config.user_agents)}")
    logger.info(f"  - Max retries: {config.max_retries}")

    with SubitoScraper(config) as scraper:
        # Test con una ricerca semplice, solo 1 pagina
        query = "bicicletta"
        logger.info(f"\nCerco: '{query}' (max 1 pagina)")

        try:
            listings = scraper.search(
                query=query,
                max_pages=1  # Solo 1 pagina per test veloce
            )

            # Risultati
            stats = scraper.get_stats()
            logger.info(f"\n{'=' * 80}")
            logger.info("RISULTATI TEST:")
            logger.info(f"{'=' * 80}")
            logger.info(f"✓ Annunci trovati: {len(listings)}")
            logger.info(f"  - Richieste totali: {stats['requests']}")
            logger.info(f"  - Richieste riuscite: {stats['successful']}")
            logger.info(f"  - Richieste fallite: {stats['failed']}")

            if listings:
                logger.info(f"\n📋 Primi 3 annunci:")
                for i, listing in enumerate(listings[:3], 1):
                    logger.info(f"\n  {i}. {listing.title}")
                    logger.info(f"     Prezzo: {listing.price_text or 'N/A'}")
                    logger.info(f"     Location: {listing.location or 'N/A'}")
                    logger.info(f"     Link: {listing.link}")

                return True, "Test completato con successo"
            else:
                return False, "Nessun annuncio trovato - possibile blocco"

        except Exception as e:
            logger.error(f"❌ Errore durante il test: {e}")
            return False, str(e)


def test_with_filters():
    """Test ricerca con filtri."""
    logger.info("\n" + "=" * 80)
    logger.info("TEST 2: Ricerca con filtri")
    logger.info("=" * 80)

    config = ScraperConfig()

    with SubitoScraper(config) as scraper:
        query = "iphone"
        category = "telefonia"

        logger.info(f"\nCerco: '{query}' in categoria '{category}' (max 1 pagina)")

        try:
            listings = scraper.search(
                query=query,
                category=category,
                max_pages=1
            )

            stats = scraper.get_stats()
            logger.info(f"\n{'=' * 80}")
            logger.info("RISULTATI TEST:")
            logger.info(f"{'=' * 80}")
            logger.info(f"✓ Annunci trovati: {len(listings)}")
            logger.info(f"  - Richieste totali: {stats['requests']}")
            logger.info(f"  - Richieste riuscite: {stats['successful']}")
            logger.info(f"  - Richieste fallite: {stats['failed']}")

            if listings:
                return True, "Test con filtri completato con successo"
            else:
                return False, "Nessun annuncio trovato con filtri - possibile blocco"

        except Exception as e:
            logger.error(f"❌ Errore durante il test: {e}")
            return False, str(e)


def main():
    """Esegue tutti i test."""
    logger.info("🚀 Avvio test dello scraper Subito.it")
    logger.info(f"{'=' * 80}\n")

    results = []

    # Test 1: Ricerca base
    success, message = test_basic_search()
    results.append(("Ricerca base", success, message))

    # Pausa tra i test per evitare rate limiting
    import time
    logger.info(f"\n⏳ Pausa di 10 secondi prima del prossimo test...\n")
    time.sleep(10)

    # Test 2: Ricerca con filtri
    success, message = test_with_filters()
    results.append(("Ricerca con filtri", success, message))

    # Riepilogo finale
    logger.info(f"\n{'=' * 80}")
    logger.info("RIEPILOGO FINALE")
    logger.info(f"{'=' * 80}")

    for test_name, success, message in results:
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{status} - {test_name}: {message}")

    # Exit code
    all_passed = all(result[1] for result in results)
    if all_passed:
        logger.info(f"\n{'=' * 80}")
        logger.info("🎉 TUTTI I TEST SONO PASSATI!")
        logger.info(f"{'=' * 80}")
        logger.info("\n💡 Suggerimenti:")
        logger.info("   - Lo scraper sembra funzionare correttamente")
        logger.info("   - Se ricevi ancora blocchi, considera:")
        logger.info("     1. Aumentare ulteriormente i delay in settings.py")
        logger.info("     2. Ridurre il numero di pagine per ricerca")
        logger.info("     3. Usare un proxy o VPN se necessario")
        logger.info("     4. Attendere qualche ora se sei stato bloccato")
        return 0
    else:
        logger.info(f"\n{'=' * 80}")
        logger.info("⚠️  ALCUNI TEST SONO FALLITI")
        logger.info(f"{'=' * 80}")
        logger.info("\n🔧 Possibili soluzioni:")
        logger.info("   1. Verifica la connessione internet")
        logger.info("   2. Controlla se Subito.it è raggiungibile nel browser")
        logger.info("   3. Se hai ricevuto errori HTTP 403/429:")
        logger.info("      - Il tuo IP potrebbe essere temporaneamente bloccato")
        logger.info("      - Attendi almeno 1-2 ore prima di riprovare")
        logger.info("      - Considera l'uso di un proxy o VPN")
        logger.info("   4. Verifica i log sopra per dettagli specifici")
        return 1


if __name__ == '__main__':
    sys.exit(main())
