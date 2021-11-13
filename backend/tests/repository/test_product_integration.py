from sqlalchemy.orm import Session

from app.db.models import Category, Product
from app.repository.product import create, remove


def test_remove_should_not_delete_category(db_session: Session, product: Product):
    remove(db_session, product)

    assert len(db_session.query(Category).all()) == 1


def test_create_does_not_create_duplicates(
    db_session: Session, category_meat: Category
):
    chicken = {"name": "Chicken", "category": category_meat}
    pork = {"name": "Pork", "category": category_meat}

    create(db_session, chicken)
    create(db_session, pork)

    assert len(db_session.query(Category).all()) == 1
