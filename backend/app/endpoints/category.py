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
    return get_by_id(category_id, db_session)


@router.get('/', response_model=List[schemas.Category])
def get_all(current_user: models.User = Depends(get_current_user), db_session: Session = Depends(get_db)) -> List[schemas.Category]:
    return get_list(db_session)


@router.post('/', response_model=schemas.Category)
def add(
        new_category: schemas.Category,
        current_user: models.User = Depends(get_current_user),
        db_session: Session = Depends(get_db)
) -> schemas.Category:
    db_category = db_session.query(models.Category).filter(models.Category.name == new_category.name).first()

    if db_category:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail='The category with this name already exists in the system.'
        )

    return create(new_category, db_session)


@router.delete('/{category_id}')
def remove(
        category_id: int,
        current_user: models.User = Depends(get_current_user),
        db_session: Session = Depends(get_db)
):
    if not get_by_id():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'The category with id "{category_id}" not found.'
        )

    return remove_by_id(category_id, db_session)
