from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.db.session import Base


product_list = Table(
    'product_list',
    Base.metadata,
    Column('list_id', Integer, ForeignKey('list.id')),
    Column('product_id', Integer, ForeignKey('product.id'))
)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(50), nullable=False)
    hashed_password = Column(String(100), nullable=False)
    is_admin = Column(Boolean, default=False)
    lists = relationship('list', back_populates='user', cascade='all, delete', passive_deletes=True)


class List(Base):
    __tablename__ = 'list'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default=datetime.utcnow().date().isoformat())
    created_at = Column(Date, default=datetime.utcnow())
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user = relationship('user', back_populates='list')
    products = relationship('product', secondary=product_list)


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('category', back_populates='product')


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    products = relationship('product', back_populates='category')
