from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime, timedelta

from db.models import CurrencyCode


class FlightCreate(BaseModel):
    flight_guide_id: int
    departure_date: datetime
    arrival_date: datetime
    price: int
    currency: CurrencyCode
    total_seats: int
    on_sale: datetime

    # region Validators
    @validator('currency')
    def currency_must_be_in_currency_code(cls, v):
        if v not in ['USD', 'EUR', 'RUB', 'UZS']:
            raise ValueError('currency must be in CurrencyCode[USD, EUR, RUB, UZS]')
        return v

    @validator('departure_date')
    def departure_date_must_be_greater_than_now(cls, v):
        if v < datetime.now():
            raise ValueError('departure_date must be greater than now')
        return v

    @validator('arrival_date')
    def arrival_date_must_be_greater_than_departure_date(cls, v, values):
        if v < values.get('departure_date'):
            raise ValueError('arrival_date must be greater than departure_date')
        return v

    @validator('price')
    def price_must_be_greater_than_0(cls, v):
        if v < 1:
            raise ValueError('price must be greater than 0')
        return v

    @validator('total_seats')
    def total_seats_must_be_greater_than_0(cls, v):
        if v < 1:
            raise ValueError('total_seats must be greater or equal than 0')
        return v

    # endregion

    class Config:
        schema_extra = {
            "example": {
                "flight_guide_id": 1,
                "departure_date": (datetime.now() + timedelta(hours=6)).strftime("%Y-%m-%d %H:%M"),
                "arrival_date": (datetime.now() + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M"),
                "price": 1500,
                "currency": "RUB",
                "total_seats": 30,
                "on_sale": (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
            }
        }


class FlightUpdate(FlightCreate):
    flight_guide_id: Optional[int]
    departure_date: Optional[datetime]
    arrival_date: Optional[datetime]
    price: Optional[int]
    currency: Optional[str]
    total_seats: Optional[int]
    left_seats: Optional[int]
    on_sale: Optional[datetime]
    actor_id: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                **FlightCreate.Config.schema_extra.get("example"),
                "left_seats": 100,
            }
        }


class Flight(FlightUpdate):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    tickets: list

    # price_history: list

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **FlightUpdate.Config.schema_extra.get("example"),
                "left_seats": 100,
                "created_at": "2021-07-01T10:00:00",
                "updated_at": "2021-07-01T10:00:00",
                "deleted_at": "2021-07-01T10:00:00",
                "tickets": [],
                # "price_history": []
            }
        }


# region FlightHistory

class FlightHistoryCreate(BaseModel):
    flight_id: int
    new_price: int
    currency: str
    comment: Optional[str]

    @validator('flight_id')
    def flight_id_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('flight_id must be greater than 0')
        return v

    class Config:
        schema_extra = {
            "example": {
                "flight_id": 1,
                "new_price": 100000,
                "currency": "RUB",
                "comment": "Some comment",
            }
        }


class FlightHistory(FlightHistoryCreate):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **FlightHistoryCreate.Config.schema_extra.get("example"),
                "created_at": "2021-07-01T10:00:00",
            }
        }
