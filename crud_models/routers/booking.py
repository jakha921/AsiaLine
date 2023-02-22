from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging
from datetime import datetime

from auth.auth_token.auth_bearer import JWTBearer
from auth.auth_token.auth_handler import check_permissions, get_user_id
from crud_models.views.flights import Flight
from db.database import get_db
from crud_models.schemas import booking as schemas
from crud_models.views.booking import Booking
from users.views.agents import Agent

routers = APIRouter()


@routers.get("/bookings", response_model=list[schemas.Booking], tags=["bookings"])
async def get_bookings(page: Optional[int] = None,
                       limit: Optional[int] = None,
                       jwt: dict = Depends(JWTBearer()),
                       db: Session = Depends(get_db)):
    """
    Get bookings list where booking is not deleted and flight departure date is greater than current date and
    flight is not deleted
    """
    if not check_permissions("get_bookings", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        return Booking.get_list(db, page, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/booking/{booking_id}", tags=["bookings"])
async def get_booking(booking_id: int,
                      jwt: dict = Depends(JWTBearer()),
                      db: Session = Depends(get_db)):
    """
    Get booking by id where booking is not deleted and flight departure date is greater than current date and
    flight is not deleted
    """
    if not check_permissions("get_booking", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        db_booking = Booking.get_by_id(db, booking_id)
        if db_booking is None:
            raise ValueError("Booking not found")
        return schemas.Booking.from_orm(db_booking)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.post("/booking", tags=["bookings"])
async def create_booking(booking: schemas.BookingCreate,
                         jwt: dict = Depends(JWTBearer()),
                         db: Session = Depends(get_db)):
    """
    Create booking
    **Rules:**\n
    * if flight is not on sale, booking will not be created
    * if flight is deleted, booking will not be created
    * if flight departure date is less than current date, booking will not be created
    * if flight left seats is less or equal to 0, booking will not be created
    """
    if not check_permissions("create_booking", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        if booking.flight_id is None:
            raise ValueError("Flight id is required")
        db_flight = Flight.get_by_id(db, booking.flight_id)
        if db_flight is None or db_flight.deleted_at is not None or db_flight.departure_date < datetime.now():
            raise ValueError("Flight not found")
        if db_flight.left_seats < 0:
            raise ValueError("Flight left seats is less than 0")
        if not Agent.get_by_id(db, booking.agent_id):
            raise ValueError("Agent not found")
        if Booking.get_by_flight_id_and_agent_id(db, booking.flight_id, booking.agent_id):
            raise ValueError("Booking already exists")

        return Booking.create(db, booking, db_flight, get_user_id(jwt))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    # except Exception as e:
        # print(logging.error(e))
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.patch("/booking/{booking_id}", tags=["bookings"])
async def update_booking(booking_id: int,
                         booking: schemas.BookingUpdate,
                         jwt: dict = Depends(JWTBearer()),
                         db: Session = Depends(get_db)):
    """
    Update booking by id\n
    **Rules:**\n
    * booking cannot be updated if flight is on sale
    * booking cannot be updated if flight is deleted
    * booking cannot be updated if flight departure date is less than current date
    * booking cannot be updated if booking is deleted
    """
    if not check_permissions("update_booking", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        db_booking = Booking.get_by_id(db, booking_id)
        if db_booking is None or db_booking.deleted_at is not None:
            raise ValueError("Booking not found")

        db_flight = Flight.get_by_id(db, booking.flight_id)
        if db_flight is None or db_flight.deleted_at is not None or db_flight.departure_date < datetime.now():
            raise ValueError("Flight not found")

        # if Booking.get_by_flight_id_and_agent_id(db, booking.flight_id, booking.agent_id):
        #     raise ValueError("Booking already exists")

        return Booking.update(db, booking, db_booking, db_flight, get_user_id(jwt))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@routers.delete("/booking/{booking_id}", tags=["bookings"])
async def delete_booking(booking_id: int,
                         jwt: dict = Depends(JWTBearer()),
                         db: Session = Depends(get_db)):
    """ Delete booking by id """
    if not check_permissions("delete_booking", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        db_booking = Booking.get_by_id(db, booking_id)
        if db_booking is None or db_booking.deleted_at is not None:
            raise ValueError("Booking not found")
        return Booking.delete(db, booking_id, get_user_id(jwt))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
