from typing import Optional

from sqlalchemy.orm import Session

from db import models
from crud_models.schemas import airports as schemas


class Airport:
    @staticmethod
    def get_list(db: Session, offset: Optional[int], limit: Optional[int]):
        airport = db.query(models.Airport)
        if offset and limit:
            return airport.offset(limit * (offset - 1)).limit(limit).all()
        return airport.all()

    @staticmethod
    def get_by_id(db: Session, airport_id: int):
        return db.query(models.Airport).filter(models.Airport.id == airport_id).first()

    @staticmethod
    def create(db: Session, airport: schemas.AirportCreate):
        db_airport = models.Airport(**airport.dict())
        db.add(db_airport)
        db.commit()
        db.refresh(db_airport)
        return db_airport

    @staticmethod
    def update(db: Session, db_airport: models.Airport, airport: schemas.AirportUpdate):
        for key, value in airport.dict().items():
            if value is not None:
                setattr(db_airport, key, value)
        db.commit()
        return db_airport

    @staticmethod
    def delete(db: Session, db_airport: models.Airport):
        db.delete(db_airport)
        db.commit()
        return db_airport

    @staticmethod
    def get_with_cities(db: Session, page: Optional[int], limit: Optional[int], search: Optional[str]):
        query = f"SELECT a.id, a.airport_ru, a.airport_en, a.airport_uz, a.code, \
                json_build_object( \
                'id', c.id, \
                'city_ru', c.city_ru, \
                'city_en', c.city_en, \
                'city_uz', c.city_uz, \
                'code', c.code \
                ) as city \
                FROM airports AS a \
                LEFT JOIN cities AS c ON a.city_id = c.id "

        if search:
            search = search.lower()
            query += f"WHERE (LOWER(a.airport_ru) LIKE '%{search}%' \
                    OR LOWER(a.airport_en) LIKE '%{search}%' \
                    OR LOWER(a.airport_uz) LIKE '%{search}%' \
                    OR LOWER(a.code) LIKE '%{search}%' \
                    OR LOWER(c.city_ru) LIKE '%{search}%' \
                    OR LOWER(c.city_en) LIKE '%{search}%' \
                    OR LOWER(c.city_uz) LIKE '%{search}%' \
                    OR LOWER(c.code) LIKE '%{search}%') "

        counter = db.execute(query).fetchall()

        if page and limit:
            query += f"OFFSET {limit * (page - 1)} LIMIT {limit} "

        return db.execute(query).fetchall(), len(counter)
