from pydantic import BaseModel

# Schema

class RoomBase(BaseModel):
    label: str
    invite_link : str
    style :str
    


class RoomCreate(ProcessorBase):
   users : list[int] = []


class Room(ProcessorBase):
    id: int

    class Config:
        orm_mode = True

