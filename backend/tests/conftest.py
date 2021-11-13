import pytest
from app import settings
from app.auth import pwd_context
from app.db.models import Category
from app.db.models import List as ShoppingList
from app.db.models import Product, User
from app.db.session import Base
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, close_all_sessions, sessionmaker


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
    engine = create_engine("postgresql://postgres:postgres@invalid_host:5432/db")
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    yield session()

    close_all_sessions()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def example_user():
    return User(
        email="test@user.cc",
        username="test",
        hashed_password=pwd_context.hash("passwd"),
    )


@pytest.fixture
def user(db_session, example_user):
    db_session.add(example_user)
    db_session.commit()

    return example_user


@pytest.fixture
def token(db_session: Session, client, user):
    login_response = client.post(
        "/login", data={"username": user.email, "password": "passwd"}
    )
    body = login_response.json()

    return body["access_token"]


@pytest.fixture
def example_categories():
    return [
        Category(name="meat"),
        Category(name="sweets"),
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
def example_products(category_meat, category_sweets):
    return [
        Product(name="Chicken", category=category_meat),
        Product(name="Pork", category=category_meat),
        Product(name="Chocolate", category=category_sweets),
    ]


@pytest.fixture
def example_product(category_meat):
    return Product(name="Chicken", category=category_meat)


@pytest.fixture
def example_products_without_category():
    return [
        Product(name="bread"),
        Product(name="milk"),
        Product(name="eggs"),
    ]


@pytest.fixture
def products(db_session: Session, example_products):
    db_session.add_all(example_products)
    db_session.commit()

    return example_products


@pytest.fixture
def product(db_session, example_product):
    db_session.add(example_product)
    db_session.commit()

    return example_product


@pytest.fixture
def empty_shopping_list(products, user):
    return ShoppingList(name="empty", user_id=user.id)


@pytest.fixture
def example_shopping_lists(products, user):
    return [
        ShoppingList(name="list_one", user_id=user.id, products=products),
        ShoppingList(name="list_one", user_id=user.id),
    ]


@pytest.fixture
def example_shopping_list(products, user):
    return ShoppingList(name="list_one", user_id=user.id, products=products)


@pytest.fixture
def shopping_list(db_session, example_shopping_list):
    db_session.add(example_shopping_list)
    db_session.commit()

    return example_shopping_list


@pytest.fixture
def shopping_lists(db_session, example_shopping_lists):
    db_session.add_all(example_shopping_lists)
    db_session.commit()

    return example_shopping_lists
