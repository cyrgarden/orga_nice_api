from enum import Enum
from pydantic import BaseModel


class OrderBy(str, Enum):
    pass


class Search(BaseModel):
    pass

