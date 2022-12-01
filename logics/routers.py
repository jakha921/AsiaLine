from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, date, timedelta

from db.database import get_db
from crud_models import crud
from logics import api, sort
from app import crud as user_crud

routers = APIRouter()



@routers.get("/main/flights/dates")
async def get_flight_range_counter(db: Session = Depends(get_db), from_date: Optional[date] = datetime.now().date(), to_date: Optional[date]= datetime.now().date() + timedelta(days=1)):
    """ get dates and count flights for each date """
    dates_range = api.get_flights_by_range_departure_date(db, from_date, to_date)
    return sort.sort_by_date_flights(dates_range)


@routers.get("/main/flights/range")
async def get_static_flight_range(db: Session = Depends(get_db), from_date: Optional[date] = datetime.now().date(), date_to: Optional[date]= datetime.now().date() + timedelta(days=2)):
    """ get flights by range departure date and last currency rate """
    db_currency_rate = api.get_currency_last_item(db)
    db_flights = api.get_flights_by_range_departure_date(db, from_date, date_to)
    db_pass = api.get_reg_passenger_for_last_30_days(db)
    db_sold_tickets = api.get_sold_tickets_for_last_30_days(db)
    
    sorted_cur = sort.sort_currency_rate(db_currency_rate)
    sorted_flights = sort.group_flights(db, db_flights)

    result = {
        "currency":sorted_cur,
        "registered_passengers_for_last_30_days": db_pass,
        "sold_tickets_for_last_30_days": db_sold_tickets,
        "flights": sorted_flights
        }
    return result


@routers.get("/flights/main")
def get_flights(db: Session = Depends(get_db), from_date: Optional[date] = datetime.now().date()):
    """ get all flights where departure_date >= now and on_sale >= now """
    db_flights = api.get_flights_by_departure_date_and_on_sale(db, from_date)
    
    # get id from db_flights and get for this competitors_prices and add to dict
    for i in db_flights:
        get_competitors_prices = api.get_competitors_prices_by_flight_id(db, i.id)   
        
        i.competitors_prices = get_competitors_prices

    result = {'fli': len(db_flights), 'flights': db_flights}
    return result

@routers.get("/flights/queue")
def get_flights_queue(db: Session = Depends(get_db), from_date: Optional[date] = datetime.now().date()):
    """ get all flights where departure_date >= now and on_sale >= now """
    db_flights = api.get_flights_by_on_sale_date(db, from_date)

    result = {'queue_flights': db_flights}
    return result

