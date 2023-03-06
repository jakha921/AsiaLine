from typing import Optional

from sqlalchemy.orm import Session

from crud_models.views.airports import Airport
from db import models
from crud_models.schemas import cities as schemas


class City:
    @staticmethod
    def get_list(db: Session, page: Optional[int] = None, limit: Optional[int] = None, is_count: bool = False):
        city = db.query(models.City)
        if page and limit:
            if is_count:
                return city.offset(limit * (page - 1)).limit(limit).all(), city.count()
            return city.offset(limit * (page - 1)).limit(limit).all()
        if is_count:
            return city.all(), city.count()
        return city.all()

    @staticmethod
    def get_by_id(db: Session, city_id: int):
        return db.query(models.City).filter(models.City.id == city_id).first()

    @staticmethod
    def create(db: Session, city: schemas.CityCreate):
        db_city = models.City(**city.dict())
        db.add(db_city)
        db.commit()
        db.refresh(db_city)
        return db_city

    @staticmethod
    def update(db: Session, db_city: models.City, city: schemas.CityUpdate):
        for key, value in city.dict().items():
            if value is not None:
                setattr(db_city, key, value)
        db.commit()
        return db_city

    @staticmethod
    def delete(db: Session, db_city: models.City):
        for db_airport in db_city.airports:
            Airport.delete(db, db_airport)
        db.delete(db_city)
        db.commit()
        return db_city
