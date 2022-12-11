from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from datetime import datetime, date 

from db.models import CurrencyCode, Language, Platform


#? Country
class CountryBase(BaseModel):
    country_ru: str
    short_name: str
    code: str
    
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
    country_en: Optional[str]
    country_uz: Optional[str]

class CountryUpdate(CountryCreate):
    country_ru: Optional[str]
    country_en: Optional[str]
    country_uz: Optional[str]
    short_name: Optional[str]
    code: Optional[str]

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
    city_en: Optional[str]
    city_uz: Optional[str]

class CityUpdate(CityCreate):
    city_ru: Optional[str]
    city_en: Optional[str] = ''
    city_uz: Optional[str] = ''
    country_id: Optional[int]

class City(BaseModel):
    id: Optional[int]
    city_ru: Optional[str]
    city_en: Optional[str]
    city_uz: Optional[str]
    country_id: Optional[int]
    
    class Config:
        orm_mode = True


#? Airport
class AirportBase(BaseModel):
    airport_ru: str
    city_id: int
    
    class Config:
        orm_mode = True
        
    @validator('city_id')
    def city_id_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('city_id must be greater than 0')
        return v

class AirportCreate(AirportBase):
    airport_en: Optional[str]
    airport_uz: Optional[str] 

class AirportUpdate(AirportCreate):
    airport_ru: Optional[str]
    airport_en: Optional[str]
    airport_uz: Optional[str]
    city_id: Optional[int]

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
    left_seats: Optional[int]
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
    
    @validator('left_seats')
    def left_seats_lt_than_total_seats(cls, v, values):
        if v > values['total_seats']:
            raise ValueError('left_seats must be less than total_seats')
        return v
    
    # departure_date must be after now
    @validator('departure_date')
    def departure_date_must_be_after_now(cls, v):
        if v <= datetime.now():
            raise ValueError('departure_date must be after now')
        return v
    
    # price must be positive
    @validator('price')
    def price_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('price must be positive')
        return v
    
    # arrival time must be after now
    @validator('arrival_date')
    def arrival_date_must_be_after_now(cls, v, values):
        if v < datetime.now():
            raise ValueError('arrival_date must be after now')
        return v

class FlightCreate(FlightBase):
    pass

class FlightUpdate(FlightBase):
    flight_number: Optional[str]
    from_airport_id: Optional[int]
    to_airport_id: Optional[int]
    departure_date: Optional[datetime]
    arrival_date: Optional[datetime]
    price: Optional[int]
    currency: str = CurrencyCode.RUB
    total_seats: Optional[int]
    left_seats: Optional[int]
    on_sale: Optional[datetime]
    actor_id: Optional[datetime]
    deleted_at: datetime = None

class Flight(BaseModel):
    id: int
    flight_number: str | None = None
    from_airport_id: int | None = None
    to_airport_id: int | None = None
    departure_date: datetime | None = None
    arrival_date: datetime | None = None
    price: int | None = None
    currency: str = CurrencyCode.RUB
    total_seats: int | None = None
    left_seats: Optional[int] | None = None
    on_sale: datetime | None = None
    actor_id: int | None = None


class CurrencyRate(BaseModel):
    rub_to_usd: float
    rub_to_eur: float
    rub_to_uzs: float
    updated_at: datetime
    

    class Config:
        orm_mode = True


# Flight price history
class FlightPriceHistory(BaseModel):
    id: int
    flight_id: Optional[int]
    new_price: int
    currency: str = CurrencyCode.RUB
    comment: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True


# ? Ticket
class TicketBase(BaseModel):
    flight_id: int
    first_name: str
    surname: str
    dob: date
    gender_id: Optional[int]
    passport: str
    citizenship: Optional[int]
    class_id: Optional[int]
    price: int 
    currency: str = CurrencyCode.RUB
    taking_amount: int
    status_id: Optional[int] = None

    class Config:
        orm_mode = True
        
    @validator('flight_id')
    def flight_id_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('flight_id must be greater than 0')
        return v
    
    @validator('first_name')
    def first_name_must_be_3_characters(cls, v):
        if len(v) < 2:
            raise ValueError('first_name must be more than 2 characters')
        return v
    
    @validator('surname')
    def surname_must_be_2_characters(cls, v):
        if len(v) < 2:
            raise ValueError('surname must be more than 2 characters')
        return v
    
    @validator('gender_id')
    def gender_must_be_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('gender_id must be more than 0 characters')
        return v
    
    @validator('citizenship')
    def citizenship_must_be_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('citizenship must be more than 0 characters')
        return v

    @validator('class_id')
    def class_id_must_be_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('class_id must be more than 0 characters')
        return v

    @validator('status_id')
    def status_id_must_be_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('status_id must be more than 0 characters')
        return v
    
    @validator('dob')
    def dob_must_be_low_than_now(cls, v):
        if v > datetime.now().date():
            raise ValueError('dob must be low than now')
        return v

class TicketCreate(TicketBase):
    agent_id: Optional[int]
    passenger_id: Optional[int]
    middle_name: Optional[str]
    discount_id: Optional[int]
    comment: Optional[str]
    luggage: Optional[int]
    actor_id: Optional[int]
    platform: str = Platform.WEB
    
    @validator('agent_id')
    def agent_id_must_be_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('agent_id must be greater than 0')
        return v
    
    @validator('passenger_id')
    def passenger_id_must_be_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('passenger_id must be greater than 0')
        return v
    
    @validator('discount_id')
    def discount_id_must_be_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('discount_id must be greater than 0')
        return v
    
    @validator('actor_id')
    def actor_id_must_be_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('actor_id must be greater than 0')
        return v

class TicketUpdate(TicketCreate):
    pass

class Ticket(TicketBase):
    id: int
    platform: str = Platform.WEB

    class Config:
        orm_mode = True
















































