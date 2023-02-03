from pydantic import BaseModel
from typing import Optional


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
