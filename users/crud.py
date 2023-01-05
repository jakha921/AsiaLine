from datetime import datetime

from user_auth.hashing import encode_password, decode_password
from users import schemas
from db import models

from sqlalchemy.orm import Session
from typing import Optional


class Role:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.Role).offset(min).limit(max).all()
        return db.query(models.Role).all()

    def get_by_id(db: Session, role_id: int):
        return db.query(models.Role).filter(models.Role.id == role_id).first()

    def create(db: Session, role: schemas.RoleCreate):
        db_role = models.Role(**role.dict())
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
        return db_role

    def update(db: Session, role_id: int, role: schemas.RoleUpdate):
        db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
        for key, value in role.dict().items():
            if value is not None:
                setattr(db_role, key, value)
        db.commit()
        return db_role

    def delete(db: Session, role_id: int):
        db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
        db.delete(db_role)
        db.commit()
        return db_role


class User:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.User). \
                filter(models.User.deleted_at == None). \
                offset(min).limit(max).all()
        return db.query(models.User).all()

    def get_by_id(db: Session, user_id: int):
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            # decode user password
            user.password = decode_password(user.password)
        return user

    def get_by_email(db: Session, email: str):
        return db.query(
            models.User
        ).filter(models.User.email == email).first()

    def create(db: Session, user: schemas.UserCreate):
        db_user = models.User(**user.dict())
        #     hash password and save user
        db_user.password = encode_password(db_user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update(db: Session, user_id: int, user: schemas.UserUpdate):
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        #    hash password and save user
        if db_user.password != encode_password(user.password):
            user.password = encode_password(user.password)
        for key, value in user.dict().items():
            if value is not None:
                setattr(db_user, key, value)
        db.commit()
        return db_user

    def delete(db: Session, user_id: int):
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        db.delete(db_user)
        db.commit()
        return {"success": "User deleted successfully"}


class Section:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.Section).offset(min).limit(max).all()
        return db.query(models.Section).all()

    def get_by_id(db: Session, section_id: int):
        return db.query(models.Section).filter(models.Section.id == section_id).first()

    def create(db: Session, section: schemas.SectionCreate):
        db_section = models.Section(**section.dict())
        db.add(db_section)
        db.commit()
        db.refresh(db_section)
        return db_section

    def update(db: Session, section_id: int, section: schemas.SectionUpdate):
        db_section = db.query(models.Section).filter(models.Section.id == section_id).first()
        for key, value in section.dict().items():
            if value is not None:
                setattr(db_section, key, value)
        db.commit()
        return db_section

    def delete(db: Session, section_id: int):
        """ get section by id and delete all permissions related to it than delete section """
        db.query(models.Permission).filter(models.Permission.section_id == section_id).delete()
        db.query(models.Section).filter(models.Section.id == section_id).delete()
        db.commit()
        return {"success": "Section deleted successfully with all permissions related to it"}


class Permission:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.Permission).offset(min).limit(max).all()
        return db.query(models.Permission).all()

    def get_by_id(db: Session, permission_id: int):
        return db.query(models.Permission).filter(models.Permission.id == permission_id).first()

    def create(db: Session, permission: schemas.PermissionCreate):
        db_permission = models.Permission(**permission.dict())
        db.add(db_permission)
        db.commit()
        db.refresh(db_permission)
        return db_permission

    def update(db: Session, permission_id: int, permission: schemas.PermissionUpdate):
        db_permission = db.query(models.Permission).filter(models.Permission.id == permission_id).first()
        for key, value in permission.dict().items():
            if value is not None:
                setattr(db_permission, key, value)
        db.commit()
        return db_permission

    def delete(db: Session, permission_id: int):
        db_permission = db.query(models.Permission).filter(models.Permission.id == permission_id).first()
        db.delete(db_permission)
        db.commit()
        return db_permission


class RolePermission:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.RolePermission).offset(min).limit(max).all()
        return db.query(models.RolePermission).all()

    def get_by_id(db: Session, role_permission_id: int):
        return db.query(models.RolePermission).filter(models.RolePermission.id == role_permission_id).first()

    def create(db: Session, role_permission: schemas.RolePermissionCreate):
        db_role_permission = models.RolePermission(**role_permission.dict())
        db.add(db_role_permission)
        db.commit()
        db.refresh(db_role_permission)
        return db_role_permission

    def update(db: Session, role_permission_id: int, role_permission: schemas.RolePermissionUpdate):
        db_role_permission = db.query(models.RolePermission).filter(
            models.RolePermission.id == role_permission_id).first()
        db_role_permission.role_id = role_permission.role_id
        db_role_permission.permission_id = role_permission.permission_id
        db.commit()
        return db_role_permission

    def delete(db: Session, role_permission_id: int):
        db_role_permission = db.query(models.RolePermission).filter(
            models.RolePermission.id == role_permission_id).first()
        db.delete(db_role_permission)
        db.commit()
        return db_role_permission


class Agent:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.Agent).filter(
                models.Agent.block_date == None
            ).offset(min).limit(max).all()
        return db.query(models.Agent).filter(
            models.Agent.block_date == None
        ).all()

    def get_by_id(db: Session, agent_id: int):
        return db.query(models.Agent).filter(
            models.Agent.id == agent_id,
            models.Agent.block_date == None).first()

    def create(db: Session, agent: schemas.AgentCreate):
        db_agent = models.Agent(**agent.dict())
        db.add(db_agent)
        db.commit()
        db.refresh(db_agent)
        return db_agent

    def update(db: Session, agent_id: int, agent: schemas.AgentUpdate):
        db_agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
        for key, value in agent.dict().items():
            if value is not None:
                setattr(db_agent, key, value)
        db.commit()
        return db_agent

    def delete(db: Session, agent_id: int):
        db_agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
        db_agent.block_date = datetime.now()
        db.commit()
        return db_agent


class Discount:
    def get_list(db: Session, min: Optional[int], max: Optional[int]):
        if min and max:
            return db.query(models.Discount).offset(min).limit(max).all()
        return db.query(models.Discount).all()

    def get_by_id(db: Session, discount_id: int):
        return db.query(models.Discount).filter(models.Discount.id == discount_id).first()

    def create(db: Session, discount: schemas.DiscountCreate):
        db_discount = models.Discount(**discount.dict())
        db.add(db_discount)
        db.commit()
        db.refresh(db_discount)
        return db_discount

    def update(db: Session, discount_id: int, discount: schemas.DiscountUpdate):
        db_discount = db.query(models.Discount).filter(models.Discount.id == discount_id).first()
        for key, value in discount.dict().items():
            if value is not None:
                setattr(db_discount, key, value)
        db.commit()
        return db_discount

    def delete(db: Session, discount_id: int):
        db_discount = db.query(models.Discount).filter(models.Discount.id == discount_id).first()
        db.delete(db_discount)
        db.commit()
        return db_discount
