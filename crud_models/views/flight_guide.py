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
        flight_guide = db.query(models.FlightGuide)
        if page and limit:
            return flight_guide.offset(limit * (page - 1)).limit(limit).all()
        return db.query(models.FlightGuide).all()

    @staticmethod
    def get_by_id(db: Session, flight_guide_id: int):
        return db.query(models.FlightGuide). \
            filter(models.FlightGuide.id == flight_guide_id).first()

    @staticmethod
    def get_by_flight_number(db: Session, flight_number: str):
        return db.query(models.FlightGuide). \
            filter(models.FlightGuide.flight_number == flight_number).first()

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

    @staticmethod
    def get_detail_flight_guide(db: Session, page: Optional[int], limit: Optional[int], search: Optional[str] = None):
        query = f"SELECT fg.id, fg.flight_number, \
            json_build_object('id', c.id, 'name', c.name, 'code', c.code, 'description', c.description) as company, \
            json_build_object('id', a1.id, 'name_ru', a1.airport_ru, 'name_en', a1.airport_en, 'name_uz', a1.airport_uz,\
            'code', a1.code) as airport_from, \
            json_build_object('id', a2.id, 'name_ru', a2.airport_ru, 'name_en', a2.airport_en,'name_en', a1.airport_en, \
            'code', a2.code) as airport_to, \
            fg.luggage, fg.baggage_weight \
            FROM flight_guides AS fg \
            JOIN companies AS c ON fg.company_id = c.id \
            JOIN airports AS a1 ON fg.from_airport_id = a1.id \
            JOIN airports AS a2 ON fg.to_airport_id = a2.id "

        if search:
            search = search.lower()
            query += f"WHERE LOWER(fg.flight_number) LIKE '%{search}%' \
                OR LOWER(c.name) LIKE '%{search}%' \
                OR LOWER(a1.code) LIKE '%{search}%' \
                OR LOWER(a2.code) LIKE '%{search}%' "

        counter = db.execute(query).fetchall()

        if page and limit:
            query += f" OFFSET {limit * (page - 1)} LIMIT {limit}"

        return db.execute(query).fetchall(), len(counter)

