from typing import Optional, List

from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound

from app.db import models
from app.repository.product import get_by_id as get_product_by_id


def order_by_category(shopping_list: models.List) -> models.List:
    """Sorts products from the list by their category"""
    shopping_list.products = sorted(shopping_list.products, key=lambda x: x.category_id)

    return shopping_list


def get_by_id(db_session: Session, shopping_list_id: int) -> Optional[models.List]:
    return db_session.query(models.List).filter(models.List.id == shopping_list_id).one()


def get_by_name(db_session: Session, shopping_list_name) -> Optional[models.List]:
    return db_session.query(models.List).filter(models.List.name == shopping_list_name).one()


def get_many(db_session: Session) -> List[models.List]:
    shopping_lists = db_session.query(models.List).all()

    return [order_by_category(sl) for sl in shopping_lists]


def create(db_session: Session, shopping_list_dict: dict, owner: models.User) -> models.List:
    try:
        products = [get_product_by_id(db_session, product_id) for product_id in shopping_list_dict['product_ids']]
        del shopping_list_dict['product_ids']
    except NoResultFound:
        raise ValueError('Provided products does not exist in the system')

    shopping_list = models.List(**shopping_list_dict, user_id=owner.id, products=products)

    db_session.add(shopping_list)
    db_session.commit()

    return shopping_list


def remove(db_session: Session, shopping_list: models.List):
    db_session.delete(shopping_list)
    db_session.commit()
