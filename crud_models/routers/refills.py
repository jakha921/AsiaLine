from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging

from auth.auth_token.auth_bearer import JWTBearer
from auth.auth_token.auth_handler import check_permissions
from db.database import get_db
from crud_models.schemas import refills as schemas
from crud_models.views.refills import Refill

routers = APIRouter()


@routers.get("/refills", response_model=list[schemas.Refill], tags=['refills'])
async def get_refills(page: Optional[int] = None,
                      limit: Optional[int] = None,
                      db: Session = Depends(get_db)):
    try:
        return Refill.get_list(db, page, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/refill/{refill_id}", tags=['refills'])
async def get_refill(refill_id: int,
                     db: Session = Depends(get_db)):
    try:
        db_refill = Refill.get_by_id(db, refill_id)
        if db_refill is None:
            raise ValueError("Refill not found")
        return schemas.Refill.from_orm(db_refill)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.post("/refill", tags=['refills'])
async def create_refill(refill: schemas.RefillCreate,
                        jwt: dict = Depends(JWTBearer()),
                        db: Session = Depends(get_db)):
    if not check_permissions('create_refill', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    try:
        return schemas.Refill.from_orm(Refill.create(db, refill))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.patch("/refill/{refill_id}", tags=["refills"])
async def update_refill(refill_id: int,
                        refill: schemas.RefillUpdate,
                        jwt: dict = Depends(JWTBearer()),
                        db: Session = Depends(get_db)):
    if not check_permissions('update_refill', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    try:
        db_refill = Refill.get_by_id(db, refill_id)
        if db_refill is None:
            raise ValueError("Refill not found")
        return schemas.Refill.from_orm(Refill.update(db, refill_id, refill))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.delete("/refill/{refill_id}", tags=["refills"])
async def delete_refill(refill_id: int,
                        jwt: dict = Depends(JWTBearer()),
                        db: Session = Depends(get_db)):
    if not check_permissions('delete_refill', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    try:
        db_refill = Refill.get_by_id(db, refill_id)
        if db_refill is None or db_refill.is_deleted:
            raise ValueError("Refill not found")
        return Refill.delete(db, refill_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
