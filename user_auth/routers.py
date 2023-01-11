from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from user_auth.hashing import decode_password
from user_auth.schemas import UserSchema, UserLoginSchema

from user_auth.auth.auth_handler import sign_jwt, decode_jwt
from user_auth.auth.auth_bearer import JWTBearer
from users.crud import User
from db.database import get_db

router = APIRouter()
users = []


# def check_user(data: UserLoginSchema):
#     for user in users:
#         if user.email == data.email and user.password == data.password:
#             return True
#     return False
#
#
# @router.post("/user/signup", tags=["user"])
# def create_user(user: UserSchema):
#     users.append(user)  # replace with db call, making sure to hash the password first
#     print(users)
#     return sign_jwt(user.email, user.role_id)
#
#
# @router.post("/user/login", tags=["auth"])
# def user_login(user: UserLoginSchema = Body(...)):
#     if check_user(user):
#         for u in users:
#             if u.email == user.email:
#                 foo = decode_jwt(sign_jwt(u.email, u.role_id))
#                 foo.get("role")
#                 return sign_jwt(u.email, u.role_id)
#     return {
#         "error": "Wrong login details!"
#     }

@router.post("/user/login", tags=["auth"])
def user_login(user: UserLoginSchema = Body(...), db: Session = Depends(get_db)):
    """ Check user credentials and return a JWT token from the user email and role in db """
    query = User.get_by_email(db, user.email)
    if query:
        if decode_password(query.password) == user.password:
            return sign_jwt(query.email, query.role_id)
    return {
        "error": "Wrong login details!"
    }


# hello world msg
@router.get("/hello", tags=["root"], dependencies=[Depends(JWTBearer())])
def read_root():
    return {"msg": "Hello World"}


# example of a protected route
@router.get("/protected", tags=["root"])
def protected(JWT: dict = Depends(JWTBearer())):
    token = decode_jwt(JWT)
    print(token)
    return {"msg": "This is a protected route"}


# example of a protected route with role based access control (RBAC) [admin only]  [admin can access this route]
@router.get("/protected/admin", tags=["root"])
def protected_admin(JWT: dict = Depends(JWTBearer())):
    token = decode_jwt(JWT)
    print(token)
    print(type(token))
    print(token.get("role"))
    if token.get("role") == "admin":
        return {"msg": "This is a protected route for admin only"}
    return {"msg": "You are not an admin"}
