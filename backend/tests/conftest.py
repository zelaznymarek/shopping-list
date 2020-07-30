import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, close_all_sessions, Session

from app import settings
from app.db.models import User
from app.db.session import Base


@pytest.fixture
def db_session():
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = session()

    yield db

    close_all_sessions()
    Base.metadata.drop_all(engine)


@pytest.fixture
def example_user():
    return User(
        email='example@email.com',
        name='Example',
        hashed_password='secret'
    )


@pytest.fixture
def db_user(db_session: Session, example_user):
    db_session.add(example_user)
    db_session.commit()

    yield example_user

    db_session.delete(example_user)
    db_session.commit()
