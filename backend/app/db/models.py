from datetime import datetime

from app.db.session import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

product_list = Table(
    "product_list",
    Base.metadata,
    Column("list_id", Integer, ForeignKey("list.id", ondelete="CASCADE")),
    Column("product_id", Integer, ForeignKey("product.id", ondelete="CASCADE")),
)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True, nullable=False)
    username = Column(String(50), nullable=False)
    hashed_password = Column(String(100), nullable=False)
    is_admin = Column(Boolean, default=False)
    lists = relationship(
        "List", back_populates="user", cascade="all, delete", passive_deletes=True
    )


class List(Base):
    __tablename__ = "list"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default=datetime.utcnow().date().isoformat())
    created_at = Column(DateTime, default=datetime.utcnow())
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="lists")
    products = relationship("Product", secondary=product_list, back_populates="lists")


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="products")
    lists = relationship("List", secondary=product_list, back_populates="products")


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    products = relationship("Product", back_populates="category")
