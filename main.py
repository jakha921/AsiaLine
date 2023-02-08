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

from users.routers.auth_token import routers as auth_token
from users.routers.roles import routers as roles
from users.routers.users import routers as users
from users.routers.sections import routers as sections
from users.routers.permissions import routers as permissions
from users.routers.role_permissions import routers as role_permissions
from users.routers.agents import routers as agents
from users.routers.discounts import routers as discounts

from pages.routers import routers as logics_router
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
app.include_router(logics_router, prefix="", tags=["pages"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
