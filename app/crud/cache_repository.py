import json
from typing import Optional
from uuid import UUID

from redis import Redis

from app.schemas.user import UserOut


async def get_user_by_id_from_cache(redis, id: UUID) -> Optional[UserOut]:
    user = await redis.get(f"user:{id}")
    if user:
        return UserOut(**json.loads(user))
    return None


async def set_user_to_redis(redis: Redis, user: UserOut, unix_timestamp: int) -> None:
    await redis.set(f"user:{user.id}", user.model_dump_json(), ex=unix_timestamp)


async def get_trading_dates_redis(redis: Redis, key: str):
    trades = await redis.get(f"trades:{key}")
    if trades:
        return trades
    return None


async def set_trading_data_to_redis(
    redis: Redis, key: str, data: dict, unix_timestamp: int
) -> None:
    await redis.set(f"trades:{key}", data, ex=unix_timestamp)
