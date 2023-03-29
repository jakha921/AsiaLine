from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from db import models
from users.schemas import user_history as schemas


class History:
    @staticmethod
    def get_list(db: Session, offset: Optional[int], limit: Optional[int]):
        if offset and limit:
            return db.query(models.UserHistory).offset(offset).limit(limit).all()
        return db.query(models.UserHistory).all()

    @staticmethod
    def get_by_user_id(db: Session, user_id: int, offset: Optional[int], limit: Optional[int]):

        query = db.query(models.UserHistory). \
            filter(models.UserHistory.user_id == user_id). \
            order_by(models.UserHistory.created_at.desc())

        if offset and limit:
            return query.offset(limit * (offset - 1)).limit(limit).all()
        return query.all()

    @staticmethod
    def create(db: Session, user_id: int, action: str, extra_info: Optional[str]):
        db_user = models.UserHistory(user_id=user_id, action=action, extra_info=extra_info)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
