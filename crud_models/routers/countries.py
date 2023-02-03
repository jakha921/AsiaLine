from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging

from db.database import get_db
from crud_models.schemas import countries as schemas
from crud_models.views.countries import Country

routers = APIRouter()


@routers.get("/countries", tags=["countries"], response_model=list[schemas.Country])
async def get_countries(
        page: Optional[int] = None,
        limit: Optional[int] = None,
        db: Session = Depends(get_db)):
    """
    Get list of countries\n
    *if offset and limit None return all countries*\n
    *if offset and limit not None return countries between offset and limit*.
    """
    try:
        return Country.get_list(db, page, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="get country list error")


@routers.get("/country/{country_id}", tags=["countries"])
async def get_country(country_id: int,
                      db: Session = Depends(get_db)):
    """ Get country by id """
    try:
        db_country = Country.get_by_id(db, country_id)
        if db_country is None:
            raise ValueError("Country not found")
        return schemas.Country.from_orm(db_country)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Get country error")


@routers.post("/country", tags=["countries"])
async def create_country(country: schemas.CountryCreate,
                         db: Session = Depends(get_db)):
    """ Create new country """
    try:
        return schemas.Country.from_orm(Country.create(db, country))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Create country error")


@routers.patch("/country/{country_id}", tags=["countries"])
async def update_country(country_id: int,
                         country: schemas.CountryUpdate,
                         db: Session = Depends(get_db)):
    """
    Update country by id\n
    **Optional fields**:\n
    *all fields*
    """
    try:
        db_country = Country.get_by_id(db, country_id)
        if db_country is None:
            raise ValueError("Country not found")
        return schemas.Country.from_orm(Country.update(db, db_country, country))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Update country error")


@routers.delete("/country/{country_id}", tags=["countries"])
async def delete_country(country_id: int,
                         db: Session = Depends(get_db)):
    """ Delete country by id """
    try:
        db_country = Country.get_by_id(db, country_id)
        if db_country is None:
            raise ValueError("Country not found")
        return Country.delete(db, db_country)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Delete country error")
