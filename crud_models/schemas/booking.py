from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


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

    @validator('hard_block')
    def hard_block_can_not_be_negative(cls, v):
        if v < 0:
            raise ValueError('hard_block can not be negative')
        return v

    @validator('soft_block')
    def soft_block_can_not_be_negative(cls, v):
        if v < 0:
            raise ValueError('soft_block can not be negative')
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
    price: Optional[int]
    currency: Optional[str]
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
