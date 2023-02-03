from typing import Optional
from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from datetime import datetime
import logging

from crud_models.schemas.tickets import TicketCancel
from crud_models.views.booking import Booking
from crud_models.views.tickets import Ticket
from db import models
from crud_models.schemas import flights as schemas


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
    def create(db: Session, flight: schemas.FlightCreate, user_id: int):
        db_flight = models.Flight(**flight.dict())
        db_flight.left_seats = flight.total_seats
        db_flight.actor_id = user_id
        db.add(db_flight)
        db.commit()
        db.refresh(db_flight)
        return db_flight

    @staticmethod
    def update(db: Session, db_flight: models.Flight, flight: schemas.FlightUpdate):
        for key, value in flight.dict().items():
            if value is not None:
                setattr(db_flight, key, value)
        db.commit()
        return db_flight

    @staticmethod
    def delete(db: Session, flight: models.Flight):
        """ get all bookings and tickets of this flight and delete them """
        try:
            db_ticket = db.query(models.Ticket).filter(models.Ticket.flight_id == flight.id).all()
            db_booking = db.query(models.Booking).filter(models.Booking.flight_id == flight.id).all()

            for ticket in db_ticket:
                ticket_schema = TicketCancel(
                    ticket_id=ticket.id,
                    fine=0,
                    currency='RUB',
                )
                Ticket.cancel(db, ticket_schema)
            for booking in db_booking:
                Booking.delete(db, booking.id)
            flight.deleted_at = datetime.now()
            db.commit()
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
