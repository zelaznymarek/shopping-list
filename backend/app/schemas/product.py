from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    category_id: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode: True
