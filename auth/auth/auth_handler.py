# create jwt token, decode jwt token and user permission checker
import time
from fastapi import HTTPException

import jwt

import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv('jwt_secret')
JWT_ALGORITHM = os.getenv('jwt_algorithm')

permission = [
    'get_roles',
    'get_countries',
    'get_country',
    'create_country',
    'update_country',
    # 'delete_country',
]


def sign_jwt(id: int, email: str, permissions: list = None):
    if email == 'user@gmail.com':
        permissions = permission
    payload = {
        "expires": time.time() + 60,  # 10 minutes
        "iat": time.time(),
        "id": id,
        "email": email,
        "permissions": permissions
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"access_token": token}


def decode_jwt(access_token: str) -> dict:
    try:
        payload = jwt.decode(access_token, JWT_SECRET, algorithms=JWT_ALGORITHM)
    except jwt.exceptions.InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=400, detail="Invalid token")

    return payload


def check_permissions(allowed_permissions: str, jwt_token: dict) -> bool:
    if allowed_permissions in (decode_jwt(jwt_token).get("permissions")):
        return True
    return False
