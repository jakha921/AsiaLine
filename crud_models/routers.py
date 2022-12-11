from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Union
from datetime import datetime
import traceback
import logging

from crud_models import crud, schemas
from db.database import get_db


routers = APIRouter()

#? Country
# get countries
@routers.get("/countries", response_model=list[schemas.Country])
async def get_countries(min: Optional[int] = None, max: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        return crud.Country.get_list(db, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
        
# get country by id
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

# create country
@routers.post("/country", response_model=schemas.Country)
async def create_country(country: schemas.CountryCreate, db: Session = Depends(get_db)):
    try:
        return crud.Country.create(db, country)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# update country
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

# delete country
@routers.delete("/country/{country_id}", response_model=schemas.Country)
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


#? City
# get cities
@routers.get("/cities")
async def get_cities(min: Optional[int] = None, max: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        return crud.City.get_list(db, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# get city by id
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

# create city
@routers.post("/city", response_model=schemas.City)
async def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    try:
        return crud.City.create(db, city)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# update city
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

# delete city
@routers.delete("/city/{city_id}", response_model=schemas.City)
async def delete_city(city_id: int, db: Session = Depends(get_db)):
    try:
        return crud.City.delete(db, city_id)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

#? Airport
# get airports
@routers.get("/airports", response_model=list[schemas.Airport])
async def get_airports(min: Optional[int] = None, max: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        return crud.Airport.get_list(db, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# get airport by id
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

# create airport
@routers.post("/airport", response_model=schemas.Airport)
async def create_airport(airport: schemas.AirportCreate, db: Session = Depends(get_db)):
    try:
        return crud.Airport.create(db, airport)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# update airport
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

# delete airport
@routers.delete("/airport/{airport_id}", response_model=schemas.Airport)
async def delete_airport(airport_id: int, db: Session = Depends(get_db)):
    try:
        return crud.Airport.delete(db, airport_id)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

#? Flight
# get flights
@routers.get("/flights")
async def get_flights(min: Optional[int] = None, max: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        return crud.Flight.get_list(db, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# get flight by id
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

# create flight
@routers.post("/flight")
async def create_flight(flight: schemas.FlightCreate, db: Session = Depends(get_db)):
    try:
        if flight.from_airport_id == flight.to_airport_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="from airport id and to airport id must be deferent")
        if flight.departure_date >= flight.arrival_date:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="departure time must be before arrival time")
        create = crud.Flight.create(db, flight)
        if flight.price != 0:
            crud.FlightPriceHistory.create(db, flight.price, create.id)
        return create
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# update flight 
@routers.patch("/flight/{flight_id}")
async def update_flight(flight_id: int, flight: schemas.FlightUpdate, db: Session = Depends(get_db)):
    try:
        db_flight = crud.Flight.get_by_id(db, flight_id)
        if db_flight is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
        if flight.from_airport_id == flight.to_airport_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="from airport id and to airport id must be deferent")
        if flight.departure_date > flight.arrival_date:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="departure time must be before arrival time")    
        
        current_price , db_price = flight.price, db_flight.price
        update = crud.Flight.update(db, flight_id, flight)
        if current_price != db_price:
            crud.FlightPriceHistory.create(db, flight.price, update.id)
        return update

    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# delete flight
@routers.delete("/flight/{flight_id}")
async def delete_flight(flight_id: int, db: Session = Depends(get_db)):
    try:
        return crud.Flight.delete(db, flight_id)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# ? Flight price history
# get flight price history
# @routers.get("/flight/prices")
# async def get_flight_prices(min: Optional[int] = 0, max: Optional[int] = 10, db: Session = Depends(get_db)):
#     return crud.FlightPriceHistory.get_list(db, min, max)

# get flight price history by flight id
@routers.get("/flight/{flight_id}/prices", response_model=list[schemas.FlightPriceHistory])
async def get_flight_prices_by_flight_id(flight_id: int, min: Optional[int] = 1, max: Optional[int] = 10, db: Session = Depends(get_db)):
    try:
        return crud.FlightPriceHistory.get_by_flight_id(db, flight_id, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# ? Ticket
# get tickets
@routers.get("/tickets", response_model=list[schemas.Ticket])
async def get_tickets(min: Optional[int] = None, max: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        return crud.Ticket.get_list(db, min, max)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# get ticket by id
@routers.get("/ticket/{ticket_id}", response_model=schemas.Ticket)
async def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = crud.Ticket.get_by_id(db, ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return db_ticket

# create ticket
@routers.post("/ticket", response_model=schemas.Ticket)
async def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    try:
        if ticket.flight_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="flight id is required")
        db_flight = crud.Flight.get_by_id(db, ticket.flight_id)
        if db_flight is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
        
        return crud.Ticket.create(db, ticket, db_flight)
    except Exception as e:
        # print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# update ticket
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

# delete ticket
@routers.delete("/ticket/{ticket_id}")
async def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    try:
        return crud.Ticket.delete(db, ticket_id)
    except Exception as e:
        print(logging.error(e))
        print(logging.error(traceback.format_exc()))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")






