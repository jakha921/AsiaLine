from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response 

from jwt.routers import router as jwt_router
from app.routers import routers as app_router
from crud_models.routers import routers as crud_router
from logics.routers import routers as logics_router
from db.database import SessionLocal

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internet server error", status_code=500)
    try: 
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response



# include router
# app.include_router(jwt_router, prefix="/jwt", tags=["jwt"])
# app.include_router(app_router, prefix="", tags=["users"])
app.include_router(crud_router, prefix="", tags=["crud"])
app.include_router(logics_router, prefix="", tags=["main"])

