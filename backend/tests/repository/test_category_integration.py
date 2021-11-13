from app.db.models import Category, Product
from app.repository.category import create, remove, update
from sqlalchemy.orm import Session


def test_create(db_session: Session):
    category_dict = {"name": "sweets"}

    category = create(db_session, category_dict)

    assert category.id == 1
    assert category.name == category_dict["name"]
    assert category.products == []


def test_remove_by_id(db_session: Session, category_meat: Category):
    remove(db_session, category_meat)

    assert len(db_session.query(Category).all()) == 0


def test_remove_should_not_delete_products(db_session: Session, product: Product):
    remove(db_session, product.category)

    assert len(db_session.query(Product).all()) == 1


def test_update(db_session: Session, category_meat: Category):
    updated_category = {"name": "updated"}

    result = update(
        db_session, db_category=category_meat, category_to_update=updated_category
    )

    from_db = db_session.query(Category).filter(Category.id == category_meat.id).first()

    assert result.id == category_meat.id == from_db.id
    assert result.name == updated_category["name"] == from_db.name
