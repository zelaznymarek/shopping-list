from typing import List
from datetime import datetime

from pydantic import BaseModel

from app.schemas.product import Product


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
