from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.health_checks import is_db_healthy

router = APIRouter()


class Health(BaseModel):
    database: bool = False


@router.get(
    path="/",
    response_model=Health,
    status_code=status.HTTP_200_OK,
    summary="System health check",
)
def health_check(db: Session = Depends(get_db)):
    """
    Check if listed services are in a healthy state:
    - **database**
    """
    health = Health()

    health.database = is_db_healthy(db)

    return health
