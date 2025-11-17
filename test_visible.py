from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

print("="*60)
print("TEST SELENIUM - BROWSER VISIBILE")
print("="*60)

options = Options()
# IMPORTANTE: headless=False per vedere cosa succede
# options.add_argument('--headless')  # COMMENTATO
options.add_argument('--no-sandbox')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

# Aggiungi questo per evitare detection
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--start-maximized')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Nascondi che è Selenium
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

try:
    print("\nCarico pagina (browser visibile)...")
    driver.get("https://www.subito.it/annunci-italia/vendita/usato/?q=iphone")
    
    print("Attendo caricamento (guarda il browser!)...")
    time.sleep(8)  # Più tempo per vedere cosa succede
    
    # Prova ad aspettare un elemento specifico
    try:
        print("Cerco elementi annunci...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    except:
        pass
    
    # Scroll
    print("Scrolling...")
    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 1000);")
    time.sleep(2)
    
    # Cerca TUTTI i link
    all_links = driver.find_elements(By.TAG_NAME, "a")
    print(f"\nTrovati {len(all_links)} link totali nella pagina")
    
    # Cerca link con pattern annunci
    ad_links = []
    for link in all_links:
        href = link.get_attribute('href')
        if href and 'subito.it' in href and any(x in href for x in ['/telefonia/', '/informatica/', '/annunci/']):
            ad_links.append(href)
            text = link.text[:50] if link.text else "No text"
            print(f"  ✓ {text} → {href[:80]}")
    
    print(f"\n✅ Trovati {len(ad_links)} possibili annunci")
    
    # Salva screenshot
    driver.save_screenshot('screenshot.png')
    print("\n📸 Screenshot salvato: screenshot.png")
    
    # Salva HTML
    with open('debug_visible.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print("💾 HTML salvato: debug_visible.html")
    
    print("\n⏸️ Premi CTRL+C per chiudere...")
    time.sleep(30)  # Tempo per guardare il browser
    
except KeyboardInterrupt:
    print("\n👋 Chiusura...")
except Exception as e:
    print(f"❌ Errore: {e}")
    import traceback
    traceback.print_exc()
finally:
    driver.quit()
    print("✅ Browser chiuso")