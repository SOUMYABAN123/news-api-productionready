import requests
from app.core.config import settings

def fetch_top_headlines() -> dict:
    url = "https://gnews.io/api/v4/top-headlines"
    params = {
        "token": settings.GNEWS_API_KEY,
        "lang": settings.GNEWS_LANG,
        "country": settings.GNEWS_COUNTRY,
        "max": settings.GNEWS_MAX,
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json()
