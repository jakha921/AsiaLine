from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging

from auth.auth_token.auth_bearer import JWTBearer
from auth.auth_token.auth_handler import check_permissions
from db.database import get_db
from pages.views import users

routers = APIRouter()


@routers.get("/users/main")
async def get_users(db: Session = Depends(get_db),
                    searching_text: Optional[str] = None,
                    page: Optional[int] = None,
                    limit: Optional[int] = None,
                    # jwt: dict = Depends(JWTBearer())
                    ):
    """ get all users with then roles """
    # if not check_permissions('users_main', jwt):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        db_users, counter = users.get_all_users_with_role(db, page, limit, searching_text)

        return {
            'users_count': counter,
            'users': db_users
        }
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@routers.get("/users/roles")
async def get_roles(db: Session = Depends(get_db),
                    searching_text: Optional[str] = None,
                    page: Optional[int] = None,
                    limit: Optional[int] = None,
                    # jwt: dict = Depends(JWTBearer())
                    ):
    """ get all roles that can be assigned to users """
    # if not check_permissions('users_roles', jwt):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        db_roles, counter = users.get_all_roles(db, page=page, limit=limit, search_text=searching_text)
        return {
            'roles_count': counter,
            'roles': db_roles
        }
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
