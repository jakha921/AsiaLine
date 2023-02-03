from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator


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
