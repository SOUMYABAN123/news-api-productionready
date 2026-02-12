import redis
from app.core.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)

def cache_get(key: str) -> str | None:
    return redis_client.get(key)

def cache_set(key: str, value: str, ttl_sec: int = 300) -> None:
    redis_client.setex(key, ttl_sec, value)
