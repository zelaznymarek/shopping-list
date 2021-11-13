from datetime import datetime
from typing import List

from app.schemas.product import Product
from pydantic import BaseModel


class ShoppingListBase(BaseModel):
    name: str


class ShoppingListCreate(ShoppingListBase):
    product_ids: List[int]


class ShoppingList(ShoppingListBase):
    id: int
    created_at: datetime
    products: List[Product]
    user_id: int

    class Config:
        orm_mode = True
