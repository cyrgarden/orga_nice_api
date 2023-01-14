from pydantic import BaseModel

# Schema

class RoomBase(BaseModel):
    label: str
    invite_link : str
    style :str
    


class RoomCreate(RoomBase):
   users : list[int] = []


class Room(RoomBase):
    id: int

    class Config:
        orm_mode = True

