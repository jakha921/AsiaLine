from typing import Optional
from pydantic import BaseModel, validator
from datetime import datetime, date

from db.models import CurrencyCode, Platform


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

# region Ticket
# class TicketBase(BaseModel):
#     flight_id: int
#     first_name: str
#     surname: str
#     dob: date
#     gender_id: Optional[int]
#     passport: str
#     citizenship: Optional[int]
#     class_id: Optional[int]
#     price: int
#     currency: str = CurrencyCode.RUB
#     taking_amount: int
#     status_id: Optional[int] = None
#
#     class Config:
#         orm_mode = True
#
#     # region Validation
#     @validator('flight_id')
#     def flight_id_gt_than_0(cls, v):
#         if v < 1:
#             raise ValueError('flight_id must be greater than 0')
#         return v
#
#     @validator('first_name')
#     def first_name_must_be_3_characters(cls, v):
#         if len(v) < 2:
#             raise ValueError('first_name must be more than 2 characters')
#         return v
#
#     @validator('surname')
#     def surname_must_be_2_characters(cls, v):
#         if len(v) < 2:
#             raise ValueError('surname must be more than 2 characters')
#         return v
#
#     @validator('gender_id')
#     def gender_must_be_gt_than_0(cls, v):
#         if v < 1:
#             raise ValueError('gender_id must be more than 0 characters')
#         return v
#
#     @validator('citizenship')
#     def citizenship_must_be_gt_than_0(cls, v):
#         if v < 1:
#             raise ValueError('citizenship must be more than 0 characters')
#         return v
#
#     @validator('class_id')
#     def class_id_must_be_gt_than_0(cls, v):
#         if v < 1:
#             raise ValueError('class_id must be more than 0 characters')
#         return v
#
#     @validator('status_id')
#     def status_id_must_be_gt_than_0(cls, v):
#         if v < 1:
#             raise ValueError('status_id must be more than 0 characters')
#         return v
#
#     @validator('dob')
#     def dob_must_be_low_than_now(cls, v):
#         if v > datetime.now().date():
#             raise ValueError('dob must be low than now')
#         return v
#
#     # region Validation
#
#
# class TicketCreate(TicketBase):
#     agent_id: Optional[int]
#     passenger_id: Optional[int]
#     middle_name: Optional[str]
#     discount_id: Optional[int]
#     comment: Optional[str]
#     luggage: Optional[int]
#     actor_id: Optional[int]
#     platform: str = Platform.WEB
#
#     @validator('passenger_id')
#     def passenger_id_must_be_gt_than_0(cls, v):
#         if v < 1:
#             raise ValueError('passenger_id must be greater than 0')
#         return v
#
#     @validator('discount_id')
#     def discount_id_must_be_gt_than_0(cls, v):
#         if v < 1:
#             raise ValueError('discount_id must be greater than 0')
#         return v
#
#     @validator('actor_id')
#     def actor_id_must_be_gt_than_0(cls, v):
#         if v < 1:
#             raise ValueError('actor_id must be greater than 0')
#         return v
#
#
# class TicketUpdate(TicketCreate):
#     pass
#
#
# class Ticket(TicketBase):
#     id: int
#     platform: str = Platform.WEB
#
#     class Config:
#         orm_mode = True


# endregion
