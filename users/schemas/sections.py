from pydantic import BaseModel
from typing import Optional


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
