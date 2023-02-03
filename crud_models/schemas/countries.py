from pydantic import BaseModel, validator
from typing import Optional


class CountryCreate(BaseModel):
    country_ru: str
    country_en: Optional[str]
    country_uz: Optional[str]
    short_name: str
    code: str

    @validator('short_name')
    def short_name_must_be_less_than_3_characters(cls, v):
        if len(v) > 2:
            raise ValueError('short_name must be less than 2 characters')
        return v

    @validator('code')
    def code_must_be_less_than_3_characters(cls, v):
        if len(v) > 3:
            raise ValueError('code must be less than 3 characters')
        return v

    class Config:
        schema_extra = {
            "example": {
                "country_ru": "Россия",
                "country_en": "Russia",
                "country_uz": "Rossiya",
                "short_name": "RU",
                "code": "RUS"
            }
        }


class CountryUpdate(CountryCreate):
    country_ru: Optional[str]
    short_name: Optional[str]
    code: Optional[str]


class Country(CountryCreate):
    id: int
    cities: list

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **CountryCreate.Config.schema_extra.get("example"),
                "cities": []
            }
        }
