from typing import Set, Union, List
from pydantic import BaseModel
from app.schemas.utils import OrderBy, Search
from app.schemas.task import Task, TaskCreate

# Schema


class RecoIndispoBase(BaseModel):
    date : str


class RecoIndispoCreate(RecoIndispoBase):
   reco_id : int


class RecoIndispo(RecoIndispoBase):
    id: int
    reco_id : int
   
    class Config:
        orm_mode = True


class RecoIndispoOrderBy(OrderBy):
    id = "id"