from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.db import models
from app import schemas

router = APIRouter()


@router.get('/me', response_model=schemas.User)
def user_info(user: models.User = Depends(get_current_user)):
    return user
