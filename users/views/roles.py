from typing import Optional

from sqlalchemy.orm import Session

from db import models
from users.schemas import roles as schemas


class Role:

    @staticmethod
    def get_list(page: Optional[int],
                 limit: Optional[int],
                 db: Session, ):
        if page and limit:
            return db.query(models.Role).offset(limit * (page - 1)).limit(limit).all()
        return db.query(models.Role).all()

    @staticmethod
    def get_by_id(db: Session, role_id: int):
        return db.query(models.Role).filter(models.Role.id == role_id).first()

    @staticmethod
    def create(db: Session, role: schemas.RoleCreate):
        db_role = models.Role(**role.dict())
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
        return db_role

    @staticmethod
    def update(db: Session, role_id: int, role: schemas.RoleUpdate):
        db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
        for key, value in role.dict().items():
            if value is not None:
                setattr(db_role, key, value)
        db.commit()
        return db_role

    @staticmethod
    def delete(db: Session, role_id: int):
        db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
        db.delete(db_role)
        db.commit()
        return db_role
