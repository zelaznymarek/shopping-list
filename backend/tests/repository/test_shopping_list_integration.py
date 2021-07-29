from typing import List

import pytest
from sqlalchemy.orm import Session

from app.db.models import List as ShoppingList, Product, Category
from app.repository.shopping_list import create, remove, get_many


def test_create_returns_created_list(db_session: Session, products: List[Product], user):
    product_ids = [p.id for p in products]
    shopping_list = {'name': 'zakupy', 'product_ids': product_ids}

    created_shopping_list = create(db_session, shopping_list, user)

    assert len(db_session.query(ShoppingList).all()) == 1
    assert created_shopping_list.name == shopping_list['name']
    assert len(created_shopping_list.products) == 3
    assert created_shopping_list.user_id == user.id
    assert created_shopping_list.id
    assert created_shopping_list.created_at
    assert created_shopping_list.completed is False


def test_create_throws_exception(db_session, user):
    """Check whether ValueError will be thrown if provided products does not exist"""
    shopping_list = {'name': 'zakupy', 'product_ids': [1, 2]}

    with pytest.raises(ValueError, match='Provided products does not exist in the system'):
        create(db_session, shopping_list, user)


def test_remove_does_not_delete_products_and_categories(db_session: Session, shopping_list):
    remove(db_session, shopping_list)

    assert len(db_session.query(Product).all()) == 3
    assert len(db_session.query(Category).all()) == 2


@pytest.fixture
def sweet_and_meet_products(db_session: Session, category_sweets, category_meat):
    category_meat.order = 1
    category_sweets.order = 2

    products = [
        Product(name='Chocolate', category=category_sweets),
        Product(name='chicken', category=category_meat),
        Product(name='pork', category=category_meat),
        Product(name='Nutella', category=category_sweets),
        Product(name='beef', category=category_meat),
        Product(name='Cake', category=category_sweets),
    ]

    db_session.add_all(products)
    db_session.commit()

    return products


@pytest.fixture
def unordered_shopping_list(db_session: Session, sweet_and_meet_products: List[Product], user):
    shopping_list = ShoppingList(name='new_list', user=user, products=sweet_and_meet_products)

    db_session.add(shopping_list)
    db_session.commit()


@pytest.mark.usefixtures('unordered_shopping_list')
def test_get_many_returns_ordered_list(db_session: Session):
    """Check whether products on the list are grouped by category and sorted by category order"""
    result = get_many(db_session)

    ordered_shopping_list = result[0]
    assert ordered_shopping_list.name == 'new_list'

    categories = [p.category_id for p in ordered_shopping_list.products]
    assert categories == [1, 1, 1, 2, 2, 2]
