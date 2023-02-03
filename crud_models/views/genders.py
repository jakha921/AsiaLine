from typing import Optional
from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from db import models
from crud_models.schemas import genders as schemas


class Gender:
    @staticmethod
    def get_list(db: Session, page: Optional[int], limit: Optional[int]):
        if page and limit:
            return db.query(models.Gender).offset(limit * (page - 1)).limit(limit).all()
        return db.query(models.Gender).all()

    @staticmethod
    def get_by_id(db: Session, gender_id: int):
        return db.query(models.Gender).filter(models.Gender.id == gender_id).first()

    @staticmethod
    def create(db: Session, gender: schemas.GenderCreate):
        db_gender = models.Gender(**gender.dict())
        db.add(db_gender)
        db.commit()
        db.refresh(db_gender)
        return db_gender

    @staticmethod
    def update(db: Session, db_gender: models.Gender, gender: schemas.GenderUpdate):
        for key, value in gender.dict().items():
            if value is not None:
                setattr(db_gender, key, value)
        db.commit()
        return db_gender

    @staticmethod
    def delete(db: Session, gender_id: int):
        try:
            db_gender = db.query(models.Gender).filter(models.Gender.id == gender_id).first()
            if db_gender is None:
                raise ValueError('Gender not found')
            db.delete(db_gender)
            db.commit()
            return {"message": "Gender deleted successfully"}
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
