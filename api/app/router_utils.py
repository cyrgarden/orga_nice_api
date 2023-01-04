import datetime
import os
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt  # type: ignore
from sqlalchemy import create_engine
import sqlalchemy  # type: ignore
from sqlalchemy.orm import sessionmaker, Session

import app.crud.user as crud_user


# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
