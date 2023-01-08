from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from datetime import datetime, date, timedelta

from db.models import CurrencyCode, Language, Platform


# region Country
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


# endregion


# region City
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


# endregion


# region Airport
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


# endregion


# region Flight
class FlightCreate(BaseModel):
    flight_number: str
    from_airport_id: int
    to_airport_id: int
    departure_date: datetime
    arrival_date: datetime
    price: int
    currency: CurrencyCode
    total_seats: int
    on_sale: datetime
    actor_id: int

    # region Validators
    @validator('currency')
    def currency_must_be_in_currency_code(cls, v):
        if v not in ['USD', 'EUR', 'RUB', 'UZS']:
            raise ValueError('currency must be in CurrencyCode[USD, EUR, RUB, UZS]')
        return v

    @validator('from_airport_id')
    def from_airport_id_must_be_greater_than_0(cls, v):
        if v < 1:
            raise ValueError('from_airport_id must be greater than 0')
        return v

    @validator('to_airport_id')
    def to_airport_id_must_be_greater_than_0(cls, v):
        if v < 1:
            raise ValueError('to_airport_id must be greater than 0')
        return v

    @validator('actor_id')
    def actor_id_must_be_greater_than_0(cls, v):
        if v < 1:
            raise ValueError('actor_id must be greater than 0')
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
                "flight_number": "WZ 1234",
                "from_airport_id": 1,
                "to_airport_id": 2,
                "departure_date": (datetime.now() + timedelta(hours=12)).strftime("%Y-%m-%d %H:%M"),
                "arrival_date": (datetime.now() + timedelta(hours=18)).strftime("%Y-%m-%d %H:%M"),
                "price": 10000,
                "currency": "RUB",
                "total_seats": 100,
                "on_sale": (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
                "actor_id": 1
            }
        }


class FlightUpdate(FlightCreate):
    flight_number: Optional[str]
    from_airport_id: Optional[int]
    to_airport_id: Optional[int]
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

# endregion

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

    # endregion

    # region Ticket
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

    # endregion


# endregion


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


# endregion


# region Ticket
class TicketCreate(BaseModel):
    flight_id: int
    first_name: str
    surname: str
    middle_name: Optional[str]
    dob: date
    gender_id: int
    passport: str
    citizenship: int
    class_id: int
    agent_id: int
    comment: Optional[str]
    luggage: int
    actor_id: int
    status_id: int = 1
    platform: Platform = Platform.WEB

    # region Validators
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

    @validator('dob')
    def dob_must_be_low_than_now(cls, v):
        if v > datetime.now().date():
            raise ValueError('dob must be low than now')
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

    @validator('agent_id')
    def agent_id_must_be_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('agent_id must be greater than 0')
        return v

    @validator('passport')
    def passport_must_be_gt_than_0(cls, v):
        if len(v) < 1 and len(v) > 10:
            raise ValueError('passport must be greater than 0 and less than 10')
        return v

    @validator('platform')
    def platform_must_be_in_list(cls, v):
        if v not in [Platform.WEB, Platform.ANDROID, Platform.IOS]:
            raise ValueError('platform must be in list')
        return v

    # endregion

    class Config:
        schema_extra = {
            "example": {
                "flight_id": 1,
                "first_name": "John",
                "surname": "Doe",
                "middle_name": "Not required (type: str)",
                "dob": "1990-01-01",
                "gender_id": 1,
                "passport": "AA1234567",
                "citizenship": 1,
                "class_id": 1,
                "agent_id": 1,
                "comment": "Not required (type: str)",
                "luggage": 500,
                "actor_id": 1,
            }
        }


class TicketUpdate(TicketCreate):
    flight_id: Optional[int]
    price: Optional[int]
    first_name: Optional[str]
    surname: Optional[str]
    middle_name: Optional[str]
    dob: Optional[date]
    gender_id: Optional[int]
    passport: Optional[str]
    citizenship: Optional[int]
    class_id: Optional[int]
    status_id: Optional[int]
    agent_id: Optional[int]
    discount_id: Optional[int]
    comment: Optional[str]
    luggage: Optional[int]
    actor_id: Optional[int]
    platform: Optional[str]

    class Config:
        schema_extra = {
                    "example": {
                        **TicketCreate.Config.schema_extra.get("example"),
                    }
                }


class Ticket(TicketUpdate):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **TicketCreate.Config.schema_extra.get("example"),
                "created_at": "2021-07-01T10:00:00",
                "updated_at": "2021-07-01T10:00:00",
            }
        }


class TicketCancel(BaseModel):
    ticket_id: int
    fine: int
    currency: str

    @validator('currency')
    def currency_must_be_in_list(cls, v):
        if v not in [CurrencyCode.RUB, CurrencyCode.USD, CurrencyCode.EUR]:
            raise ValueError('currency must be in list [RUB, USD, EUR]')
        return v

    class Config:
        schema_extra = {
            "example": {
                "ticket_id": 1,
                "fine": 1000,
                "currency": "RUB",
            }
        }

