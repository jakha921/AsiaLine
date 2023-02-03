from typing import Optional

from sqlalchemy.orm import Session

from db import models
from users.schemas import discounts as schemas


class Discount:

    @staticmethod
    def get_list(page: Optional[int],
                 limit: Optional[int],
                 db: Session):
        if page and limit:
            return db.query(models.Discount).offset(limit * (page - 1)).limit(limit).all()
        return db.query(models.Discount).all()

    @staticmethod
    def get_by_id(discount_id: int, db: Session):
        return db.query(models.Discount).filter(models.Discount.id == discount_id).first()

    @staticmethod
    def create(discount: schemas.DiscountCreate, db: Session, ):
        db_discount = models.Discount(**discount.dict())
        db.add(db_discount)
        db.commit()
        db.refresh(db_discount)
        return db_discount

    @staticmethod
    def update(db: Session, db_discount: models.Discount, discount: schemas.DiscountUpdate):
        for key, value in discount.dict().items():
            if value is not None:
                setattr(db_discount, key, value)
        db.commit()
        return db_discount

    @staticmethod
    def delete(db_discount: models.Discount, db: Session):
        db.delete(db_discount)
        db.commit()
        return db_discount
