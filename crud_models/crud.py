from crud_models import schemas
from db import models

from sqlalchemy.orm import Session
from typing import Optional

class Country:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.Country).offset(min).limit(max).all()
        return db.query(models.Country).all()
    
    def get_by_id(db: Session, country_id: int):
        return db.query(models.Country).filter(models.Country.id == country_id).first()

    def create(db: Session, country: schemas.CountryCreate):
        db_country = models.Country(**country.dict())
        db.add(db_country)
        db.commit()
        db.refresh(db_country)
        return db_country
    
    def update(db: Session, country_id: int, country: schemas.CountryUpdate):
        db_country = db.query(models.Country).filter(models.Country.id == country_id).first()
        db_country.country_ru = country.country_ru
        db_country.country_en = country.country_en
        db_country.country_uz = country.country_uz
        db_country.short_name = country.short_name
        db_country.code = country.code
        db.commit()
        db.refresh(db_country)
        return db_country
    
    def delete(db: Session, country_id: int):
        db_country = db.query(models.Country).filter(models.Country.id == country_id).first()
        db.delete(db_country)
        db.commit()
        return db_country


class City:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.City).offset(min).limit(max).all()
        return db.query(models.City).all()
    
    def get_by_id(db: Session, city_id: int):
        return db.query(models.City).filter(models.City.id == city_id).first()
    
    def create(db: Session, city: schemas.CityCreate):
        db_city = models.City(**city.dict())
        db.add(db_city)
        db.commit()
        db.refresh(db_city)
        return db_city
    
    def update(db: Session, city_id: int, city: schemas.CityUpdate):
        db_city = db.query(models.City).filter(models.City.id == city_id).first()
        db_city.city_ru = city.city_ru
        db_city.city_en = city.city_en
        db_city.city_uz = city.city_uz
        db_city.country_id = city.country_id
        db.commit()
        db.refresh(db_city)
        return db_city
    
    def delete(db: Session, city_id: int):
        db_city = db.query(models.City).filter(models.City.id == city_id).first()
        db.delete(db_city)
        db.commit()
        return db_city


class Airport:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.Airport).offset(min).limit(max).all()
        return db.query(models.Airport).all()
    
    def get_by_id(db: Session, airport_id: int):
        return db.query(models.Airport).filter(models.Airport.id == airport_id).first()
    
    def create(db: Session, airport: schemas.AirportCreate):
        db_airport = models.Airport(**airport.dict())
        db.add(db_airport)
        db.commit()
        db.refresh(db_airport)
        return db_airport
    
    def update(db: Session, airport_id: int, airport: schemas.AirportUpdate):
        db_airport = db.query(models.Airport).filter(models.Airport.id == airport_id).first()
        db_airport.airport_ru = airport.airport_ru
        db_airport.airport_en = airport.airport_en
        db_airport.airport_uz = airport.airport_uz
        db_airport.city_id = airport.city_id
        db.commit()
        db.refresh(db_airport)
        return db_airport
    
    def delete(db: Session, airport_id: int):
        db_airport = db.query(models.Airport).filter(models.Airport.id == airport_id).first()
        db.delete(db_airport)
        db.commit()
        return db_airport


class Flight:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.Flight).offset(min).limit(max).all()
        return db.query(models.Flight).all()
    
    def get_by_id(db: Session, flight_id: int):
        return db.query(models.Flight).filter(models.Flight.id == flight_id).first()
    

    def create(db: Session, flight: schemas.FlightCreate):
        db_flight = models.Flight(**flight.dict())
        db.add(db_flight)
        db.commit()
        db.refresh(db_flight)
        return db_flight
    
    def update(db: Session, flight_id: int, flight: schemas.FlightUpdate):
        db_flight = db.query(models.Flight).filter(models.Flight.id == flight_id).first()
        db_flight.flight_number = flight.flight_number
        db_flight.from_airport_id = flight.from_airport_id
        db_flight.to_airport_id = flight.to_airport_id
        db_flight.departure_date = flight.departure_date
        db_flight.arrival_date = flight.arrival_date
        db_flight.price = flight.price
        db_flight.currency = flight.currency
        db_flight.total_seats = flight.total_seats
        db_flight.left_seats = flight.left_seats
        db_flight.on_sale = flight.on_sale
        db_flight.actor_id = flight.actor_id
        db.commit()
        db.refresh(db_flight)
        return db_flight
    
    def delete(db: Session, flight_id: int):
        db_flight = db.query(models.Flight).filter(models.Flight.id == flight_id).first()
        db.delete(db_flight)
        db.commit()
        return db_flight