# endregion


# region Booking:
class BookingCreate(BaseModel):
    flight_id: int
    agent_id: int
    hard_block: int
    soft_block: int

    # region Validation
    @validator('flight_id')
    def flight_id_must_be_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('flight_id must be greater than 0')
        return v

    @validator('agent_id')
    def agent_id_must_be_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('agent_id must be greater than 0')
        return v

    # endregion

    class Config:
        schema_extra = {
            "example": {
                "flight_id": 1,
                "agent_id": 1,
                "hard_block": 10,
                "soft_block": 10,
            }
        }


class BookingUpdate(BookingCreate):
    pass


class Booking(BookingUpdate):
    id: int
    flight_id: Optional[int]
    agent_id: Optional[int]
    hard_block: Optional[int]
    soft_block: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **BookingCreate.Config.schema_extra.get("example"),
                "created_at": "2021-07-01T10:00:00",
                "updated_at": "2021-07-01T10:00:00",
                "deleted_at": "2021-07-01T10:00:00",
            }
        }

# endregion


# region ScrapedPrice:
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

# endregion


# region Gender
class GenderCreate(BaseModel):
    gender_ru: str
    gender_en: str
    gender_uz: str
    description: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "gender_ru": "Мужской",
                "gender_en": "Male",
                "gender_uz": "Erkak",
                "description": "Мужской пол Optional[str]",
            }
        }


class GenderUpdate(GenderCreate):
    gender_ru: Optional[str]
    gender_en: Optional[str]
    gender_uz: Optional[str]


class Gender(GenderUpdate):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **GenderCreate.Config.schema_extra.get("example"),
            }
        }

# endregion


# region Refill
class RefillCreate(BaseModel):
    receiver_id: int
    agent_id: int
    amount: int
    comment: Optional[str]

    # region Validation
    @validator('receiver_id')
    def receiver_id_must_be_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('receiver_id must be greater than 0')
        return v

    @validator('agent_id')
    def agent_id_must_be_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('agent_id must be greater than 0')
        return v

    @validator('amount')
    def amount_not_negative(cls, v):
        if v < 0:
            raise ValueError('amount must be greater than 0')
        return v

    # endregion

    class Config:
        schema_extra = {
            "example": {
                "receiver_id": 1,
                "agent_id": 1,
                "amount": 100000,
                "comment": "Refill comment Optional[str]",
            }
        }


class RefillUpdate(RefillCreate):
    receiver_id: Optional[int]
    agent_id: Optional[int]
    amount: Optional[int]


class Refill(RefillUpdate):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **RefillCreate.Config.schema_extra.get("example"),
                "created_at": "2021-07-01T10:00:00",
                "updated_at": "2021-07-01T10:00:00",
                "deleted_at": "2021-07-01T10:00:00",
            }
        }

# endregion


# region Agent Debt
class AgentDebt(BaseModel):
    agent_id: int
    flight_id: int
    ticket_id: int
    type: str
    amount: int
    comment: Optional[str]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    # region Validation
    @validator('agent_id')
    def agent_id_must_be_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('agent_id must be greater than 0')
        return v

    @validator('flight_id')
    def flight_id_must_be_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('flight_id must be greater than 0')
        return v

    @validator('ticket_id')
    def ticket_id_must_be_gt_than_0(cls, v):
        if v < 1:
            raise ValueError('ticket_id must be greater than 0')
        return v

    @validator('type')
    def type_must_be_in_list(cls, v):
        """ type must be in list AgentDebt [refund, debt] """
        if v not in [AgentDebt.type for i in AgentDebt]:
            raise ValueError('type must be in list [refund, debt]')
        return v

    @validator('amount')
    def amount_not_negative(cls, v):
        if v < 0:
            raise ValueError('amount must be greater than 0')
        return v

    # endregion

    class Config:
        schema_extra = {
            "example": {
                "agent_id": 1,
                "flight_id": 1,
                "ticket_id": 1,
                "type": "refund",
                "amount": 100000,
                "comment": "Комментарий",
                "created_at": "2021-07-01T10:00:00",
                "updated_at": "2021-07-01T10:00:00",
                "deleted_at": "2021-07-01T10:00:00",
            }
        }

# endregion


# region Ticket Class
class TicketClassCreate(BaseModel):
    name_ru: str
    name_en: Optional[str]
    name_uz: Optional[str]
    code: str
    description: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name_ru": "Эконом",
                "name_en": "Economy",
                "name_uz": "Ekonom",
                "code": "Y",
                "description": "Эконом класс",
            }
        }


class TicketClassUpdate(TicketClassCreate):
    name_ru: Optional[str]
    name_en: Optional[str]
    name_uz: Optional[str]
    code: Optional[str]


class TicketClass(TicketClassUpdate):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **TicketClassCreate.Config.schema_extra.get("example"),
            }
        }

# endregion
