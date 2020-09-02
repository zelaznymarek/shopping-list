from sqlalchemy.orm import Session

from app.crud.user import create, remove, get_all
from app.schemas import UserCreate
from app.db.models import User


def test_create_defaults(db_session):
    example_user_schema = UserCreate(
        email='example@user.cc',
        password='bababa'
    )

    user: User = create(db_session, example_user_schema)

    assert user.email == example_user_schema.email
    assert user.is_admin is False
    assert user.lists == []
    assert user.username == 'example'
    assert user.hashed_password


def test_create(db_session):
    example_user_schema = UserCreate(
        email='example@user.cc',
        password='bababa',
        username='example_username',
        is_admin=True
    )

    user: User = create(db_session, example_user_schema)

    assert user.email == example_user_schema.email
    assert user.username == example_user_schema.username
    assert user.is_admin is True
    assert user.lists == []
    assert user.hashed_password


def test_remove(db_session):
    example_user = User(
        email='example@user.cc',
        username='example',
        hashed_password='this_is_hashed',
        is_admin=False
    )

    db_session.add(example_user)
    db_session.commit()

    users = db_session.query(User).all()
    assert len(users) == 1

    remove(db_session, example_user)

    users = db_session.query(User).all()
    assert len(users) == 0


def test_get_all(db_session: Session):
    example_users = [
        User(
            email='example@user.cc',
            username='example',
            hashed_password='this_is_hashed',
            is_admin=False
        ),
        User(
            email='example2@user.cc',
            username='example2',
            hashed_password='this_is_hashed',
            is_admin=False
        )
    ]

    db_session.add_all(example_users)
    db_session.commit()

    users = get_all(db_session)

    assert len(users) == 2
