from typing import Set, Union, List
from pydantic import BaseModel
from app.schemas.utils import OrderBy, Search

# Schema

class PendingPasswordBase(BaseModel):
    user_id :int 
    new_password: str


class PendingPasswordCreate(PendingPasswordBase):
   pass


class PendingPassword(PendingPasswordBase):
    id: int

    class Config:
        orm_mode = True

