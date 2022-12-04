from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, date, timedelta
import traceback
import logging

from db.database import get_db
from crud_models import crud
from app import crud as user_crud
from app.currency_rate import get_currency_rate 
from db import models

routers = APIRouter()


# to exist date add min and max time
def add_time(from_date, to_date):
    from_date = datetime.combine(from_date, datetime.now().time())
    to_date = datetime.combine(to_date, datetime.max.time())
    return from_date, to_date

#? Static
def get_flights_by_range_departure_date(db: Session, from_date, to_date):
    """ get flights by delete data and departure date """
    from_date, to_date = add_time(from_date, to_date)
    return db.query(models.Flight).filter(models.Flight.deleted_at == None, models.Flight.departure_date >= from_date, models.Flight.departure_date <= to_date).order_by(models.Flight.departure_date).all()

def update_currency_rate(db: Session):
    """ get currency rate from api and update currency rate """
    currency_rate = get_currency_rate()
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


# ! check it
def get_sold_tickets_for_last_30_days(db: Session):
    """ get sold tickets for last 30 days """
    return db.query(models.Ticket).filter(models.Ticket.status_id == 3).all()

# ! optimize it
def get_flights_by_departure_date_and_on_sale(db: Session, from_date, to_date):
    """ get flights by departure_date is >= now and on_sale <= now """
    from_date, to_date = add_time(from_date, to_date)
    print(from_date, '\n', to_date)
    return db.query(
        models.Flight
        ).filter(
            models.Flight.deleted_at == None,
            models.Flight.departure_date >= from_date,
            models.Flight.departure_date <= to_date,
            models.Flight.on_sale <= from_date
            ).order_by(models.Flight.departure_date, models.Flight.on_sale).all()


def get_competitors_prices_by_flight_id(db: Session, flight_id: int):
    """ get competitors prices by flight_id """
    return db.query(models.ScrapedPrice).filter(models.ScrapedPrice.flight_id == flight_id).all()


def get_flights_by_on_sale_date(db: Session, from_date, to_date):
    """ get flights by on_sale is >= now """
    from_date, to_date = add_time(from_date, to_date)
    return db.query(
        models.Flight
        ).filter(
            models.Flight.deleted_at == None,
            models.Flight.on_sale >= from_date,
            models.Flight.departure_date >= from_date,
            models.Flight.departure_date <= to_date,
            ).order_by(models.Flight.on_sale).all()


def get_quotas_by_flight_id(db, flight_id):
    """ get all from booking where flights departure_date >= now """
    try:
        return db.query(models.Booking).filter(models.Booking.flight_id == flight_id).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_tickets_by_departure_date_and_on_sale(db: Session, from_date, to_date):
    """ get tickets by departure_date is >= now and on_sale <= now """
    try:
        from_date, to_date = add_time(from_date, to_date)
        return db.query(
            models.Flight, models.Ticket, models.TicketStatus
            ).filter(
                models.Flight.deleted_at == None,
                models.Flight.departure_date >= from_date,
                models.Flight.departure_date <= to_date,
                models.Flight.on_sale <= from_date,
                models.Ticket.flight_id == models.Flight.id,
                models.Ticket.deleted_at == None,
                models.TicketStatus.id == models.Ticket.status_id
                
                ).order_by(models.Flight.departure_date, models.Ticket.created_at).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_all_passengers_with_role(db: Session):
    """ get all passengers with role """
    try:
        return db.query(
            models.User, models.Role
                ).filter(
                    models.User.role_id == models.Role.id).order_by(models.User.date_joined).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))

