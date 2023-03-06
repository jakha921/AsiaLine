from sqlalchemy.orm import Session
from typing import Optional

from crud_models.views.cities import City
from db import models
from crud_models.schemas import countries as schemas


class Country:
    @staticmethod
    def get_list(db: Session, page: Optional[int] = None, limit: Optional[int] = None, is_count=False):
        country = db.query(models.Country)
        if page and limit:
            if is_count:
                return country.offset(limit * (page - 1)).limit(limit).all(), country.count()
            else:
                return country.offset(limit * (page - 1)).limit(limit).all()

        if is_count:
            return country.all(), country.count()
        else:
            return country.all()

    @staticmethod
    def get_by_id(db: Session, country_id: int):
        return db.query(models.Country).filter(models.Country.id == country_id).first()

    @staticmethod
    def create(db: Session, country: schemas.CountryCreate):
        db_country = models.Country(**country.dict())
        db.add(db_country)
        db.commit()
        db.refresh(db_country)
        return db_country

    @staticmethod
    def update(db: Session, db_country: models.Country, country: schemas.CountryUpdate):
        for key, value in country.dict().items():
            if value is not None:
                setattr(db_country, key, value)
        db.commit()
        return db_country

    @staticmethod
    def delete(db: Session, db_country: models.Country):
        for db_city in db_country.cities:
            City.delete(db, db_city)
        db.delete(db_country)
        db.commit()
        return db_country
