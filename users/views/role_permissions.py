from typing import Optional

from sqlalchemy.orm import Session

from db import models
from users.schemas import role_permissions as schemas


class RolePermission:
    @staticmethod
    def get_list(page: Optional[int],
                 limit: Optional[int],
                 db: Session):
        if page and limit:
            return db.query(models.RolePermission).offset(limit * (page - 1)).limit(limit).all()
        return db.query(models.RolePermission).all()

    @staticmethod
    def get_by_id(role_permission_id: int,
                  db: Session):
        return db.query(models.RolePermission).filter(models.RolePermission.id == role_permission_id).first()

    @staticmethod
    def create(role_permission: schemas.RolePermissionCreate,
               db: Session, ):
        db_role_permission = models.RolePermission(**role_permission.dict())
        db.add(db_role_permission)
        db.commit()
        db.refresh(db_role_permission)
        return db_role_permission

    @staticmethod
    def update(db: Session, db_role_permission: models.RolePermission, role_permission: schemas.RolePermissionUpdate):
        db_role_permission.role_id = role_permission.role_id
        db_role_permission.permission_id = role_permission.permission_id
        db.commit()
        return db_role_permission

    @staticmethod
    def delete(db: Session, db_role_permission: models.RolePermission):
        db.delete(db_role_permission)
        db.commit()
        return db_role_permission
