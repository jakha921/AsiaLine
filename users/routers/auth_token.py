import logging

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from auth.auth_token.auth_handler import sign_jwt
from auth.hashing import decode_password
from users.schemas import auth_token as schemas
from db.database import get_db
from users.views.users import User

routers = APIRouter()


@routers.post("/user/login", tags=["auth_token"])
def user_login(user: schemas.UserLoginSchema, db: Session = Depends(get_db)):
    """ Check user credentials and return a JWT token from the user email and role in db """

    query = User.get_by_email(db, user.email)
    try:
        if query:
            if decode_password(query.password) == user.password:
                return sign_jwt(id=query.id, email=query.email, permissions=User.get_permissions(db, query.id))
    except Exception as e:
        print(logging.error(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
