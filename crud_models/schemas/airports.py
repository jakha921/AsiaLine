from typing import Optional
from pydantic import BaseModel, validator


class AirportCreate(BaseModel):
    city_id: int
    airport_ru: str
    airport_en: Optional[str]
    airport_uz: Optional[str]
    code: Optional[str]

    @validator('city_id')
    def city_id_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('city_id must be greater than 0')
        return v

    @validator('code')
    def code_must_be_upper(cls, v):
        if v != v.upper():
            raise ValueError('code must be upper')
        return v

    @validator('code')
    def code_must_be_3_characters(cls, v):
        if len(v) != 3:
            raise ValueError('code must be 3 characters')
        return v

    class Config:
        schema_extra = {
            "example": {
                "city_id": 1,
                "airport_ru": "Шереметьево",
                "airport_en": "Sheremetyevo",
                "airport_uz": "Sheremetyevo",
                "code": "SVO"
            }
        }


class AirportUpdate(AirportCreate):
    airport_ru: Optional[str]
    city_id: Optional[int]


class Airport(AirportCreate):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **AirportCreate.Config.schema_extra.get("example"),
            }
        }
