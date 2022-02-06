from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException
from freezegun import freeze_time
from jose import jwt

from shopping_list.auth import (
    ALGORITHM,
    authenticate_user,
    create_access_token,
    get_current_admin_user,
    get_current_user,
    is_decoded_token_valid,
    pwd_context,
)
from shopping_list.db.models import User


@pytest.fixture
def example_user():
    return User(id=1, email="example@user.aa", username="example", is_admin=False)


def test_get_current_admin_user_with_admin(example_user):
    example_user.is_admin = True

    assert get_current_admin_user(example_user) == example_user


def test_get_current_admin_user_with_non_admin(example_user):
    with pytest.raises(HTTPException) as exc:
        get_current_admin_user(example_user)

    assert exc.value.status_code == 401
    assert exc.value.detail == "The user does not have enough privileges"


date = datetime.fromisoformat("2020-01-01")


@freeze_time(date)
def test_create_access_token_with_expiration():
    """Check whether token expiration date considers passed timedelta"""
    data = {"sub": "some_username"}
    delta = timedelta(days=1)
    secret_key = "notsosecret"

    with patch("shopping_list.auth.SECRET_KEY", secret_key):
        token = create_access_token(data, delta)

    decoded = jwt.decode(token, secret_key, algorithms=[ALGORITHM])

    assert decoded["sub"] == data["sub"]
    assert decoded["exp"] == (datetime.utcnow() + delta).timestamp()


@freeze_time(date)
def test_create_access_token_with_default_expiration():
    """Check whether token expiration date is created with default timedelta"""
    data = {"sub": "some_username"}
    secret_key = "notsosecret"

    with patch("shopping_list.auth.SECRET_KEY", secret_key):
        token = create_access_token(data)

    decoded = jwt.decode(token, secret_key, algorithms=[ALGORITHM])

    assert decoded["sub"] == data["sub"]
    assert decoded["exp"] == (datetime.utcnow() + timedelta(minutes=15)).timestamp()


def test_authenticate_user(example_user):
    example_user.hashed_password = pwd_context.hash("bababa")

    with patch("shopping_list.auth.get_user", return_value=example_user):
        user = authenticate_user(Mock(), email=example_user.email, password="bababa")

    assert user == example_user


def test_authenticate_user_wrong_password(example_user):
    example_user.hashed_password = pwd_context.hash("bababa")

    with patch("shopping_list.auth.get_user", return_value=example_user):
        user = authenticate_user(Mock(), email=example_user.email, password="wrong")

    assert user is False


def test_authenticate_user_wrong_user(example_user):
    example_user.hashed_password = pwd_context.hash("bababa")

    with patch("shopping_list.auth.get_user", return_value=None):
        user = authenticate_user(Mock(), email=example_user.email, password="bababa")

    assert user is False


@pytest.mark.parametrize(
    "decoded_token",
    [
        {"sub": "username", "exp": 125},
        {"sub": "username"},
        {"exp": (datetime.utcnow() + timedelta(days=10)).timestamp()},
    ],
)
def test_is_decoded_token_valid_returns_false(decoded_token):
    assert is_decoded_token_valid(decoded_token) is False


def test_is_decoded_token_valid_returns_true():
    decoded_token = {
        "sub": "username",
        "exp": (datetime.utcnow() + timedelta(days=10)).timestamp(),
    }

    assert is_decoded_token_valid(decoded_token) is True


def test_get_current_user(example_user):
    db_mock = Mock()
    secret_key = "notsosecret"
    data = {"sub": example_user.username, "exp": datetime.utcnow() + timedelta(days=10)}

    with patch("shopping_list.auth.SECRET_KEY", secret_key):
        token = jwt.encode(data, secret_key, algorithm=ALGORITHM)

        with patch("shopping_list.auth.get_user", return_value=example_user) as get_user_mock:
            user = get_current_user(db_mock, token)

    get_user_mock.assert_called_once_with(db_mock, example_user.username)

    assert user == example_user


def test_get_current_user_invalid_token(example_user):
    db_mock = Mock()

    with pytest.raises(HTTPException) as exc:
        with patch("shopping_list.auth.get_user", return_value=example_user) as get_user_mock:
            get_current_user(db_mock, "invalid_token")

    get_user_mock.assert_not_called()

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid authentication credentials"
    assert exc.value.headers == {"Authenticate": "Bearer"}
