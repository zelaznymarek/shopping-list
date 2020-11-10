import pytest

from sqlalchemy.orm import Session

from app.crud.category import create, remove, update
from app.db.models import Category


def test_create(db_session: Session):
    category_dict = {
        'name': 'sweets'
    }

    category = create(db_session, category_dict)

    assert category.id == 1
    assert category.name == category_dict['name']
    assert category.products == []


@pytest.fixture
def example_category(db_session: Session):
    category = Category(name='example')

    db_session.add(category)
    db_session.commit()

    return category


def test_remove_by_id(db_session: Session, example_category: Category):
    remove(db_session, example_category)

    assert len(db_session.query(Category).all()) == 0


def test_update(db_session: Session, example_category: Category):
    updated_category = {'name': 'updated'}

    result = update(db_session, db_category=example_category, category_to_update=updated_category)

    from_db = db_session.query(Category).filter(Category.id == example_category.id).first()

    assert result.id == example_category.id == from_db.id
    assert result.name == updated_category['name'] == from_db.name
