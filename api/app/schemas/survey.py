from pydantic import BaseModel
from app.schemas.utils import OrderBy, Search

# Schema

class SurveyBase(BaseModel):
    label: str
    response_type: int
    answers: List[int]


class SurveyCreate(ProcessorBase):
   pass


class Survey(ProcessorBase):
    id: int

    class Config:
        orm_mode = True

