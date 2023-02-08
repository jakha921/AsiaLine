from pydantic import BaseModel, validator
from typing import Optional


class FlightGuideCreate(BaseModel):
    company_id: int
    flight_number: str
    from_airport_id: int
    to_airport_id: int
    luggage: Optional[int]

    # region Validators
    @validator('luggage')
    def luggage_must_be_equal_or_greater_than_0(cls, v):
        if v < 0:
            raise ValueError('luggage must be equal or greater than 0')
        return v

    # endregion

    class Config:
        schema_extra = {
            "example": {
                "company_id": 1,
                "flight_number": "WZ 1234",
                "from_airport_id": 1,
                "to_airport_id": 2,
                "luggage": 0
            }
        }


class FlightGuide(FlightGuideCreate):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                **FlightGuideCreate.Config.schema_extra['example']
            }
        }
