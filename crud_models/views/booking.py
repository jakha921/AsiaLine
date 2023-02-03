from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from db import models
from crud_models.schemas import booking as schemas


class Booking:
    @staticmethod
    def get_list(db: Session, offset: Optional[int], limit: Optional[int]):

        query = db.query(models.Booking) \
            .filter(
            models.Booking.deleted_at == None,
            models.Flight.id == models.Booking.flight_id,
            models.Flight.deleted_at == None,
            models.Flight.departure_date >= datetime.now())

        if offset and limit:
            return query.offset(limit * (offset - 1)).limit(limit).all()
        return query.all()

    @staticmethod
    def get_by_id(db: Session, booking_id: int):
        return db.query(models.Booking). \
            filter(
            models.Booking.id == booking_id,
            models.Booking.deleted_at == None,
            models.Flight.id == models.Booking.flight_id,
            models.Flight.deleted_at == None,
            models.Flight.departure_date >= datetime.now()
        ).first()

    @staticmethod
    def create(db: Session,
               booking: schemas.BookingCreate,
               flight: models.Flight):
        """ if booking created successfully, -1 from models Flight left_seats """
        try:
            if flight.left_seats - booking.hard_block - booking.soft_block < 0:
                raise ValueError('Flight has not enough seats')

            flight.left_seats -= booking.hard_block + booking.soft_block
            db_booking = models.Booking(**booking.dict())
            db_booking.price = flight.price
            db.add(db_booking)
            db.commit()
            db.refresh(db_booking)

            return db_booking
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    @staticmethod
    def update(db: Session, patch: schemas.BookingUpdate, booking: models.Booking, flight: models.Flight):
        """ find difference between old and new booking and update models Flight left_seats """

        diff = booking.hard_block + booking.soft_block - patch.hard_block - patch.soft_block
        flight.left_seats += diff
        if flight.left_seats < 0:
            return {'error': 'Flight has not enough seats'}

        for key, value in patch.dict().items():
            if value is not None:
                setattr(booking, key, value)
        db.commit()
        return booking

    @staticmethod
    def delete(db: Session, booking_id: int):
        db_booking = db.query(models.Booking, models.Agent, models.Flight). \
            filter(models.Booking.id == booking_id,
                   models.Agent.id == models.Booking.agent_id,
                   models.Flight.id == models.Booking.flight_id).first()

        booking = db_booking['Booking']
        agent = db_booking['Agent']
        flight = db_booking['Flight']

        agent.balance += booking.price * booking.hard_block

        flight.left_seats += booking.hard_block + booking.soft_block

        booking.deleted_at = datetime.now()
        db.commit()

        return {"message": "Booking deleted successfully"}
