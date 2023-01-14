from typing import List, Union
from pydantic import BaseModel
from app.schemas.room import Room
from app.schemas.event import Event

class UserBase(BaseModel):
    username: str
    password: Union[str, None] = None
    admin: bool = False



class UserCreate(UserBase):
    password: str
    all_rooms : list[int] = []
    all_events : list[int] = []


class User(UserBase):
    id: int

    class Config:
        orm_mode = True