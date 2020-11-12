import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, close_all_sessions
from fastapi.testclient import TestClient

from app import settings
from app.main import app
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
def invalid_db_session():
    engine = create_engine('postgresql://postgres:postgres@invalid_host:5432/db')
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    yield session()

    close_all_sessions()


@pytest.fixture
def client():
    return TestClient(app)
