# This file is responsible for signing , encoding , decoding and returning JWTS
import time
from typing import Dict
from fastapi import HTTPException

import jwt

JWT_SECRET = 'secret'
JWT_ALGORITHM = "HS256"


def token_response(token: str):
    return {
        "access_token": token
    }


# function used for signing the JWT string
def sign_jwt(email: str, user_role: str = None) -> Dict[str, str]:
    payload = {
        "expires": time.time() + 600, # 10 minutes
        "iat": time.time(),
        "email": email,
        "role_id": user_role
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


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




if __name__ == '__main__':
    token = (sign_jwt('joe@xyz.com', 'admin'))
    print(decode_jwt(token.get('access_token')))
    pass