from typing import Optional

from sqlalchemy.orm import Session

from db import models
from users.schemas import roles as schemas
from users.schemas.role_permissions import RolePermissionCreate
from users.views.permissions import Permission
from users.views.role_permissions import RolePermission


class Role:

    @staticmethod
    def get_list(page: Optional[int],
                 limit: Optional[int],
                 db: Session, ):
        if page and limit:
            return db.query(models.Role).offset(limit * (page - 1)).limit(limit).all()
        return db.query(models.Role).all()

    @staticmethod
    def get_role_by_id(db: Session, role_id: int):
        return db.query(models.Role).filter(models.Role.id == role_id).first()

    @staticmethod
    def get_by_id(db: Session, role_id: int):
        query = f"SELECT r.*, COUNT(rp.id) AS permissions_count,\
                COALESCE(json_agg(\
                    jsonb_build_object(\
                        'id', p.id,\
                        'alias', p.alias, \
                        'title_ru', p.title_ru, \
                        'title_en', p.title_en, \
                        'title_uz', p.title_uz, \
                        'descriptions', p.description)) FILTER (WHERE p.id IS NOT NULL), '[]') AS permissions \
                FROM roles AS r \
                LEFT JOIN role_permissions rp ON r.id = rp.role_id \
                LEFT JOIN permissions p ON rp.permission_id = p.id \
                WHERE r.id = {role_id} \
                GROUP BY r.id"

        return db.execute(query).fetchall() if db.execute(query).fetchall() else None

    @staticmethod
    def create(db: Session, role: schemas.RoleCreate):
        permissions = None
        db_role = role.dict()
        if db_role.get('permissions'):
            permissions = db_role.pop('permissions')
        db_role = models.Role(**db_role)
        db.add(db_role)
        db.commit()
        db.refresh(db_role)

        role_permissions = []
        if permissions:
            for permission in set(permissions):
                rp = RolePermission.create(RolePermissionCreate(
                    role_id=db_role.id,
                    permission_id=permission
                ), db)
                role_permissions.append(rp)

        permissions = []
        for permission in role_permissions:
            perm = Permission.get_by_id(db, permission.permission_id)
            permissions.append(perm)

        result = {}
        print(db_role)
        for key, value in db_role.__dict__.items():
            if key != 'permissions':
                result[key] = value

        result['permissions'] = permissions
        return result

    @staticmethod
    def update(db: Session, role_id: int, role: schemas.RoleUpdate):
        permissions = None
        update_role = role.dict()
        if update_role.get('permissions'):
            permissions = update_role.pop('permissions')

        db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
        for key, value in update_role.items():
            if value is not None:
                setattr(db_role, key, value)

        db_role_permissions = db.query(models.RolePermission).filter(models.RolePermission.role_id == role_id).all()

        if permissions:
            permissions = list(set(permissions))

            for db_role_permission in db_role_permissions:
                if db_role_permission.permission_id not in permissions:
                    RolePermission.delete(db, db_role_permission)

            # remove repeated from permissions list compare with db_role_permissions
            permissions = [x for x in permissions if x not in
                           [db_role_permission.permission_id for db_role_permission in db_role_permissions]]

            for permission in permissions:
                if permission not in [db_role_permission.permission_id for db_role_permission in db_role_permissions]:
                    RolePermission.create(RolePermissionCreate(
                        role_id=role_id,
                        permission_id=permission
                    ), db)

        db.commit()
        db.refresh(db_role)

        # get permissions
        db_role_permissions = db.query(models.RolePermission).filter(models.RolePermission.role_id == role_id).all()

        permissions = []
        for db_role_permission in db_role_permissions:
            perm = Permission.get_by_id(db, db_role_permission.permission_id)
            permissions.append(perm)

        result = {}
        for key, value in db_role.__dict__.items():
            if key != 'permissions':
                result[key] = value

        result['permissions'] = permissions
        return result

    @staticmethod
    def delete(db: Session, db_role: models.Role):
        role_permissions = db.query(models.RolePermission).filter(models.RolePermission.role_id == db_role.id).all()
        print(role_permissions)
        if role_permissions:
            for role_permission in role_permissions:
                RolePermission.delete(db, role_permission)
        db.delete(db_role)
        db.commit()
        return db_role
