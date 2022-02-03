from typing import List

import pytest
from sqlalchemy.orm import Session

from shopping_list.db.models import Category
from shopping_list.db.models import List as ShoppingList
from shopping_list.db.models import Product
from shopping_list.repository.shopping_list import create, remove


def test_create_returns_created_list(
    db_session: Session, products: List[Product], user
):
    product_ids = [p.id for p in products]
    shopping_list = {"name": "zakupy", "product_ids": product_ids}

    created_shopping_list = create(db_session, shopping_list, user)

    assert len(db_session.query(ShoppingList).all()) == 1
    assert created_shopping_list.name == shopping_list["name"]
    assert len(created_shopping_list.products) == 3
    assert created_shopping_list.user_id == user.id
    assert created_shopping_list.id
    assert created_shopping_list.created_at
    assert created_shopping_list.completed is False


def test_create_throws_exception(db_session, user):
    """Check whether ValueError will be thrown if provided products does not exist"""
    shopping_list = {"name": "zakupy", "product_ids": [1, 2]}

    with pytest.raises(
        ValueError, match="Provided products does not exist in the system"
    ):
        create(db_session, shopping_list, user)


def test_remove_does_not_delete_products_and_categories(
    db_session: Session, shopping_list
):
    remove(db_session, shopping_list)

    assert len(db_session.query(Product).all()) == 3
    assert len(db_session.query(Category).all()) == 2
