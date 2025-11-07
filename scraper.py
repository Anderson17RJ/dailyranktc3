import cloudscraper
import json
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "https://www.thecrims.com"

def get_top50():
    scraper = cloudscraper.create_scraper()
    url = f"{BASE_URL}/api/v1/stats/killers?country=&character=&level="
    r = scraper.get(url)
    data = r.json()
    return data["killers"][:50]

def fetch_user(user_id):
    scraper = cloudscraper.create_scraper()
    url = f"{BASE_URL}/api/v1/user/{user_id}/stats"
    r = scraper.get(url)
    data = r.json()

    stats_user = data["stats_user"]
    respect_stats = data["respectStats"]

    kills_totais = stats_user["kills"]
    kills_ontem = respect_stats[-1]["kills"] if respect_stats else 0
    kills_hoje = kills_totais - kills_ontem

    return [stats_user["username"], kills_hoje]


if __name__ == "__main__":
    top50 = get_top50()

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
