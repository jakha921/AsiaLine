from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging
from datetime import datetime

from crud_models.views.flights import Flight, FlightPriceHistory
from db import models
from db.database import get_db
from crud_models.schemas import flights as schemas
from auth.auth_token.auth_bearer import JWTBearer
from auth.auth_token.auth_handler import check_permissions, get_user_id

routers = APIRouter()


# region Flight
@routers.get("/flights", response_model=list[schemas.Flight], tags=["flights"])
async def get_flights(page: Optional[int] = None,
                      limit: Optional[int] = None,
                      jwt: dict = Depends(JWTBearer()),
                      db: Session = Depends(get_db)):
    """
    Get list of flights where departure date is greater than current date and flight is not deleted\n
    *if offset and limit None return all flights*\n
    *if offset and limit not None return flights between offset and limit.*
    """
    if not check_permissions("get_flights", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        return Flight.get_list(db, page, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/flight/{flight_id}", tags=["flights"])
async def get_flight(flight_id: int,
                     jwt: dict = Depends(JWTBearer()),
                     db: Session = Depends(get_db)):
    """ Get flight by id if departure date is greater than current date and flight is not deleted """
    if not check_permissions("get_flight", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        db_flight = Flight.get_by_id(db, flight_id)
        if db_flight is None:
            raise ValueError("Flight not found")
        return schemas.Flight.from_orm(db_flight)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.post("/flight", tags=["flights"])
async def create_flight(flight: schemas.FlightCreate,
                        jwt: dict = Depends(JWTBearer()),
                        db: Session = Depends(get_db)):
    """
    Create new flight\n
    **Rules**:\n
    * departure date must be greater than current date\n
    * arrival date must be greater than departure date\n
    * departure airport must be different from arrival airport\n
    * on sale date must be greater than current date\n
    """
    if not check_permissions("create_flight", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        # check flight.flight_guide_id and departure_date is same return error
        if Flight.is_flight_exist_today(db, flight.flight_guide_id, flight.departure_date):
            raise ValueError("This flight is already exists today")
        create = Flight.create(db, flight, get_user_id(jwt))
        if flight.price > 0:
            FlightPriceHistory.create(db, flight.price, create.id)
        return schemas.Flight.from_orm(create)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.patch("/flight/{flight_id}", tags=["flights"])
async def update_flight(flight_id: int,
                        flight: schemas.FlightUpdate,
                        jwt: dict = Depends(JWTBearer()),
                        db: Session = Depends(get_db)):
    """
    Update flight by id\n
    **Optional fields:**\n
    * all fields except id\n
    **Rules:**\n
    * departure date must be greater than current date\n
    * arrival date must be greater than departure date\n
    * departure airport must be different from arrival airport\n
    * left seats must be less than total seats\n
    * on sale date must be greater than current date\n
    * left seats must be less than total seats\n
    * total seats must be greater than left seats\n
    * price must be greater than 0\n
    """
    if not check_permissions("update_flight", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        db_flight = Flight.get_by_id(db, flight_id)
        if db_flight is None:
            raise ValueError("Flight not found")

        if flight.total_seats and flight.left_seats:
            if flight.total_seats < flight.left_seats:
                raise ValueError("Total seats must be greater than left seats")

        if flight.total_seats:
            if flight.total_seats < db_flight.left_seats:
                raise ValueError("Total seats must be greater than left seats")
        elif flight.left_seats:
            if flight.left_seats > db_flight.total_seats:
                raise ValueError("Left seats must be less than total seats")
        else:
            flight.total_seats = db_flight.total_seats
            flight.left_seats = db_flight.left_seats

        current_price, db_price = flight.price, db_flight.price
        update = Flight.update(db, db_flight, flight, get_user_id(jwt))
        if current_price != db_price:
            FlightPriceHistory.create(db, flight.price, update.id)
        return schemas.Flight.from_orm(update)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.delete("/flight/{flight_id}", tags=["flights"])
async def delete_flight(flight_id: int,
                        jwt: dict = Depends(JWTBearer()),
                        db: Session = Depends(get_db)):
    """
     **Attention:**\n
     Get all quotas and tickets of this flight and delete them.
     """
    if not check_permissions("delete_flight", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        db_flight = Flight.get_by_id(db, flight_id)
        if db_flight is None or db_flight.deleted_at is not None:
            raise ValueError("Flight not found")
        if db_ticket := db.query(models.Ticket).filter(models.Ticket.flight_id == db_flight.id).all():
            raise ValueError(f"Flight has {len(db_ticket)} tickets")
        if db_booking := db.query(models.Booking).filter(models.Booking.flight_id == db_flight.id).all():
            raise ValueError(f"Flight has {len(db_booking)} bookings")
        return Flight.delete(db, db_flight, get_user_id(jwt))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/flight/{flight_id}/tickets", tags=["flights"])
async def get_flight_tickets(flight_id: int,
                             jwt: dict = Depends(JWTBearer()),
                             db: Session = Depends(get_db)):
    """ Get all tickets of flight by id """
    if not check_permissions("get_flight_tickets", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        tickets = Flight.get_flight_tickets(db, flight_id)
        if not tickets:
            raise ValueError("Tickets not found")
        return tickets
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.patch("/flight-set-on-sale/{flight_id}", tags=["flights"])
async def set_flight_for_sale(flight_id: int,
                              jwt: dict = Depends(JWTBearer()),
                              db: Session = Depends(get_db)):
    """ Set flight for sale from now """
    if not check_permissions("set_flight_for_sale", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        db_flight = Flight.get_by_id(db, flight_id)
        if db_flight is None or db_flight.deleted_at is not None or db_flight.departure_date < datetime.now():
            raise ValueError("Flight not found")
        if db_flight.on_sale < datetime.now():
            raise ValueError("Flight already on sale")
        return Flight.set_on_sale_now(db, db_flight)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/flight/{flight_id}/prices", response_model=list[schemas.FlightHistory], tags=["flights"])
async def get_flight_price_history_by_flight_id(flight_id: int,
                                                page: Optional[int] = None,
                                                limit: Optional[int] = None,
                                                jwt: dict = Depends(JWTBearer()),
                                                db: Session = Depends(get_db)):
    """ Get flight ID and return list of flight price history for this flight """
    if not check_permissions("get_flight_prices", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        return FlightPriceHistory.get_by_flight_id(db, flight_id, page, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

# endregion
