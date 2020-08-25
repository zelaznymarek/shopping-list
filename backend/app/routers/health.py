from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import DatabaseError


from app.db.session import get_db

router = APIRouter()


class Health(BaseModel):
    database: bool = False


@router.get(
    path='/',
    response_model=Health,
    status_code=status.HTTP_200_OK,
    summary='System health check'
)
def health_check(db: Session = Depends(get_db)):
    """
    Check if listed services are in healthy state:
    - **database**
    """
    health = Health()

    health.database = is_db_healthy(db)

    return health


def is_db_healthy(db):
    try:
        return db.execute('SELECT 1').first() == (1,)
    except DatabaseError as exc:
        print(f'Database error: {exc}')

    return False
