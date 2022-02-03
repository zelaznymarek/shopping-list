from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str]
    category_id: Optional[int]


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
