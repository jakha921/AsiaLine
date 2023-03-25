from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from db import models
from crud_models.schemas import booking as schemas
from users.views.user_history import History


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
    def is_agent_has_booking(db: Session, agent_id: int, flight_id: int):
        return db.query(models.Booking). \
            filter(
                models.Booking.agent_id == agent_id,
                models.Booking.flight_id == flight_id,
        ).first()

    @staticmethod
    def get_by_flight_id_and_agent_id(db: Session, flight_id: int, agent_id: int):
        return db.query(models.Booking). \
            filter(
            models.Booking.flight_id == flight_id,
            models.Booking.agent_id == agent_id,
            models.Booking.deleted_at == None,
            models.Flight.id == models.Booking.flight_id,
            models.Flight.deleted_at == None,
            models.Flight.departure_date >= datetime.now()
        ).first()

    @staticmethod
    def create(db: Session,
               booking: schemas.BookingCreate,
               flight: models.Flight,
               user_id: int):
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

            # add history
            query = db.query(models.User.username, models.FlightGuide.flight_number). \
                filter(models.User.id == user_id,
                       models.FlightGuide.id == flight.flight_guide_id).first()
            print("query: ", query)
            print(f'For agent {db_booking.agent_id} created booking for flight {db_booking.flight_id}')
            History.create(db, user_id=user_id, action='create booking',
                           extra_info=f'Booking {db_booking.id} created')

            return db_booking
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    @staticmethod
    def update(db: Session, booking: schemas.BookingUpdate, db_booking: models.Booking, flight: models.Flight,
               user_id: int):
        """ find difference between old and new booking and update models Flight left_seats """

        diff = db_booking.hard_block + db_booking.soft_block - booking.hard_block - booking.soft_block
        flight.left_seats += diff
        if flight.left_seats < 0:
            raise ValueError('Flight has not enough seats')

        extra_info = ''
        for key, value in booking.dict().items():
            if value is not None:
                # add to extra_info data which is changed
                if value != getattr(db_booking, key):
                    extra_info += f"{key}: {getattr(db_booking, key)} -> {value}\n"
                setattr(db_booking, key, value)
        db.commit()

        # add history
        print(extra_info)
        History.create(db, user_id=user_id, action='update booking',
                       extra_info=f'Booking {db_booking.id} updated\n{extra_info}')
        return db_booking

    @staticmethod
    def delete(db: Session, booking_id: int, user_id: int):
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

        # add history
        History.create(db, user_id=user_id, action='delete booking',
                       extra_info=f'Booking {booking.id} deleted')
        return {"message": "Booking deleted successfully"}
