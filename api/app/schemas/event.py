from pydantic import BaseModel
from app.schemas.utils import OrderBy, Search

# Schema


class EventBase(BaseModel):
    name: str
    date: int
    place: int
    category: int
    description: int


class EventCreate(EventBase):
   participants : list[int] = []


class Event(EventBase):
    id: int
    room_id: int

    class Config:
        orm_mode = True


class EventOrderBy(OrderBy):
    id = "id"