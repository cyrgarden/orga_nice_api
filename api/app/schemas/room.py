from typing import Set, Union, List
from pydantic import BaseModel
from app.schemas.event import Event

# Schema

class RoomBase(BaseModel):
    label: str
    invite_link : str
    style :str
    
    


class RoomCreate(RoomBase):
   users : list[int] = []


class Room(RoomBase):
    id: int
    events: Union[List[Event], None] = None
    

    class Config:
        orm_mode = True

