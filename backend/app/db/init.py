from sqlalchemy.orm import Session

from backend.app import settings
from backend.app.auth import get_password_hash
from backend.app.db.models import User
from backend.app.settings import get_logger

logger = get_logger(__name__)


def init(db_session: Session) -> None:
    user = db_session.query(User).filter(User.username == settings.FIRST_ADMIN).first()
    if not user:
        logger.info("Initializing database")
        user = User(
            email="ja@marek.org",
            username=settings.FIRST_ADMIN,
            hashed_password=get_password_hash(settings.FIRST_ADMIN_PASSWORD),
            is_admin=True,
        )

        db_session.add(user)
        db_session.commit()
        logger.info("Database initialized")
