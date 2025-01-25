from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from config import EMAIL_LENGTH, PASSWORD_REGEX, USERNAME_LENGTH


class UserAuthentication(BaseModel):
    email: EmailStr = Field(..., description="Email")
    password: str = Field(..., description="Password")


class UserCreate(BaseModel):
    email: EmailStr = Field(..., max_length=EMAIL_LENGTH, description="Email address")
    username: str = Field(
        ...,
        max_length=USERNAME_LENGTH,
        pattern=r"^[\w.@+-]+$",
        description="Username (alphanumeric + [@.+-] only, max length: 50 characters).",
    )
    password: str = Field(
        ...,
        pattern=PASSWORD_REGEX,
        description="Password (8-50 characters, must include lower-case, upper-case, digits, and special symbols).",
    )


class UserOut(BaseModel):
    id: UUID = Field(..., description="User id")
    email: EmailStr = Field(..., description="Email address")
    username: str = Field(..., description="Username")

    model_config = ConfigDict(from_attributes=True)
