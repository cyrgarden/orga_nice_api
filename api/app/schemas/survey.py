from typing import List
from pydantic import BaseModel

# Schema


class SurveyBase(BaseModel):
    label: str
    response_type: int
    answers: List[int]


class SurveyCreate(SurveyBase):
    pass


class Survey(SurveyBase):
    id: int

    class Config:
        orm_mode = True
