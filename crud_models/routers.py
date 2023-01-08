from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Union
from datetime import datetime
import traceback
import logging

from crud_models import crud, schemas
from db.database import get_db

routers = APIRouter()


# region Country
@routers.get("/countries", tags=["countries"], response_model=list[schemas.Country])
async def get_countries(
        min: Optional[int] = None,
        max: Optional[int] = None,
        db: Session = Depends(get_db)):
    """
    Get list of countries\n
    *if min and max None return all countries*\n
    *if min and max not None return countries between min and max*.
    """
    try:
        return crud.Country.get_list(db, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


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
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.post("/country", tags=["countries"])
async def create_country(country: schemas.CountryCreate, db: Session = Depends(get_db)):
    """ Create new country """
    try:
        return schemas.Country.from_orm(crud.Country.create(db, country))
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


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
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


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
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# endregion


# region City
@routers.get("/cities", tags=["cities"], response_model=list[schemas.City])
async def get_cities(min: Optional[int] = None, max: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Get list of cities\n
    *if min and max None return all cities*\n
    *if min and max not None return cities between min and max*.
    """
    try:
        return crud.City.get_list(db, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


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
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.post("/city", tags=["cities"])
async def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    """ Create new city """
    try:
        return crud.City.create(db, city)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


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
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


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
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# endregion


# region Airport
@routers.get("/airports", response_model=list[schemas.Airport], tags=["airports"])
async def get_airports(min: Optional[int] = None, max: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Get list of airports\n
    *if min and max None return all airports*\n
    *if min and max not None return airports between min and max.*
    """
    try:
        return crud.Airport.get_list(db, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


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
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.post("/airport", tags=["airports"])
async def create_airport(airport: schemas.AirportCreate, db: Session = Depends(get_db)):
    """ Create new airport """
    try:
        return schemas.Airport.from_orm(crud.Airport.create(db, airport))
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


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
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


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
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# endregion


# region Flight
@routers.get("/flights", response_model=list[schemas.Flight], tags=["flights"])
async def get_flights(min: Optional[int] = None, max: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Get list of flights where departure date is greater than current date and flight is not deleted\n
    *if min and max None return all flights*\n
    *if min and max not None return flights between min and max.*
    """
    try:
        return crud.Flight.get_list(db, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.get("/flight/{flight_id}", tags=["flights"])
async def get_flight(flight_id: int, db: Session = Depends(get_db)):
    """ Get flight by id if departure date is greater than current date and flight is not deleted """
    try:
        db_flight = crud.Flight.get_by_id(db, flight_id)
        if db_flight is None:
            return {"detail": "Flight not found"}
        return schemas.Flight.from_orm(db_flight)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.post("/flight", tags=["flights"])
async def create_flight(flight: schemas.FlightCreate, db: Session = Depends(get_db)):
    """
    Create new flight\n
    **Rules**:\n
    * departure date must be greater than current date\n
    * arrival date must be greater than departure date\n
    * departure airport must be different from arrival airport\n
    * on sale date must be greater than current date\n
    """
    try:
        if flight.from_airport_id == flight.to_airport_id:
            return {"error": "From and to airports cannot be the same"}
        if flight.departure_date >= flight.arrival_date:
            return {"error": "departure date must be before arrival date"}
        if flight.on_sale <= datetime.now():
            return {"error": "on sale date must be before current date"}
        create = crud.Flight.create(db, flight)
        if flight.price > 0:
            crud.FlightPriceHistory.create(db, flight.price, create.id)
        return schemas.Flight.from_orm(create)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.patch("/flight/{flight_id}", tags=["flights"])
async def update_flight(flight_id: int, flight: schemas.FlightUpdate, db: Session = Depends(get_db)):
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
    try:
        db_flight = crud.Flight.get_by_id(db, flight_id)
        if db_flight is None:
            return {"error": "Flight not found"}
        if flight.from_airport_id == flight.to_airport_id:
            return {"error": "From and to airports cannot be the same"}
        if flight.total_seats and flight.left_seats:
            if flight.total_seats < flight.left_seats:
                return {"error": "Total seats cannot be less than left seats"}

        if flight.total_seats or flight.left_seats:
            if flight.total_seats < db_flight.left_seats:
                return {"error": "Total seats cannot be less than left seats"}
            if flight.left_seats > db_flight.total_seats:
                return {"error": "Left seats cannot be more than total seats"}

        current_price, db_price = flight.price, db_flight.price
        update = crud.Flight.update(db, db_flight, flight)
        if current_price != db_price:
            crud.FlightPriceHistory.create(db, flight.price, update.id)
        return schemas.Flight.from_orm(update)

    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.delete("/flight/{flight_id}", tags=["flights"])
async def delete_flight(flight_id: int, db: Session = Depends(get_db)):
    """
     **Attention:**\n
     Get all quotas and tickets of this flight and delete them.
     """
    try:
        db_flight = crud.Flight.get_by_id(db, flight_id)
        if db_flight is None or db_flight.deleted_at is not None:
            return {"error": "Flight not found"}
        return crud.Flight.delete(db, db_flight)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.get("/flight/{flight_id}/tickets", tags=["flights"])
async def get_flight_tickets(flight_id: int, db: Session = Depends(get_db)):
    """ Get all tickets of flight by id """
    try:
        tickets = crud.Flight.get_flight_tickets(db, flight_id)
        if tickets == []:
            return {"detail": "Flight not found or flight has no tickets"}
        return tickets

    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.patch("/flight-set-on-sale/{flight_id}", tags=["flights"])
async def set_flight_for_sale(flight_id: int, db: Session = Depends(get_db)):
    """ Set flight for sale from now """
    try:
        db_flight = crud.Flight.get_by_id(db, flight_id)
        if db_flight is None or db_flight.deleted_at is not None or db_flight.departure_date < datetime.now():
            return {"error": "Flight not found"}
        if db_flight.on_sale < datetime.now():
            return {"error": "Flight is already on sale"}
        return crud.Flight.set_on_sale_now(db, db_flight)

    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.get("/flight/{flight_id}/prices", response_model=list[schemas.FlightHistory], tags=["flights"])
async def get_flight_price_history_by_fligh_id(flight_id: int, min: Optional[int] = 1, max: Optional[int] = 10,
                                               db: Session = Depends(get_db)):
    """ Get flight id and return list of flight price history for this flight """
    try:
        return crud.FlightPriceHistory.get_by_flight_id(db, flight_id, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# endregion


# region Ticket
@routers.get("/tickets", response_model=list[schemas.Ticket], tags=["tickets"])
async def get_tickets(min: Optional[int] = None, max: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Get all tickets where ticket and flight are not deleted and flight departure date is greater than current date
    """
    try:
        return crud.Ticket.get_list(db, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error get tickets")


@routers.get("/ticket/{ticket_id}", tags=["tickets"])
async def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """ Get ticket by id where ticket and flight are not deleted and flight departure date is greater than current date """
    db_ticket = crud.Ticket.get_by_id(db, ticket_id)
    if db_ticket is None:
        return {"error": "Ticket not found"}
    return schemas.Ticket.from_orm(db_ticket)


@routers.post("/ticket", tags=["tickets"])
async def create_ticket(ticket: schemas.TicketCreate, hard: bool = False, soft: bool = False,
                        db: Session = Depends(get_db)):
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
            return {"error": "You cannot use hard and soft blocks at the same time"}
        if ticket.flight_id is None:
            return {"error": "Flight id is required"}
        db_flight = crud.Flight.get_by_id(db, ticket.flight_id)
        if db_flight is None or db_flight.deleted_at is not None or db_flight.on_sale > datetime.now() or \
                db_flight.departure_date < datetime.now():
            return {"error": "Flight not found or flight is not on sale or flight is deleted or flight departure date is less than current date"}
        if db_flight.left_seats <= 0:
            return {"error": "No seats left"}

        return crud.Ticket.create(db, ticket, db_flight, hard, soft)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.patch("/ticket/{ticket_id}", tags=["tickets"])
async def update_ticket(ticket_id: int, ticket: schemas.TicketUpdate, db: Session = Depends(get_db)):
    """
    Update ticket by id\n
    **Rules:**\n
    * ticket cannot be updated if flight is on sale
    * ticket cannot be updated if flight is deleted
    * ticket cannot be updated if flight departure date is less than current date
    * ticket cannot be updated if ticket is deleted
    """
    try:
        db_ticket = crud.Ticket.get_by_id(db, ticket_id)
        if db_ticket is None or db_ticket.deleted_at is not None:
            return {"error": "Ticket not found"}
        if ticket.flight_id is not None:
            db_flight = crud.Flight.get_by_id(db, ticket.flight_id)
            if db_flight is None or db_flight.deleted_at is not None or db_flight.on_sale > datetime.now() or \
                    db_flight.departure_date < datetime.now():
                return {"error": "Flight not found"}
        return schemas.Ticket.from_orm(crud.Ticket.update(db, db_ticket, ticket))
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


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
            return {"error": "Ticket not found"}
        return crud.Ticket.delete(db, db_ticket)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.post("/ticket/cancellation", tags=["tickets"])
async def cancel_ticket_add_to_agent_fine(ticket_cancel: schemas.TicketCancel, db: Session = Depends(get_db)):
    """
    Cancel ticket and add fine to agent will bу added to flight left seats\n
    """
    try:
        db_ticket = crud.Ticket.get_by_id(db, ticket_cancel.ticket_id)
        if db_ticket.deleted_at or db_ticket is None:
            return {"error": "Ticket not found"}
        return crud.Ticket.cancel(db, ticket_cancel)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# endregion


# region Booking
@routers.get("/bookings", response_model=list[schemas.Booking], tags=["bookings"])
async def get_bookings(min: Optional[int] = None, max: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Get bookings list where booking is not deleted and flight departure date is greater than current date and flight is not deleted
    """
    try:
        return crud.Booking.get_list(db, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error get bookings")


@routers.get("/booking/{booking_id}", tags=["bookings"])
async def get_booking(booking_id: int, db: Session = Depends(get_db)):
    """
    Get booking by id where booking is not deleted and flight departure date is greater than current date and flight is not deleted
    """
    db_booking = crud.Booking.get_by_id(db, booking_id)
    if db_booking is None:
        return {"error": "Booking not found"}
    return schemas.Booking.from_orm(db_booking)


@routers.post("/booking", tags=["bookings"])
async def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    """
    Create booking
    **Rules:**\n
    * if flight is not on sale, booking will not be created
    * if flight is deleted, booking will not be created
    * if flight departure date is less than current date, booking will not be created
    * if flight left seats is less or equal to 0, booking will not be created
    """
    try:
        if booking.flight_id is None:
            return {"error": "Flight id is required"}
        db_flight = crud.Flight.get_by_id(db, booking.flight_id)
        if db_flight is None or db_flight.deleted_at is not None or db_flight.on_sale > datetime.now() or \
                db_flight.departure_date < datetime.now():
            return {"error": "Flight not found"}
        if db_flight.left_seats < 0:
            return {"error": "No seats left"}

        return crud.Booking.create(db, booking, db_flight)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.patch("/booking/{booking_id}", tags=["bookings"])
async def update_booking(booking_id: int, booking: schemas.BookingUpdate, db: Session = Depends(get_db)):
    """
    Update booking by id\n
    **Rules:**\n
    * booking cannot be updated if flight is on sale
    * booking cannot be updated if flight is deleted
    * booking cannot be updated if flight departure date is less than current date
    * booking cannot be updated if booking is deleted
    """
    try:
        db_booking = crud.Booking.get_by_id(db, booking_id)
        if db_booking is None or db_booking.deleted_at is not None:
            return {"error": "Booking not found"}

        db_flight = crud.Flight.get_by_id(db, booking.flight_id)
        if db_flight is None or db_flight.deleted_at is not None or db_flight.on_sale > datetime.now() or \
                db_flight.departure_date < datetime.now():
            return {"error": "Flight not found"}

        return crud.Booking.update(db, booking, db_booking, db_flight)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.delete("/booking/{booking_id}", tags=["bookings"])
async def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    """ Delete booking by id """
    try:
        db_booking = crud.Booking.get_by_id(db, booking_id)
        if db_booking is None or db_booking.deleted_at is not None:
            return {"error": "Booking not found"}
        return crud.Booking.delete(db, booking_id)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# endregion


# region Scraped Price
@routers.get("/scraped_prices", response_model=list[schemas.ScrapedPrice], tags=["scraped_prices"])
async def get_scraped_prices(min: Optional[int] = None, max: Optional[int] = None, db: Session = Depends(get_db)):
    """ Get scraped prices list """
    try:
        return crud.ScrapedPrice.get_list(db, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error get scraped price")


@routers.post("/scraped_price", tags=["scraped_prices"])
async def create_scraped_price(scraped_price: schemas.ScrapedPriceCreate, db: Session = Depends(get_db)):
    """ Create scraped price """
    try:
        return crud.ScrapedPrice.create(db, scraped_price)
    except Exception as e:
        # print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


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
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.delete("/scraped_price/{scraped_price_id}", tags=["scraped_prices"])
async def delete_scraped_price(scraped_price_id: int, db: Session = Depends(get_db)):
    try:
        db_scraped_price = crud.ScrapedPrice.get_by_id(db, scraped_price_id)
        if db_scraped_price is None:
            return {"error": "Scraped price not found"}
        return crud.ScrapedPrice.delete(db, db_scraped_price)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# endregion


# region Gender
@routers.get("/genders", response_model=list[schemas.Gender], tags=['genders'])
async def get_genders(db: Session = Depends(get_db), min: Optional[int] = None, max: Optional[int] = None):
    try:
        return crud.Gender.get_list(db, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


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
        # print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.patch("/gender/{gender_id}", tags=["genders"])
async def update_gender(gender_id: int, gender: schemas.GenderUpdate, db: Session = Depends(get_db)):
    try:
        db_gender = crud.Gender.get_by_id(db, gender_id)
        if db_gender is None:
            return {"error": "Gender not found"}
        return crud.Gender.update(db, db_gender, gender)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.delete("/gender/{gender_id}", tags=["genders"])
async def delete_gender(gender_id: int, db: Session = Depends(get_db)):
    try:
        return crud.Gender.delete(db, gender_id)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# endregion


# region Refill (get agents and add to balance)
@routers.get("/refills", response_model=list[schemas.Refill])
async def get_refills(db: Session = Depends(get_db), min: Optional[int] = None, max: Optional[int] = None):
    try:
        return crud.Refill.get_list(db, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.get("/refill/{refill_id}", response_model=schemas.Refill)
async def get_refill(refill_id: int, db: Session = Depends(get_db)):
    db_refill = crud.Refill.get_by_id(db, refill_id)
    if db_refill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Refill not found")
    return db_refill


@routers.post("/refill")
async def create_refill(refill: schemas.RefillCreate, db: Session = Depends(get_db)):
    try:
        return crud.Refill.create(db, refill)
    except Exception as e:
        # print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.patch("/refill/{refill_id}", response_model=schemas.Refill)
async def update_refill(refill_id: int, refill: schemas.RefillUpdate, db: Session = Depends(get_db)):
    try:
        db_refill = crud.Refill.get_by_id(db, refill_id)
        if db_refill is None:
            return {"error": "Refill not found"}
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Refill not found")
        return crud.Refill.update(db, refill_id, refill)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.delete("/refill/{refill_id}")
async def delete_refill(refill_id: int, db: Session = Depends(get_db)):
    try:
        return crud.Refill.delete(db, refill_id)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# endregion


# region Agent Debt
@routers.get("/agent_debts/{agent_id}")
async def get_agent_debts(agent_id: int, db: Session = Depends(get_db), min: Optional[int] = None,
                          max: Optional[int] = None):
    try:
        return crud.AgentDebt.get_list(db, agent_id, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# endregion


# region Ticket Class
@routers.get("/ticket_classes", response_model=list[schemas.TicketClass])
async def get_ticket_classes(db: Session = Depends(get_db), min: Optional[int] = None, max: Optional[int] = None):
    try:
        return crud.TicketClass.get_list(db, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.get("/ticket_class/{ticket_class_id}", response_model=schemas.TicketClass)
async def get_ticket_class(ticket_class_id: int, db: Session = Depends(get_db)):
    db_ticket_class = crud.TicketClass.get_by_id(db, ticket_class_id)
    if db_ticket_class is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket Class not found")
    return db_ticket_class


@routers.post("/ticket_class")
async def create_ticket_class(ticket_class: schemas.TicketClassCreate, db: Session = Depends(get_db)):
    try:
        return crud.TicketClass.create(db, ticket_class)
    except Exception as e:
        # print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.patch("/ticket_class/{ticket_class_id}", response_model=schemas.TicketClass)
async def update_ticket_class(ticket_class_id: int, ticket_class: schemas.TicketClassUpdate,
                              db: Session = Depends(get_db)):
    try:
        db_ticket_class = crud.TicketClass.get_by_id(db, ticket_class_id)
        if db_ticket_class is None:
            return {"error": "Ticket Class not found"}
        return crud.TicketClass.update(db, ticket_class_id, ticket_class)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.delete("/ticket_class/{ticket_class_id}")
async def delete_ticket_class(ticket_class_id: int, db: Session = Depends(get_db)):
    try:
        return crud.TicketClass.delete(db, ticket_class_id)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# endregion
