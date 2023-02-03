from typing import Optional
from pydantic import BaseModel, validator


class AirportCreate(BaseModel):
    airport_ru: str
    airport_en: Optional[str]
    airport_uz: Optional[str]
    city_id: int

    @validator('city_id')
    def city_id_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('city_id must be greater than 0')
        return v

    class Config:
        schema_extra = {
            "example": {
                "airport_ru": "Шереметьево",
                "airport_en": "Sheremetyevo",
                "airport_uz": "Sheremetyevo",
                "city_id": 1
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
