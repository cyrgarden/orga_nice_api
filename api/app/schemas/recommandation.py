from pydantic import BaseModel
from app.schemas.utils import OrderBy, Search
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
import app.crud.room as crud_room
import app.models as models
from app.schemas.room import Room, RoomCreate
from app.schemas.user import User, UserCreate
from app.router_utils import get_db, get_current_user, logger, error_to_status_code


# Schema

class RecommandationBase(BaseModel):
    label: str
    recommandation_type: str
    place: str
    price : float
    availabilites :str
    url :str


class RecommandationCreate(RecommandationBase):
   pass


class Recommandation(RecommandationBase):
    id: int

    class Config:
        orm_mode = True


class RecommandationOrderBy(OrderBy):
    id = "id"
    label = "name"

