from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging

from db.database import get_db
from crud_models.schemas import flight_guide as schemas
from crud_models.views.flight_guide import FlightGuide
from auth.auth_token.auth_bearer import JWTBearer
from auth.auth_token.auth_handler import check_permissions, get_user_id

routers = APIRouter()


@routers.get("/flight_guide", response_model=list[schemas.FlightGuide], tags=["flight_guide"])
async def get_flight_guide(page: Optional[int] = None,
                           limit: Optional[int] = None,
                           db: Session = Depends(get_db)):
    try:
        return FlightGuide.get_list(db, page, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/flight_guide/{flight_guide_id}", tags=["flight_guide"])
async def get_flight_guide(flight_guide_id: int,
                           db: Session = Depends(get_db)):
    try:
        db_flight_guide = FlightGuide.get_by_id(db, flight_guide_id)
        if db_flight_guide is None:
            raise ValueError("FlightGuide not found")
        return schemas.FlightGuide.from_orm(db_flight_guide)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.post("/flight_guide", tags=["flight_guide"])
async def create_flight_guide(flight_guide: schemas.FlightGuideCreate,
                              jwt: dict = Depends(JWTBearer()),
                              db: Session = Depends(get_db)):
    if not check_permissions("create_flight_guide", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        if flight_guide.from_airport_id == flight_guide.to_airport_id:
            raise ValueError("Departure airport must be different from arrival airport")
        if FlightGuide.get_by_flight_number(db, flight_guide.flight_number):
            raise ValueError("FlightGuide with this flight number already exists")
        db_flight_guide = FlightGuide.create(db, flight_guide)
        return schemas.FlightGuide.from_orm(db_flight_guide)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.patch("/flight_guide/{flight_guide_id}", tags=["flight_guide"])
async def update_flight_guide(flight_guide_id: int,
                              flight_guide: schemas.FlightGuideCreate,
                              jwt: dict = Depends(JWTBearer()),
                              db: Session = Depends(get_db)):
    if not check_permissions("update_flight_guide", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        if flight_guide.from_airport_id == flight_guide.to_airport_id:
            raise ValueError("Departure airport must be different from arrival airport")
        db_flight_guide = FlightGuide.get_by_id(db, flight_guide_id)
        if db_flight_guide is None:
            raise ValueError("FlightGuide not found")
        db_flight_guide_update = FlightGuide.update(db, db_flight_guide, flight_guide)
        return schemas.FlightGuide.from_orm(db_flight_guide_update)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.delete("/flight_guide/{flight_guide_id}", tags=["flight_guide"])
async def delete_flight_guide(flight_guide_id: int,
                              jwt: dict = Depends(JWTBearer()),
                              db: Session = Depends(get_db)):
    if not check_permissions("delete_flight_guide", jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        db_flight_guide = FlightGuide.get_by_id(db, flight_guide_id)
        if db_flight_guide is None:
            raise ValueError("FlightGuide not found")
        return FlightGuide.delete(db, db_flight_guide)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
