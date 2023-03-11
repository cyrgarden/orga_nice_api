from typing import Set, Union, List
from pydantic import BaseModel
from app.schemas.utils import OrderBy, Search
from app.schemas.task import Task, TaskCreate

# Schema


class IndisponibilityBase(BaseModel):
    date : str


class IndisponibilityCreate(IndisponibilityBase):
   user_id : int
   room_id : int


class Indisponibility(IndisponibilityBase):
    id: int
    user_id : int
    room_id : int

    class Config:
        orm_mode = True


class IndisponibilityOrderBy(OrderBy):
    id = "id"