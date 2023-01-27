from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import logging

from starlette.responses import JSONResponse

from auth.auth.auth_bearer import JWTBearer
from auth.auth.auth_handler import check_permissions, get_user_id
from crud_models import crud, schemas
from db.database import get_db

routers = APIRouter()


# region Country
@routers.get("/countries", tags=["countries"], response_model=list[schemas.Country])
async def get_countries(
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        db: Session = Depends(get_db)):
    """
    Get list of countries\n
    *if offset and limit None return all countries*\n
    *if offset and limit not None return countries between offset and limit*.
    """
    try:
        return crud.Country.get_list(db, offset, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="get country list error")


@routers.get("/country/{country_id}", tags=["countries"])
async def get_country(country_id: int, db: Session = Depends(get_db)):
    """ Get country by id """
    try:
        db_country = crud.Country.get_by_id(db, country_id)
        if db_country is None:
            return {"detail": "Country not found"}
        return schemas.Country.from_orm(db_country)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="get country error")


@routers.post("/country", tags=["countries"])
async def create_country(country: schemas.CountryCreate, db: Session = Depends(get_db)):
    """ Create new country """
    try:
        return schemas.Country.from_orm(crud.Country.create(db, country))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="create country error")


@routers.patch("/country/{country_id}", tags=["countries"])
async def update_country(country_id: int, country: schemas.CountryUpdate, db: Session = Depends(get_db)):
    """
    Update country by id\n
    **Optional fields**:\n
    *all fields*
    """
    try:
        db_country = crud.Country.get_by_id(db, country_id)
        if db_country is None:
            return {"detail": "Country not found"}
        return schemas.Country.from_orm(crud.Country.update(db, db_country, country))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="update country error")


@routers.delete("/country/{country_id}", tags=["countries"])
async def delete_country(country_id: int, db: Session = Depends(get_db)):
    """ Delete country by id """
    try:
        db_country = crud.Country.get_by_id(db, country_id)
        if db_country is None:
            return {"detail": "Country not found"}
        return crud.Country.delete(db, db_country)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="delete country error")


# endregion


# region City
@routers.get("/cities", tags=["cities"], response_model=list[schemas.City])
async def get_cities(offset: Optional[int] = None, limit: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Get list of cities\n
    *if offset and limit None return all cities*\n
    *if offset and limit not None return cities between offset and limit*.
    """
    try:
        return crud.City.get_list(db, offset, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="get city list error")


@routers.get("/city/{city_id}", tags=["cities"])
async def get_city(city_id: int, db: Session = Depends(get_db)):
    """ Get city by id """
    try:
        db_city = crud.City.get_by_id(db, city_id)
        if db_city is None:
            return {"detail": "City not found"}
        return schemas.City.from_orm(db_city)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="get city error")


@routers.post("/city", tags=["cities"])
async def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    """ Create new city """
    try:
        return crud.City.create(db, city)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="create city error")


@routers.patch("/city/{city_id}", tags=["cities"])
async def update_city(city_id: int, city: schemas.CityUpdate, db: Session = Depends(get_db)):
    """
    Update city by id\n
    **Optional fields**:\n
    *all fields*
    """
    try:
        db_city = crud.City.get_by_id(db, city_id)
        if db_city is None:
            return {"detail": "City not found"}
        return schemas.City.from_orm(crud.City.update(db, db_city, city))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="update city error")


@routers.delete("/city/{city_id}", tags=["cities"])
async def delete_city(city_id: int, db: Session = Depends(get_db)):
    """ Delete city by id """
    try:
        db_city = crud.City.get_by_id(db, city_id)
        if db_city is None:
            return {"detail": "City not found"}
        return crud.City.delete(db, db_city)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="delete city error")


# endregion


# region Airport
@routers.get("/airports", response_model=list[schemas.Airport], tags=["airports"])
async def get_airports(offset: Optional[int] = None, limit: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Get list of airports\n
    *if offset and limit None return all airports*\n
    *if offset and limit not None return airports between offset and limit.*
    """
    try:
        return crud.Airport.get_list(db, offset, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="get airport list error")


@routers.get("/airport/{airport_id}", tags=["airports"])
async def get_airport(airport_id: int, db: Session = Depends(get_db)):
    """ Get airport by id """
    try:
        db_airport = crud.Airport.get_by_id(db, airport_id)
        if db_airport is None:
            return {"detail": "Airport not found"}
        return schemas.Airport.from_orm(db_airport)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="get airport error")


