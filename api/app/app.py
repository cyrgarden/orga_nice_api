from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import app.crud.user as crud
import app.models as models
import app.schemas.user as schemas
from app.routers.user import router as user_router

from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)