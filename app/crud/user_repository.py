import json
from typing import Optional
from uuid import UUID

from pydantic import EmailStr
from redis import Redis
from sqlalchemy import or_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate, UserOut


async def check_username_and_email(
    session: AsyncSession, username: str, email: EmailStr
) -> Optional[User]:
    query = select(User).where(or_(User.username == username, User.email == email))
    result = await session.execute(query)
    return result.scalar()


async def get_user_by_id(session: AsyncSession, id: UUID) -> Optional[User]:
    query = select(User).filter_by(id=id)
    result = await session.execute(query)
    return result.scalar()


async def get_user_by_id_from_cache(redis, id: UUID) -> Optional[UserOut]:
    user = await redis.get(f"user:{id}")
    if user:
        return UserOut(**json.loads(user))
    return None


async def set_user_to_redis(redis: Redis, user: UserOut, unix_timestamp: int) -> None:
    print("LEO")
    await redis.set(f"user:{user.id}", user.model_dump_json(), ex=unix_timestamp)


async def get_user_by_email(session: AsyncSession, email: EmailStr) -> Optional[User]:
    query = select(User).filter_by(email=email)
    result = await session.execute(query)
    return result.scalar()


async def get_user_by_username(session: AsyncSession, username: str) -> Optional[User]:
    query = select(User).filter_by(username=username)
    result = await session.execute(query)
    return result.scalar()


async def create_new_user(session: AsyncSession, user_data: UserCreate) -> User:
    new_user = User(**user_data.model_dump())
    session.add(new_user)
    await session.commit()
    return new_user
