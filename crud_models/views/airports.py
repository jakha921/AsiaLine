from typing import Optional

from sqlalchemy.orm import Session

from db import models
from crud_models.schemas import airports as schemas


class Airport:
    @staticmethod
    def get_list(db: Session, offset: Optional[int], limit: Optional[int]):
        if offset and limit:
            return db.query(models.Airport).offset(limit * (offset - 1)).limit(limit).all()
        return db.query(models.Airport).all()

    @staticmethod
    def get_by_id(db: Session, airport_id: int):
        return db.query(models.Airport).filter(models.Airport.id == airport_id).first()

    @staticmethod
    def create(db: Session, airport: schemas.AirportCreate):
        db_airport = models.Airport(**airport.dict())
        db.add(db_airport)
        db.commit()
        db.refresh(db_airport)
        return db_airport

    @staticmethod
    def update(db: Session, db_airport: models.Airport, airport: schemas.AirportUpdate):
        for key, value in airport.dict().items():
            if value is not None:
                setattr(db_airport, key, value)
        db.commit()
        return db_airport

    @staticmethod
    def delete(db: Session, db_airport: models.Airport):
        db.delete(db_airport)
        db.commit()
        return db_airport