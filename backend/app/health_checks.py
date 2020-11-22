from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session

from app.settings import get_logger

logger = get_logger(__name__)


def is_db_healthy(db: Session):
    try:
        db.execute('SELECT 1').first()
        return True
    except DatabaseError as exc:
        logger.error(f'Database error: {exc.orig}')

    return False
