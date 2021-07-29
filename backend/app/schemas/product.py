from typing import Optional

from pydantic import BaseModel, validator


class ProductBase(BaseModel):
    name: str
    category_id: int

    @validator('name')
    def name_length(cls, value):
        if any([len(value) < 1, len(value) > 255]):
            raise ValueError('Name must be 1 to 255 chars long')
        return value


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str]
    category_id: Optional[int]


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
