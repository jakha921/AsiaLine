from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging

from crud_models.views.countries import Country
from db.database import get_db
from crud_models.schemas import cities as schemas
from crud_models.views.cities import City

routers = APIRouter()


@routers.get("/cities", tags=["cities"], response_model=list[schemas.City])
async def get_cities(page: Optional[int] = None,
                     limit: Optional[int] = None,
                     db: Session = Depends(get_db)):
    """
    Get list of cities\n
    *if offset and limit None return all cities*\n
    *if offset and limit not None return cities between offset and limit*.
    """
    try:
        return City.get_list(db, page, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/city/{city_id}", tags=["cities"])
async def get_city(city_id: int,
                   db: Session = Depends(get_db)):
    """ Get city by id """
    try:
        db_city = City.get_by_id(db, city_id)
        if db_city is None:
            raise ValueError("City not found")
        return schemas.City.from_orm(db_city)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.post("/city", tags=["cities"])
async def create_city(city: schemas.CityCreate,
                      db: Session = Depends(get_db)):
    """ Create new city """
    try:
        if not Country.get_by_id(db, city.country_id):
            raise ValueError("Country not found")
        return City.create(db, city)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.patch("/city/{city_id}", tags=["cities"])
async def update_city(city_id: int,
                      city: schemas.CityUpdate,
                      db: Session = Depends(get_db)):
    """
    Update city by id\n
    **Optional fields**:\n
    *all fields*
    """
    try:
        db_city = City.get_by_id(db, city_id)
        if db_city is None:
            raise ValueError("City not found")
        if city.country_id and not Country.get_by_id(db, city.country_id):
            raise ValueError("Country not found")
        return schemas.City.from_orm(City.update(db, db_city, city))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.delete("/city/{city_id}", tags=["cities"])
async def delete_city(city_id: int,
                      db: Session = Depends(get_db)):
    """ Delete city by id """
    try:
        db_city = City.get_by_id(db, city_id)
        if db_city is None:
            raise ValueError("City not found")
        return City.delete(db, db_city)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
