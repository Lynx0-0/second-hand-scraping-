from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

print("="*60)
print("DEBUG SELENIUM - ANALISI SELETTORI")
print("="*60)

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print("\nCarico pagina Subito.it...")
    driver.get("https://www.subito.it/annunci-italia/vendita/usato/?q=iphone")
    
    # Attendi di più per il caricamento dinamico
    print("Attendo 5 secondi per caricamento completo...")
    time.sleep(5)
    
    # Scroll per attivare lazy loading
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    
    # Salva HTML per debug
    html = driver.page_source
    with open('debug_page.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✅ HTML salvato in: debug_page.html")
    
    # Prova diversi selettori
    selectors = [
        ("items__item", By.CLASS_NAME),
        ("SmallCard-module", By.CLASS_NAME),
        ("Card-module", By.CLASS_NAME),
        ("listing", By.CLASS_NAME),
        ("item", By.CLASS_NAME),
        ("[data-testid='listing-card']", By.CSS_SELECTOR),
        ("article", By.TAG_NAME),
        ("a[href*='/annunci/']", By.CSS_SELECTOR),
    ]
    
    print("\n" + "="*60)
    print("TEST SELETTORI:")
    print("="*60)
    
    for selector, by_type in selectors:
        try:
            elements = driver.find_elements(by_type, selector)
            if len(elements) > 0:
                print(f"✅ '{selector}' → {len(elements)} elementi trovati")
            else:
                print(f"❌ '{selector}' → 0 elementi")
        except Exception as e:
            print(f"❌ '{selector}' → Errore: {e}")
    
    # Cerca tutti i link annunci
    print("\n" + "="*60)
    print("LINK ANNUNCI:")
    print("="*60)
    all_links = driver.find_elements(By.TAG_NAME, "a")
    ad_links = [link.get_attribute('href') for link in all_links if link.get_attribute('href') and '/annunci/' in link.get_attribute('href')]
    print(f"Trovati {len(ad_links)} link ad annunci")
    
    if ad_links:
        print("\nPrimi 3 link:")
        for link in ad_links[:3]:
            print(f"  - {link}")
    
    print("\n💡 Apri 'debug_page.html' in un browser per vedere la struttura HTML")
    
except Exception as e:
    print(f"❌ Errore: {e}")
    import traceback
    traceback.print_exc()
finally:
    driver.quit()
    print("\n✅ Browser chiuso")