from typing import Set, Union, List
from pydantic import BaseModel
from app.schemas.event import Event
from app.schemas.indisponibility import Indisponibility


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
    all_indisponibitilies : Union [List[Indisponibility], None] = None
    

    class Config:
        orm_mode = True

