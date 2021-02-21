import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, close_all_sessions, Session
from fastapi.testclient import TestClient

from app import settings
from app.main import app
from app.db.session import Base
from app.db.models import Category, Product, User
from app.auth import pwd_context


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


@pytest.fixture
def token(db_session: Session, client):
    user = User(
        email='test@user.cc',
        username='test',
        hashed_password=pwd_context.hash('passwd')
    )

    db_session.add(user)
    db_session.commit()

    login_response = client.post('/login', data={'username': user.email, 'password': 'passwd'})
    body = login_response.json()

    return body['access_token']


@pytest.fixture
def example_categories():
    return [
        Category(name='meat'),
        Category(name='sweets'),
    ]


@pytest.fixture
def category_meat(db_session, example_categories):
    db_session.add(example_categories[0])
    db_session.commit()

    return example_categories[0]


@pytest.fixture
def category_sweets(db_session, example_categories):
    db_session.add(example_categories[1])
    db_session.commit()

    return example_categories[1]


@pytest.fixture
def example_product(category_meat):
    return Product(name='Chicken', category=category_meat)


@pytest.fixture
def product(db_session, example_product):
    db_session.add(example_product)
    db_session.commit()

    return example_product
