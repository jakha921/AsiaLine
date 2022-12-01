from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from datetime import datetime 

from db.models import CurrencyCode

#? Country
class CountryBase(BaseModel):
    country_ru: str = 'Узбекистан'
    short_name: str = 'UZ'
    code: str = 'uzb'
    
    class Config:
        orm_mode = True

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


class CountryCreate(CountryBase):
    country_en: Optional[str] = None
    country_uz: Optional[str] = None


class CountryUpdate(CountryCreate):
    pass


class Country(BaseModel):
    id: int
    country_ru: str
    country_en: Optional[str]
    country_uz: Optional[str]
    short_name: str
    code: str
    
    class Config:
        orm_mode = True


#? City
class CityBase(BaseModel):
    city_ru: str
    country_id: int = 1 
    
    class Config:
        orm_mode = True


class CityCreate(CityBase):
    city_en: str
    city_uz: str


class CityUpdate(CityCreate):
    pass


class City(BaseModel):
    id: int
    city_ru: str
    city_en: str
    city_uz: str
    country_id: int
    
    class Config:
        orm_mode = True


#? Airport
class AirportBase(BaseModel):
    airport_ru: str
    city_id: int
    
    class Config:
        orm_mode = True


class AirportCreate(AirportBase):
    airport_en: Optional[str] = 'null'
    airport_uz: Optional[str] = 'null'


class AirportUpdate(AirportCreate):
    pass


class Airport(AirportCreate):
    id: int
    airport_ru: str
    airport_en: Optional[str]
    airport_uz: Optional[str]
    city_id: int
    
    class Config:
        orm_mode = True


#? Flight
class FlightBase(BaseModel):
    flight_number: str
    from_airport_id: int = 1
    to_airport_id: int = 2
    departure_date: datetime
    arrival_date: datetime
    price: int
    currency: str = CurrencyCode.RUB
    total_seats: int
    left_seats: int
    on_sale: datetime
    actor_id: int = 1
    # deleted_at: datetime | None = None
    
    class Config:
        orm_mode = True

    @validator('currency')
    def currency_must_be_3_characters(cls, v):
        if len(v) > 3:
            raise ValueError('currency must be less than 3 characters')
        return v
    
    @validator('from_airport_id')
    def from_airport_id_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('from_airport_id must be greater than 0')
        return v
    
    @validator('to_airport_id')
    def to_airport_id_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('to_airport_id must be greater than 0')
        return v
    
    @validator('actor_id')
    def actor_id_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('actor_id must be greater than 0')
        return v


class FlightCreate(FlightBase):
    pass


class FlightUpdate(FlightBase):
    deleted_at: datetime = None


class Flight(FlightBase):
    id: int


class CurrencyRate(BaseModel):
    rub_to_usd: float
    rub_to_eur: float
    rub_to_uzs: float
    updated_at: datetime

    class Config:
        orm_mode = True
























































