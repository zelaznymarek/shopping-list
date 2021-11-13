from typing import List

from app.auth import get_current_user
from app.db import models
from app.db.session import get_db
from app.repository import product as crud
from app.schemas import product as schemas
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

router = APIRouter()


@router.get(
    "/{product_id}",
    response_model=schemas.Product,
    responses={status.HTTP_404_NOT_FOUND: {}},
)
def get_one(
    product_id: int,
    current_user: models.User = Depends(get_current_user),
    db_session: Session = Depends(get_db),
):
    try:
        db_product = crud.get_by_id(db_session, product_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'The product with id "{product_id}" not found.',
        )

    return db_product


@router.get("/", response_model=List[schemas.Product])
def get_all(
    current_user: models.User = Depends(get_current_user),
    db_session: Session = Depends(get_db),
):
    return crud.get_many(db_session)


@router.post(
    "/",
    response_model=schemas.Product,
    responses={status.HTTP_422_UNPROCESSABLE_ENTITY: {}},
)
def add(
    new_product: schemas.ProductCreate,
    current_user: models.User = Depends(get_current_user),
    db_session: Session = Depends(get_db),
) -> schemas.Product:
    try:
        crud.get_by_name(db_session, new_product.name)

        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="The product with this name already exists in the system.",
        )
    except NoResultFound:
        return crud.create(db_session, new_product.dict())


@router.delete("/{product_id}")
def remove(
    product_id: int,
    current_user: models.User = Depends(get_current_user),
    db_session: Session = Depends(get_db),
):
    try:
        db_product = crud.get_by_id(db_session, product_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'The product with id "{product_id}" not found.',
        )

    return crud.remove(db_session, db_product)


@router.put("/{product_id}", response_model=schemas.Product)
def update(
    product_id: int,
    product_to_update: schemas.ProductUpdate,
    current_user: models.User = Depends(get_current_user),
    db_session: Session = Depends(get_db),
):
    try:
        db_product = crud.get_by_id(db_session, product_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'The product with id "{product_id}" not found.',
        )

    return crud.update(
        db_session, db_product=db_product, product_to_update=product_to_update.dict()
    )
