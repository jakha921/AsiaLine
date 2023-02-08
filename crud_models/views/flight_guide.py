from typing import Optional
from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from datetime import datetime
import logging

from crud_models.schemas.tickets import TicketCancel
from crud_models.views.booking import Booking
from crud_models.views.tickets import Ticket
from db import models
from crud_models.schemas import flight_guide as schemas


class FlightGuide:
    @staticmethod
    def get_list(db: Session, page: Optional[int], limit: Optional[int]):
        if page and limit:
            return db.query(models.FlightGuide).offset(limit * (page - 1)).limit(limit).all()
        return db.query(models.FlightGuide).all()

    @staticmethod
    def get_by_id(db: Session, flight_guide_id: int):
        return db.query(models.FlightGuide). \
            filter(models.FlightGuide.id == flight_guide_id).first()

    @staticmethod
    def create(db: Session, flight_guide: schemas.FlightGuideCreate):
        db_flight_guide = models.FlightGuide(**flight_guide.dict())
        db.add(db_flight_guide)
        db.commit()
        db.refresh(db_flight_guide)
        return db_flight_guide

    @staticmethod
    def update(db: Session, db_flight_guide: models.FlightGuide, flight_guide: schemas.FlightGuideCreate):
        for key, value in flight_guide.dict(exclude_unset=True).items():
            setattr(db_flight_guide, key, value)
        db.commit()
        db.refresh(db_flight_guide)
        return db_flight_guide

    @staticmethod
    def delete(db: Session, db_flight_guide: models.FlightGuide):
        db.delete(db_flight_guide)
        db.commit()
        return {"message": "Flight guide deleted"}