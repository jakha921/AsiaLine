from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, date, timedelta
import traceback
import logging

from db.database import get_db
from crud_models import crud as crud_models
from logics import api, sort
from app import crud as user_crud

routers = APIRouter()


@routers.get("/currency_rate")
async def get_currency_rate(db: Session = Depends(get_db)):
    """ get currency rate from api and update currency rate """
    try:
        return api.get_currency_last_item(db)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


@routers.get("/main/flights/dates")
async def get_flight_range_counter(db: Session = Depends(get_db), from_date: Optional[date] = datetime.now().date(), to_date: Optional[date] = datetime.now().date()):
    """ get dates and count flights for each date """
    try:
        dates_range = api.get_flights_by_range_departure_date(db, from_date, to_date)
        return sort.sort_by_date_flights(dates_range)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))



@routers.get("/main/flights/range")
async def get_static_flight_range(db: Session = Depends(get_db), from_date: Optional[date] = datetime.now().date(), date_to: Optional[date]= datetime.now().date(), lang: Optional[str] = "ru"):
    """ get flights by range departure date and last currency rate """
    db_currency_rate = api.get_currency_last_item(db)
    db_flights = api.get_flights_by_range_departure_date(db, from_date, date_to)
    
    db_pass = api.get_reg_passenger_for_last_30_days(db)
    db_sold_tickets = api.get_sold_tickets_for_last_30_days(db)
    
    sorted_cur = sort.sort_currency_rate(db_currency_rate)
    sorted_flights = sort.sort_flights(db, db_flights, lang)

    result = {
        "currency":sorted_cur,
        "statistics" : {
            "new_passengers": db_pass,
            "sold_tickets": len(db_sold_tickets),
            "revenue": sum(ticket.price for ticket in db_sold_tickets),
            },
        "flights_count": len(sorted_flights),
        "flights": sorted_flights
        }
    return result


@routers.get("/flights/main")
async def get_flights(db: Session = Depends(get_db), from_date: Optional[date] = datetime.now().date(), to_date: Optional[date] = datetime.now().date(), lang: Optional[str] = "ru"):
    """ get all flights where departure_date >= now and on_sale >= now """
    db_flights = api.get_flights_by_departure_date_and_on_sale(db, from_date, to_date)
    sorted_flights = sort.sort_flights(db, db_flights, lang)
    currency_rate = api.get_currency_last_item(db)

    result = {
        'currency': sort.sort_currency_rate(currency_rate),
        'flights_count': len(db_flights),
        'flights': sorted_flights
        }
    return result


@routers.get("/flights/queue")
async def get_flights_queue(db: Session = Depends(get_db), from_date: Optional[date] = datetime.now().date(), to_date: Optional[date] = datetime.now().date(), lang: Optional[str] = "ru"):
    """ get all flights where departure_date >= now and on_sale >= now """
    db_flights = api.get_flights_by_on_sale_date(db, from_date, to_date)
    sorted_flights = sort.sort_flights(db, db_flights, lang)
    
    currency_rate = api.get_currency_last_item(db)

    result = {
        'currency': sort.sort_currency_rate(currency_rate),
        'flights_count': len(sorted_flights),
        'queue_flights': sorted_flights
        }
    return result


@routers.get("/flights/quotas")
async def get_flight_quotas(db: Session = Depends(get_db), from_date: Optional[date] = datetime.now().date(), to_date: Optional[date] = datetime.now().date(), lang: Optional[str] = "ru"):
    """ get all quotas for flight """
    # db_quotas = api.get_quotas_by_flight_id(db, from_date, to_date)
    db_flights = api.get_flights_by_departure_date_and_on_sale(db, from_date, to_date)
    # sorted_flights = sort.sort_flights(db, db_flights)
    # currency_rate = api.get_currency_last_item(db)
    
    # # get id from sorted_flights and get for this quoter by flight id and add to dict
    # for flight in sorted_flights:
    #     flight["quotas"] = api.get_quotas_by_flight_id(db, flight["id"])

        
    result = {
        # 'currency': sort.sort_currency_rate(currency_rate),
        # 'quotas_count': len(db_flights),
        'quotas': db_flights
        }
    return result


@routers.get("/tickets/main")
async def get_tickets(db: Session = Depends(get_db), from_date: Optional[date] = datetime.now().date(), to_date: Optional[date] = datetime.now().date(), lang: Optional[str] = "ru"):
    """ get all tickets where departure_date >= now and on_sale >= now """
    try:
        db_tickets = api.get_tickets_by_departure_date_and_on_sale(db, from_date, to_date)
        sorted_tickets = sort.sort_tickets(db_tickets, lang)
        currency_rate = api.get_currency_last_item(db)

        result = {
            'currency': sort.sort_currency_rate(currency_rate),
            'tickets_count': len(sorted_tickets),
            'tickets': sorted_tickets
            }
        return result
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


@routers.get("/users/main")
async def get_passengers(db: Session = Depends(get_db), lang: Optional[str] = "ru"):
    """ get all passengers """
    db_passengers = api.get_all_passengers_with_role(db)
    sorted_passengers = sort.sort_passengers(db_passengers, lang)
    return sorted_passengers

























