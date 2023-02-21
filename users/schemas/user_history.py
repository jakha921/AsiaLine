from datetime import datetime

from pydantic import BaseModel, validator
from typing import Optional

from sqlalchemy import Enum


class UserHistoryCreate(BaseModel):
    user_id: int
    action: Enum(
        "flight_create",
        "flight_update",
        "flight_delete",
        "ticket_create",
        "ticket_update",
        "ticket_delete",
        "booking_create",
        "booking_update",
        "booking_delete",
        "user_create",
        "user_update",
        "user_delete",
        "agent_create",
        "agent_update",
        "agent_delete",
        "agent_balance_update",
        "agent_credit_update",
        "agent_block",
        "agent_unblock"
    )
    extra_info: Optional[str]

    # region Validators
    @validator('user_id')
    def user_id_must_be_positive(cls, v):
        if v < 1:
            raise ValueError('user_id must be positive')
        return v

    @validator('action')
    def action_must_be_valid(cls, v):
        if v not in [
            "flight_create",
            "flight_update",
            "flight_delete",
            "ticket_create",
            "ticket_update",
            "ticket_delete",
            "booking_create",
            "booking_update",
            "booking_delete",
            "user_create",
            "user_update",
            "user_delete",
            "agent_create",
            "agent_update",
            "agent_delete",
            "agent_balance_update",
            "agent_credit_update",
            "agent_block",
            "agent_unblock"
        ]:
            raise ValueError('action must be valid')
        return v

    # endregion

    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "action": "user_create",
                "extra_info": "User created by id 1"
            }
        }

    class Config:
        orm_mode = True


class UserHistory(UserHistoryCreate):
    id: int
    created_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "action": "user_create",
                "extra_info": "User created by id 1",
                "created_at": "2021-05-01 00:00:00"
            }
        }

    class Config:
        orm_mode = True
