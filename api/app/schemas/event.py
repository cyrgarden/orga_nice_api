from typing import Set, Union, List
from pydantic import BaseModel
from app.schemas.utils import OrderBy, Search
from app.schemas.task import Task, TaskCreate

# Schema


class EventBase(BaseModel):
    name: str
    date: int
    place: int
    category: int
    description: int


class EventCreate(EventBase):
   participants : list[int] = []
   room_id : int


class Event(EventBase):
    id: int
    room_id: int
    associated_tasks: Union[List[Task], None] = None

    class Config:
        orm_mode = True


class EventOrderBy(OrderBy):
    id = "id"