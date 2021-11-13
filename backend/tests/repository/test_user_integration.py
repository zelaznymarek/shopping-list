from app.db.models import User
from app.repository.user import create, get_all, remove, update
from app.schemas import UserCreate
from sqlalchemy.orm import Session


def test_create_defaults(db_session):
    example_user_schema = UserCreate(email="example@user.cc", password="bababa")

    user: User = create(db_session, example_user_schema)

    assert user.email == example_user_schema.email
    assert user.is_admin is False
    assert user.lists == []
    assert user.username == "example"
    assert user.hashed_password


def test_create(db_session):
    example_user_schema = UserCreate(
        email="example@user.cc",
        password="bababa",
        username="example_username",
        is_admin=True,
    )

    user: User = create(db_session, example_user_schema)

    assert user.email == example_user_schema.email
    assert user.username == example_user_schema.username
    assert user.is_admin is True
    assert user.lists == []
    assert user.hashed_password


def test_remove(db_session):
    example_user = User(
        email="example@user.cc",
        username="example",
        hashed_password="this_is_hashed",
        is_admin=False,
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
            email="example@user.cc",
            username="example",
            hashed_password="this_is_hashed",
            is_admin=False,
        ),
        User(
            email="example2@user.cc",
            username="example2",
            hashed_password="this_is_hashed",
            is_admin=False,
        ),
    ]

    db_session.add_all(example_users)
    db_session.commit()

    users = get_all(db_session)

    assert len(users) == 2


def test_update_by_regular_user(db_session: Session):
    example_user = User(
        email="example@user.cc",
        username="example",
        hashed_password="this_is_hashed",
        is_admin=False,
    )

    db_session.add(example_user)
    db_session.commit()

    user_dict = {"username": "different", "is_admin": True}

    db_user = db_session.query(User).first()

    updated_user = update(
        db_session, db_user=db_user, user_to_update=user_dict, updated_by_admin=False
    )

    db_user: User = db_session.query(User).first()

    assert db_user.email == example_user.email == updated_user.email
    assert (
        db_user.hashed_password
        == example_user.hashed_password
        == updated_user.hashed_password
    )
    assert db_user.is_admin == example_user.is_admin == updated_user.is_admin
    assert db_user.username == user_dict["username"] == updated_user.username


def test_update_by_admin(db_session: Session):
    example_user = User(
        email="example@user.cc",
        username="example",
        hashed_password="this_is_hashed",
        is_admin=False,
    )

    db_session.add(example_user)
    db_session.commit()

    user_dict = {"username": "different", "is_admin": True}

    db_user = db_session.query(User).first()

    updated_user = update(
        db_session, db_user=db_user, user_to_update=user_dict, updated_by_admin=True
    )

    db_user: User = db_session.query(User).first()

    assert db_user.email == example_user.email == updated_user.email
    assert (
        db_user.hashed_password
        == example_user.hashed_password
        == updated_user.hashed_password
    )
    assert db_user.is_admin == user_dict["is_admin"] == updated_user.is_admin
    assert db_user.username == user_dict["username"] == updated_user.username
