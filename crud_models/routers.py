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
@routers.get("/countries", response_model=list[schemas.Country])
async def get_countries(
        min: Optional[int] = None,
        max: Optional[int] = None,
        db: Session = Depends(get_db)):
    try:
        return crud.Country.get_list(db, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.get("/country/{country_id}", response_model=schemas.Country)
async def get_country(country_id: int, db: Session = Depends(get_db)):
    try:
        db_country = crud.Country.get_by_id(db, country_id)
        if db_country is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")
        return db_country
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.post("/country", response_model=schemas.Country)
async def create_country(country: schemas.CountryCreate, db: Session = Depends(get_db)):
    try:
        return crud.Country.create(db, country)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.patch("/country/{country_id}", response_model=schemas.Country)
async def update_country(country_id: int, country: schemas.CountryUpdate, db: Session = Depends(get_db)):
    try:
        db_country = crud.Country.get_by_id(db, country_id)
        if db_country is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")
        return crud.Country.update(db, country_id, country)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.delete("/country/{country_id}")
async def delete_country(country_id: int, db: Session = Depends(get_db)):
    try:
        db_country = crud.Country.get_by_id(db, country_id)
        if db_country is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")
        return crud.Country.delete(db, country_id)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# endregion


# region City
@routers.get("/cities")
async def get_cities(min: Optional[int] = None, max: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        return crud.City.get_list(db, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.get("/city/{city_id}", response_model=schemas.City)
async def get_city(city_id: int, db: Session = Depends(get_db)):
    try:
        db_city = crud.City.get_by_id(db, city_id)
        if db_city is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
        return db_city
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.post("/city", response_model=schemas.City)
async def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    try:
        return crud.City.create(db, city)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.patch("/city/{city_id}", response_model=schemas.City)
async def update_city(city_id: int, city: schemas.CityUpdate, db: Session = Depends(get_db)):
    try:
        db_city = crud.City.get_by_id(db, city_id)
        if db_city is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
        return crud.City.update(db, city_id, city)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.delete("/city/{city_id}")
async def delete_city(city_id: int, db: Session = Depends(get_db)):
    try:
        return crud.City.delete(db, city_id)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# endregion


# region Airport
@routers.get("/airports", response_model=list[schemas.Airport])
async def get_airports(min: Optional[int] = None, max: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        return crud.Airport.get_list(db, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.get("/airport/{airport_id}", response_model=schemas.Airport)
async def get_airport(airport_id: int, db: Session = Depends(get_db)):
    try:
        db_airport = crud.Airport.get_by_id(db, airport_id)
        if db_airport is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Airport not found")
        return db_airport
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.post("/airport", response_model=schemas.Airport)
async def create_airport(airport: schemas.AirportCreate, db: Session = Depends(get_db)):
    try:
        return crud.Airport.create(db, airport)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.patch("/airport/{airport_id}", response_model=schemas.Airport)
async def update_airport(airport_id: int, airport: schemas.AirportUpdate, db: Session = Depends(get_db)):
    try:
        db_airport = crud.Airport.get_by_id(db, airport_id)
        if db_airport is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Airport not found")
        return crud.Airport.update(db, airport_id, airport)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.delete("/airport/{airport_id}")
async def delete_airport(airport_id: int, db: Session = Depends(get_db)):
    try:
        return crud.Airport.delete(db, airport_id)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# endregion


# region Flight
@routers.get("/flights")
async def get_flights(min: Optional[int] = None, max: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        return crud.Flight.get_list(db, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.get("/flight/{flight_id}")
async def get_flight(flight_id: int, db: Session = Depends(get_db)):
    try:
        db_flight = crud.Flight.get_by_id(db, flight_id)
        if db_flight is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
        return db_flight
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.post("/flight", response_model=schemas.Flight)
async def create_flight(flight: schemas.FlightCreate, db: Session = Depends(get_db)):
    try:
        if flight.from_airport_id == flight.to_airport_id:
            return {"error": "From and to airports cannot be the same"}
        if flight.departure_date >= flight.arrival_date:
            return {"error": "departure date must be before arrival date"}
        create = crud.Flight.create(db, flight)
        if flight.price != 0:
            crud.FlightPriceHistory.create(db, flight.price, create.id)
        return create
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.patch("/flight/{flight_id}")
async def update_flight(flight_id: int, flight: schemas.FlightUpdate, db: Session = Depends(get_db)):
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
        update = crud.Flight.update(db, flight_id, flight)
        if current_price != db_price:
            crud.FlightPriceHistory.create(db, flight.price, update.id)
        return update

    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.delete("/flight/{flight_id}")
async def delete_flight(flight_id: int, db: Session = Depends(get_db)):
    try:
        return crud.Flight.delete(db, flight_id)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# get all tickets for a flight
@routers.get("/flight/{flight_id}/tickets")
async def get_flight_tickets(flight_id: int, db: Session = Depends(get_db)):
    try:
        return crud.Flight.get_flight_tickets(db, flight_id)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.patch("/flight-set-on-sale/{flight_id}")
async def set_flight_for_sale(flight_id: int, db: Session = Depends(get_db)):
    try:
        db_flight = crud.Flight.get_by_id(db, flight_id)
        if db_flight is None and db_flight.deleted_at is None:
            return {"error": "Flight not found"}
        if db_flight.on_sale < datetime.now():
            return {"error": "Flight is already on sale"}
        return {"message": "Flight is now on sale", "flight": crud.Flight.set_on_sale_now(db, flight_id, True)}

    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# endregion


# region Flight price history
@routers.get("/flight/{flight_id}/prices", response_model=list[schemas.FlightHistory])
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
@routers.get("/tickets")
async def get_tickets(min: Optional[int] = None, max: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        return crud.Ticket.get_list(db, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error get tickets")


@routers.get("/ticket/{ticket_id}", response_model=schemas.Ticket)
async def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = crud.Ticket.get_by_id(db, ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return db_ticket


@routers.post("/ticket")
async def create_ticket(ticket: schemas.TicketCreate, hard: bool = False, soft: bool = False, db: Session = Depends(get_db)):
    try:
        if hard and soft:
            return {"error": "You cannot use hard and soft blocks at the same time"}
        if ticket.flight_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="flight id is required")
        db_flight = crud.Flight.get_by_id(db, ticket.flight_id)
        if db_flight is None:
            return {"error": "Flight not found"}
        if db_flight.left_seats <= 0:
            return {"error": "No seats left"}

        return crud.Ticket.create(db, ticket, db_flight, hard, soft)
    except Exception as e:
        # print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.patch("/ticket/{ticket_id}", response_model=schemas.Ticket)
async def update_ticket(ticket_id: int, ticket: schemas.TicketUpdate, db: Session = Depends(get_db)):
    try:
        db_ticket = crud.Ticket.get_by_id(db, ticket_id)
        if db_ticket is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
        if ticket.flight_id is not None:
            db_flight = crud.Flight.get_by_id(db, ticket.flight_id)
            if db_flight is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
        return crud.Ticket.update(db, ticket_id, ticket)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.delete("/ticket/{ticket_id}")
async def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    try:
        return crud.Ticket.delete(db, ticket_id)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.post("/ticket/cancellation")
async def cancel_ticket_add_to_agent_fine(ticket_cancel: schemas.TicketCancel, db: Session = Depends(get_db)):
    try:
        db_ticket = crud.Ticket.get_by_id(db, ticket_cancel.ticket_id)
        if db_ticket.deleted_at or db_ticket is None:
            return {"error": "Ticket not found"}
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
        return crud.Ticket.cancel(db, ticket_cancel)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# endregion


# region Booking
@routers.get("/bookings", response_model=list[schemas.Booking])
async def get_bookings(min: Optional[int] = None, max: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        return crud.Booking.get_list(db, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error get bookings")


@routers.get("/booking/{booking_id}", response_model=schemas.Booking)
async def get_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = crud.Booking.get_by_id(db, booking_id)
    if db_booking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return db_booking


@routers.post("/booking")
async def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    try:
        if booking.flight_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="flight id is required")
        db_flight = crud.Flight.get_by_id(db, booking.flight_id)
        if db_flight is None:
            return {"error": "Flight not found"}
        if db_flight.left_seats == 0:
            return {"error": "No seats left"}

        return crud.Booking.create(db, booking, db_flight)
    except Exception as e:
        # print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.patch("/booking/{booking_id}")
async def update_booking(booking_id: int, booking: schemas.BookingUpdate, db: Session = Depends(get_db)):
    try:
        db_booking = crud.Booking.get_by_id(db, booking_id)
        if db_booking is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        if booking.flight_id is not None:
            db_flight = crud.Flight.get_by_id(db, booking.flight_id)
            if db_flight is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
        return crud.Booking.update(db, booking_id, booking)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.delete("/booking/{booking_id}")
async def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    try:
        return crud.Booking.delete(db, booking_id)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# endregion


# region Scraped Price
@routers.get("/scraped_prices", response_model=list[schemas.ScrapedPrice])
async def get_scraped_prices(min: Optional[int] = None, max: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        return crud.ScrapedPrice.get_list(db, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error get scraped prices")


@routers.get("/scraped_price/{scraped_price_id}", response_model=schemas.ScrapedPrice)
async def get_scraped_price(scraped_price_id: int, db: Session = Depends(get_db)):
    db_scraped_price = crud.ScrapedPrice.get_by_id(db, scraped_price_id)
    if db_scraped_price is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scraped price not found")
    return db_scraped_price


@routers.post("/scraped_price")
async def create_scraped_price(scraped_price: schemas.ScrapedPriceCreate, db: Session = Depends(get_db)):
    try:
        return crud.ScrapedPrice.create(db, scraped_price)
    except Exception as e:
        # print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.patch("/scraped_price/{scraped_price_id}", response_model=schemas.ScrapedPrice)
async def update_scraped_price(scraped_price_id: int, scraped_price: schemas.ScrapedPriceUpdate, db: Session = Depends(get_db)):
    try:
        db_scraped_price = crud.ScrapedPrice.get_by_id(db, scraped_price_id)
        if db_scraped_price is None:
            return {"error": "Scraped price not found"}
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scraped price not found")
        return crud.ScrapedPrice.update(db, scraped_price_id, scraped_price)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.delete("/scraped_price/{scraped_price_id}")
async def delete_scraped_price(scraped_price_id: int, db: Session = Depends(get_db)):
    try:
        return crud.ScrapedPrice.delete(db, scraped_price_id)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# endregion


# region Gender
@routers.get("/genders", response_model=list[schemas.Gender])
async def get_genders(db: Session = Depends(get_db), min: Optional[int] = None, max: Optional[int] = None):
    try:
        return crud.Gender.get_list(db, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.get("/gender/{gender_id}", response_model=schemas.Gender)
async def get_gender(gender_id: int, db: Session = Depends(get_db)):
    db_gender = crud.Gender.get_by_id(db, gender_id)
    if db_gender is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gender not found")
    return db_gender


@routers.post("/gender")
async def create_gender(gender: schemas.GenderCreate, db: Session = Depends(get_db)):
    try:
        return crud.Gender.create(db, gender)
    except Exception as e:
        # print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.patch("/gender/{gender_id}", response_model=schemas.Gender)
async def update_gender(gender_id: int, gender: schemas.GenderUpdate, db: Session = Depends(get_db)):
    try:
        db_gender = crud.Gender.get_by_id(db, gender_id)
        if db_gender is None:
            return {"error": "Gender not found"}
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gender not found")
        return crud.Gender.update(db, gender_id, gender)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@routers.delete("/gender/{gender_id}")
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