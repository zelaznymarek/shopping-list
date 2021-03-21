from typing import List, Optional

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


def remove(db_session: Session, user_to_delete: User) -> None:
    db_session.delete(user_to_delete)
    db_session.commit()


def get_all(db_session: Session) -> List[User]:
    return db_session.query(User).all()


def get_by_email(db_session: Session, email: str) -> Optional[User]:
    return db_session.query(User).filter(User.email == email).first()


def update(db_session: Session, *, db_user: User, user_to_update: dict, updated_by_admin: bool) -> User:
    if not updated_by_admin:
        try:
            del user_to_update['is_admin']
        except KeyError:
            pass

    for field, value in user_to_update.items():
        setattr(db_user, field, value)

    db_session.add(db_user)
    db_session.commit()

    return db_user
