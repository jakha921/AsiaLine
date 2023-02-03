from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging

from db.database import get_db
from users.schemas import permissions as schemas
from users.views.permissions import Permission

routers = APIRouter()


@routers.get("/permissions", tags=["permissions"])
async def get_permissions_list(page: Optional[int] = None,
                               limit: Optional[int] = None,
                               db: Session = Depends(get_db)):
    return Permission.get_list(page, limit, db)


@routers.get("/permission/{permission_id}", tags=["permissions"])
async def get_permission(permission_id: int,
                         db: Session = Depends(get_db)):
    try:
        db_permission = Permission.get_by_id(db, permission_id)
        if db_permission is None:
            raise ValueError("Permission not found")
        return db_permission
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.post("/permission", tags=["permissions"])
async def create_permission(permission: schemas.PermissionCreate,
                            db: Session = Depends(get_db)):
    return schemas.Permission.from_orm(Permission.create(db, permission))


@routers.patch("/permission/{permission_id}", tags=["permissions"])
async def update_permission(permission_id: int,
                            permission: schemas.PermissionUpdate,
                            db: Session = Depends(get_db)):
    try:
        db_permission = Permission.get_by_id(db, permission_id)
        if db_permission is None:
            raise ValueError("Permission not found")
        return schemas.Permission.from_orm(Permission.update(db, permission_id, permission))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.delete("/permission/{permission_id}", tags=["permissions"])
async def delete_permission(permission_id: int,
                            db: Session = Depends(get_db)):
    try:
        db_permission = Permission.get_by_id(db, permission_id)
        if db_permission is None:
            raise ValueError("Permission not found")
        return Permission.delete(db, db_permission)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
