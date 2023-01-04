from pydantic import BaseModel
from app.schemas.utils import OrderBy, Search

# Schema


class TaskBase(BaseModel):
    name: str
    completed: bool
    description: int


class TaskCreate(ProcessorBase):
   pass


class Task(ProcessorBase):
    id: int

    class Config:
        orm_mode = True

