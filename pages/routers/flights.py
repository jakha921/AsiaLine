from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from auth.auth_token.auth_bearer import JWTBearer
from auth.auth_token.auth_handler import check_permissions
from db.database import get_db
from pages.views.currency import get_currency_last_item

from pages.views.flights import get_flights_by_range_date, get_flight_quotes
from pages.views.tickets import get_tickets_by_flight

routers = APIRouter()


@routers.get("/flights/main")
async def get_flights_and_search(db: Session = Depends(get_db),
                                 searching_text: Optional[str] = None,
                                 from_date: Optional[date] = None,
                                 to_date: Optional[date] = None,
                                 page: Optional[int] = None,
                                 limit: Optional[int] = None,
                                 jwt: dict = Depends(JWTBearer())
                                 ):
    """ Get flights and search by text """
    if not check_permissions('get_flights_main', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    db_flights, counter = get_flights_by_range_date(db, from_date=from_date, to_date=to_date, page=page, limit=limit,
                                                    search_text=searching_text, is_on_sale=False)

    result = {
        "currency": get_currency_last_item(db),
        "flights_count": counter,
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
    db_tickets, counter = get_tickets_by_flight(db, flight_id=flight_id, search_text=searching_text, page=page, limit=limit)

    result = {
        "currency": get_currency_last_item(db),
        "tickets_count": counter,
        "tickets": db_tickets
    }
    return result


@routers.get("/flights/queue")
async def get_queue_flights(db: Session = Depends(get_db),
                            searching_text: Optional[str] = None,
                            from_date: Optional[date] = None,
                            to_date: Optional[date] = None,
                            page: Optional[int] = None,
                            limit: Optional[int] = None,
                            jwt: dict = Depends(JWTBearer())
                            ):
    """ Get all flights where on sale date >= now """
    if not check_permissions('get_flights_queue', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    db_flights, counter = get_flights_by_range_date(db, from_date=from_date, to_date=to_date, page=page, limit=limit,
                                                    search_text=searching_text, is_on_sale=True)

    result = {
        'currency': get_currency_last_item(db),
        'flights_count': counter,
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
                            jwt: dict = Depends(JWTBearer())
                            ):
    """ get all flight quotes """
    if not check_permissions('get_flights_quotas', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    db_flights, counter = get_flight_quotes(db, flight_id=flight_id, from_date=from_date, to_date=to_date, page=page,
                                            limit=limit,
                                            search_text=searching_text)
    resault = {
        'currency': get_currency_last_item(db),
        'flights_count': counter,
        'flights': db_flights
    }
    return resault
