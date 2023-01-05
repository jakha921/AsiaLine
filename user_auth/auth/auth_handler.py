# This file is responsible for signing , encoding , decoding and returning JWTS
import time
from typing import Dict

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
        "expires": time.time() + 600,
        "iat": time.time(),
        "email": email,
        "role": user_role
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET)
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}


if __name__ == '__main__':
    # print(sign_jwt('joe@xyz.com', 'admin'))
    pass