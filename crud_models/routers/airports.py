from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging

from auth.auth_token.auth_bearer import JWTBearer
from auth.auth_token.auth_handler import check_permissions
from crud_models.views.cities import City
from db.database import get_db
from crud_models.schemas import airports as schemas
from crud_models.views.airports import Airport

routers = APIRouter()


@routers.get("/airports", response_model=list[schemas.Airport], tags=["airports"])
async def get_airports(page: Optional[int] = None,
                       limit: Optional[int] = None,
                       db: Session = Depends(get_db)):
    """
    Get list of airports\n
    *if offset and limit None return all airports*\n
    *if offset and limit not None return airports between offset and limit.*
    """
    try:
        return Airport.get_list(db, page, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="get airport list error")


@routers.get("/airport/{airport_id}", tags=["airports"])
async def get_airport(airport_id: int,
                      db: Session = Depends(get_db)):
    """ Get airport by id """
    try:
        db_airport = Airport.get_by_id(db, airport_id)
        if db_airport is None:
            raise ValueError("Airport not found")
        return schemas.Airport.from_orm(db_airport)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="get airport error")


@routers.post("/airport", tags=["airports"])
async def create_airport(airport: schemas.AirportCreate,
                         jwt: dict = Depends(JWTBearer()),
                         db: Session = Depends(get_db)):
    """ Create new airport """
    if not check_permissions('create_airport', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    try:
        if City.get_by_id(db, airport.city_id) is None:
            raise ValueError("City not found")
        return schemas.Airport.from_orm(Airport.create(db, airport))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="create airport error")


@routers.patch("/airport/{airport_id}", tags=["airports"])
async def update_airport(airport_id: int,
                         airport: schemas.AirportUpdate,
                         jwt: dict = Depends(JWTBearer()),
                         db: Session = Depends(get_db)):
    """
    Update airport by id\n
    **Optional fields**:\n
    *all fields*
    """
    if not check_permissions('update_airport', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    try:
        db_airport = Airport.get_by_id(db, airport_id)
        if db_airport is None:
            raise ValueError("Airport not found")
        if City.get_by_id(db, airport.city_id) is None:
            raise ValueError("City not found")
        return schemas.Airport.from_orm(Airport.update(db, db_airport, airport))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="update airport error")


@routers.delete("/airport/{airport_id}", tags=["airports"])
async def delete_airport(airport_id: int,
                         jwt: dict = Depends(JWTBearer()),
                         db: Session = Depends(get_db)):
    """ Delete airport by id """
    if not check_permissions('delete_airport', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    try:
        db_airport = Airport.get_by_id(db, airport_id)
        if db_airport is None:
            raise ValueError("Airport not found")
        if City.get_by_id(db, db_airport.city_id) is None:
            raise ValueError("City not found")
        return Airport.delete(db, db_airport)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="delete airport error")
