from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging

from db.database import get_db
from users.schemas import role_permissions as schemas
from users.views.role_permissions import RolePermission

routers = APIRouter()


@routers.get("/role_permissions", response_model=list[schemas.RolePermission], tags=["role-permissions"])
async def get_role_permissions_list(
        page: Optional[int] = None,
        limit: Optional[int] = None,
        db: Session = Depends(get_db)):
    try:
        return RolePermission.get_list(page, limit, db)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/role_permission/{role_permission_id}", tags=["role-permissions"])
async def get_role_permission(role_permission_id: int,
                              db: Session = Depends(get_db)):
    try:
        db_role_permission = RolePermission.get_by_id(role_permission_id, db)
        if db_role_permission is None:
            raise ValueError("Role Permission not found")
        return schemas.RolePermission.from_orm(db_role_permission)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.post("/role_permission", response_model=schemas.RolePermission, tags=["role-permissions"])
async def create_role_permission(role_permission: schemas.RolePermissionCreate,
                                 db: Session = Depends(get_db)):
    try:
        return RolePermission.create(role_permission, db)
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.patch("/role_permission/{role_permission_id}", tags=["role-permissions"])
async def update_role_permission(role_permission_id: int,
                                 role_permission: schemas.RolePermissionUpdate,
                                 db: Session = Depends(get_db)):
    try:
        db_role_permission = RolePermission.get_by_id(role_permission_id, db)
        if db_role_permission is None:
            raise ValueError("Role Permission not found")
        return schemas.RolePermission.from_orm(RolePermission.update(db, db_role_permission, role_permission))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.delete("/role_permission/{role_permission_id}", tags=["role-permissions"])
async def delete_role_permission(role_permission_id: int,
                                 db: Session = Depends(get_db)):
    try:
        db_role_permission = RolePermission.get_by_id(role_permission_id, db)
        if db_role_permission is None:
            raise ValueError("Role Permission not found")
        return RolePermission.delete(db, db_role_permission)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
