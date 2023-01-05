from fastapi import APIRouter
from sqlalchemy import func, case
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import traceback
import logging

from users.currency_rate import get_currency_rate
from db import models

routers = APIRouter()


def add_time(from_date, to_date):
    """ To exist date add min and max time """
    from_date = datetime.combine(from_date, datetime.now().time())
    to_date = datetime.combine(to_date, datetime.max.time())
    return from_date, to_date


def update_currency_rate(db: Session):
    """ get currency rate from api and update currency rate """
    currency_rate = get_currency_rate()
    print(currency_rate)
    db_currency_rate = models.CurrencyRate(
        rub_to_usd=currency_rate['RUBUSD'],
        rub_to_eur=currency_rate['RUBEUR'],
        rub_to_uzs=currency_rate['RUBUZS'],
        updated_at=currency_rate['updated_at']
    )
    db.add(db_currency_rate)
    db.commit()
    db.refresh(db_currency_rate)
    return db_currency_rate


def get_currency_last_item(db: Session):
    """ Get last currency rate if updated_at <= 8 hours, update currency rate """
    db_currency_rate = db.query(models.CurrencyRate).order_by(models.CurrencyRate.updated_at.desc()).first()
    if not db_currency_rate:
        update_currency_rate(db)
        get_currency_last_item(db)
    if db_currency_rate.updated_at <= datetime.now() - timedelta(hours=8):
        db_currency_rate = update_currency_rate(db)

    return db_currency_rate


# Statics
def get_flights_by_range_departure_date(db: Session, from_date, to_date):
    """ Get flights where now <= departure_date <= now """
    from_date, to_date = add_time(from_date, to_date)
    return db.query(models.Flight
                    ).filter(
                        models.Flight.deleted_at == None,
                        models.Flight.departure_date >= from_date,
                        models.Flight.departure_date <= to_date,
                        models.Flight.on_sale <= from_date
                    ).order_by(models.Flight.departure_date,
                               models.Flight.on_sale).all()


def get_reg_passenger_for_last_30_days(db: Session):
    """ Get registered passenger for last 30 days """
    return db.query(models.Passenger).filter(models.Passenger.created_at >= datetime.now() - timedelta(days=30)).count()


# ! check it status_id
def get_sold_tickets_for_last_30_days(db: Session):
    """ Get sold tickets for last 30 days """
    try:
        return db.query(
            models.Ticket
        ).filter(
            models.Ticket.status_id == 3).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_tickets_by_flight_id(db: Session, flight_id):
    """ Get all tickets by flight_id """
    try:
        return db.query(
            models.Ticket
        ).filter(
            models.Ticket.deleted_at == None,
            models.Ticket.flight_id == flight_id
        ).order_by(models.Ticket.created_at).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


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


def get_quotas_by_flight_id(db, from_date, to_date):
    """ Get booking by flight_id """
    try:
        from_date, to_date = add_time(from_date, to_date)

    #     get models Flight, Agent and Booking
        return db.query(
            models.Flight,
            models.Agent,
            models.Booking,
        ).filter(
            models.Flight.deleted_at == None,
            models.Flight.departure_date >= from_date,
            models.Flight.departure_date <= to_date,
            models.Flight.on_sale <= from_date,
            models.Flight.id == models.Booking.flight_id,
            models.Booking.deleted_at == None,
            models.Agent.id == models.Booking.agent_id,
        ).order_by(models.Flight.departure_date,
                     models.Flight.on_sale).all()
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


def get_all_users_with_role(db: Session):
    """ get all passengers with role """
    try:
        return db.query(
            models.User, models.Role
        ).filter(
            models.User.role_id == models.Role.id).order_by(models.User.date_joined).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_all_roles(db: Session):
    """ get all roles """
    try:
        return db.query(models.Role).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


# get tickets by agent_id
def get_tickets_by_agent_id(db: Session, from_date, to_date):
    """ get tickets by departure_date is >= now and on_sale <= now """
    try:
        from_date, to_date = add_time(from_date, to_date)

        return db.query(
            models.Refill, models.Agent, models.User
        ).filter(
            models.Refill.deleted_at == None,
            models.Refill.created_at >= from_date,
            models.Refill.created_at <= to_date,
            models.Agent.id == models.Refill.agent_id,
            models.User.id == models.Agent.user_id
        ).order_by(models.Refill.created_at.desc()).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_agents_balance(db: Session, agent_id):
    """ get agents by agent_id if agent_id is None then get all agents """
    try:
        if agent_id:
            return db.query(
                models.Agent
            ).filter(
                models.Agent.id == agent_id,
                models.Agent.deleted_at == None
            ).all()
        else:
            return db.query(
                models.Agent
            ).filter(
                models.Agent.deleted_at == None
            ).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_agents_discounts(db: Session):
    """ get agents and discounts by agent_id """
    try:
        return db.query(
            models.Agent, models.Discount, models.User
        ).filter(
            models.Agent.discount_id == models.Discount.id,
            models.Agent.deleted_at == None,
            models.User.id == models.Agent.user_id
        ).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_discounts(db: Session):
    """ get discounts """
    try:
        return db.query(
            models.Discount
        ).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_airports(db: Session):
    """ get airports """
    try:
        return db.query(
            models.Airport
        ).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_cities(db: Session):
    """ get cities """
    try:
        return db.query(
            models.City
        ).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_countries(db: Session):
    """ get countries """
    try:
        return db.query(
            models.Country
        ).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def get_ticket_classes(db: Session):
    """ get ticket class """
    try:
        return db.query(
            models.TicketClass
        ).all()
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))