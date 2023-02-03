from typing import Optional
from pydantic import BaseModel


class GenderCreate(BaseModel):
    gender_ru: str
    gender_en: str
    gender_uz: str
    description: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "gender_ru": "Мужской",
                "gender_en": "Male",
                "gender_uz": "Erkak",
                "description": "Мужской пол Optional[str]",
            }
        }


class GenderUpdate(GenderCreate):
    gender_ru: Optional[str]
    gender_en: Optional[str]
    gender_uz: Optional[str]


class Gender(GenderUpdate):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **GenderCreate.Config.schema_extra.get("example"),
            }
        }
