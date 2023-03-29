from fastapi import Depends, APIRouter, HTTPException, status
import logging

from sqlalchemy.orm import Session

from db import models

from db.database import get_db

routers = APIRouter()


@routers.get("/payments/type", tags=['refills'])
async def get_genders(db: Session = Depends(get_db)):
    try:
        return db.query(models.PaymentType).all()
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
