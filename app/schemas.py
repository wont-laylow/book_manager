from pydantic import BaseModel
from typing import Optional

class CreateBook(BaseModel):
    title: str
    author: str
    description : str

class ResponseBook(CreateBook):
    id: int

    class Config:
        from_attributes = True