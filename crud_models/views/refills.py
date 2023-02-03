import logging
from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db import models
from crud_models.schemas import refills as schemas


class Refill:
    @staticmethod
    def get_list(db: Session, page: Optional[int], limit: Optional[int]):
        if page and limit:
            return db.query(models.Refill).filter(models.Refill.deleted_at == None). \
                offset(limit * (page - 1)).limit(limit).all()
        return db.query(models.Refill).filter(models.Refill.deleted_at == None).all()

    @staticmethod
    def get_by_id(db: Session, refill_id: int):
        return db.query(models.Refill).filter(models.Refill.id == refill_id, models.Refill.deleted_at == None).first()

    @staticmethod
    def create(db: Session, refill: schemas.RefillCreate):
        db_refill = models.Refill(**refill.dict())

        agent = db.query(models.Agent).filter(models.Agent.id == refill.agent_id).first()
        agent.balance += refill.amount

        db.add(db_refill)
        db.commit()
        db.refresh(db_refill)
        return db_refill

    @staticmethod
    def update(db: Session, refill_id: int, refill: schemas.RefillUpdate):
        """ get refill and find difference between old and new amount than add it to agent balance """
        db_refill = db.query(models.Refill, models.Agent). \
            filter(models.Refill.id == refill_id,
                   models.Agent.id == models.Refill.agent_id).first()
        refill_db = db_refill['Refill']
        agent = db_refill['Agent']

        agent.balance += refill.amount - refill_db.amount

        for key, value in refill.dict().items():
            if value is not None:
                setattr(refill_db, key, value)

        db.commit()
        return refill_db

    @staticmethod
    def delete(db: Session, refill_id: int):
        refill_db = db.query(models.Refill, models.Agent). \
            filter(models.Refill.id == refill_id,
                   models.Agent.id == models.Refill.agent_id).first()

        db_refill = refill_db['Refill']
        agent = refill_db['Agent']

        agent.balance -= db_refill.amount

        db_refill.deleted_at = datetime.now()
        db.commit()
        return {"message": "Refill deleted successfully"}
