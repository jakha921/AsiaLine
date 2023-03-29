from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging

from auth.auth_token.auth_bearer import JWTBearer
from auth.auth_token.auth_handler import check_permissions
from db.database import get_db
from users.schemas import discounts as schemas
from users.views.discounts import Discount

routers = APIRouter()


@routers.get("/discounts", response_model=list[schemas.Discount], tags=["discounts"])
async def get_discounts_list(page: Optional[int] = None,
                             limit: Optional[int] = None,
                             db: Session = Depends(get_db)):
    try:
        return Discount.get_list(page, limit, db)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/discount/{discount_id}", tags=["discounts"])
async def get_discount(discount_id: int, db: Session = Depends(get_db)):
    try:
        db_discount = Discount.get_by_id(discount_id, db)
        if db_discount is None:
            raise ValueError("Discount not found")
        return schemas.Discount.from_orm(db_discount)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.post("/discount", tags=["discounts"])
async def create_discount(discount: schemas.DiscountCreate,
                          jwt: dict = Depends(JWTBearer()),
                          db: Session = Depends(get_db)):
    if not check_permissions('create_discount', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    try:
        return schemas.Discount.from_orm(Discount.create(discount, db))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.patch("/discount/{discount_id}", tags=["discounts"])
async def update_discount(discount_id: int,
                          discount: schemas.DiscountUpdate,
                          jwt: dict = Depends(JWTBearer()),
                          db: Session = Depends(get_db)):
    if not check_permissions('update_discount', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    try:
        db_discount = Discount.get_by_id(discount_id, db)
        if db_discount is None:
            raise ValueError("Discount not found")
        return schemas.Discount.from_orm(Discount.update(db, db_discount, discount))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.delete("/discount/{discount_id}", tags=["discounts"])
async def delete_discount(discount_id: int,
                          jwt: dict = Depends(JWTBearer()),
                          db: Session = Depends(get_db)):
    if not check_permissions('delete_discount', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    try:
        db_discount = Discount.get_by_id(discount_id, db)
        if db_discount is None:
            raise ValueError("Discount not found")
        return Discount.delete(db_discount, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
