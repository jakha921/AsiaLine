from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional



class RoleBase(BaseModel):
    name: str
    title_ru: str

    class Config:
        orm_mode = True


class RoleCreate(RoleBase):
    title_en: Optional[str] = 'null'
    title_uz: Optional[str] = 'null'
    description: Optional[str] = 'null'


class RoleUpdate(RoleCreate):
    pass

class Role(RoleCreate):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr = Field(None)
    username: str = Field(None)
    role_id: Optional[int] = 'null'
    
    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
    phone: str
    language: str = 'ru'
    
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


class UserUpdate(UserCreate):
    pass


class User(BaseModel):
    id: int
    email: EmailStr = Field(None)
    username: str = Field(None)
    role_id: int = Field(None)
    phone: str = Field(None)
    language: str = Field(None)
    role_id: int = Field(None)
    
    class Config:
        orm_mode = True


