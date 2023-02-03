from pydantic import BaseModel
from typing import Optional


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
