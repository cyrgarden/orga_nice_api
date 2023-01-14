from pydantic import BaseModel
from app.schemas.utils import OrderBy, Search

# Schema


class ErrandBase(BaseModel):
    name: str
    completed: bool
    description: int


class ErrandCreate(ProcessorBase):
   pass


class Errand(ProcessorBase):
    id: int

    class Config:
        orm_mode = True

