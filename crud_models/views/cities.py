from typing import Optional

from sqlalchemy.orm import Session

from crud_models.views.airports import Airport
from db import models
from crud_models.schemas import cities as schemas


class City:
    @staticmethod
    def get_list(db: Session, page: Optional[int] = None, limit: Optional[int] = None):
        city = db.query(models.City)
        if page and limit:
            return city.offset(limit * (page - 1)).limit(limit).all()
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

    @staticmethod
    def get_with_countries(db: Session, page: Optional[int] = None, limit: Optional[int] = None,
                           searching_text: Optional[str] = None):
        query = f"SELECT c.id, c.city_ru, c.city_en, c.city_uz, c.code as  city_code, \
                json_build_object( \
                'id', co.id, \
                'country_ru', co.country_ru, \
                'country_en', co.country_en, \
                'country_uz', co.country_uz, \
                'code', co.code \
                ) as country \
                FROM cities AS c \
                LEFT JOIN countries AS co ON c.country_id = co.id "\

        if searching_text:
            searching_text = searching_text.lower()
            query += f"WHERE (LOWER(c.city_ru) LIKE '%{searching_text}%' \
                    OR LOWER(c.city_en) LIKE '%{searching_text}%' \
                    OR LOWER(c.city_uz) LIKE '%{searching_text}%' \
                    OR LOWER(co.country_ru) LIKE '%{searching_text}%' \
                    OR LOWER(co.country_en) LIKE '%{searching_text}%' \
                    OR LOWER(co.country_uz) LIKE '%{searching_text}%')"

        counter = db.execute(query).fetchall()

        if page and limit:
            query += f" OFFSET {limit * (page - 1)} LIMIT {limit}"

        return db.execute(query).fetchall(), len(counter)
