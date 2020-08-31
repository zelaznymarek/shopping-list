from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user, get_current_admin_user
from app.db import models
from app.db.session import get_db
from app import schemas
from app.crud.user import create, remove, get_all

router = APIRouter()


@router.get('/me', response_model=schemas.User)
def about_me(current_user: models.User = Depends(get_current_user)):
    """Get info about currently logged user."""
    return current_user


@router.post('/', response_model=schemas.User)
def add(
      new_user: schemas.UserCreate,
      db_session: Session = Depends(get_db),
      current_user: models.User = Depends(get_current_admin_user)
):
    """Create a new user."""
    db_user = db_session.query(models.User).filter(models.User.username == new_user.username).first()

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The user with this username already exists in the system.'
        )

    return create(db_session, new_user)


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT, responses={404: {}})
def delete_by_username(
      user_to_delete: schemas.UserDelete,
      db_session: Session = Depends(get_db),
      current_user: models.User = Depends(get_current_admin_user)
):
    """Delete a user"""
    db_user = db_session.query(models.User).filter(models.User.username == user_to_delete.username).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User "{user_to_delete.username}" not found.'
        )

    remove(db_session, db_user)


@router.get('/', response_model=List[schemas.User])
def get_list(db_session: Session = Depends(get_db), current_user: models.User = Depends(get_current_admin_user)):
    """Get the list of all users"""
    return get_all(db_session)
