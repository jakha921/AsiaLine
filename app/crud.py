from app import schemas
from db import models

# from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import Optional

class Role:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.Role).offset(min).limit(max).all()
        return db.query(models.Role).all()
    
    def get_by_id(db: Session, role_id: int):
        return db.query(models.Role).filter(models.Role.id == role_id).first()
    
    def get_by_name(db: Session, name: str):
        return db.query(models.Role).filter(models.Role.name == name).first()
    
    def create(db: Session, role: schemas.RoleCreate):
        db_role = models.Role(**role.dict())
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
        return db_role
    
    def update(db: Session, role_id: int, role: schemas.RoleUpdate):
        db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
        db_role.name = role.name
        db_role.title_ru = role.title_ru
        db_role.title_uz = role.title_uz
        db_role.title_en = role.title_en
        db.commit()
        db.refresh(db_role)
        return db_role
    
    def delete(db: Session, role_id: int):
        db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
        db.delete(db_role)
        db.commit()
        return db_role


class User:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.User).offset(min).limit(max).all()
        return db.query(models.User).all()

    def get_by_id(db: Session, user_id: int):
        return db.query(models.User).filter(models.User.id == user_id).first()

    def get_by_email(db: Session, email: str):
        return db.query(models.User).filter(models.User.email == email).first()

    def create(db: Session, user: schemas.UserCreate):
        db_user = models.User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update(db: Session, user: schemas.UserUpdate):
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        print(user)
        db_user.username = user.username
        db_user.email = user.email
        db_user.password = user.password
        db.commit()
        db.refresh(db_user)
        return db_user

    def delete(db: Session, user_id: int):
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        db.delete(db_user)
        db.commit()
        return db_user

