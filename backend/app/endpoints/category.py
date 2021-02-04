from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

from app.auth import get_current_user
from app.db.session import get_db
from app.db import models
from app.schemas import category as schemas
from app.crud import category as crud

router = APIRouter(redirect_slashes=False)


@router.get('/{category_id}', response_model=schemas.Category, responses={status.HTTP_404_NOT_FOUND: {}})
def get_one(
        category_id: int,
        current_user: models.User = Depends(get_current_user),
        db_session: Session = Depends(get_db)
):
    if not (db_category := crud.get_by_id(db_session, category_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'The category with id "{category_id}" not found.'
        )

    return db_category


@router.get('/', response_model=List[schemas.Category])
def get_all(
        current_user: models.User = Depends(get_current_user),
        db_session: Session = Depends(get_db)
):
    return crud.get_many(db_session)


@router.post('/', response_model=schemas.Category, responses={status.HTTP_422_UNPROCESSABLE_ENTITY: {}})
def add(
        new_category: schemas.CategoryCreate,
        current_user: models.User = Depends(get_current_user),
        db_session: Session = Depends(get_db)
) -> schemas.Category:
    if crud.get_by_name(db_session, new_category.name):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail='The category with this name already exists in the system.'
        )

    return crud.create(db_session, new_category.dict())


@router.delete('/{category_id}')
def remove(
        category_id: int,
        current_user: models.User = Depends(get_current_user),
        db_session: Session = Depends(get_db)
):
    if not (db_category := crud.get_by_id(db_session, category_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'The category with id "{category_id}" not found.'
        )

    return crud.remove(db_session, db_category)


@router.put('/{category_id}', response_model=schemas.Category)
def update(
        category_id: int,
        category_to_update: schemas.CategoryCreate,
        current_user: models.User = Depends(get_current_user),
        db_session: Session = Depends(get_db)
):
    if not (db_category := crud.get_by_id(db_session, category_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'The category with id "{category_id}" not found.'
        )

    return crud.update(db_session, db_category=db_category, category_to_update=category_to_update.dict())
