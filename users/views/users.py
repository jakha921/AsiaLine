from typing import Optional

from sqlalchemy.orm import Session

from auth.hashing import decode_password, encode_password
from db import models
from users.schemas import users as schemas


class User:

    @staticmethod
    def get_list(page: Optional[int],
                 limit: Optional[int],
                 db: Session):
        query = db.query(models.User). \
            filter(models.User.deleted_at == None)
        if page and limit:
            return query.offset(limit * (page - 1)).limit(limit).all()
        return query.all()

    @staticmethod
    def get_by_id(db: Session,
                  user_id: int):
        user = db.query(models.User).filter(models.User.id == user_id).first()
        # if user:
            # decode user password
            # user.password = decode_password(user.password)
        return user

    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(
            models.User
        ).filter(models.User.email == email).first()

    @staticmethod
    def create(db: Session, user: schemas.UserCreate):
        db_user = models.User(**user.dict())
        #     hash password and save user
        db_user.password = encode_password(db_user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update(db: Session, user_id: int, user: schemas.UserUpdate):
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        #    hash password and save user
        if user.password is not None and db_user.password != encode_password(user.password):
            user.password = encode_password(user.password)
        for key, value in user.dict().items():
            if value is not None:
                setattr(db_user, key, value)
        db.commit()
        return db_user

    @staticmethod
    def delete(db: Session, user_id: int):
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        db.delete(db_user)
        db.commit()
        return {"success": "User deleted successfully"}

    @staticmethod
    def get_permissions(db: Session, user_id: int):
        """ get all permissions of a user, based on his role_id, role_permission and permission tables """
        query = db.query(models.Permission.alias). \
            filter(models.Permission.id == models.RolePermission.permission_id). \
            filter(models.RolePermission.role_id == models.User.role_id). \
            filter(models.User.id == user_id).all()
        return [permission.alias for permission in query]
