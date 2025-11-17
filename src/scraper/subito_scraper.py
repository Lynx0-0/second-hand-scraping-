"""Scraper specifico per Subito.it."""

from typing import List, Optional
from urllib.parse import urljoin, urlparse, parse_qs
import re
import logging

from .base_scraper import BaseScraper
from ..models.listing import Listing
from ..config.settings import ScraperConfig


logger = logging.getLogger(__name__)


class SubitoScraper(BaseScraper):
    """Scraper per il sito Subito.it."""

    def __init__(self, config: Optional[ScraperConfig] = None):
        """Inizializza lo scraper per Subito.it."""
        super().__init__(config)
        self.base_url = self.config.subito_base_url

    def scrape_listings(self, url: str, max_pages: int = 1) -> List[Listing]:
        """
        Scrape annunci da Subito.it.

        Args:
            url: URL della pagina di ricerca o categoria
            max_pages: Numero massimo di pagine da processare

        Returns:
            Lista di Listing
        """
        all_listings = []

        for page in range(1, max_pages + 1):
            logger.info(f"Scraping pagina {page}/{max_pages}: {url}")

            # Costruisci URL con paginazione
            page_url = self._build_page_url(url, page)

            # Fetch della pagina
            response = self.fetch_page(page_url)

            if not response:
                logger.error(f"Impossibile recuperare la pagina {page}")
                break

            # Salva HTML se configurato
            self.save_html(response.text, f"subito_page_{page}.html")

            # Parse HTML
            soup = self.parse_html(response.text)

            # Estrai annunci
            listings = self._extract_listings_from_page(soup)

            if not listings:
                logger.warning(f"Nessun annuncio trovato nella pagina {page}")
                break

            all_listings.extend(listings)
            self.stats['listings_found'] += len(listings)

            logger.info(f"Trovati {len(listings)} annunci nella pagina {page}")

        logger.info(f"Totale annunci trovati: {len(all_listings)}")
        return all_listings

    def scrape_listing_details(self, listing: Listing) -> Listing:
        """
        Estrae dettagli completi di un singolo annuncio.

        Args:
            listing: Listing con almeno il link

        Returns:
            Listing con tutti i dettagli
        """
        if not listing.link:
            logger.warning("Listing senza link, impossibile estrarre dettagli")
            return listing

        logger.debug(f"Estrazione dettagli per: {listing.link}")

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
        Costruisce URL con paginazione.

        Args:
            base_url: URL base
            page: Numero pagina

        Returns:
            URL con parametro di paginazione
        """
        if page == 1:
            return base_url

        # Subito.it usa parametro 'o' per offset (es. o=25, o=50)
        separator = '&' if '?' in base_url else '?'
        offset = (page - 1) * 25  # Subito.it mostra 25 annunci per pagina
        return f"{base_url}{separator}o={offset}"

    def _extract_listings_from_page(self, soup) -> List[Listing]:
        """
        Estrae lista di annunci da una pagina.

        Args:
            soup: BeautifulSoup object della pagina

        Returns:
            Lista di Listing
        """
        listings = []

        # Subito.it usa diverse strutture HTML. Proviamo vari selettori comuni.
        # Nota: questi selettori potrebbero cambiare nel tempo

        # Prova 1: Cerca elementi con data-id (formato più recente)
        items = soup.find_all('div', attrs={'data-id': True})

        if not items:
            # Prova 2: Cerca classi comuni per gli annunci
            items = soup.find_all('div', class_=re.compile(r'item|listing|ad-item', re.I))

        if not items:
            # Prova 3: Cerca link che sembrano annunci
            items = soup.find_all('a', href=re.compile(r'/\w+/\w+/.*\.htm'))

        logger.debug(f"Trovati {len(items)} potenziali annunci")

        for item in items:
            try:
                listing = self._extract_listing_from_element(item)
                if listing and listing.is_valid():
                    listings.append(listing)
            except Exception as e:
                logger.debug(f"Errore estrazione annuncio: {e}")
                continue

        return listings

    def _extract_listing_from_element(self, element) -> Optional[Listing]:
        """
        Estrae dati di un annuncio da un elemento HTML.

        Args:
            element: Elemento BeautifulSoup

        Returns:
            Listing o None
        """
        # Estrai titolo
        title = None
        title_elem = (
            element.find('h2') or
            element.find('h3') or
            element.find(class_=re.compile(r'title|heading', re.I)) or
            element.find('a', class_=re.compile(r'title', re.I))
        )
        if title_elem:
            title = title_elem.get_text(strip=True)

        # Estrai link
        link = None
        link_elem = element.find('a', href=True)
        if link_elem:
            href = link_elem['href']
            link = urljoin(self.base_url, href)

        # Estrai ID annuncio dal link o data-id
        listing_id = None
        if element.get('data-id'):
            listing_id = element.get('data-id')
        elif link:
            # Cerca pattern ID nel link (es. numero.htm)
            match = re.search(r'(\d+)\.htm', link)
            if match:
                listing_id = match.group(1)

        # Estrai prezzo
        price = None
        price_text = None
        price_elem = element.find(class_=re.compile(r'price|prezzo', re.I))
        if price_elem:
            price_text = price_elem.get_text(strip=True)
            # Prova a estrarre valore numerico
            price_match = re.search(r'([\d.,]+)', price_text.replace('.', '').replace(',', '.'))
            if price_match:
                try:
                    price = float(price_match.group(1))
                except ValueError:
                    pass

        # Estrai foto
        photos = []
        img_elem = element.find('img', src=True)
        if img_elem:
            img_src = img_elem['src']
            # Aggiungi foto se non è placeholder
            if img_src and not img_src.endswith(('placeholder.jpg', 'placeholder.png')):
                photos.append(img_src)

        # Estrai location
        location = None
        location_elem = element.find(class_=re.compile(r'location|city|town', re.I))
        if location_elem:
            location = location_elem.get_text(strip=True)

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
            listing_id=listing_id
        )

    def _extract_listing_details(self, soup, listing: Listing) -> Listing:
        """
        Estrae dettagli completi da pagina singolo annuncio.

        Args:
            soup: BeautifulSoup object della pagina
            listing: Listing da aggiornare

        Returns:
            Listing aggiornato
        """
        # Estrai descrizione
        desc_elem = soup.find('div', class_=re.compile(r'description|desc|body', re.I))
        if desc_elem:
            listing.description = desc_elem.get_text(strip=True)

        # Estrai tutte le foto
        photos = []
        # Cerca galleria immagini
        gallery = soup.find('div', class_=re.compile(r'gallery|carousel|images', re.I))
        if gallery:
            img_elems = gallery.find_all('img', src=True)
            for img in img_elems:
                src = img['src']
                # Prova anche data-src per lazy loading
                if not src or src.endswith(('placeholder.jpg', 'placeholder.png')):
                    src = img.get('data-src', '')

                if src and src not in photos:
                    photos.append(src)

        if photos:
            listing.photos = photos

        # Estrai info venditore
        seller_elem = soup.find(class_=re.compile(r'seller|vendor|owner', re.I))
        if seller_elem:
            seller_name = seller_elem.get_text(strip=True)
            if seller_name:
                listing.seller_name = seller_name

        # Estrai categoria
        category_elem = soup.find('a', class_=re.compile(r'category|breadcrumb', re.I))
        if category_elem:
            listing.category = category_elem.get_text(strip=True)

        # Estrai data pubblicazione
        date_elem = soup.find(class_=re.compile(r'date|published|posted', re.I))
        if date_elem:
            listing.posted_date = date_elem.get_text(strip=True)

        return listing

    def search(
        self,
        query: str,
        category: Optional[str] = None,
        region: Optional[str] = None,
        max_pages: int = 1
    ) -> List[Listing]:
        """
        Cerca annunci su Subito.it.

        Args:
            query: Query di ricerca
            category: Categoria (es. 'arredamento', 'elettronica')
            region: Regione (es. 'lazio', 'lombardia')
            max_pages: Numero massimo di pagine

        Returns:
            Lista di Listing
        """
        # Costruisci URL di ricerca
        search_url = f"{self.base_url}/annunci-italia"

        if category:
            search_url += f"/{category}"

        if region:
            search_url += f"?r={region}"
            separator = '&'
        else:
            separator = '?'

        if query:
            search_url += f"{separator}q={query.replace(' ', '+')}"

        logger.info(f"Ricerca: '{query}' in categoria: {category or 'tutte'}")

        return self.scrape_listings(search_url, max_pages=max_pages)
