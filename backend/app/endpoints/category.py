from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

from app.auth import get_current_user
from app.db.session import get_db
from app.db import models
from app.schemas import category as schemas

router = APIRouter()


@router.get('/{category_id}', response_model=schemas.Category)
def get_one(
        category_id: int,
        current_user: models.User = Depends(get_current_user),
        db_session: Session = Depends(get_db)
) -> schemas.Category:
    return crud.get_by_id(db_session, category_id)


@router.get('/', response_model=List[schemas.Category])
def get_all(current_user: models.User = Depends(get_current_user), db_session: Session = Depends(get_db)) -> List[schemas.Category]:
    return crud.get_list(db_session)


@router.post('/', response_model=schemas.Category)
def add(
        new_category: schemas.CategoryCreate,
        current_user: models.User = Depends(get_current_user),
        db_session: Session = Depends(get_db)
) -> schemas.Category:
    db_category = db_session.query(models.Category).filter(models.Category.name == new_category.name).first()

    if db_category:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail='The category with this name already exists in the system.'
        )

    return crud.create(db_session, new_category)


@router.delete('/{category_id}')
def remove(
        category_id: int,
        current_user: models.User = Depends(get_current_user),
        db_session: Session = Depends(get_db)
):
    if not crud.get_by_id(db_session, category_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'The category with id "{category_id}" not found.'
        )

    return crud.remove_by_id(db_session, category_id)


@router.put('/{category_id}', response_model=schemas.Category)
def update(
        category_id: int,
        category_updated: schemas.CategoryCreate,
        current_user: models.User = Depends(get_current_user),
        db_session: Session = Depends(get_db)
):
    db_category = crud.get_by_id(db_session, category_id)

    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'The category with id "{category_id}" not found.'
        )

    crud.update(db_session, db_category, category_updated)
