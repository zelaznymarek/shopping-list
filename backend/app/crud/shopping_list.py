from typing import Optional, List

from sqlalchemy.orm.session import Session

from app.db import models


def get_by_id(db_session: Session, shopping_list_id: int) -> Optional[models.List]:
    return db_session.query(models.List).filter(models.List.id == shopping_list_id).first()


def get_by_name(db_session: Session, shopping_list_name) -> Optional[models.List]:
    return db_session.query(models.List).filter(models.List.name == shopping_list_name).first()


def get_many(db_session: Session) -> List[models.List]:
    return db_session.query(models.List).all()


def create(db_session: Session, shopping_list_dict: dict) -> models.List:
    shopping_list = models.List(**shopping_list_dict)

    db_session.add(shopping_list)
    db_session.commit()

    return shopping_list


def remove(db_session: Session, shopping_list: models.List):
    db_session.delete(shopping_list)
    db_session.commit()
