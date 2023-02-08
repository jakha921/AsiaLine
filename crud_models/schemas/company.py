from pydantic import BaseModel, validator
from typing import Optional


class CompanyCreate(BaseModel):
    name: str
    icon: Optional[str]
    code: Optional[str]
    description: Optional[str]

    # region Validators
    @validator('code')
    def code_must_be_less_than_3_characters(cls, v):
        if len(v) > 3:
            raise ValueError('code must be less than 3 characters')
        return v

    # endregion

    class Config:
        schema_extra = {
            "example": {
                "name": "Red Wings",
                "icon":
                    "https://www.ch-aviation.com/images/stockPhotos/5657/9097500ce46c786feaf14e391fc829cc154157c2.jpg",
                "code": "WZ",
                "description":
                    "Wizz Air is a Hungarian low-cost airline, based in Budapest. "
                    "It operates scheduled and charter services to 44 destinations in 16 countries, "
                    "mainly in Central and Eastern Europe, North Africa and the Middle East."
            }
        }


class Company(CompanyCreate):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **CompanyCreate.Config.schema_extra['example']
            }
        }