from datetime import datetime

from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str]
    role_id: int
    language: Optional[str] = Field(default="ru", max_length=2)

    # region Validators
    @validator('email')
    def email_must_contain_at_symbol(cls, v):
        if '@' not in v:
            raise ValueError('email must contain @ symbol')
        return v

    @validator('password')
    def password_must_contain_at_least_8_characters(cls, v):
        if len(v) < 8:
            raise ValueError('password must contain at least 8 characters')
        return v

    @validator('role_id')
    def role_id_must_be_positive(cls, v):
        if v < 1:
            raise ValueError('role_id must be positive')
        return v

    # endregion

    class Config:
        schema_extra = {
            "example": {
                "email": "user@gmail.com",
                "password": "12345678",
                "username": "user",
                "role_id": 1,
                "language": "ru"
            }
        }


class UserUpdate(UserCreate):
    email: Optional[EmailStr]
    password: Optional[str]
    phone: Optional[str]

    @validator('username')
    def username_must_contain_at_least_3_characters(cls, v):
        if len(v) < 3:
            raise ValueError('username must contain at least 3 characters')
        return v

    @validator('role_id')
    def role_id_must_be_greater_than_0(cls, v):
        if v < 0:
            raise ValueError('role_id must be greater than 0')
        return v

    @validator('phone')
    def phone_must_contain_at_least_9_characters(cls, v):
        if len(v) < 9:
            raise ValueError('phone must contain at least 9 characters')
        return v

    class Config:
        schema_extra = {
            "example": {
                **UserCreate.Config.schema_extra.get("example"),
                "phone": "+998901234567",
            }
        }


class User(UserCreate):
    id: Optional[int]
    email: Optional[EmailStr]
    password: Optional[str] = None
    phone: Optional[str]
    date_joined: Optional[datetime]
    last_login: Optional[datetime]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **UserCreate.Config.schema_extra.get("example"),
                "phone": "+998901234567",
                "date_joined": "2021-01-01 00:00:00",
                "last_login": "2021-01-01 00:00:00",
            }
        }
