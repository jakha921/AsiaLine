from crud_models import schemas
from db import models

from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from fastapi import Depends, APIRouter, HTTPException, status
import traceback
import logging


class Country:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        print(min, max)
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
        for key, value in country.dict().items():
            if value is not None:
                setattr(db_country, key, value)
        db.commit()
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
        for key, value in city.dict().items():
            if value is not None:
                setattr(db_city, key, value)
        db.commit()
        return db_city
    
    def delete(db: Session, city_id: int):
        try:
            db_city = db.query(models.City).filter(models.City.id == city_id).first()
            if db_city is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
            else:
                db.delete(db_city)
                db.commit()
                return db_city
        except Exception as e:
            print(logging.error(traceback.format_exc()))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


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
        for key, value in airport.dict().items():
            if value is not None:
                setattr(db_airport, key, value)
        db.commit()
        return db_airport
    
    def delete(db: Session, airport_id: int):
        try:
            db_airport = db.query(models.Airport).filter(models.Airport.id == airport_id).first()
            if db_airport is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Airport not found")
            else:
                db.delete(db_airport)
                db.commit()
                return db_airport
        except Exception as e:
            print(logging.error(traceback.format_exc()))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


class Flight:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        try:
            if min and max:
                return db.query(models.Flight).filter(models.Flight.deleted_at == None, models.Flight.departure_date >= datetime.now()).order_by(models.Flight.departure_date).offset(min).limit(max).all()
            return db.query(models.Flight).filter(models.Flight.deleted_at == None, models.Flight.departure_date >= datetime.now()).order_by(models.Flight.departure_date).all()
        except Exception as e:
            print(e)
    
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
        for key, value in flight.dict().items():
            if value is not None:
                setattr(db_flight, key, value)
        db.commit()
        return db_flight
    
    def delete(db: Session, flight_id: int):
        try:
            db_flight = db.query(models.Flight).filter(models.Flight.id == flight_id).first()
            if db_flight is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
            if db_flight.deleted_at is None:
                db_flight.deleted_at = datetime.now()
            else:
                return {"message": "Flight already deleted"}
            db.commit()
            return {"message": "Flight deleted successfully"}
        except Exception as e:
            print(logging.error(traceback.format_exc()))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


class FlightPriceHistory:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        print(min, max)
        if min and max:
            return db.query(models.FlightPriceHistory).offset(min).limit(max).all()
        return db.query(models.FlightPriceHistory).all()

    def get_by_flight_id(db: Session, flight_id: int, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.FlightPriceHistory).filter(models.FlightPriceHistory.flight_id == flight_id).order_by(models.FlightPriceHistory.created_at.desc()).offset(min).limit(max).all()
        return db.query(models.FlightPriceHistory).filter(models.FlightPriceHistory.flight_id == flight_id).order_by(models.FlightPriceHistory.created_at.desc()).all()
    
    def create(db: Session, price: int, flight_id: int):
        db_price = models.FlightPriceHistory(new_price=price, flight_id=flight_id)
        db.add(db_price)
        db.commit()
        db.refresh(db_price)
        return db_price


class Ticket:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.Ticket).offset(min).limit(max).all()
        return db.query(models.Ticket).all()
    
    def get_by_id(db: Session, ticket_id: int):
        return db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    
    def create(db: Session, ticket: schemas.TicketCreate, db_flight: models.Flight):
        """ if ticket created successfully, -1 from models Flight left_seats """
        db_ticket = models.Ticket(**ticket.dict())
        db.add(db_ticket)
        db.commit()
        db.refresh(db_ticket)
        print('before', db_flight.left_seats)
        db_flight.left_seats -= 1
        db.commit()
        print('after', db_flight.left_seats)
        return db_ticket
    
    def update(db: Session, ticket_id: int, ticket: schemas.TicketUpdate):
        db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
        for key, value in ticket.dict().items():
            if value is not None:
                setattr(db_ticket, key, value)
        db.commit()
        return db_ticket

    def delete(db: Session, ticket_id: int):
        try:
            db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
            if db_ticket is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
            if db_ticket.deleted_at is None:
                db_ticket.deleted_at = datetime.now()
            else:
                return {"message": "Ticket already deleted"}
            db.commit()
            
            db_flight = db.query(models.Flight).filter(models.Flight.id == db_ticket.flight_id).first()
            print(db_flight.left_seats)
            db_flight.left_seats += 1
            db.commit()
            print(db_flight.left_seats)
            
            return {"message": "Ticket deleted successfully"}
        except Exception as e:
            print(logging.error(traceback.format_exc()))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")




