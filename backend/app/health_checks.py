from app.settings import get_logger
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session

logger = get_logger(__name__)


def is_db_healthy(db: Session):
    try:
        db.execute("SELECT 1").first()
        return True
    except DatabaseError as exc:
        logger.error(f"Database error: {exc.orig}")

    return False
