"""
Crea lo scraper Selenium completo integrato nel progetto
"""
import os

SELENIUM_SCRAPER_CODE = '''"""
Scraper Subito.it con Selenium - Versione Production Ready
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import sys
import os
import json

# Aggiungi src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.listing import Listing
from utils.logger import setup_logger

logger = setup_logger('selenium_scraper')

class SubitoSeleniumScraper:
    """Scraper Subito.it con Selenium per bypassare protezioni anti-bot"""
    
    def __init__(self, headless=True):
        """
        Args:
            headless: Se True, browser invisibile (più veloce)
                      Se False, vedi il browser (utile per debug)
        """
        self.headless = headless
        self.driver = None
        self._setup_driver()
    
    def _setup_driver(self):
        """Configura Chrome driver"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        # Opzioni anti-detection
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("✅ Chrome driver inizializzato")
        except Exception as e:
            logger.error(f"❌ Errore inizializzazione driver: {e}")
            raise
    
    def search(self, query, category=None, max_pages=1):
        """
        Cerca annunci su Subito.it
        
        Args:
            query: Termine di ricerca
            category: Categoria (es. 'telefonia')
            max_pages: Numero massimo di pagine
        
        Returns:
            Lista di oggetti Listing
        """
        listings = []
        
        try:
            # Costruisci URL
            if category:
                url = f"https://www.subito.it/annunci-italia/{category}?q={query}"
            else:
                url = f"https://www.subito.it/annunci-italia/vendita/usato/?q={query}"
            
            logger.info(f"🔍 Ricerca: {query} (pagine: {max_pages})")
            
            for page in range(1, max_pages + 1):
                logger.info(f"📄 Pagina {page}/{max_pages}")
                
                page_url = f"{url}&o={page}" if page > 1 else url
                self.driver.get(page_url)
                
                # Attendi annunci
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "items__item"))
                    )
                except:
                    logger.warning(f"⚠️ Timeout pagina {page}")
                
                # Scroll
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                
                # Parsa
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                ads = soup.find_all('div', class_='items__item')
                
                logger.info(f"  → Trovati {len(ads)} annunci")
                
                for ad in ads:
                    listing = self._parse_listing(ad)
                    if listing:
                        listings.append(listing)
                
                if page < max_pages:
                    time.sleep(2)
            
            logger.info(f"✅ Totale: {len(listings)} annunci")
            
        except Exception as e:
            logger.error(f"❌ Errore: {e}")
        
        return listings
    
    def _parse_listing(self, ad_element):
        """Estrae dati da annuncio"""
        try:
            # Titolo
            title_elem = ad_element.find('h2', class_='ItemTitle')
            title = title_elem.get_text(strip=True) if title_elem else None
            
            # Link
            link_elem = ad_element.find('a', class_='SmallCard-link')
            link = "https://www.subito.it" + link_elem['href'] if link_elem and link_elem.get('href') else None
            
            # Prezzo
            price_elem = ad_element.find('p', class_='price')
            price_text = price_elem.get_text(strip=True) if price_elem else None
            
            price = None
            if price_text and '€' in price_text:
                try:
                    price_clean = price_text.replace('€', '').replace('.', '').replace(',', '.').strip()
                    price = float(price_clean)
                except:
                    pass
            
            # Località
            location_elem = ad_element.find('span', class_='town')
            location = location_elem.get_text(strip=True) if location_elem else None
            
            # Foto
            img_elem = ad_element.find('img', class_='SmallCard-image')
            photo = img_elem['src'] if img_elem and img_elem.get('src') else None
            photos = [photo] if photo else []
            
            listing = Listing(
                title=title,
                price=price,
                price_text=price_text,
                link=link,
                location=location,
                photos=photos
            )
            
            return listing if listing.is_valid() else None
            
        except Exception as e:
            logger.error(f"Errore parsing: {e}")
            return None
    
    def close(self):
        """Chiude browser"""
        if self.driver:
            self.driver.quit()
            logger.info("🔒 Browser chiuso")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# Test
if __name__ == "__main__":
    print("="*70)
    print("TEST SELENIUM SCRAPER COMPLETO")
    print("="*70)
    
    with SubitoSeleniumScraper(headless=True) as scraper:
        listings = scraper.search("iphone", category="telefonia", max_pages=1)
        
        print(f"\\n✅ Trovati {len(listings)} annunci\\n")
        
        for i, listing in enumerate(listings[:5], 1):
            print(f"{i}. {listing.title}")
            print(f"   💰 €{listing.price}")
            print(f"   📍 {listing.location}")
            print(f"   🔗 {listing.link}")
            print("-"*70)
        
        # Salva
        if listings:
            os.makedirs('output', exist_ok=True)
            output_file = 'output/selenium_results.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump([l.to_dict() for l in listings], f, ensure_ascii=False, indent=2)
            print(f"\\n💾 Salvati in: {output_file}")
'''

# Crea il file
filename = "selenium_scraper.py"
with open(filename, 'w', encoding='utf-8') as f:
    f.write(SELENIUM_SCRAPER_CODE)

print("✅ File creato: selenium_scraper.py")
print("\n📝 Prossimi passi:")
print("1. Test: python selenium_scraper.py")
print("2. Se funziona, integra nel progetto principale")
print("\n💡 Per vedere il browser in azione:")
print("   Modifica headless=False nella riga 'with SubitoSeleniumScraper(headless=True)'")