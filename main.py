from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from user_auth.routers import router as jwt_router
from users.routers import routers as app_router
from crud_models.routers import routers as crud_router
from pages.routers import routers as logics_router
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
# app.include_router(jwt_router, prefix="/auth")
app.include_router(app_router)
app.include_router(crud_router)
app.include_router(logics_router, prefix="", tags=["pages"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
