import cloudscraper
import json
from concurrent.futures import ThreadPoolExecutor
import logging

BASE_URL = "https://www.thecrims.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/142.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://www.thecrims.com/"
}
logging.basicConfig(level=logging.DEBUG)

def get_top50(scraper):
    url = f"{BASE_URL}/api/v1/stats/killers?country=&character=&level="
    r = scraper.get(url,headers=HEADERS, timeout=15)
    print(r.status_code)
    print(r.text[:500])
    data = r.json()
    return data["killers"][:50]

def fetch_user(scraper, user_id):
    url = f"{BASE_URL}/api/v1/user/{user_id}/stats"
    r = scraper.get(url,headers=HEADERS, timeout=15)
    data = r.json()

    stats_user = data["stats_user"]
    respect_stats = data["respectStats"]

    kills_totais = stats_user["kills"]
    kills_ontem = respect_stats[-1]["kills"] if respect_stats else 0
    kills_hoje = kills_totais - kills_ontem

    return [stats_user["username"], kills_hoje]


if __name__ == "__main__":
    scraper = cloudscraper.create_scraper(
    browser={"custom": HEADERS["User-Agent"]}
    )

    top50 = get_top50(scraper)

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda p: fetch_user(p["user"]["id"]), top50))

    results = sorted(results, key=lambda x: x[1], reverse=True)
    print(json.dumps(results))
    
#if __name__ == "__main__":
#    scraper = cloudscraper.create_scraper()
#    top50 = get_top50()
#    results = []

#    for player in top50:  # pega só 5 pra teste rápido
#        uid = player["user"]["id"]
#        row = fetch_user(scraper, uid)
#        results.append(row)

    # imprime SOMENTE o JSON
#    results = sorted(results, key=lambda x: x[1], reverse=True)
#    print(json.dumps(results))
