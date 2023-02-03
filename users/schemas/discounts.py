from pydantic import BaseModel
from typing import Optional


class DiscountCreate(BaseModel):
    amount: str
    name: str

    class Config:
        schema_extra = {
            "example": {
                "amount": "10",
                "name": "10% discount",
            }
        }


class DiscountUpdate(DiscountCreate):
    amount: Optional[str]
    name: Optional[str]


class Discount(DiscountCreate):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **DiscountCreate.Config.schema_extra.get("example"),
            }
        }
