import logging

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from auth.auth_token.auth_bearer import JWTBearer
from auth.auth_token.auth_handler import check_permissions
from db.database import get_db
from users.schemas import users as schemas
from users.views.users import User

routers = APIRouter()


@routers.get("/users", response_model=list[schemas.User], tags=["users"])
async def get_users_list(
        page: Optional[int] = None,
        limit: Optional[int] = None,
        jwt: dict = Depends(JWTBearer()),
        db: Session = Depends(get_db)):
    if not check_permissions('get_users', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return User.get_list(page, limit, db)


@routers.get("/user/{user_id}", tags=["users"])
async def get_user(
        user_id: int,
        jwt: dict = Depends(JWTBearer()),
        db: Session = Depends(get_db)):
    if not check_permissions('get_user', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    try:
        if user := User.get_by_id(db, user_id):
            return schemas.User.from_orm(user)
        raise ValueError("User not found")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.post("/user", tags=["users"])
async def create_user(user: schemas.UserCreate,
                      jwt: dict = Depends(JWTBearer()),
                      db: Session = Depends(get_db)):
    if not check_permissions('create_user', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    try:
        db_user = User.get_by_email(db, user.email)
        if not db_user:
            return schemas.User.from_orm(User.create(db, user))
        raise ValueError("User already exists")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.patch("/user/{user_id}", tags=["users"])
async def update_user(user_id: int,
                      user: schemas.UserUpdate,
                      jwt: dict = Depends(JWTBearer()),
                      db: Session = Depends(get_db)):
    if not check_permissions('update_user', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    try:
        db_user = User.get_by_id(db, user_id)
        if db_user is None:
            raise ValueError("User not found")

        # Check if user exists in db by email
        if db_user.email != user.email:
            if User.get_by_email(db, user.email):
                raise ValueError("User with this email already exists")

        return schemas.User.from_orm(User.update(db, user_id, user))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.delete("/user/{user_id}", tags=["users"])
async def delete_user(user_id: int,
                      jwt: dict = Depends(JWTBearer()),
                      db: Session = Depends(get_db)):
    if not check_permissions('delete_user', jwt):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    try:
        db_user = User.get_by_id(db, user_id)
        if db_user is not None:
            return User.delete(db, user_id)
        raise ValueError("User not found")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
