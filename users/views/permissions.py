from typing import Optional

from sqlalchemy.orm import Session

from db import models
from users.schemas import permissions as schemas


class Permission:

    @staticmethod
    def get_list(page: Optional[int],
                 limit: Optional[int],
                 db: Session):
        if page and limit:
            return db.query(models.Permission).offset(limit * (page - 1)).limit(limit).all()
        return db.query(models.Permission).all()

    @staticmethod
    def get_by_id(db: Session, permission_id: int):
        return db.query(models.Permission).filter(models.Permission.id == permission_id).first()

    @staticmethod
    def create(db: Session, permission: schemas.PermissionCreate):
        db_permission = models.Permission(**permission.dict())
        db.add(db_permission)
        db.commit()
        db.refresh(db_permission)
        return db_permission

    @staticmethod
    def update(db: Session, permission_id: int, permission: schemas.PermissionUpdate):
        db_permission = db.query(models.Permission).filter(models.Permission.id == permission_id).first()
        for key, value in permission.dict().items():
            if value is not None:
                setattr(db_permission, key, value)
        db.commit()
        return db_permission

    @staticmethod
    def delete(db: Session, db_permission: models.Permission):
        db.delete(db_permission)
        db.commit()
        return db_permission
