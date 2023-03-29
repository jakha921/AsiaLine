from datetime import datetime

from pydantic import BaseModel, validator
from typing import Optional

from sqlalchemy import Enum


class UserHistory(BaseModel):
    id: int
    user_id: int
    action: str
    extra_info: Optional[str]
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
