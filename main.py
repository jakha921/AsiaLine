import asyncio

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from fastapi.middleware.cors import CORSMiddleware

from crud_models.routers.countries import routers as countries
from crud_models.routers.cities import routers as cities
from crud_models.routers.airports import routers as airports
from crud_models.routers.company import routers as company
from crud_models.routers.flight_guide import routers as flight_guide
from crud_models.routers.flights import routers as flights
from crud_models.routers.tickets import routers as tickets
from crud_models.routers.booking import routers as booking
from crud_models.routers.scraped_price import routers as scraped_price
from crud_models.routers.genders import routers as genders
from crud_models.routers.refills import routers as refills
from crud_models.routers.ticket_classes import routers as ticket_classes
# from db.db_redis import redis_client

from users.routers.auth_token import routers as auth_token
from users.routers.roles import routers as roles
from users.routers.users import routers as users
from users.routers.sections import routers as sections
from users.routers.permissions import routers as permissions
from users.routers.role_permissions import routers as role_permissions
from users.routers.agents import routers as agents
from users.routers.discounts import routers as discounts

from pages.routers.currency import routers as currency
from pages.routers.main import routers as main_page
from pages.routers.flights import routers as flights_page
from pages.routers.tickets import routers as tickets_page
from pages.routers.users import routers as users_page
from pages.routers.payments import routers as payments_page
from pages.routers.agents import routers as agents_page
from pages.routers.guides import routers as guides_page


from db.database import SessionLocal

app = FastAPI()

origins = ["*"]
#     "http://asialine.ru",
#     "https://apitest.asialine.ru",
#     "http://localhost",
#     "http://localhost:8080",
#     "http://localhost:3000",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internet server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# @app.post("/set_key_value")
# async def set_key_value(key: str, value: str):
#     # Set the key-value pair in Redis with an expiry time of 5 minutes
#     redis_client.set(key, value, ex=5)
#
#     return {"message": "Key-value pair set successfully"}
#
#
# @app.get("/get_value")
# async def get_value(key: str):
#     # Get the value for the given key from Redis
#     value = redis_client.get(key)
#
#     if value is not None:
#         return {"value": value.decode()}
#     else:
#         return {"message": "Key not found"}

# users
app.include_router(auth_token)
app.include_router(roles)
app.include_router(users)
app.include_router(sections)
app.include_router(permissions)
app.include_router(role_permissions)
app.include_router(discounts)
app.include_router(agents)

# CRUDs
app.include_router(countries)
app.include_router(cities)
app.include_router(airports)
app.include_router(company)
app.include_router(flight_guide)
app.include_router(flights)
app.include_router(tickets)
app.include_router(booking)
app.include_router(scraped_price)
app.include_router(genders)
app.include_router(refills)
app.include_router(ticket_classes)

# pages
app.include_router(currency)
app.include_router(main_page, tags=["pages"])
app.include_router(flights_page, tags=["pages"])
app.include_router(tickets_page, tags=["pages"])
app.include_router(users_page, tags=["pages"])
app.include_router(payments_page, tags=["pages"])
app.include_router(agents_page, tags=["pages"])
app.include_router(guides_page, tags=["pages"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
