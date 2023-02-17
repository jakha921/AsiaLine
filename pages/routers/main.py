from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
import logging

from auth.auth_token.auth_bearer import JWTBearer
from auth.auth_token.auth_handler import check_permissions
from db.database import get_db
from pages.views.currency import get_currency_last_item
from pages.views.main import get_dates_range, get_flights_and_search

# from pages import sort
# from pages.views import api

routers = APIRouter()


@routers.get("/main/flights/dates", tags=["pages"])
async def get_dates_and_count_flights(db: Session = Depends(get_db),
                                      from_date: date = ...,
                                      to_date: date = ...,
                                      jwt: dict = Depends(JWTBearer())
                                      ):
    """ Get dates and count flights for each date """
    if not check_permissions('main_page', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        dates_range = get_dates_range(db, from_date, to_date)
        if dates_range:
            # count flights by same date
            flight_by_date = {}
            for flight in dates_range:
                date = flight[0].date()
                if date in flight_by_date:
                    flight_by_date[flight[0].date()] += 1
                else:
                    flight_by_date[flight[0].date()] = 1

            # sort dict by date
            flight_by_date = dict(sorted(flight_by_date.items(), key=lambda item: item[0]))
            return flight_by_date
        return []
    except Exception as e:
        print(logging.error(e))


@routers.get("/main/flights", tags=["pages"])
async def get_flights(db: Session = Depends(get_db),
                      searching_text: Optional[str] = None,
                      from_date: Optional[date] = None,
                      to_date: Optional[date] = None,
                      page: int = None,
                      limit: int = None,
                      jwt: dict = Depends(JWTBearer())
                      ):
    """ Get flights where departure date is between from_date and to_date and search by text """
    if not check_permissions('flights_main', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    db_flights, counter = get_flights_and_search(db, searching_text, from_date, to_date, page, limit)

    result = {
        'currency': get_currency_last_item(db),
        'flights_count': counter,
        'flights': db_flights
    }
    return result