@routers.post("/airport", tags=["airports"])
async def create_airport(airport: schemas.AirportCreate, db: Session = Depends(get_db)):
    """ Create new airport """
    try:
        return schemas.Airport.from_orm(crud.Airport.create(db, airport))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="create airport error")


@routers.patch("/airport/{airport_id}", tags=["airports"])
async def update_airport(airport_id: int, airport: schemas.AirportUpdate, db: Session = Depends(get_db)):
    """
    Update airport by id\n
    **Optional fields**:\n
    *all fields*
    """
    try:
        db_airport = crud.Airport.get_by_id(db, airport_id)
        if db_airport is None:
            return {"detail": "Airport not found"}
        return schemas.Airport.from_orm(crud.Airport.update(db, db_airport, airport))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="update airport error")


@routers.delete("/airport/{airport_id}", tags=["airports"])
async def delete_airport(airport_id: int, db: Session = Depends(get_db)):
    """ Delete airport by id """
    try:
        db_airport = crud.Airport.get_by_id(db, airport_id)
        if db_airport is None:
            return {"detail": "Airport not found"}
        return crud.Airport.delete(db, db_airport)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="delete airport error")


# endregion


# region Flight
@routers.get("/flights", response_model=list[schemas.Flight], tags=["flights"])
async def get_flights(offset: Optional[int] = None, limit: Optional[int] = None,
                      db: Session = Depends(get_db), jwt: dict = Depends(JWTBearer())):
    """
    Get list of flights where departure date is greater than current date and flight is not deleted\n
    *if offset and limit None return all flights*\n
    *if offset and limit not None return flights between offset and limit.*
    """
    if not check_permissions("get_flights", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        return crud.Flight.get_list(db, offset, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/flight/{flight_id}", tags=["flights"])
async def get_flight(flight_id: int, db: Session = Depends(get_db), jwt: dict = Depends(JWTBearer())):
    """ Get flight by id if departure date is greater than current date and flight is not deleted """
    if not check_permissions("get_flight", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        db_flight = crud.Flight.get_by_id(db, flight_id)
        if db_flight is None:
            return {"detail": "Flight not found"}
        return schemas.Flight.from_orm(db_flight)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.post("/flight", tags=["flights"])
async def create_flight(flight: schemas.FlightCreate, db: Session = Depends(get_db), jwt: dict = Depends(JWTBearer())):
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
        if flight.from_airport_id == flight.to_airport_id:
            raise ValueError("Departure airport must be different from arrival airport")
        if flight.departure_date >= flight.arrival_date:
            raise ValueError("Arrival date must be greater than departure date")
        create = crud.Flight.create(db, flight, get_user_id(jwt))
        if flight.price > 0:
            crud.FlightPriceHistory.create(db, flight.price, create.id)
        return schemas.Flight.from_orm(create)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.patch("/flight/{flight_id}", tags=["flights"])
async def update_flight(flight_id: int, flight: schemas.FlightUpdate, db: Session = Depends(get_db),
                        jwt: dict = Depends(JWTBearer())):
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
        db_flight = crud.Flight.get_by_id(db, flight_id)
        if db_flight is None:
            raise ValueError("Flight not found")
        if flight.from_airport_id == flight.to_airport_id:
            raise ValueError("Departure airport must be different from arrival airport")
        if flight.total_seats and flight.left_seats:
            if flight.total_seats < flight.left_seats:
                raise ValueError("Total seats must be greater than left seats")

        if flight.total_seats or flight.left_seats:
            if flight.total_seats < db_flight.left_seats:
                raise ValueError("Total seats must be greater than left seats")
            if flight.left_seats > db_flight.total_seats:
                raise ValueError("Left seats must be less than total seats")

        current_price, db_price = flight.price, db_flight.price
        update = crud.Flight.update(db, db_flight, flight)
        if current_price != db_price:
            crud.FlightPriceHistory.create(db, flight.price, update.id)
        return schemas.Flight.from_orm(update)

    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.delete("/flight/{flight_id}", tags=["flights"])
async def delete_flight(flight_id: int, db: Session = Depends(get_db), jwt: dict = Depends(JWTBearer())):
    """
     **Attention:**\n
     Get all quotas and tickets of this flight and delete them.
     """
    if not check_permissions("delete_flight", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        db_flight = crud.Flight.get_by_id(db, flight_id)
        if db_flight is None or db_flight.deleted_at is not None:
            raise ValueError("Flight not found")
        return crud.Flight.delete(db, db_flight)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/flight/{flight_id}/tickets", tags=["flights"])
async def get_flight_tickets(flight_id: int, db: Session = Depends(get_db), jwt: dict = Depends(JWTBearer())):
    """ Get all tickets of flight by id """
    if not check_permissions("get_flight_tickets", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        tickets = crud.Flight.get_flight_tickets(db, flight_id)
        if tickets == []:
            raise ValueError("Flight not found")
        return tickets
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.patch("/flight-set-on-sale/{flight_id}", tags=["flights"])
async def set_flight_for_sale(flight_id: int, db: Session = Depends(get_db), jwt: dict = Depends(JWTBearer())):
    """ Set flight for sale from now """
    if not check_permissions("set_flight_for_sale", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        db_flight = crud.Flight.get_by_id(db, flight_id)
        if db_flight is None or db_flight.deleted_at is not None or db_flight.departure_date < datetime.now():
            raise ValueError("Flight not found")
        if db_flight.on_sale < datetime.now():
            raise ValueError("Flight already on sale")
        return crud.Flight.set_on_sale_now(db, db_flight)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/flight/{flight_id}/prices", response_model=list[schemas.FlightHistory], tags=["flights"])
async def get_flight_price_history_by_fligh_id(flight_id: int, offset: Optional[int] = 1, limit: Optional[int] = 10,
                                               db: Session = Depends(get_db), jwt: dict = Depends(JWTBearer())):
    """ Get flight id and return list of flight price history for this flight """
    if not check_permissions("get_flight_prices", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        return crud.FlightPriceHistory.get_by_flight_id(db, flight_id, offset, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


# endregion


# region Ticket
@routers.get("/tickets", response_model=list[schemas.Ticket], tags=["tickets"])
async def get_tickets(offset: Optional[int] = None, limit: Optional[int] = None,
                      db: Session = Depends(get_db), jwt: dict = Depends(JWTBearer())):
    """
    Get all tickets where ticket and flight are not deleted and flight departure date is greater than current date
    """
    if not check_permissions("get_tickets", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        return crud.Ticket.get_list(db, offset, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Internal server error get tickets")


@routers.get("/ticket/{ticket_id}", tags=["tickets"])
async def get_ticket(ticket_id: int, db: Session = Depends(get_db), jwt: dict = Depends(JWTBearer())):
    """ Get ticket by id where ticket and flight are not deleted and flight departure date is greater
    than current date """
    if not check_permissions("get_ticket", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    db_ticket = crud.Ticket.get_by_id(db, ticket_id)
    if db_ticket is None:
        return {"error": "Ticket not found"}
    return schemas.Ticket.from_orm(db_ticket)


@routers.post("/ticket", tags=["tickets"])
async def create_ticket(ticket: schemas.TicketCreate, hard: bool = False, soft: bool = False,
                        db: Session = Depends(get_db), jwt: dict = Depends(JWTBearer())):
    """
    Create ticket for flight\n
    **Rules:**\n
    * hard and soft cannot be true at the same time
    * if hard and soft are false,
     then ticket will be created from flight left seats quotes,
     if there are enough seats\n
    * if flight is not on sale, ticket will not be created
    * if flight is deleted, ticket will not be created
    * if flight departure date is less than current date, ticket will not be created
    * if flight left seats is less or equal to 0, ticket will not be created
    """
    try:
        if hard and soft:
            raise ValueError("hard and soft cannot be true at the same time")
        if ticket.flight_id is None:
            raise ValueError("flight_id is required")
        db_flight = crud.Flight.get_by_id(db, ticket.flight_id)
        if db_flight is None or db_flight.deleted_at is not None or db_flight.on_sale > datetime.now() or \
                db_flight.departure_date < datetime.now():
            raise ValueError("Flight not found")
        if db_flight.left_seats <= 0:
            raise ValueError("Flight left seats is less or equal to 0")
        return crud.Ticket.create(db, ticket, db_flight, hard, soft)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.patch("/ticket/{ticket_id}", tags=["tickets"])
async def update_ticket(ticket_id: int, ticket: schemas.TicketUpdate, db: Session = Depends(get_db),
                        jwt: dict = Depends(JWTBearer())):
    """
    Update ticket by id\n
    **Rules:**\n
    * ticket cannot be updated if flight is on sale
    * ticket cannot be updated if flight is deleted
    * ticket cannot be updated if flight departure date is less than current date
    * ticket cannot be updated if ticket is deleted
    """
    if not check_permissions("update_ticket", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        db_ticket = crud.Ticket.get_by_id(db, ticket_id)
        if db_ticket is None or db_ticket.deleted_at is not None:
            raise ValueError("Ticket not found")
        if ticket.flight_id is not None:
            db_flight = crud.Flight.get_by_id(db, ticket.flight_id)
            if db_flight is None or db_flight.deleted_at is not None or db_flight.on_sale > datetime.now() or \
                    db_flight.departure_date < datetime.now():
                raise ValueError("Flight not found")
        return schemas.Ticket.from_orm(crud.Ticket.update(db, db_ticket, ticket))
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


# @routers.delete("/ticket/{ticket_id}", tags=["tickets"])
async def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """
    Delete ticket by id\n
    **Rules:**\n
    * ticket cannot be deleted is already deleted
    """
    try:
        db_ticket = crud.Ticket.get_by_id(db, ticket_id)
        if db_ticket is None or db_ticket.deleted_at is not None:
            raise ValueError("Ticket not found")
        return crud.Ticket.delete(db, db_ticket)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.post("/ticket/cancellation", tags=["tickets"])
async def cancel_ticket_add_to_agent_fine(ticket_cancel: schemas.TicketCancel,
                                          db: Session = Depends(get_db), jwt: dict = Depends(JWTBearer())):
    """
    Cancel ticket and add fine to agent will bу added to flight left seats\n
    """
    if not check_permissions("cancel_ticket", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        db_ticket = crud.Ticket.get_by_id(db, ticket_cancel.ticket_id)
        if db_ticket.deleted_at or db_ticket is None:
            raise ValueError("Ticket not found")
        return crud.Ticket.cancel(db, ticket_cancel)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


# endregion


# region Booking
@routers.get("/bookings", response_model=list[schemas.Booking], tags=["bookings"])
async def get_bookings(offset: Optional[int] = None, limit: Optional[int] = None,
                       db: Session = Depends(get_db), jwt: dict = Depends(JWTBearer())):
    """
    Get bookings list where booking is not deleted and flight departure date is greater than current date and
    flight is not deleted
    """
    if not check_permissions("get_bookings", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        return crud.Booking.get_list(db, offset, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Internal server error get bookings")


@routers.get("/booking/{booking_id}", tags=["bookings"])
async def get_booking(booking_id: int, db: Session = Depends(get_db), jwt: dict = Depends(JWTBearer())):
    """
    Get booking by id where booking is not deleted and flight departure date is greater than current date and
    flight is not deleted
    """
    if not check_permissions("get_booking", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    db_booking = crud.Booking.get_by_id(db, booking_id)
    if db_booking is None:
        return {"error": "Booking not found"}
    return schemas.Booking.from_orm(db_booking)


@routers.post("/booking", tags=["bookings"])
async def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db),
                         jwt: dict = Depends(JWTBearer())):
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
        db_flight = crud.Flight.get_by_id(db, booking.flight_id)
        if db_flight is None or db_flight.deleted_at is not None or db_flight.departure_date < datetime.now():
            raise ValueError("Flight not found")
        if db_flight.left_seats < 0:
            raise ValueError("Flight left seats is less than 0")

        return crud.Booking.create(db, booking, db_flight)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.patch("/booking/{booking_id}", tags=["bookings"])
async def update_booking(booking_id: int, booking: schemas.BookingUpdate,
                         db: Session = Depends(get_db), jwt: dict = Depends(JWTBearer())):
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
        db_booking = crud.Booking.get_by_id(db, booking_id)
        if db_booking is None or db_booking.deleted_at is not None:
            raise ValueError("Booking not found")

        db_flight = crud.Flight.get_by_id(db, booking.flight_id)
        if db_flight is None or db_flight.deleted_at is not None or db_flight.departure_date < datetime.now():
            raise ValueError("Flight not found")

        return crud.Booking.update(db, booking, db_booking, db_flight)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.delete("/booking/{booking_id}", tags=["bookings"])
async def delete_booking(booking_id: int, db: Session = Depends(get_db), jwt: dict = Depends(JWTBearer())):
    """ Delete booking by id """
    if not check_permissions("delete_booking", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        db_booking = crud.Booking.get_by_id(db, booking_id)
        if db_booking is None or db_booking.deleted_at is not None:
            return {"error": "Booking not found"}
        return crud.Booking.delete(db, booking_id)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


# endregion


# region Scraped Price
@routers.get("/scraped_prices", response_model=list[schemas.ScrapedPrice], tags=["scraped_prices"])
async def get_scraped_prices(offset: Optional[int] = None, limit: Optional[int] = None, db: Session = Depends(get_db)):
    """ Get scraped prices list """
    try:
        return crud.ScrapedPrice.get_list(db, offset, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Internal server error get scraped prices")


@routers.get("/scraped_price/{scraped_price_id}", tags=["scraped_prices"])
async def get_scraped_price(scraped_price_id: int, db: Session = Depends(get_db)):
    """ Get scraped price by id """
    try:
        db_scraped_price = crud.ScrapedPrice.get_by_id(db, scraped_price_id)
        if db_scraped_price is None:
            return {"error": "Scraped price not found"}
        return schemas.ScrapedPrice.from_orm(db_scraped_price)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Internal server error get scraped price")


@routers.post("/scraped_price", tags=["scraped_prices"])
async def create_scraped_price(scraped_price: schemas.ScrapedPriceCreate, db: Session = Depends(get_db)):
    """ Create scraped price """
    try:
        return crud.ScrapedPrice.create(db, scraped_price)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.patch("/scraped_price/{scraped_price_id}", tags=["scraped_prices"])
async def update_scraped_price(scraped_price_id: int, scraped_price: schemas.ScrapedPriceUpdate,
                               db: Session = Depends(get_db)):
    try:
        db_scraped_price = crud.ScrapedPrice.get_by_id(db, scraped_price_id)
        if db_scraped_price is None:
            return {"error": "Scraped price not found"}
        return crud.ScrapedPrice.update(db, db_scraped_price, scraped_price)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.delete("/scraped_price/{scraped_price_id}", tags=["scraped_prices"])
async def delete_scraped_price(scraped_price_id: int, db: Session = Depends(get_db)):
    try:
        db_scraped_price = crud.ScrapedPrice.get_by_id(db, scraped_price_id)
        if db_scraped_price is None:
            return {"error": "Scraped price not found"}
        return crud.ScrapedPrice.delete(db, db_scraped_price)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


# endregion


# region Gender
@routers.get("/genders", response_model=list[schemas.Gender], tags=['genders'])
async def get_genders(db: Session = Depends(get_db), offset: Optional[int] = None, limit: Optional[int] = None):
    try:
        return crud.Gender.get_list(db, offset, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/gender/{gender_id}", tags=['genders'])
async def get_gender(gender_id: int, db: Session = Depends(get_db)):
    db_gender = crud.Gender.get_by_id(db, gender_id)
    if db_gender is None:
        return {"error": "Gender not found"}
    return schemas.Gender.from_orm(db_gender)


@routers.post("/gender", tags=['genders'])
async def create_gender(gender: schemas.GenderCreate, db: Session = Depends(get_db)):
    try:
        return crud.Gender.create(db, gender)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.patch("/gender/{gender_id}", tags=["genders"])
async def update_gender(gender_id: int, gender: schemas.GenderUpdate, db: Session = Depends(get_db)):
    try:
        db_gender = crud.Gender.get_by_id(db, gender_id)
        if db_gender is None:
            return {"error": "Gender not found"}
        return crud.Gender.update(db, db_gender, gender)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.delete("/gender/{gender_id}", tags=["genders"])
async def delete_gender(gender_id: int, db: Session = Depends(get_db)):
    try:
        return crud.Gender.delete(db, gender_id)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


# endregion


# region Refill (get agents and add to balance)
@routers.get("/refills", response_model=list[schemas.Refill], tags=['refills'])
async def get_refills(offset: Optional[int] = None, limit: Optional[int] = None, db: Session = Depends(get_db),
                      jwt: dict = Depends(JWTBearer())):
    if not check_permissions('get_refills', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        return crud.Refill.get_list(db, offset, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/refill/{refill_id}", tags=['refills'])
async def get_refill(refill_id: int, db: Session = Depends(get_db), jwt: dict = Depends(JWTBearer())):
    if not check_permissions('get_refill', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    db_refill = crud.Refill.get_by_id(db, refill_id)
    if db_refill is None:
        return {"error": "Refill not found"}
    return schemas.Refill.from_orm(db_refill)


@routers.post("/refill", tags=['refills'])
async def create_refill(refill: schemas.RefillCreate, db: Session = Depends(get_db), jwt: dict = Depends(JWTBearer())):
    if not check_permissions('create_refill', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        return schemas.Refill.from_orm(crud.Refill.create(db, refill))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.patch("/refill/{refill_id}", tags=["refills"])
async def update_refill(refill_id: int, refill: schemas.RefillUpdate, db: Session = Depends(get_db),
                        jwt: dict = Depends(JWTBearer())):
    if not check_permissions('update_refill', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        db_refill = crud.Refill.get_by_id(db, refill_id)
        if db_refill is None:
            return {"error": "Refill not found"}
        return schemas.Refill.from_orm(crud.Refill.update(db, refill_id, refill))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.delete("/refill/{refill_id}", tags=["refills"])
async def delete_refill(refill_id: int, db: Session = Depends(get_db), jwt: dict = Depends(JWTBearer())):
    if not check_permissions('delete_refill', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        db_refill = crud.Refill.get_by_id(db, refill_id)
        if db_refill is None:
            return {"error": "Refill not found"}
        return crud.Refill.delete(db, refill_id)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


# endregion


# region Agent Debt
@routers.get("/agent_debts/{agent_id}", response_model=list[schemas.AgentDebt], tags=['agents'])
async def get_agent_debts(agent_id: int, db: Session = Depends(get_db), offset: Optional[int] = None,
                          limit: Optional[int] = None):
    try:
        return crud.AgentDebt.get_list(db, agent_id, offset, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


# endregion


# region Ticket Class
@routers.get("/ticket_classes", response_model=list[schemas.TicketClass], tags=['ticket_classes'])
async def get_ticket_classes(db: Session = Depends(get_db), offset: Optional[int] = None, limit: Optional[int] = None):
    try:
        return crud.TicketClass.get_list(db, offset, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/ticket_class/{ticket_class_id}", tags=['ticket_classes'])
async def get_ticket_class(ticket_class_id: int, db: Session = Depends(get_db)):
    db_ticket_class = crud.TicketClass.get_by_id(db, ticket_class_id)
    if db_ticket_class is None:
        return {"error": "Ticket class not found"}
    return schemas.TicketClass.from_orm(db_ticket_class)


@routers.post("/ticket_class", tags=['ticket_classes'])
async def create_ticket_class(ticket_class: schemas.TicketClassCreate, db: Session = Depends(get_db)):
    try:
        return schemas.TicketClass.from_orm(crud.TicketClass.create(db, ticket_class))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.patch("/ticket_class/{ticket_class_id}", tags=["ticket_classes"])
async def update_ticket_class(ticket_class_id: int, ticket_class: schemas.TicketClassUpdate,
                              db: Session = Depends(get_db)):
    try:
        db_ticket_class = crud.TicketClass.get_by_id(db, ticket_class_id)
        if db_ticket_class is None:
            return {"error": "Ticket Class not found"}
        return schemas.TicketClass.from_orm(crud.TicketClass.update(db, db_ticket_class, ticket_class))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.delete("/ticket_class/{ticket_class_id}", tags=["ticket_classes"])
async def delete_ticket_class(ticket_class_id: int, db: Session = Depends(get_db)):
    try:
        db_ticket_class = crud.TicketClass.get_by_id(db, ticket_class_id)
        if db_ticket_class is None:
            return {"error": "Ticket Class not found"}
        return crud.TicketClass.delete(db, db_ticket_class)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

# endregion
