from fastapi import Depends, APIRouter, HTTPException, status
import logging

from sqlalchemy.orm import Session

from typing import Optional
from crud_models.views.genders import Gender
from crud_models.schemas import genders as schemas

from db.database import get_db

routers = APIRouter()


@routers.get("/genders", response_model=list[schemas.Gender], tags=['genders'])
async def get_genders(db: Session = Depends(get_db),
                      page: Optional[int] = None,
                      limit: Optional[int] = None):
    try:
        return Gender.get_list(db, page, limit)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/gender/{gender_id}", tags=['genders'])
async def get_gender(gender_id: int,
                     db: Session = Depends(get_db)):
    try:
        db_gender = Gender.get_by_id(db, gender_id)
        if db_gender is None:
            raise ValueError('Gender not found')
        return schemas.Gender.from_orm(db_gender)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.post("/gender", tags=['genders'])
async def create_gender(gender: schemas.GenderCreate,
                        db: Session = Depends(get_db)):
    try:
        return Gender.create(db, gender)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.patch("/gender/{gender_id}", tags=["genders"])
async def update_gender(gender_id: int,
                        gender: schemas.GenderUpdate,
                        db: Session = Depends(get_db)):
    try:
        db_gender = Gender.get_by_id(db, gender_id)
        if db_gender is None:
            raise ValueError('Gender not found')
        return Gender.update(db, db_gender, gender)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.delete("/gender/{gender_id}", tags=["genders"])
async def delete_gender(gender_id: int, db: Session = Depends(get_db)):
    return Gender.delete(db, gender_id)
