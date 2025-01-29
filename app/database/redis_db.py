from typing import AsyncIterator
from redis.asyncio import from_url, Redis

from config import REDIS_URL


async def get_redis() -> AsyncIterator[Redis]:
    redis = from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    yield redis
    await redis.aclose()
