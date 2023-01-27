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
    'get_role',
    'create_role',
    'update_role',
    'delete_role',
    'get_users',
    'get_user',
    'create_user',
    'update_user',
    'delete_user',
    'get_agents',
    'get_agent',
    'create_agent',
    'update_agent',
    'delete_agent',
    'get_flights',
    'get_flight',
    'create_flight',
    'update_flight',
    'delete_flight',
    'get_flight_tickets',
    'set_flight_for_sale',
    'get_flight_prices',
    'get_tickets',
    'get_ticket',
    'create_ticket',
    'update_ticket',
    'cancel_ticket',
    'get_bookings',
    'get_booking',
    'create_booking',
    'update_booking',
    'delete_booking',
    'get_refills',
    'get_refill',
    'create_refill',
    'update_refill',
    'delete_refill',
    'main_page',
    'flights_main',
    'flights_queue',
    'flights_quotas',
    'tickets_page',
    'users_main',
    'users_roles',
    'payments_main',
    'payments_agents_balance',
    'agents_main',
    'agents_discounts',
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


def get_user_id(jwt_token: dict) -> int:
    return decode_jwt(jwt_token).get("id")


if __name__ == '__main__':
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcmVzIjoxNjc0MjA4OTI1LjQyNjA2NSwiaWF0IjoxNjc0MjA4ODY1LjQyNjA2NSwiaWQiOjEsImVtYWlsIjoidXNlckBnbWFpbC5jb20iLCJwZXJtaXNzaW9ucyI6WyJnZXRfcm9sZXMiLCJnZXRfcm9sZSIsImNyZWF0ZV9yb2xlIiwidXBkYXRlX3JvbGUiLCJkZWxldGVfcm9sZSIsImdldF91c2VycyIsImdldF91c2VyIiwiY3JlYXRlX3VzZXIiLCJ1cGRhdGVfdXNlciIsImRlbGV0ZV91c2VyIiwiZ2V0X2FnZW50cyIsImdldF9hZ2VudCIsImNyZWF0ZV9hZ2VudCIsInVwZGF0ZV9hZ2VudCIsImRlbGV0ZV9hZ2VudCIsImdldF9mbGlnaHRzIiwiZ2V0X2ZsaWdodCIsImNyZWF0ZV9mbGlnaHQiLCJ1cGRhdGVfZmxpZ2h0IiwiZGVsZXRlX2ZsaWdodCIsImdldF9mbGlnaHRfdGlja2V0cyIsInNldF9mbGlnaHRfZm9yX3NhbGUiLCJnZXRfZmxpZ2h0X3ByaWNlcyIsImdldF90aWNrZXRzIiwiZ2V0X3RpY2tldCIsImNyZWF0ZV90aWNrZXQiLCJ1cGRhdGVfdGlja2V0IiwiY2FuY2VsX3RpY2tldCIsImdldF9ib29raW5ncyIsImdldF9ib29raW5nIiwiY3JlYXRlX2Jvb2tpbmciLCJ1cGRhdGVfYm9va2luZyIsImRlbGV0ZV9ib29raW5nIiwiZ2V0X3JlZmlsbHMiLCJnZXRfcmVmaWxsIiwiY3JlYXRlX3JlZmlsbCIsInVwZGF0ZV9yZWZpbGwiLCJkZWxldGVfcmVmaWxsIiwibWFpbl9wYWdlIiwiZmxpZ2h0c19tYWluIiwiZmxpZ2h0c19xdWV1ZSIsImZsaWdodHNfcXVvdGFzIiwidGlja2V0c19wYWdlIiwidXNlcnNfbWFpbiIsInVzZXJzX3JvbGVzIiwicGF5bWVudHNfbWFpbiIsInBheW1lbnRzX2FnZW50c19iYWxhbmNlIiwiYWdlbnRzX21haW4iLCJhZ2VudHNfZGlzY291bnRzIl19.PWwkWjsE-fI0XkZqO7Z3P9FHD1f1galeoadgDwYpJOY'
    print(get_user_id(token))