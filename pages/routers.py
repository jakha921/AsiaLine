from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, date, timedelta
import traceback
import logging

from db.database import get_db
from pages import api, sort

routers = APIRouter()


@routers.get("/currency_rate")
async def get_currency_rate(db: Session = Depends(get_db)):
    """ Get currency rate from api and update currency rate """
    try:
        return api.get_currency_last_item(db)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


@routers.get("/main/flights/dates")
async def get_dates_and_count_flights(db: Session = Depends(get_db),
                                      from_date: Optional[date] = datetime.now().date(),
                                      to_date: Optional[date] = datetime.now().date()):
    """ Get dates and count flights for each date """
    try:
        dates_range = api.get_flights_by_range_departure_date(db, from_date, to_date)
        return sort.sort_by_date_flights(dates_range)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


@routers.get("/main/flights/range")
async def get_static_flight_range(db: Session = Depends(get_db),
                                  from_date: Optional[date] = datetime.now().date(),
                                  date_to: Optional[date] = datetime.now().date()):
    """ get flights by range departure date and last currency rate """
    db_currency_rate = api.get_currency_last_item(db)
    db_flights = api.get_flights_by_range_departure_date(db, from_date, date_to)

    db_pass = api.get_reg_passenger_for_last_30_days(db)
    db_sold_tickets = api.get_sold_tickets_for_last_30_days(db)

    sorted_cur = sort.sort_currency_rate(db_currency_rate)
    sorted_flights = sort.sort_flights(db, db_flights)

    result = {
        "currency": sorted_cur,
        "statistics": {
            "new_passengers": db_pass,
            "sold_tickets": len(db_sold_tickets),
            "revenue": sum(ticket.price for ticket in db_sold_tickets),
        },
        "flights_count": len(sorted_flights),
        "flights": sorted_flights
    }
    return result


@routers.get("/flights/main")
async def get_flights(db: Session = Depends(get_db),
                      from_date: Optional[date] = datetime.now().date(),
                      to_date: Optional[date] = datetime.now().date()):
    """ Get all flights where departure date >= now and on sale <= now """
    db_flights = api.get_flights_by_range_departure_date(db, from_date, to_date)
    sorted_flights = sort.sort_flights(db, db_flights)
    currency_rate = api.get_currency_last_item(db)

    result = {
        'currency': sort.sort_currency_rate(currency_rate),
        'flights_count': len(db_flights),
        'flights': sorted_flights
    }
    return result


@routers.get("/flights/tickets")
async def get_tickets_by_flight_id(db: Session = Depends(get_db),
                                   flight_id: int = ...):
    """ Get all tickets for given flight id """
    db_tickets = api.get_tickets_by_flight_id(db, flight_id)
    db_currency_rate = api.get_currency_last_item(db)

    sorted_cur = sort.sort_currency_rate(db_currency_rate)

    result = {
        "currency": sorted_cur,
        "tickets_count": len(db_tickets),
        "tickets": db_tickets
    }
    return result


@routers.get("/flights/queue")
async def get_queue_fligths(db: Session = Depends(get_db),
                            from_date: Optional[date] = datetime.now().date(),
                            to_date: Optional[date] = datetime.now().date()):
    """ Get all flights where on sale date >= now """
    db_flights = api.get_flights_by_on_sale_date(db, from_date, to_date)
    sorted_flights = sort.sort_flights(db, db_flights)

    currency_rate = api.get_currency_last_item(db)

    result = {
        'currency': sort.sort_currency_rate(currency_rate),
        'flights_count': len(sorted_flights),
        'queue_flights': sorted_flights
    }
    return result


@routers.get("/flights/quotas")
async def get_flight_quotas(db: Session = Depends(get_db),
                            from_date: Optional[date] = datetime.now().date(),
                            to_date: Optional[date] = datetime.now().date()):
    """ get all flight quotes """
    db_flights = api.get_quotas_by_flight_id(db, from_date, to_date)
    sorted_quotas = sort.sort_flight_quotas(db_flights)

    return sorted_quotas


@routers.get("/tickets/main")
async def get_tickets(db: Session = Depends(get_db),
                      from_date: Optional[date] = datetime.now().date(),
                      to_date: Optional[date] = datetime.now().date(),
                      agent_id: Optional[int] = None):
    """ Get tickets by flights where departure date is not past now """
    try:
        db_tickets = api.get_tickets_by_departure_date_and_on_sale(db, from_date, to_date, agent_id)
        sorted_tickets = sort.sort_tickets(db_tickets)
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
async def get_users(db: Session = Depends(get_db)):
    """ get all users with then roles """
    try:
        db_users = api.get_all_users_with_role(db)
        sorted_users = sort.sort_users(db_users)

        return {
            'users_count': len(sorted_users),
            'users': sorted_users
        }
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


@routers.get("/users/roles")
async def get_roles(db: Session = Depends(get_db)):
    """ get all roles that can be assigned to users """
    try:
        db_roles = api.get_all_roles(db)
        return {
            'count_roles': len(db_roles),
            'roles': db_roles
        }
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


# payment
@routers.get("/payments/main")
async def get_tickets(db: Session = Depends(get_db),
                      from_date: Optional[date] = datetime.now().date() - timedelta(days=7),
                      to_date: Optional[date] = datetime.now().date(),
                      agent_id: Optional[int] = None):
    """ get all payments who paid amount of agents for fill the balance """
    try:
        db_payments = api.get_tickets_by_agent_id(db, from_date, to_date, agent_id)
        sorted_payments = sort.sorted_payments(db_payments)
        return {
            'payments_count': len(sorted_payments),
            'payments': sorted_payments
        }
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


@routers.get("/payments/agents/balance")
async def get_agent_balances(db: Session = Depends(get_db),
                             agent_id: Optional[int] = None):
    """ Get all agent balances or by agent id """
    return api.get_agents_balance(db, agent_id)


# agents
@routers.get("/agents/main")
async def get_agents(db: Session = Depends(get_db), agent_id: Optional[int] = None):
    """ Get all agents and their discounts """
    try:
        db_agents = api.get_agents_discounts(db, agent_id)
        sorted_agents = sort.sorted_agents(db_agents)
        return sorted_agents
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


@routers.get("/agents/discounts")
async def get_discounts(db: Session = Depends(get_db)):
    """ get all discounts that can be assigned to agents """
    try:
        return api.get_discounts(db)
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


# airports
@routers.get("/guide/airports")
async def get_airports(db: Session = Depends(get_db)):
    """ get all airports """
    try:
        db_airports = api.get_airports(db)
        return {
            'airports_count': len(db_airports),
            'airports': db_airports
        }
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


# city
@routers.get("/guide/cities")
async def get_cities(db: Session = Depends(get_db)):
    """ get all cities """
    try:
        db_cities = api.get_cities(db)
        return {
            'cities_count': len(db_cities),
            'cities': db_cities
        }
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


# countries
@routers.get("/guide/countries")
async def get_countries(db: Session = Depends(get_db)):
    """ get all countries """
    try:
        db_countries = api.get_countries(db)
        return {
            'countries_count': len(db_countries),
            'countries': db_countries
        }
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


# ticket classes
@routers.get("/guide/ticket_classes")
async def get_ticket_classes(db: Session = Depends(get_db)):
    """ get all ticket classes """
    try:
        db_classes = api.get_ticket_classes(db)
        return {
            'ticket_classes_count': len(db_classes),
            'ticket_classes': db_classes
        }
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))
