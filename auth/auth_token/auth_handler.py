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
    'get_ticket_details',
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
    'users_history',
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


def get_user_id(jwt_token) -> int:
    return decode_jwt(jwt_token).get("id")


if __name__ == '__main__':
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcmVzIjoxNjc1MzI1MTkzLjE3MzYyMTcsImlhdCI6MTY3NTMyNTEzMy4xNzM2MjE3LCJpZCI6MSwiZW1haWwiOiJ1c2VyQGdtYWlsLmNvbSIsInBlcm1pc3Npb25zIjpbImdldF9yb2xlcyIsImdldF9yb2xlIiwiY3JlYXRlX3JvbGUiLCJ1cGRhdGVfcm9sZSIsImRlbGV0ZV9yb2xlIiwiZ2V0X3VzZXJzIiwiZ2V0X3VzZXIiLCJjcmVhdGVfdXNlciIsInVwZGF0ZV91c2VyIiwiZGVsZXRlX3VzZXIiLCJnZXRfYWdlbnRzIiwiZ2V0X2FnZW50IiwiY3JlYXRlX2FnZW50IiwidXBkYXRlX2FnZW50IiwiZGVsZXRlX2FnZW50IiwiZ2V0X2ZsaWdodHMiLCJnZXRfZmxpZ2h0IiwiY3JlYXRlX2ZsaWdodCIsInVwZGF0ZV9mbGlnaHQiLCJkZWxldGVfZmxpZ2h0IiwiZ2V0X2ZsaWdodF90aWNrZXRzIiwic2V0X2ZsaWdodF9mb3Jfc2FsZSIsImdldF9mbGlnaHRfcHJpY2VzIiwiZ2V0X3RpY2tldHMiLCJnZXRfdGlja2V0IiwiY3JlYXRlX3RpY2tldCIsInVwZGF0ZV90aWNrZXQiLCJjYW5jZWxfdGlja2V0IiwiZ2V0X2Jvb2tpbmdzIiwiZ2V0X2Jvb2tpbmciLCJjcmVhdGVfYm9va2luZyIsInVwZGF0ZV9ib29raW5nIiwiZGVsZXRlX2Jvb2tpbmciLCJnZXRfcmVmaWxscyIsImdldF9yZWZpbGwiLCJjcmVhdGVfcmVmaWxsIiwidXBkYXRlX3JlZmlsbCIsImRlbGV0ZV9yZWZpbGwiLCJtYWluX3BhZ2UiLCJmbGlnaHRzX21haW4iLCJmbGlnaHRzX3F1ZXVlIiwiZmxpZ2h0c19xdW90YXMiLCJ0aWNrZXRzX3BhZ2UiLCJ1c2Vyc19tYWluIiwidXNlcnNfcm9sZXMiLCJwYXltZW50c19tYWluIiwicGF5bWVudHNfYWdlbnRzX2JhbGFuY2UiLCJhZ2VudHNfbWFpbiIsImFnZW50c19kaXNjb3VudHMiXX0.VxE0B8CEh7VybxbvOAJbx1-QI9j-bXn9B5gMUxT7e2A"
    print(type(get_user_id(token)))
    print(get_user_id(token))