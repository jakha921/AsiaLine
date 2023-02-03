from typing import Optional
from pydantic import BaseModel, validator


class CityCreate(BaseModel):
    city_ru: str
    city_en: Optional[str]
    city_uz: Optional[str]
    country_id: int

    @validator('country_id')
    def country_id_must_be_greater_than_0(cls, v):
        if v < 1:
            raise ValueError('country_id must be greater than 0')
        return v

    class Config:
        schema_extra = {
            "example": {
                "city_ru": "Москва",
                "city_en": "Moscow",
                "city_uz": "Moskva",
                "country_id": 1
            }
        }


class CityUpdate(CityCreate):
    city_ru: Optional[str]
    country_id: Optional[int]


class City(CityCreate):
    id: int
    airports: list

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **CityCreate.Config.schema_extra.get("example"),
                "airports": []
            }
        }
