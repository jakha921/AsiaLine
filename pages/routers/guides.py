from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
import logging

from auth.auth_token.auth_bearer import JWTBearer
from auth.auth_token.auth_handler import check_permissions
from db.database import get_db
from crud_models.views.countries import Country
from crud_models.views.cities import City
from crud_models.views.airports import Airport
from crud_models.views.company import Company
from crud_models.views.flight_guide import FlightGuide
from pages.views.currency import get_currency_last_item

routers = APIRouter()


@routers.get("/guide/countries")
async def get_countries(db: Session = Depends(get_db),
                        searching_text: Optional[str] = None,
                        page: Optional[int] = None,
                        limit: Optional[int] = None):
    try:
        db_countries, counter = Country.get_countries(db, page, limit, searching_text)
        return {
            'countries_count': counter,
            'countries': db_countries
        }
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/guide/cities")
async def get_cities(db: Session = Depends(get_db),
                     searching_text: Optional[str] = None,
                     page: Optional[int] = None,
                     limit: Optional[int] = None):
    try:
        db_cities, counter = City.get_with_countries(db, page, limit, searching_text)
        return {
            'cities_count': counter,
            'cities': db_cities
        }
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/guide/airports")
async def get_airports(db: Session = Depends(get_db),
                       searching_text: Optional[str] = None,
                       page: Optional[int] = None,
                       limit: Optional[int] = None):
    try:
        db_airports, counter = Airport.get_with_cities(db, page, limit, searching_text)
        return {
            'airports_count': counter,
            'airports': db_airports
        }
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/guide/companies")
async def get_companies(db: Session = Depends(get_db),
                        searching_text: Optional[str] = None,
                        page: Optional[int] = None,
                        limit: Optional[int] = None):
    try:
        db_companies, counter = Company.get_list(db, page, limit, searching_text)
        return {
            'companies_count': counter,
            'companies': db_companies
        }
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/guide/flight_guide")
async def get_flight_guide(db: Session = Depends(get_db),
                           searching_text: Optional[str] = None,
                           page: Optional[int] = None,
                           limit: Optional[int] = None):
    try:
        db_companies, counter = FlightGuide.get_detail_flight_guide(db, page, limit, searching_text)
        return {
            'currency': get_currency_last_item(db),
            'flights_count': counter,
            'flights': db_companies
        }
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
