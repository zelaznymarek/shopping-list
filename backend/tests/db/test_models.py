from datetime import datetime
from typing import List

import pytest
from sqlalchemy.orm import Session

from app.db.models import User, List as ShoppingList, Product, Category


@pytest.fixture
def example_user():
    return User(
        email='example@email.com',
        name='Example',
        hashed_password='secret'
    )


@pytest.fixture
def example_list():
    return ShoppingList(name='example_list')


@pytest.fixture
def example_product():
    return Product(name='chocolate')


@pytest.fixture
def example_category():
    return Category(name='meat')

# Test models


def test_user(db_session: Session, example_user: User):
    results = db_session.query(User).all()
    assert len(results) == 0

    db_session.add(example_user)
    db_session.commit()

    results = db_session.query(User).all()
    assert len(results) == 1

    user: User = results[0]

    assert user.name == example_user.name
    assert user.email == example_user.email
    assert user.is_admin is False
    assert user.lists == []


def test_list(db_session: Session):
    results = db_session.query(ShoppingList).all()
    assert len(results) == 0

    db_session.add(ShoppingList())
    db_session.commit()

    results = db_session.query(ShoppingList).all()
    assert len(results) == 1

    shopping_list: ShoppingList = results[0]

    assert shopping_list.name == datetime.utcnow().date().isoformat()
    assert type(shopping_list.created_at).__name__ == 'datetime'
    assert shopping_list.completed is False
    assert shopping_list.user_id is None
    assert shopping_list.products == []


def test_product(db_session: Session, example_product: Product):
    results = db_session.query(Product).all()
    assert len(results) == 0

    db_session.add(example_product)
    db_session.commit()

    results = db_session.query(Product).all()
    assert len(results) == 1

    product: Product = results[0]

    assert product.name == example_product.name
    assert product.category_id is None
    assert product.category is None


def test_category(db_session: Session, example_category: Category):
    results = db_session.query(Category).all()
    assert len(results) == 0

    db_session.add(example_category)
    db_session.commit()

    results = db_session.query(Category).all()
    assert len(results) == 1

    category: Category = results[0]

    assert category.name == example_category.name
    assert category.products == []


# Test relations

def test_user_list_relation(db_session: Session, example_user: User, example_list: ShoppingList):
    """
    Check whether user is added to db when list with assigned user is added.
    Also check whether relations are kept in both objects.
    """
    example_list.user = example_user

    db_session.add(example_list)
    db_session.commit()

    result = db_session.query(User).all()
    user: User = result[0]

    assert user.lists == [example_list]
    assert user.lists[0].user_id == user.id


def test_user_list_cascade_delete(db_session: Session, example_user: User, example_list: ShoppingList):
    """Check whether removing user also removes his lists."""
    example_list.user = example_user

    db_session.add(example_list)
    db_session.commit()

    users = db_session.query(User).all()
    lists = db_session.query(ShoppingList).all()

    assert len(users) == 1
    assert len(lists) == 1

    db_session.delete(example_user)
    db_session.commit()

    users = db_session.query(User).all()
    lists = db_session.query(ShoppingList).all()

    assert len(users) == 0
    assert len(lists) == 0


def test_list_user_cascade_delete(db_session: Session, example_user: User, example_list: ShoppingList):
    """Check whether deleting list doesn't delete its owner"""
    example_list.user = example_user

    db_session.add(example_list)
    db_session.commit()

    users = db_session.query(User).all()
    lists = db_session.query(ShoppingList).all()

    assert len(users) == 1
    assert len(lists) == 1

    db_session.delete(example_list)
    db_session.commit()

    users = db_session.query(User).all()
    lists = db_session.query(ShoppingList).all()

    assert len(users) == 1
    assert len(lists) == 0


@pytest.fixture
def example_products():
    return [
        Product(name='bread'),
        Product(name='milk'),
        Product(name='eggs'),
    ]


def test_list_products_relation(db_session: Session, example_list: ShoppingList, example_products: List[Product]):
    """Check whether products are being added to the list"""
    example_list.products = example_products

    db_session.add(example_list)
    db_session.commit()

    lists = db_session.query(ShoppingList).all()
    products = db_session.query(Product).all()

    assert len(lists) == 1
    assert len(products) == 3

    shopping_list = lists[0]

    assert shopping_list.products == example_products


def test_list_delete(db_session: Session, example_list: ShoppingList, example_products: List[Product]):
    """Check whether list deletion doesn't remove products"""
    example_list.products = example_products

    db_session.add(example_list)
    db_session.commit()

    db_session.delete(example_list)
    db_session.commit()

    lists = db_session.query(ShoppingList).all()
    products = db_session.query(Product).all()

    assert len(lists) == 0
    assert len(products) == 3


def test_user_delete_keeps_products(
      db_session: Session,
      example_user: User,
      example_list: ShoppingList,
      example_products: List[Product]
):
    """Check whether user deletion doesn't remove products from his list"""
    example_list.user = example_user
    example_list.products = example_products

    db_session.add(example_list)
    db_session.commit()

    db_session.delete(example_user)
    db_session.commit()

    user = db_session.query(User).all()
    lists = db_session.query(ShoppingList).all()
    products = db_session.query(Product).all()

    assert len(user) == 0
    assert len(lists) == 0
    assert len(products) == 3
