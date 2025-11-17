"""
Fix per errore 403 - Migliora headers per bypassare blocco anti-bot
"""
import requests
from bs4 import BeautifulSoup
import time

def test_headers():
    """Testa diverse configurazioni di headers"""
    
    url = "https://www.subito.it/annunci-italia/vendita/usato/"
    
    # Headers più realistici
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Referer': 'https://www.google.com/'
    }
    
    print("🔍 Test 1: Headers migliorati...")
    try:
        response = requests.get(url, headers=headers, timeout=30)
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            ads = soup.find_all('div', class_='items__item')
            print(f"✅ Trovati {len(ads)} annunci!")
            return True
        else:
            print(f"❌ Status Code: {response.status_code}")
    except Exception as e:
        print(f"❌ Errore: {e}")
    
    return False

def test_with_session():
    """Testa con sessione persistente"""
    
    print("\n🔍 Test 2: Sessione persistente...")
    
    session = requests.Session()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'it-IT,it;q=0.9',
        'Referer': 'https://www.google.com/',
        'DNT': '1'
    }
    
    session.headers.update(headers)
    
    try:
        # Prima richiesta alla home per ottenere cookies
        print("  → Visita homepage...")
        home_response = session.get("https://www.subito.it/", timeout=30)
        time.sleep(2)
        
        # Seconda richiesta agli annunci
        print("  → Accesso annunci...")
        url = "https://www.subito.it/annunci-italia/vendita/usato/"
        response = session.get(url, timeout=30)
        
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            ads = soup.find_all('div', class_='items__item')
            print(f"✅ Trovati {len(ads)} annunci!")
            print(f"✅ Cookies: {len(session.cookies)}")
            return True
    except Exception as e:
        print(f"❌ Errore: {e}")
    
    return False

if __name__ == "__main__":
    print("=" * 60)
    print("FIX ERRORE 403 - Test Headers")
    print("=" * 60)
    
    # Test 1
    if test_headers():
        print("\n✅ SOLUZIONE TROVATA: Headers migliorati funzionano!")
        print("\n📝 PROSSIMI PASSI:")
        print("1. Aggiorna src/scraper/subito_scraper.py con questi headers")
        print("2. Esegui di nuovo: python examples\\basic_scraping.py")
    else:
        # Test 2
        if test_with_session():
            print("\n✅ SOLUZIONE TROVATA: Sessione persistente funziona!")
            print("\n📝 PROSSIMI PASSI:")
            print("1. Aggiorna scraper per usare Session invece di requests.get")
        else:
            print("\n❌ NESSUNA SOLUZIONE SEMPLICE FUNZIONA")
            print("\n📝 SOLUZIONI ALTERNATIVE:")
            print("1. Usa Selenium/Playwright (browser reale)")
            print("2. Usa servizio proxy rotante")
            print("3. Richiedi API ufficiale a Subito.it")
            print("4. Per ora, sviluppa con DATI MOCK e testa altre piattaforme")