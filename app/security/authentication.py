from datetime import datetime, timedelta, timezone
from typing import Optional
import uuid

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from pydantic import EmailStr
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.redis_db import get_redis
from app.exceptions.exceptions import (
    InvalidTokenException,
    TokenExpiredException,
    UserNotFoundException,
)
from app.models.user import User
from app.crud.cache_repository import (
    get_user_by_id_from_cache,
    set_user_to_redis,
)
from app.crud.user_repository import (
    get_user_by_email,
    get_user_by_id,
)
from app.database.sql_database import get_session
from app.schemas.user import UserOut
from app.security.pwd_crypt import verify_password
from app.utils.utils import calculate_timestamp
from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, API_URL, SECRET_KEY


CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_URL}/auth/token/login")


async def authenticate_user(
    session: AsyncSession, email: EmailStr, password: str
) -> Optional[User]:
    user = await get_user_by_email(session, email)
    if not user or not verify_password(password, user.password):
        return None
    return user


def create_access_token(user: User) -> str:
    to_encode = {"sub": str(user.id)}
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
    token: str = Depends(oauth2_scheme),
) -> Optional[UserOut]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError:
        raise InvalidTokenException

    expire = payload.get("exp")
    if not expire:
        raise InvalidTokenException
    try:
        expiring_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    except ValueError:
        raise InvalidTokenError
    if expiring_time < datetime.now(timezone.utc):
        raise TokenExpiredException

    user_id = uuid.UUID(payload.get("sub"))
    if user_id is None:
        raise InvalidTokenException

    cached_user = await get_user_by_id_from_cache(redis, user_id)
    if cached_user:
        return cached_user

    user = await get_user_by_id(session, user_id)
    if user is None:
        raise UserNotFoundException

    user_pydantic = UserOut.model_validate(user)
    unix_timestamp = calculate_timestamp()

    await set_user_to_redis(redis, user_pydantic, unix_timestamp)

    return user_pydantic
