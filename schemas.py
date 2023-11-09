# models.py
from typing import Optional

from pydantic import BaseModel


class Book(BaseModel):
    id: int
    title: str
    author: str


class User(BaseModel):
    id: int
    username: str
    email: str
