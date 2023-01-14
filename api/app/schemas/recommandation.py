from pydantic import BaseModel
from app.schemas.utils import OrderBy, Search

# Schema

class RecommandationBase(BaseModel):
    label: str
    recommandation_type: str
    place: str
    price : float
    availabilites :str
    url :str


class RecommandationCreate(ProcessorBase):
   pass


class Recommandation(ProcessorBase):
    id: int

    class Config:
        orm_mode = True


class RecommandationOrderBy(OrderBy):
    id = "id"
    label = "name"

