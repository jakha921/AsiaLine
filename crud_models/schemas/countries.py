from pydantic import BaseModel, validator
from typing import Optional


class CountryCreate(BaseModel):
    country_ru: str
    country_en: Optional[str]
    country_uz: Optional[str]
    code: Optional[str]

    # @validator('code')
    # def code_must_be_upper(cls, v):
    #     if v != v.upper():
    #         raise ValueError('code must be upper')
    #     return v

    # @validator('code')
    # def code_must_be_3_characters(cls, v):
    #     if len(v) != 3:
    #         raise ValueError('code must be 3 characters')
    #     return v

    class Config:
        schema_extra = {
            "example": {
                "country_ru": "Россия",
                "country_en": "Russia",
                "country_uz": "Rossiya",
                "code": "RUS"
            }
        }


class CountryUpdate(CountryCreate):
    country_ru: Optional[str]


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
