from typing import Optional, List

from sqlalchemy.orm.session import Session

from app.db import models


def get_by_id(db_session: Session, category_id: int) -> Optional[models.Category]:
    return db_session.query(models.Category).filter(models.Category.id == category_id).first()


def get_by_name(db_session: Session, category_name) -> Optional[models.Category]:
    return db_session.query(models.Category).filter(models.Category.name == category_name).first()


def get_list(db_session: Session) -> List[Optional[models.Category]]:
    return db_session.query(models.Category).all()


def create(db_session: Session, category_dict: dict) -> models.Category:
    category = models.Category(**category_dict)

    db_session.add(category)
    db_session.commit()

    return category


def remove(db_session: Session, category: models.Category):
    db_session.delete(category)
    db_session.commit()


def update(db_session: Session, *, db_category: models.Category, category_to_update: dict) -> models.Category:
    for field, value in category_to_update.items():
        setattr(db_category, field, value)

    db_session.add(db_category)
    db_session.commit()

    return db_category
