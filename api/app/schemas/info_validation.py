from pydantic import BaseModel
from app.schemas.utils import OrderBy


class InfoValidationBase(BaseModel):
    user_id: int
    validation_field: str
    validation_code: str
    timestamp: str


class InfoValidationCreate(InfoValidationBase):
    pass


class InfoValidation(InfoValidationBase):
    id: int

    class Config:
        orm_mode = True


class InfoValidationOrderBy(OrderBy):
    id = "id"
    user_id = "user_id"
