from pydantic import BaseModel
from typing import Optional


class RoleCreate(BaseModel):
    name: str
    title_ru: str
    title_en: Optional[str]
    title_uz: Optional[str]
    description: Optional[str]
    permissions: Optional[list]

    class Config:
        schema_extra = {
            "example": {
                "name": "admin",
                "title_ru": "Администратор",
                "title_en": "Administrator",
                "title_uz": "Administrator",
                "description": "Роль для администратора",
                "permissions": [1, 2, 3]
            }
        }


class RoleUpdate(RoleCreate):
    name: Optional[str]
    title_ru: Optional[str]


class Role(BaseModel):
    id: int
    name: Optional[str]
    title_ru: Optional[str]
    title_en: Optional[str]
    title_uz: Optional[str]
    description: Optional[str]
    permissions: Optional[list]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "admin",
                "title_ru": "Администратор",
                "title_en": "Administrator",
                "title_uz": "Administrator",
                "description": "Роль для администратора",
                "permissions": [1, 2, 3]
            }
        }
