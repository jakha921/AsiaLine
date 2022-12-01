from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional


from app import crud, schemas
from db.database import get_db

routers = APIRouter()


# * Roles
@routers.get("/roles", response_model=list[schemas.Role])
async def get_roles(min: Optional[int] = 0, max: Optional[int] = 10, db: Session = Depends(get_db)):
    return crud.Role.get_list(db, min, max)

@routers.get("/role/{role_id}", response_model=schemas.Role)
async def get_role(role_id: int, db: Session = Depends(get_db)):
    db_role = crud.Role.get_by_id(db, role_id)
    if db_role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return db_role

@routers.post("/role", response_model=schemas.Role)
async def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    return crud.Role.create(db, role)

@routers.patch("/role", response_model=schemas.Role)
async def update_role(role: schemas.RoleUpdate, db: Session = Depends(get_db)):
    db_role = crud.Role.get_by_name(db, role.name)
    if db_role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return crud.Role.update(db, db_role.id, role)

@routers.delete("/role/{role_id}", response_model=schemas.Role)
async def delete_role(role_id: int, db: Session = Depends(get_db)):
    db_role = crud.Role.get_by_id(db, role_id)
    if db_role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return crud.Role.delete(db, role_id)


# * User
@routers.get("/users", response_model=list[schemas.User])
async def get_users_list(min: Optional[int] = 0, max: Optional[int] = 10, db: Session = Depends(get_db)):
    return crud.User.get_list(db, min, max)

@routers.get("/user/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.User.get_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@routers.post("/user", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.User.get_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.User.create(db, user)

@routers.patch("/user/", response_model=schemas.User)
async def update_user(user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.User.get_by_email(db, user.email)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return crud.User.update(db, user)

@routers.delete("/user/{user_id}", response_model=schemas.User)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.User.get_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return crud.User.delete(db, user_id)



