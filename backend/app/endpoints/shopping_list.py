from typing import List

from app.auth import get_current_user
from app.db import models
from app.db.session import get_db
from app.repository import shopping_list as crud
from app.schemas import shopping_list as schemas
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

router = APIRouter(redirect_slashes=False)


@router.get(
    "/{list_id}",
    response_model=schemas.ShoppingList,
    responses={status.HTTP_404_NOT_FOUND: {}},
)
def get_one(
    list_id: int,
    current_user: models.User = Depends(get_current_user),
    db_session: Session = Depends(get_db),
):
    try:
        db_list = crud.get_by_id(db_session, list_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'The list with id "{list_id}" not found.',
        )

    return db_list


@router.get("/", response_model=List[schemas.ShoppingList])
def get_all(
    current_user: models.User = Depends(get_current_user),
    db_session: Session = Depends(get_db),
):
    return crud.get_many(db_session)


@router.post(
    "/",
    response_model=schemas.ShoppingList,
    responses={status.HTTP_422_UNPROCESSABLE_ENTITY: {}},
)
def add(
    new_list: schemas.ShoppingListCreate,
    current_user: models.User = Depends(get_current_user),
    db_session: Session = Depends(get_db),
) -> schemas.ShoppingList:
    try:
        crud.get_by_name(db_session, new_list.name)

        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="The list with this name already exists in the system.",
        )
    except NoResultFound:
        try:
            return crud.create(db_session, new_list.dict(), current_user)
        except ValueError as exc:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.delete("/{list_id}")
def remove(
    list_id: int,
    current_user: models.User = Depends(get_current_user),
    db_session: Session = Depends(get_db),
):
    try:
        db_list = crud.get_by_id(db_session, list_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'The list with id "{list_id}" not found.',
        )

    return crud.remove(db_session, db_list)
