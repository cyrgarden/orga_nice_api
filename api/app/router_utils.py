import datetime
import os
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt  # type: ignore
from sqlalchemy import create_engine
import sqlalchemy  # type: ignore
from sqlalchemy.orm import sessionmaker, Session
from app.crud.log import add_log
from app.schemas.log import LogCreate

from app import auth, models  # type: ignore
import app.crud.user as crud_user



POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_SERVER = os.getenv('POSTGRES_SERVER')

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def logger(db: Session, user, action):
    log = LogCreate(user_id=user.id, action=action, timestamp=datetime.datetime.now())
    add_log(db, log)


def error_to_status_code(error: Exception):
    """
    Convert an exception to an HTTP status code.
    """
    if type(
        error
    ) is sqlalchemy.exc.IntegrityError and "a foreign key constraint fails" in str(
        error
    ):
        return HTTPException(status_code=412, detail="Foreign key constraint failed")
    elif type(error) is sqlalchemy.exc.IntegrityError and "Duplicate entry" in str(
        error
    ):
        return HTTPException(status_code=409, detail="Duplicate entry")
    else:
        print(str(error))
        return HTTPException(status_code=500, detail="Unknown internal server error")


async def get_current_user(
    token: str = Depends(auth.oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])  # type: ignore
        username: str = payload.get("sub")  # type: ignore
        if username is None:
            raise credentials_exception
        token_data = auth.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    if token_data is None or token_data.username is None:
        raise credentials_exception
    user = crud_user.get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

