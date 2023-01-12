from datetime import datetime

from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional


# Auth
class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user1@gmail.com",
                "password": "12345678"
            }
        }


# region Role
class RoleCreate(BaseModel):
    name: str
    title_ru: str
    title_en: Optional[str]
    title_uz: Optional[str]
    description: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "booking",
                "title_ru": "Бронирование",
                "title_en": "Booking",
                "title_uz": "Rezervatsiya",
                "description": "Роль для бронирования"
            }
        }


class RoleUpdate(RoleCreate):
    name: Optional[str]
    title_ru: Optional[str]


class Role(RoleCreate):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **RoleCreate.Config.schema_extra.get("example"),
            }
        }


# endregion


# region User
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


# endregion


# region Section
class SectionCreate(BaseModel):
    name_ru: str
    name_en: Optional[str]
    name_uz: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name_ru": "Бронирование",
                "name_en": "Booking",
                "name_uz": "Rezervatsiya",
            }
        }


class SectionUpdate(SectionCreate):
    name_ru: Optional[str]
    name_en: Optional[str]
    name_uz: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name_ru": "Бронирование",
                "name_en": "Booking",
                "name_uz": "Rezervatsiya",
            }
        }


class Section(SectionCreate):
    id: int
    permissions: list

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **SectionCreate.Config.schema_extra.get("example"),
                "permissions": []
            }
        }


# endregion


# region Permission
class PermissionCreate(BaseModel):
    alias: str
    section_id: Optional[int]
    title_ru: str
    title_en: Optional[str]
    title_uz: Optional[str]
    description: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "alias": "booking",
                "section_id": 1,
                "title_ru": "Бронирование",
                "title_en": "Booking",
                "title_uz": "Rezervatsiya",
                "description": "Роль для бронирования (Optional[str])"
            }
        }


class PermissionUpdate(PermissionCreate):
    pass


class Permission(PermissionCreate):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **PermissionCreate.Config.schema_extra.get("example"),
            }
        }


# endregion


# region Role Permission
class RolePermissionCreate(BaseModel):
    role_id: int
    permission_id: int

    @validator('role_id')
    def role_id_must_be_positive(cls, v):
        if v < 1:
            raise ValueError('role_id must be positive')
        return v

    @validator('permission_id')
    def permission_id_must_be_positive(cls, v):
        if v < 1:
            raise ValueError('permission_id must be positive')
        return v

    class Config:
        schema_extra = {
            "example": {
                "role_id": 1,
                "permission_id": 1,
            }
        }


class RolePermissionUpdate(RolePermissionCreate):
    pass


class RolePermission(RolePermissionCreate):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **RolePermissionCreate.Config.schema_extra.get("example"),
            }
        }


# endregion


# region Agent
class AgentCreate(BaseModel):
    user_id: int
    company_name: str
    balance: Optional[float]
    address: Optional[str]
    phone: Optional[str]
    registered_date: Optional[datetime]
    is_on_credit: Optional[bool] = False
    discount_id: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "company_name": "Company",
                "address": "Address",
                "phone": "+998901234567",
                "is_on_credit": False,
                "discount_id": 1,
            }
        }


class AgentUpdate(AgentCreate):
    user_id: Optional[int]
    company_name: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "company_name": "Company",
                "balance": 0.0,
                "address": "Address",
                "phone": "+998901234567",
                "is_on_credit": False,
                "discount_id": 1,
            }
        }


class Agent(AgentUpdate):
    id: int
    user_id: int
    discount_id: Optional[int]
    block_date: Optional[datetime]
    registered_date: Optional[datetime]

    # bookings: list
    # role_permissions: list
    # tickets: list

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **AgentCreate.Config.schema_extra.get("example"),
                "block_date": "2021-01-01 00:00:00",
                "registered_date": "2021-01-01 00:00:00",
                # "bookings": [],
                "role_permissions": [],
                "tickets": [],
            }
        }


# endregion


# region Discount
class DiscountCreate(BaseModel):
    amount: str
    name: str

    class Config:
        schema_extra = {
            "example": {
                "amount": "10",
                "name": "10% discount",
            }
        }


class DiscountUpdate(DiscountCreate):
    amount: Optional[str]
    name: Optional[str]


class Discount(DiscountCreate):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **DiscountCreate.Config.schema_extra.get("example"),
            }
        }

# endregion
