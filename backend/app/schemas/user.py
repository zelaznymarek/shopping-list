from typing import Optional, List

from pydantic import BaseModel

from app.schemas.list import ShoppingList


class UserBase(BaseModel):
    email: str
    username: str
    is_admin: Optional[bool] = False


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    lists: List[ShoppingList] = []

    class Config:
        orm_mode = True
