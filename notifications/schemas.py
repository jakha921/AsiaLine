from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class NotificationCreate(BaseModel):
    user_id: int = Field(..., ge=1)
    message: str = Field(..., min_length=1)
    is_read: bool = False
    created_at: Optional[datetime] = datetime.utcnow().strftime("%Y-%m-%d %H:%M")

    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "title": "Title",
                "message": "Message",
                "is_read": False,
                "created_at": "2021-01-01 00:00"
            }
        }


class Notification(NotificationCreate):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **NotificationCreate.Config.schema_extra.get("example"),
            }
        }


class NotificationUpdate(BaseModel):
    id: int = Field(..., ge=1)
    is_read: bool = True

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "is_read": True
            }
        }