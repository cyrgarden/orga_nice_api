from typing import Set, Union, List
from pydantic import BaseModel
from app.schemas.utils import OrderBy
from app.schemas.task import Task

# Schema


class EventBase(BaseModel):
    name: str
    date: str
    place: str
    category: str
    description: str


class EventCreate(EventBase):
    participants: list[int] = []
    room_id: int


class Event(EventBase):
    id: int
    room_id: int
    associated_tasks: Union[List[Task], None] = None

    class Config:
        orm_mode = True


class EventOrderBy(OrderBy):
    id = "id"
