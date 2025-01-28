from typing import Annotated

from fastapi import Depends, APIRouter, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession


from app.crud.user_repository import (
    check_username_and_email,
    create_new_user,
)
from app.database.sql_database import get_session
from app.exceptions.exceptions import (
    EmailAlreadyExistsException,
    IncorrectEmailOrPasswordException,
    UserAlreadyExistsException,
)
from app.schemas.token import Token
from app.schemas.user import UserAuthentication, UserCreate, UserOut
from app.security.authentication import authenticate_user, create_access_token
from app.security.pwd_crypt import get_hashed_password


loginrouter = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@loginrouter.post(
    "/register", response_model=UserOut, status_code=status.HTTP_201_CREATED
)
async def register_user(
    user_data: UserCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    # checks if user with same username or email already exists
    user = await check_username_and_email(session, user_data.username, user_data.email)
    if user:
        if user.username == user_data.username:
            raise UserAlreadyExistsException
        raise EmailAlreadyExistsException

    user_data.password = get_hashed_password(user_data.password)
    new_user = await create_new_user(session, user_data)

    return new_user


@loginrouter.post("/token")
async def user_access_token(
    form_data: UserAuthentication,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Token:
    user = await authenticate_user(session, form_data.email, form_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException

    access_token = create_access_token(user)
    return Token(access_token=access_token, token_type="Bearer")
