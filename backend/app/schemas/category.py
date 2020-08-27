from typing import List

from pydantic import BaseModel

from app.schemas.product import Product


class CategoryBase(BaseModel):
    name: str
    products: List[Product]


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    class Config:
        orn_mode: True
