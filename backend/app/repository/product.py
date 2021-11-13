from typing import List, Optional

from app.db import models
from sqlalchemy.orm.session import Session


def get_by_id(db_session: Session, product_id: int) -> Optional[models.Product]:
    return (
        db_session.query(models.Product).filter(models.Product.id == product_id).one()
    )


def get_by_name(db_session: Session, product_name) -> Optional[models.Product]:
    return (
        db_session.query(models.Product)
        .filter(models.Product.name == product_name)
        .one()
    )


def get_many(db_session: Session) -> List[models.Product]:
    return db_session.query(models.Product).all()


def create(db_session: Session, product_dict: dict) -> models.Product:
    product = models.Product(**product_dict)

    db_session.add(product)
    db_session.commit()

    return product


def remove(db_session: Session, product: models.Product):
    db_session.delete(product)
    db_session.commit()


def update(
    db_session: Session, *, db_product: models.Product, product_to_update: dict
) -> models.Product:
    for field, value in product_to_update.items():
        if value:
            setattr(db_product, field, value)

    db_session.add(db_product)
    db_session.commit()

    return db_product
