import datetime
import os
from fastapi import Depends, HTTPException, status
from sqlalchemy import create_engine
import sqlalchemy  # type: ignore
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from app import models

import app.crud.user as crud_user


POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_SERVER = os.getenv('POSTGRES_SERVER')

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Dependency

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    )
models.Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
