from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    products = relationship('Product', backref='category')


class List(Base):
    __tablename__ = 'lists'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow())


class ProductList(Base):
    __tablename__ = 'product_list'

    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    list_id = Column(Integer, ForeignKey('list.id'), primary_key=True)
