from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, date, timedelta

from db.database import get_db
from crud_models import crud
from app import crud as user_crud
from app.currency_rate import get_currency_rate 
from db import models

routers = APIRouter()

#? Static
@routers.get("/static")
async def get_static_flight_range(db: Session = Depends(get_db), from_date: Optional[date] = "2022-02-28", date_to: Optional[date]= "2023-01-31"):
    db_currency_rate = crud.get_currency_last_item(db)
    db_static = crud.Flight.get_by_range_departure_date(db, from_date, date_to)
    
    currency_rate = {
        "RUBUSD": db_currency_rate.rub_to_usd,
        "RUBEUR": db_currency_rate.rub_to_eur,
        "RUBUZS": db_currency_rate.rub_to_uzs,
        "updated_at": db_currency_rate.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    }
        

    
    flight = {}
    # print((db_static[0]))
    for i in db_static:
        flight['id'] = i.id
        flight['flight_name'] = i.flight_number
        flight['from_airport'] = crud.Airport.get_by_id(db, i.from_airport_id)
        flight['to_airport'] = crud.Airport.get_by_id(db, i.to_airport_id)
        flight['departure_date'] = i.departure_date.strftime("%Y-%m-%d %H:%M:%S")
        flight['arrival_date'] = i.arrival_date.strftime("%Y-%m-%d %H:%M:%S")
        flight['price'] = i.price
        flight['currency'] = i.currency
        flight['total_seats'] = i.total_seats
        flight['left_seats'] = i.left_seats
        flight['on_sale'] = i.on_sale.strftime("%Y-%m-%d %H:%M:%S")
        flight['actor_id'] = user_crud.User.get_by_id(db, i.actor_id)
        flight['created_at'] = i.created_at
        flight['updated_at'] = i.updated_at
        flight['deleted_at'] = i.deleted_at
        

    result = {"currency":currency_rate, "flights": db_static}
    return result


def get_flights_by_range_departure_date(db: Session, from_date: Optional[date] = datetime.now().date(), to_date: Optional[date] = datetime.now().date()):
    """ group by flight from_airport_id and to_airport_id"""
    return db.query(models.Flight).filter(models.Flight.departure_date >= from_date, models.Flight.departure_date <= to_date).all()

def update_currency_rate(db: Session):
    """ get currency rate from api and update currency rate """
    currency_rate = get_currency_rate()
    print(currency_rate)
    db_currency_rate = models.CurrencyRate(
        rub_to_usd = currency_rate['currency_rate']['RUBUSD'],
        rub_to_eur = currency_rate['currency_rate']['RUBEUR'],
        rub_to_uzs = currency_rate['currency_rate']['RUBUZS'],
        updated_at = datetime.now()
    )
    db.add(db_currency_rate)
    db.commit()
    db.refresh(db_currency_rate)
    return db_currency_rate

def get_currency_last_item(db: Session):
    """ get last currency rate if updated_at <= 8 hours, update currency rate """
    db_currency_rate = db.query(models.CurrencyRate).order_by(models.CurrencyRate.updated_at.desc()).first()
    if db_currency_rate.updated_at <= datetime.now() - timedelta(hours=8):
        db_currency_rate = update_currency_rate(db)
    return db_currency_rate

def get_reg_passenger_for_last_30_days(db: Session):
    """ get registered passenger for last 30 days """
    return db.query(models.Passenger).filter(models.Passenger.created_at >= datetime.now() - timedelta(days=30)).count()

def get_sold_tickets_for_last_30_days(db: Session):
    """ get sold tickets for last 30 days """
    return db.query(models.Ticket).filter(models.Ticket.created_at >= datetime.now() - timedelta(days=30)).count()

def get_flights_by_departure_date_and_on_sale(db: Session, date: Optional[date] = datetime.now().date()):
    """ get flights by departure_date is >= now and on_sale <= now """
    return db.query(models.Flight).filter(models.Flight.departure_date >= date, models.Flight.on_sale >= date).order_by(models.Flight.departure_date, models.Flight.on_sale).all()

def get_competitors_prices_by_flight_id(db: Session, flight_id: int):
    """ get competitors prices by flight_id """
    return db.query(models.ScrapedPrice).filter(models.ScrapedPrice.flight_id == flight_id).all()

def get_flights_by_on_sale_date(db: Session, date: Optional[date] = datetime.now().date()):
    """ get flights by on_sale is >= now """
    return db.query(models.Flight).filter(models.Flight.on_sale >= date).order_by(models.Flight.on_sale).all()


