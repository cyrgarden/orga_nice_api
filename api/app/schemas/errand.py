from pydantic import BaseModel
from app.schemas.utils import OrderBy

# Schema


class ErrandBase(BaseModel):
    name: str
    completed: bool
    description: int


class ErrandCreate(ErrandBase):
    pass


class Errand(ErrandBase):
    id: int

    class Config:
        orm_mode = True


class ErrandOrderBy(OrderBy):
    id = "id"
