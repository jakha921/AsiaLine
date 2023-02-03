from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from auth.auth_token.auth_bearer import JWTBearer
from auth.auth_token.auth_handler import check_permissions
from db.database import get_db
from users.schemas import roles as schemas
from users.views.roles import Role

routers = APIRouter()


@routers.get("/roles", response_model=list[schemas.Role], tags=["roles"])
async def get_all_roles(
        page: Optional[int] = None,
        limit: Optional[int] = None,
        jwt: dict = Depends(JWTBearer()),
        db: Session = Depends(get_db)):
    """ Get list of roles """
    if not check_permissions('get_roles', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return Role.get_list(page, limit, db)


@routers.get("/role/{role_id}", response_model=schemas.Role, tags=["roles"])
async def get_role(role_id: int,
                   jwt: dict = Depends(JWTBearer()),
                   db: Session = Depends(get_db)):
    """ get role by given id """
    if not check_permissions('get_role', jwt):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Access denied")

    db_role = Role.get_by_id(db, role_id)
    if db_role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return db_role


@routers.post("/role", response_model=schemas.Role, tags=["roles"])
async def create_role(role: schemas.RoleCreate,
                      jwt: dict = Depends(JWTBearer()),
                      db: Session = Depends(get_db)):
    if not check_permissions('create_role', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return Role.create(db, role)


@routers.patch("/role/{role_id}", response_model=schemas.Role, tags=["roles"])
async def update_role(role_id: int,
                      role: schemas.RoleUpdate,
                      jwt: dict = Depends(JWTBearer()),
                      db: Session = Depends(get_db)):
    if not check_permissions('update_role', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    db_role = Role.get_by_id(db, role_id)
    if db_role is not None:
        return Role.update(db, role_id, role)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")


@routers.delete("/role/{role_id}", response_model=schemas.Role, tags=["roles"])
async def delete_role(role_id: int,
                      jwt: dict = Depends(JWTBearer()),
                      db: Session = Depends(get_db)):
    if not check_permissions('delete_role', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    db_role = Role.get_by_id(db, role_id)
    if db_role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return Role.delete(db, role_id)
