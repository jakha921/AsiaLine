from typing import Optional
from pydantic import BaseModel, validator
from datetime import datetime

from db.models import CurrencyCode


class ScrapedPriceCreate(BaseModel):
    flight_id: int
    price: int
    currency: str
    name: str
    created_at: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # region Validation
    @validator('currency')
    def currency_must_be_in_list(cls, v):
        if v not in [CurrencyCode.RUB, CurrencyCode.USD, CurrencyCode.EUR]:
            raise ValueError('currency must be in list [RUB, USD, EUR]')
        return v

    @validator('flight_id')
    def flight_id_must_be_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('flight_id must be greater than 0')
        return v

    @validator('price')
    def price_not_less_than_0(cls, v):
        if v < 0:
            raise ValueError('price must be greater than 0')
        return v

    # endregion

    class Config:
        schema_extra = {
            "example": {
                "flight_id": 1,
                "price": 100000,
                "currency": "RUB",
                "name": "S7",
            }
        }


class ScrapedPriceUpdate(ScrapedPriceCreate):
    flight_id: Optional[int]
    price: Optional[int]
    currency: Optional[str]
    name: Optional[str]
    created_at: Optional[datetime]


class ScrapedPrice(ScrapedPriceUpdate):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **ScrapedPriceCreate.Config.schema_extra.get("example"),
                "created_at": "2021-07-01T10:00:00",
            }
        }
