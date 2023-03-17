from pydantic import BaseModel
from app.schemas.utils import OrderBy, Search
from app.schemas.reco_indispo import RecoIndispo


# Schema

class RecommandationBase(BaseModel):
    label: str
    recommandation_type: str
    subtype : str
    place: str
    price : float
    url :str
    lat : float
    lon : float


class RecommandationCreate(RecommandationBase):
   pass


class Recommandation(RecommandationBase):
    id: int
    all_indispos : Union [List[RecoIndispo], None] = None

    class Config:
        orm_mode = True


class RecommandationOrderBy(OrderBy):
    id = "id"
    label = "name"

