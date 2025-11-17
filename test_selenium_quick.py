from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

print("="*60)
print("TEST SELENIUM - SUBITO.IT")
print("="*60)

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

print("\nAvvio Chrome...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print("Connessione a Subito.it...")
    driver.get("https://www.subito.it/annunci-italia/vendita/usato/?q=iphone")
    time.sleep(3)
    ads = driver.find_elements(By.CLASS_NAME, "items__item")
    print(f"\nSUCCESSO! Trovati {len(ads)} annunci!")
    if len(ads) > 0:
        print("Selenium bypassa il blocco 403!")
except Exception as e:
    print(f"Errore: {e}")
finally:
    driver.quit()
    print("Browser chiuso")