from typing import Optional
from pydantic import BaseModel, validator


class CityCreate(BaseModel):
    country_id: int
    city_ru: str
    city_en: Optional[str]
    city_uz: Optional[str]
    code: Optional[str]

    @validator('country_id')
    def country_id_must_be_greater_than_0(cls, v):
        if v < 1:
            raise ValueError('country_id must be greater than 0')
        return v

    # @validator('code')
    # def code_must_be_3_characters(cls, v):
    #     if len(v) != 3:
    #         raise ValueError('code must be 3 characters')
    #     return v

    class Config:
        schema_extra = {
            "example": {
                "country_id": 1,
                "city_ru": "Москва",
                "city_en": "Moscow",
                "city_uz": "Moskva",
                "code": "MOW"
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
