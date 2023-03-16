from pydantic import BaseModel
from app.schemas.utils import OrderBy, Search


# Schema

class RecommandationBase(BaseModel):
    label: str
    recommandation_type: str
    subtype : str
    place: str
    price : float
    indispo :str
    url :str
    lat : float
    lon : float


class RecommandationCreate(RecommandationBase):
   pass


class Recommandation(RecommandationBase):
    id: int

    class Config:
        orm_mode = True


class RecommandationOrderBy(OrderBy):
    id = "id"
    label = "name"

