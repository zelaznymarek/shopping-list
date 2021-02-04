from typing import List

from pydantic import BaseModel

from app.schemas.product import Product


class ShoppingListBase(BaseModel):
    name: str
    user_id: int
    products: List[Product] = []


class ShoppingListCreate(ShoppingListBase):
    pass


class ShoppingList(ShoppingListBase):
    id: int
    created_at: str

    class Config:
        orm_mode = True
