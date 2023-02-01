from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, date, timedelta
import logging

from auth.auth.auth_bearer import JWTBearer
from auth.auth.auth_handler import check_permissions
from db.database import get_db
from pages import api, sort

routers = APIRouter()


@routers.get("/currency_rate")
async def get_currency_rate(db: Session = Depends(get_db)):
    """ Get currency rate from api and update currency rate """
    try:
        return api.get_currency_last_item(db)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/main/flights/dates")
async def get_dates_and_count_flights(db: Session = Depends(get_db),
                                      from_date: date = ...,
                                      to_date: date = ...,
                                      jwt: dict = Depends(JWTBearer())):
    """ Get dates and count flights for each date """
    if not check_permissions('main_page', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        dates_range = api.get_flights_by_range_departure_date(db, from_date, to_date)
        if dates_range:
            return sort.sort_by_date_flights(dates_range)
        return []
    except Exception as e:
        print(logging.error(e))


@routers.get("/main/flights")
async def get_flights_and_search(db: Session = Depends(get_db),
                                 searching_text: Optional[str] = None,
                                 from_date: Optional[date] = None,
                                 to_date: Optional[date] = None,
                                 page: int = None,
                                 limit: int = None,
                                 jwt: dict = Depends(JWTBearer())):
    """ Get flights where departure date is between from_date and to_date and search by text """
    if not check_permissions('flights_main', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    db_flights = api.get_flights_by_range_departure_date(db, from_date, to_date, page, limit, searching_text)
    currency_rate = api.get_currency_last_item(db)

    result = {
        'currency': sort.sort_currency_rate(currency_rate),
        'flights_count': len(db_flights),
        'flights': db_flights
    }
    return result


@routers.get("/flights/main")
async def get_flights_and_search(db: Session = Depends(get_db),
                                 searching_text: Optional[str] = None,
                                 from_date: Optional[date] = None,
                                 to_date: Optional[date] = None,
                                 page: Optional[int] = None,
                                 limit: Optional[int] = None,
                                 jwt: dict = Depends(JWTBearer())):
    """ Get flights and search by text """
    if not check_permissions('main_page', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    db_currency_rate = api.get_currency_last_item(db)
    db_flights = api.get_flights_by_range_departure_date(db, from_date, to_date, page, limit, searching_text, True)

    db_pass = api.get_reg_passenger_for_last_30_days(db)
    db_sold_tickets = api.get_sold_tickets_for_last_30_days(db)

    sorted_cur = sort.sort_currency_rate(db_currency_rate)

    result = {
        "currency": sorted_cur,
        "statistics": {
            "new_passengers": db_pass,
            "sold_tickets": len(db_sold_tickets),
            "revenue": sum(ticket.price for ticket in db_sold_tickets),
        },
        "flights_count": len(db_flights),
        "flights": db_flights
    }
    return result


@routers.get("/flights/tickets")
async def get_tickets_by_flight_id(db: Session = Depends(get_db),
                                   flight_id: int = ...,
                                   searching_text: Optional[str] = None,
                                   page: Optional[int] = None,
                                   limit: Optional[int] = None):
    """ Get all tickets for given flight id """
    db_tickets = api.get_tickets_by_departure_date_and_on_sale(db, flight_id=flight_id, page=page, limit=limit,
                                                               search_text=searching_text)

    db_currency_rate = api.get_currency_last_item(db)

    sorted_cur = sort.sort_currency_rate(db_currency_rate)

    result = {
        "currency": sorted_cur,
        "tickets_count": len(db_tickets),
        "tickets": db_tickets
    }
    return result


@routers.get("/flights/queue")
async def get_queue_fligths_and_search(db: Session = Depends(get_db),
                                       searching_text: Optional[str] = None,
                                       from_date: Optional[date] = None,
                                       to_date: Optional[date] = None,
                                       page: Optional[int] = None,
                                       limit: Optional[int] = None,
                                       jwt: dict = Depends(JWTBearer())):
    """ Get all flights where on sale date >= now """
    if not check_permissions('flights_queue', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    db_flights = api.get_flights_by_on_sale_date_and_search(db, from_date, to_date, page, limit, searching_text)

    currency_rate = api.get_currency_last_item(db)

    result = {
        'currency': sort.sort_currency_rate(currency_rate),
        'flights_count': len(db_flights),
        'queue_flights': db_flights
    }
    return result


@routers.get("/flights/quotas")
async def get_flight_quotas(db: Session = Depends(get_db),
                            flight_id: int = None,
                            searching_text: Optional[str] = None,
                            from_date: Optional[date] = None,
                            to_date: Optional[date] = None,
                            page: Optional[int] = None,
                            limit: Optional[int] = None,
                            jwt: dict = Depends(JWTBearer())):
    """ get all flight quotes """
    if not check_permissions('flights_quotas', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    db_flights = api.get_quotas_by_flight_id(db, flight_id, from_date, to_date, page, limit, searching_text)

    return db_flights


@routers.get("/tickets/main")
async def get_tickets(db: Session = Depends(get_db),
                      searching_text: Optional[str] = None,
                      from_date: Optional[date] = None,
                      to_date: Optional[date] = None,
                      agent_id: Optional[int] = None,
                      page: Optional[int] = None,
                      limit: Optional[int] = None,
                      jwt: dict = Depends(JWTBearer())):
    """ Get tickets by flights where departure date is not past now """
    if not check_permissions('tickets_page', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        db_tickets = api.get_tickets_by_departure_date_and_on_sale(db, from_date=from_date, to_date=to_date, page=page,
                                                                   limit=limit, search_text=searching_text,
                                                                   agent_id=agent_id)
        currency_rate = api.get_currency_last_item(db)

        result = {
            'currency': sort.sort_currency_rate(currency_rate),
            'tickets_count': len(db_tickets),
            'tickets': db_tickets
        }
        return result
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/users/main")
async def get_users(db: Session = Depends(get_db),
                    searching_text: Optional[str] = None,
                    page: Optional[int] = None,
                    limit: Optional[int] = None,
                    jwt: dict = Depends(JWTBearer())):
    """ get all users with then roles """
    if not check_permissions('users_main', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        db_users = api.get_all_users_with_role(db, page, limit, searching_text)

        return {
            'users_count': len(db_users),
            'users': db_users
        }
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/users/roles")
async def get_roles(db: Session = Depends(get_db),
                    searching_text: Optional[str] = None,
                    page: Optional[int] = None,
                    limit: Optional[int] = None,
                    jwt: dict = Depends(JWTBearer())):
    """ get all roles that can be assigned to users """
    if not check_permissions('users_roles', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        db_roles = api.get_all_roles(db, page=page, limit=limit, search_text=searching_text)
        return {
            # 'count_roles': len(db_roles),
            'roles': db_roles
        }
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


# payment
@routers.get("/payments/main")
async def get_tickets(db: Session = Depends(get_db),
                      searching_text: Optional[str] = None,
                      agent_id: Optional[int] = None,
                      from_date: Optional[date] = None,
                      to_date: Optional[date] = None,
                      page: Optional[int] = None,
                      limit: Optional[int] = None,
                      jwt: dict = Depends(JWTBearer())):
    """ get all payments who paid amount of agents for fill the balance """
    if not check_permissions('payments_main', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        db_payments = api.get_refill_by_agent_id(db, from_date, to_date, agent_id, page, limit, searching_text)
        return {
            'payments_count': len(db_payments),
            'payments': db_payments
        }
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/payments/agents/balance")
async def get_agent_balances(db: Session = Depends(get_db),
                             agent_id: Optional[int] = None,
                             page: Optional[int] = None,
                             limit: Optional[int] = None,
                             jwt: dict = Depends(JWTBearer())):
    """ Get all agent balances or by agent id """
    if not check_permissions('payments_agents_balance', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return api.get_agents_balance(db, agent_id, page, limit)


# agents
@routers.get("/agents/main")
async def get_agents(db: Session = Depends(get_db),
                     searching_text: Optional[str] = None,
                     agent_id: Optional[int] = None,
                     page: Optional[int] = None,
                     limit: Optional[int] = None,
                     jwt: dict = Depends(JWTBearer())):
    """ Get all agents and their discounts """
    if not check_permissions('agents_main', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        db_agents = api.get_agents_discounts(db, agent_id, page, limit, searching_text)
        return db_agents
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/agents/discounts")
async def get_discounts(db: Session = Depends(get_db),
                        searching_text: Optional[str] = None,
                        page: Optional[int] = None,
                        limit: Optional[int] = None,
                        jwt: dict = Depends(JWTBearer())):
    """ get all discounts that can be assigned to agents """
    if not check_permissions('agents_discounts', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        return api.get_discounts(db, searching_text, page, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


# airports
@routers.get("/guide")
async def get_airports(db: Session = Depends(get_db),
                       searching_text: Optional[str] = None,
                       page: Optional[int] = None,
                       limit: Optional[int] = None):
    """ get all airports """
    try:
        db_guide = api.get_guiede(db, searching_text, page, limit)
        return {
            # 'airports_count': len(db_guide),
            'guide': db_guide
        }
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


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
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
