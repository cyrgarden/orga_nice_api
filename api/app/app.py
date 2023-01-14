from datetime import timedelta
import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session  # type: ignore
from app import auth
from app.crud.user import new_user
from app.routers.user import router as user_router
from app.routers.log import router as log_router
from app.routers.room import router as room_router

from app.router_utils import *

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_SERVER = os.getenv('POSTGRES_SERVER')

app = FastAPI()


def hw_info_api_schema():
    openapi_schema = get_openapi(
        title="Hardware Info API",
        version="0.1",
        description="Find hardware components information and compatibility",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = hw_info_api_schema  # type: ignore


@app.on_event("startup")
def startup_event():
    print("Verifying user creation")
    print(os.getenv("API_PASSWORD"))
    try:
        db = SessionLocal()
        new_user(
            db,
           "fastapi",
            auth.get_password_hash("fastapi"),
            True,
        )
        db.close()
    except:
        pass


# Auth


@app.post("/token", response_model=auth.Token, tags=["Auth"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

app.include_router(user_router)
app.include_router(log_router)
app.include_router(room_router)
