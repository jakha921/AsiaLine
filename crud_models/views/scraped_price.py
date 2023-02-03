from datetime import datetime
from typing import Optional
from fastapi import HTTPException, status
import logging

from sqlalchemy.orm import Session

from db import models
from crud_models.schemas import scraped_price as schemas


class ScrapedPrice:
    @staticmethod
    def get_list(db: Session, offset: Optional[int], limit: Optional[int]):
        query = db.query(models.ScrapedPrice) \
            .filter(
            models.Flight.id == models.ScrapedPrice.flight_id,
            models.Flight.deleted_at == None,
            models.Flight.departure_date >= datetime.now())
        if offset and limit:
            return query.offset(limit * (offset - 1)).limit(limit).all()
        return query.all()

    @staticmethod
    def get_by_id(db: Session, scraped_price_id: int):
        return db.query(models.ScrapedPrice).filter(
            models.ScrapedPrice.id == scraped_price_id,
            models.Flight.id == models.ScrapedPrice.flight_id,
            models.Flight.deleted_at == None,
            models.Flight.departure_date >= datetime.now()
        ).first()

    @staticmethod
    def create(db: Session, scraped_price: schemas.ScrapedPriceCreate):
        db_scraped_price = models.ScrapedPrice(**scraped_price.dict())
        db.add(db_scraped_price)
        db.commit()
        db.refresh(db_scraped_price)
        return db_scraped_price

    @staticmethod
    def update(db: Session, db_scraped_price: models.ScrapedPrice, scraped_price: schemas.ScrapedPriceUpdate):
        for key, value in scraped_price.dict().items():
            if value is not None:
                setattr(db_scraped_price, key, value)
        db.commit()
        return db_scraped_price

    @staticmethod
    def delete(db: Session, db_scraped_price: models.ScrapedPrice):
        db.delete(db_scraped_price)
        db.commit()
        return {"message": "Scraped price deleted successfully"}
