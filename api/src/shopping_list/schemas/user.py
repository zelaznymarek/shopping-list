from typing import List, Optional

from pydantic import BaseModel, EmailStr

from shopping_list.schemas import ShoppingList


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_admin: Optional[bool] = None


class UserCreate(UserBase):
    email: EmailStr
    password: str


class User(UserBase):
    id: int
    lists: List[ShoppingList] = []

    class Config:
        orm_mode = True


class UserDelete(BaseModel):
    email: EmailStr


class UserUpdate(UserBase):
    pass
