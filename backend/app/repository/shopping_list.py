from typing import List, Optional

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from backend.app.db import models
from backend.app.repository.product import get_by_id as get_product_by_id


def get_by_id(db_session: Session, shopping_list_id: int) -> Optional[models.List]:
    return (
        db_session.query(models.List).filter(models.List.id == shopping_list_id).one()
    )


def get_by_name(db_session: Session, shopping_list_name) -> Optional[models.List]:
    return (
        db_session.query(models.List)
        .filter(models.List.name == shopping_list_name)
        .one()
    )


def get_many(db_session: Session) -> List[models.List]:
    return db_session.query(models.List).all()


def create(
    db_session: Session, shopping_list_dict: dict, owner: models.User
) -> models.List:
    try:
        products = [
            get_product_by_id(db_session, product_id)
            for product_id in shopping_list_dict["product_ids"]
        ]
        del shopping_list_dict["product_ids"]
    except NoResultFound:
        raise ValueError("Provided products does not exist in the system")

    shopping_list = models.List(
        **shopping_list_dict, user_id=owner.id, products=products
    )

    db_session.add(shopping_list)
    db_session.commit()

    return shopping_list


def remove(db_session: Session, shopping_list: models.List):
    db_session.delete(shopping_list)
    db_session.commit()
