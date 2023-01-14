from typing import Set, Union, List
from pydantic import BaseModel
from app.schemas.event import Event

# Schema

class RoomBase(BaseModel):
    label: str
    invite_link : str
    style :str
    events : List[Event] = []
    


class RoomCreate(RoomBase):
   users : list[int] = []



class Room(RoomBase):
    id: int

    class Config:
        orm_mode = True

