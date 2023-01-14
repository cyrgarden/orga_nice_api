from pydantic import BaseModel
from app.schemas.utils import OrderBy, Search

# Schema


class EventBase(BaseModel):
    name: str
    date: int
    place: int
    category: int
    description: int


class EventCreate(ProcessorBase):
   pass


class Event(ProcessorBase):
    id: int

    class Config:
        orm_mode = True


class ProcessorOrderBy(OrderBy):
    id = "id"