import datetime
from pydantic import BaseModel
from app.schemas.utils import OrderBy


class LogBase(BaseModel):
    user_id: int
    action: str
    timestamp: datetime.datetime


class LogCreate(LogBase):
    pass


class Log(LogBase):
    id: int

    class Config:
        orm_mode = True


class LogsOrderBy(OrderBy):
    user_id = "user_id"
    timestamp = "timestamp"

