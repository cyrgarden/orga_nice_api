from typing import List, Union
from pydantic import BaseModel
from app.schemas.room import Room
from app.schemas.event import Event
from app.schemas.task import Task

class UserBase(BaseModel):
    username: str
    password: Union[str, None] = None
    admin: bool = False



class UserCreate(UserBase):
    password: str
    all_rooms : list[int] = []
    all_events : list[int] = []
    all_tasks : list[int] = []
    

class User(UserBase):
    id: int
    all_rooms: Union[List[Room], None] = None
    all_events: Union[List[Event], None] = None
    all_tasks: Union[List[Task], None] = None


    class Config:
        orm_mode = True
        
        

