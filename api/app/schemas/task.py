from pydantic import BaseModel
from app.schemas.utils import OrderBy, Search

# Schema


class TaskBase(BaseModel):
    name: str
    completed: bool
    description: str


class TaskCreate(TaskBase):
   owners: list[int] = []
   event_id: int


class Task(TaskBase):
    id: int
    event_id: int
    

    class Config:
        orm_mode = True

class TaskOrderBy(OrderBy):
    id = "id"

