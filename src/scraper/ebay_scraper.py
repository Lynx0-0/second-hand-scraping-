"""Scraper specifico per eBay.it."""

from typing import List, Optional
from urllib.parse import urljoin, quote_plus
import re
import logging

from .base_scraper import BaseScraper
from ..models.listing import Listing
from ..config.settings import ScraperConfig


logger = logging.getLogger(__name__)


class EbayScraper(BaseScraper):
    """Scraper per il sito eBay.it."""

    def __init__(self, config: Optional[ScraperConfig] = None):
        """Inizializza lo scraper per eBay.it."""
        super().__init__(config)
        self.base_url = 'https://www.ebay.it'

    def scrape_listings(self, url: str, max_pages: int = 1) -> List[Listing]:
        """
        Scrape annunci da eBay.it.

        Args:
            url: URL della pagina di ricerca
            max_pages: Numero massimo di pagine da processare

        Returns:
            Lista di Listing
        """
        all_listings = []

        for page in range(1, max_pages + 1):
            logger.info(f"Scraping eBay pagina {page}/{max_pages}")

            # Costruisci URL con paginazione
            page_url = self._build_page_url(url, page)

            # Fetch della pagina
            response = self.fetch_page(page_url)

            if not response:
                logger.error(f"Impossibile recuperare la pagina {page}")
                break

            # Salva HTML se configurato
            self.save_html(response.text, f"ebay_page_{page}.html")

            # Parse HTML
            soup = self.parse_html(response.text)

            # Estrai annunci
            listings = self._extract_listings_from_page(soup)

            if not listings:
                logger.warning(f"Nessun annuncio trovato nella pagina {page}")
                break

            all_listings.extend(listings)
            self.stats['listings_found'] += len(listings)

            logger.info(f"Trovati {len(listings)} annunci eBay nella pagina {page}")

        logger.info(f"Totale annunci eBay trovati: {len(all_listings)}")
        return all_listings

    def scrape_listing_details(self, listing: Listing) -> Listing:
        """
        Estrae dettagli completi di un singolo annuncio eBay.

        Args:
            listing: Listing con almeno il link

        Returns:
            Listing con tutti i dettagli
        """
        if not listing.link:
            logger.warning("Listing senza link, impossibile estrarre dettagli")
            return listing

        logger.debug(f"Estrazione dettagli eBay per: {listing.link}")

        response = self.fetch_page(listing.link)

        if not response:
            logger.error(f"Impossibile recuperare dettagli per: {listing.link}")
            return listing

        soup = self.parse_html(response.text)

        # Aggiorna il listing con dettagli completi
        listing = self._extract_listing_details(soup, listing)

        return listing

    def _build_page_url(self, base_url: str, page: int) -> str:
        """
        Costruisce URL con paginazione eBay.

        Args:
            base_url: URL base
            page: Numero pagina

        Returns:
            URL con parametro di paginazione
        """
        if page == 1:
            return base_url

        # eBay usa parametro '_pgn' per numero pagina
        separator = '&' if '?' in base_url else '?'
        return f"{base_url}{separator}_pgn={page}"

    def _extract_listings_from_page(self, soup) -> List[Listing]:
        """
        Estrae lista di annunci da una pagina eBay.

        Args:
            soup: BeautifulSoup object della pagina

        Returns:
            Lista di Listing
        """
        listings = []

        # eBay usa diverse strutture. Proviamo i selettori più comuni
        # Prova 1: Cerca items con classe s-item (risultati ricerca)
        items = soup.find_all('div', class_='s-item__wrapper')

        if not items:
            # Prova 2: Altri selettori comuni
            items = soup.find_all('li', class_='s-item')

        if not items:
            # Prova 3: Cerca all items
            items = soup.find_all('div', attrs={'data-view': 'mi:1686|iid:1'})

        logger.debug(f"Trovati {len(items)} potenziali annunci eBay")

        for item in items:
            try:
                listing = self._extract_listing_from_element(item)
                if listing and listing.is_valid():
                    listings.append(listing)
            except Exception as e:
                logger.debug(f"Errore estrazione annuncio eBay: {e}")
                continue

        return listings

    def _extract_listing_from_element(self, element) -> Optional[Listing]:
        """
        Estrae dati di un annuncio eBay da un elemento HTML.

        Args:
            element: Elemento BeautifulSoup

        Returns:
            Listing o None
        """
        # Estrai titolo
        title = None
        title_elem = (
            element.find('div', class_='s-item__title') or
            element.find('h3', class_='s-item__title') or
            element.find('span', role='heading')
        )
        if title_elem:
            title = title_elem.get_text(strip=True)
            # eBay a volte ha "Shop su eBay" come titolo placeholder
            if title.lower() in ['shop on ebay', 'shop su ebay', 'nuova inserzione']:
                return None

        # Estrai link
        link = None
        link_elem = element.find('a', class_='s-item__link', href=True)
        if link_elem:
            link = link_elem['href']
            # Rimuovi parametri di tracking se presenti
            if '?' in link:
                link = link.split('?')[0]

        # Estrai ID annuncio dal link
        listing_id = None
        if link:
            # eBay ID è nel formato /itm/123456789
            match = re.search(r'/itm/(\d+)', link)
            if match:
                listing_id = match.group(1)

        # Estrai prezzo
        price = None
        price_text = None
        price_elem = (
            element.find('span', class_='s-item__price') or
            element.find('span', class_='POSITIVE')
        )
        if price_elem:
            price_text = price_elem.get_text(strip=True)
            # Estrai valore numerico (es. "EUR 299,99" -> 299.99)
            price_match = re.search(r'([\d.,]+)', price_text.replace('.', '').replace(',', '.'))
            if price_match:
                try:
                    price = float(price_match.group(1))
                except ValueError:
                    pass

        # Estrai foto
        photos = []
        img_elem = element.find('img', class_='s-item__image-img')
        if img_elem:
            # eBay usa 'src' per immagini caricate e 'data-src' per lazy loading
            img_src = img_elem.get('src') or img_elem.get('data-src')
            if img_src and not img_src.endswith(('placeholder.jpg', 'placeholder.png')):
                photos.append(img_src)

        # Estrai location
        location = None
        location_elem = element.find('span', class_='s-item__location')
        if location_elem:
            location = location_elem.get_text(strip=True)

        # Estrai condizione (nuovo/usato)
        condition = None
        condition_elem = element.find('span', class_='SECONDARY_INFO')
        if condition_elem:
            condition = condition_elem.get_text(strip=True)

        # Estrai shipping info
        shipping_elem = element.find('span', class_='s-item__shipping')
        shipping_info = None
        if shipping_elem:
            shipping_info = shipping_elem.get_text(strip=True)

        # Se non abbiamo almeno titolo o link, salta
        if not title and not link:
            return None

        return Listing(
            title=title or "N/A",
            price=price,
            price_text=price_text,
            link=link,
            photos=photos,
            location=location,
            listing_id=listing_id,
            # Campi aggiuntivi (possono essere None)
            condition=condition,
            shipping=shipping_info
        )

    def _extract_listing_details(self, soup, listing: Listing) -> Listing:
        """
        Estrae dettagli completi da pagina singolo annuncio eBay.

        Args:
            soup: BeautifulSoup object della pagina
            listing: Listing da aggiornare

        Returns:
            Listing aggiornato
        """
        # Estrai descrizione
        desc_elem = (
            soup.find('div', id='desc_div') or
            soup.find('div', class_='vi-desc-wrapper') or
            soup.find('div', attrs={'data-testid': 'x-item-description'})
        )
        if desc_elem:
            listing.description = desc_elem.get_text(strip=True)

        # Estrai tutte le foto dalla galleria
        photos = []
        gallery = soup.find('div', class_='ux-image-carousel')
        if gallery:
            img_elems = gallery.find_all('img')
            for img in img_elems:
                src = img.get('src') or img.get('data-src')
                if src and src not in photos and not src.endswith('placeholder'):
                    photos.append(src)

        if photos:
            listing.photos = photos

        # Estrai info venditore
        seller_elem = soup.find('span', class_='mbg-nw')
        if seller_elem:
            listing.seller_name = seller_elem.get_text(strip=True)

        # Estrai categoria
        breadcrumb = soup.find('nav', attrs={'aria-label': 'breadcrumb'})
        if breadcrumb:
            category_links = breadcrumb.find_all('a')
            if category_links:
                listing.category = category_links[-1].get_text(strip=True)

        return listing

    def search(
        self,
        query: str,
        category: Optional[str] = None,
        max_price: Optional[float] = None,
        condition: Optional[str] = None,  # "new" o "used"
        max_pages: int = 1
    ) -> List[Listing]:
        """
        Cerca annunci su eBay.it.

        Args:
            query: Query di ricerca
            category: Categoria eBay (numero categoria)
            max_price: Prezzo massimo
            condition: Condizione (new/used)
            max_pages: Numero massimo di pagine

        Returns:
            Lista di Listing
        """
        # Costruisci URL di ricerca eBay
        params = []

        # Query
        if query:
            params.append(f"_nkw={quote_plus(query)}")

        # Categoria (eBay usa numeri categoria)
        if category:
            params.append(f"_sacat={category}")

        # Prezzo massimo
        if max_price:
            params.append(f"_udhi={int(max_price)}")

        # Condizione
        if condition:
            if condition.lower() == 'new':
                params.append("LH_ItemCondition=1000")
            elif condition.lower() == 'used':
                params.append("LH_ItemCondition=3000")

        # Solo Buy It Now (no aste)
        params.append("LH_BIN=1")

        # Costruisci URL finale
        search_url = f"{self.base_url}/sch/i.html"
        if params:
            search_url += "?" + "&".join(params)

        logger.info(f"Ricerca eBay: '{query}' categoria: {category or 'tutte'}")

        return self.scrape_listings(search_url, max_pages=max_pages)
