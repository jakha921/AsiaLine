from typing import Optional
from sqlalchemy.orm import Session

from db import models
from crud_models.schemas import company as schemas


class Company:
    @staticmethod
    def get_list(db: Session, page: Optional[int], limit: Optional[int]):
        if page and limit:
            return db.query(models.Company).offset(limit * (page - 1)).limit(limit).all()
        return db.query(models.Company).all()

    @staticmethod
    def get_by_id(db: Session, company_id: int):
        return db.query(models.Company).filter(models.Company.id == company_id).first()

    @staticmethod
    def create(db: Session, company: schemas.CompanyCreate):
        db_company = models.Company(**company.dict())
        db.add(db_company)
        db.commit()
        db.refresh(db_company)
        return db_company
