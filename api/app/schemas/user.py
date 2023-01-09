from typing import List, Union

from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    password: str | None
    admin: bool = False



class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True