from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import between

from sqlalchemy.orm import Session
from datetime import datetime, date
import logging

from db import models
from crud_models.schemas import flights as schemas
from users.views.user_history import History


class FlightPriceHistory:
    @staticmethod
    def get_list(db: Session, offset: Optional[int], limit: Optional[int]):
        if offset and limit:
            return db.query(models.FlightPriceHistory).offset(offset).limit(limit).all()
        return db.query(models.FlightPriceHistory).all()

    @staticmethod
    def get_by_flight_id(db: Session, flight_id: int, offset: Optional[int], limit: Optional[int]):

        query = db.query(models.FlightPriceHistory). \
            filter(models.FlightPriceHistory.flight_id == flight_id). \
            order_by(models.FlightPriceHistory.created_at.desc())

        if offset and limit:
            return query.offset(limit * (offset - 1)).limit(limit).all()
        return query.all()

    @staticmethod
    def create(db: Session, price: int, flight_id: int):
        db_price = models.FlightPriceHistory(new_price=price, flight_id=flight_id)
        db.add(db_price)
        db.commit()
        db.refresh(db_price)
        return db_price


class Flight:
    @staticmethod
    def get_list(db: Session, page: Optional[int], limit: Optional[int]):

        query = db.query(models.Flight). \
            filter(models.Flight.deleted_at == None,
                   models.Flight.departure_date >= datetime.now()). \
            order_by(models.Flight.departure_date)

        if page and limit:
            return query.offset(limit * (page - 1)).limit(limit).all()
        return query.all()

    @staticmethod
    def get_by_id(db: Session, flight_id: int):
        return db.query(models.Flight). \
            filter(
            models.Flight.id == flight_id,
            models.Flight.deleted_at == None,
            models.Flight.departure_date >= datetime.now()).first()

    @staticmethod
    def is_flight_exist_today(db: Session, flight_guide_id: int, departure_date: date):
        min_date = datetime.combine(departure_date, datetime.min.time())
        max_date = datetime.combine(departure_date, datetime.max.time())
        return db.query(models.Flight). \
            filter(
            models.Flight.flight_guide_id == flight_guide_id,
            between(models.Flight.departure_date, min_date, max_date)).first()

    @staticmethod
    def create(db: Session, flight: schemas.FlightCreate, user_id: int):
        db_flight = models.Flight(**flight.dict())
        db_flight.left_seats = flight.total_seats
        db.add(db_flight)
        db.commit()
        db.refresh(db_flight)

        # add to user history
        History.create(db,
                       user_id=user_id,
                       action="create flight",
                       extra_info=f"Flight {db_flight.id} created")

        return db_flight

    @staticmethod
    def update(db: Session, db_flight: models.Flight, flight: schemas.FlightUpdate, user_id: int):
        extra_info = ""
        for key, value in flight.dict().items():
            if value is not None:
                # add to extra_info data which is changed
                if value != getattr(db_flight, key):
                    extra_info += f"{key}: {getattr(db_flight, key)} -> {value}\n"
                setattr(db_flight, key, value)
        db.commit()

        History.create(db,
                       user_id=user_id,
                       action="update flight",
                       extra_info=f"Flight {db_flight.id} updated:\n{extra_info}")

        return db_flight

    @staticmethod
    def delete(db: Session, flight: models.Flight, userid: int):
        """ get all bookings and tickets of this flight and delete them """
        try:
            flight.deleted_at = datetime.now()
            db.commit()

            # add to user history
            History.create(db, user_id=userid, action="delete flight", extra_info=f"Flight {flight.id} deleted")

            return {"message": "Flight deleted successfully and all tickets and bookings deleted for this flight"}
        except Exception as e:
            print(logging.error(e))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Flight has trouble on delete")

    @staticmethod
    def get_flight_tickets(db: Session, flight_id: int):
        return db.query(models.Ticket).filter(
            models.Ticket.flight_id == flight_id,
            models.Ticket.deleted_at == None,
            models.Flight.id == models.Ticket.flight_id,
            models.Flight.deleted_at == None,
            models.Flight.departure_date >= datetime.now()
        ).all()

    @staticmethod
    def set_on_sale_now(db: Session, db_flight: models.Flight):
        try:
            db_flight.on_sale = datetime.now()
            db.commit()
            return {"message": "Flight on sale now"}
        except Exception as e:
            print(logging.error(e))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Flight has trouble on sale now")
