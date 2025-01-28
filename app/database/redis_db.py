from fastapi import Depends
from redis.asyncio import from_url, Redis

from config import REDIS_URL


async def redis_pool() -> Redis:
    # Create and return an async Redis client (connection pool)
    return await from_url(REDIS_URL, encoding="utf-8", decode_responses=True)


async def get_redis(redis: Redis = Depends(redis_pool)):
    yield redis
