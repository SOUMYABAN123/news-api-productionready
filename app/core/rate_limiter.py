from fastapi import Request, HTTPException
from app.services.cache_service import redis_client

RATE_LIMIT = 30      # requests
WINDOW_SEC = 60      # per minute

async def rate_limit(request: Request) -> None:
    ip = request.client.host if request.client else "unknown"
    key = f"rl:{ip}:{request.url.path}"

    # atomic-ish pattern: INCR + EXPIRE
    count = redis_client.incr(key)
    if count == 1:
        redis_client.expire(key, WINDOW_SEC)

    if count > RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
