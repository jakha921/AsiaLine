from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Union


from crud_models import crud, schemas

from db.database import get_db

routers = APIRouter()



#? Country
# get countries
@routers.get("/countries", response_model=list[schemas.Country])
async def get_countries(min: Optional[int] = 0, max: Optional[int] = 10, db: Session = Depends(get_db)):
    return crud.Country.get_list(db, min, max)

# get country by id
@routers.get("/country/{country_id}", response_model=schemas.Country)
async def get_country(country_id: int, db: Session = Depends(get_db)):
    db_country = crud.Country.get_by_id(db, country_id)
    if db_country is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")
    return db_country

# create country
@routers.post("/country", response_model=schemas.Country)
async def create_country(country: schemas.CountryCreate, db: Session = Depends(get_db)):
    return crud.Country.create(db, country)

# update country
@routers.patch("/country/{country_id}", response_model=schemas.Country)
async def update_country(country_id: int, country: schemas.CountryUpdate, db: Session = Depends(get_db)):
    db_country = crud.Country.get_by_id(db, country_id)
    if db_country is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")
    return crud.Country.update(db, country_id, country)

# delete country
@routers.delete("/country/{country_id}", response_model=schemas.Country)
async def delete_country(country_id: int, db: Session = Depends(get_db)):
    db_country = crud.Country.get_by_id(db, country_id)
    if db_country is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")
    return crud.Country.delete(db, country_id)


#? City start
# get cities
@routers.get("/cities")
async def get_cities(min: Optional[int] = 0, max: Optional[int] = 10, db: Session = Depends(get_db)):
    return crud.City.get_list(db, min, max)

# get city by id
@routers.get("/city/{city_id}", response_model=schemas.City)
async def get_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.City.get_by_id(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    return db_city

# create city
@routers.post("/city", response_model=schemas.City)
async def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.City.create(db, city)

# update city
@routers.patch("/city/{city_id}", response_model=schemas.City)
async def update_city(city_id: int, city: schemas.CityUpdate, db: Session = Depends(get_db)):
    db_city = crud.City.get_by_id(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    return crud.City.update(db, city_id, city)

# delete city
@routers.delete("/city/{city_id}", response_model=schemas.City)
async def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.City.get_by_id(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    return crud.City.delete(db, db_city.id)


#? Airport
# get airports
@routers.get("/airports", response_model=list[schemas.Airport])
async def get_airports(min: Optional[int] = 0, max: Optional[int] = 10, db: Session = Depends(get_db)):
    return crud.Airport.get_list(db, min, max)

# get airport by id
@routers.get("/airport/{airport_id}", response_model=schemas.Airport)
async def get_airport(airport_id: int, db: Session = Depends(get_db)):
    db_airport = crud.Airport.get_by_id(db, airport_id)
    if db_airport is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Airport not found")
    return db_airport

# create airport
@routers.post("/airport", response_model=schemas.Airport)
async def create_airport(airport: schemas.AirportCreate, db: Session = Depends(get_db)):
    return crud.Airport.create(db, airport)

# update airport
@routers.patch("/airport/{airport_id}", response_model=schemas.Airport)
async def update_airport(airport_id: int, airport: schemas.AirportUpdate, db: Session = Depends(get_db)):
    db_airport = crud.Airport.get_by_id(db, airport_id)
    if db_airport is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Airport not found")
    return crud.Airport.update(db, airport_id, airport)

# delete airport
@routers.delete("/airport/{airport_id}", response_model=schemas.Airport)
async def delete_airport(airport_id: int, db: Session = Depends(get_db)):
    db_airport = crud.Airport.get_by_id(db, airport_id)
    if db_airport is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Airport not found")
    return crud.Airport.delete(db, db_airport.id)

#? Flight
# get flights
@routers.get("/flights", response_model=list[schemas.Flight])
async def get_flights(min: Optional[int] = 0, max: Optional[int] = 10, db: Session = Depends(get_db)):
    return crud.Flight.get_list(db, min, max)

# get flight by id
@routers.get("/flight/{flight_id}", response_model=schemas.Flight)
async def get_flight(flight_id: int, db: Session = Depends(get_db)):
    db_flight = crud.Flight.get_by_id(db, flight_id)
    if db_flight is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
    return db_flight

# create flight
@routers.post("/flight", response_model=schemas.Flight)
async def create_flight(flight: schemas.FlightCreate, db: Session = Depends(get_db)):
    if flight.from_airport_id == flight.to_airport_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="from airport id and to airport id must be deferent")
    return crud.Flight.create(db, flight)

# update flight 
@routers.patch("/flight/{flight_id}", response_model=schemas.Flight)
async def update_flight(flight_id: int, flight: schemas.FlightUpdate, db: Session = Depends(get_db)):
    db_flight = crud.Flight.get_by_id(db, flight_id)
    if db_flight is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
    if flight.from_airport_id == flight.to_airport_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="from airport id and to airport id must be deferent")
    return crud.Flight.update(db, flight_id, flight)

# delete flight
@routers.delete("/flight/{flight_id}", response_model=schemas.Flight)
async def delete_flight(flight_id: int, db: Session = Depends(get_db)):
    db_flight = crud.Flight.get_by_id(db, flight_id)
    if db_flight is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
    return crud.Flight.delete(db, db_flight.id)

