import json
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security import verify_token
from app.core.rate_limiter import rate_limit
from app.services.cache_service import cache_get, cache_set
from app.services.news_service import fetch_top_headlines
from app.services.ml_service import predict_category
from app.schemas.news import ClassifiedNewsResponse, ClassifiedArticle

router = APIRouter(prefix="/news", tags=["news"])
security = HTTPBearer()

def require_user(creds: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    payload = verify_token(creds.credentials)
    if not payload:
        raise HTTPException(status_code=403, detail="Invalid or expired token")
    return payload

@router.get("/classified", response_model=ClassifiedNewsResponse)
async def classified_news(
    request: Request,
    _=Depends(rate_limit),
    user=Depends(require_user),
):
    cache_key = "news:top:classified"
    cached = cache_get(cache_key)
    if cached:
        data = json.loads(cached)
        return ClassifiedNewsResponse(**data)

    raw = fetch_top_headlines()
    items = []
    for a in raw.get("articles", []):
        title = a.get("title") or ""
        url = a.get("url")
        category = predict_category(title)
        items.append(ClassifiedArticle(title=title, url=url, predicted_category=category))

    out = ClassifiedNewsResponse(items=items).model_dump()
    cache_set(cache_key, json.dumps(out), ttl_sec=180)
    return ClassifiedNewsResponse(**out)
