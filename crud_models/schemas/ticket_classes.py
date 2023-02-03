from typing import Optional
from pydantic import BaseModel


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
