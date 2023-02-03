from datetime import datetime

from pydantic import BaseModel, validator
from typing import Optional


class AgentCreate(BaseModel):
    user_id: int
    company_name: str
    balance: Optional[float]
    address: Optional[str]
    phone: Optional[str]
    registered_date: Optional[datetime]
    is_on_credit: Optional[bool] = False
    discount_id: int

    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "company_name": "Company",
                "address": "Address",
                "phone": "+998901234567",
                "is_on_credit": False,
                "discount_id": 1,
            }
        }


class AgentUpdate(BaseModel):
    user_id: Optional[int]
    company_name: Optional[str]
    balance: Optional[float]
    address: Optional[str]
    phone: Optional[str]
    registered_date: Optional[datetime]
    is_on_credit: Optional[bool] = False
    discount_id: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "company_name": "Company",
                "balance": 0.0,
                "address": "Address",
                "phone": "+998901234567",
                "is_on_credit": False,
                "discount_id": 1,
            }
        }


class Agent(AgentUpdate):
    id: int
    user_id: Optional[int]
    discount_id: Optional[int]
    block_date: Optional[datetime]
    registered_date: Optional[datetime]

    # bookings: list
    # role_permissions: list
    # tickets: list

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **AgentCreate.Config.schema_extra.get("example"),
                "block_date": "2021-01-01 00:00:00",
                "registered_date": "2021-01-01 00:00:00",
                # "bookings": [],
                # "role_permissions": [],
                # "tickets": [],
            }
        }


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

