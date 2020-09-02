from typing import List

from sqlalchemy.orm import Session

from app.auth import get_password_hash
from app.schemas.user import UserCreate
from app.db.models import User


def create(db_session: Session, new_user: UserCreate) -> User:
    user = User(
        username=new_user.username or new_user.email.split('@')[0],
        email=new_user.email,
        hashed_password=get_password_hash(new_user.password),
        is_admin=new_user.is_admin
    )

    db_session.add(user)
    db_session.commit()

    return user


def remove(db_session: Session, user_to_delete: User):
    db_session.delete(user_to_delete)
    db_session.commit()


def get_all(db_session: Session) -> List[User]:
    return db_session.query(User).all()
