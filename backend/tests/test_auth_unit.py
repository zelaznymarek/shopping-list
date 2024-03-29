from datetime import timedelta, datetime
from unittest.mock import patch, Mock

import pytest
from freezegun import freeze_time
from fastapi import HTTPException
from jose import jwt

from app.auth import (
    get_current_user,
    get_current_admin_user,
    create_access_token,
    authenticate_user,
    pwd_context,
    ALGORITHM
)
from app.db.models import User


@pytest.fixture
def example_user():
    return User(
        id=1,
        email='example@user.aa',
        username='example',
        is_admin=False
    )


def test_get_current_admin_user_with_admin(example_user):
    example_user.is_admin = True

    assert get_current_admin_user(example_user) == example_user


def test_get_current_admin_user_with_non_admin(example_user):
    with pytest.raises(HTTPException) as exc:
        get_current_admin_user(example_user)

    assert exc.value.status_code == 401
    assert exc.value.detail == 'The user does not have enough privileges'


date = datetime.fromisoformat('2020-01-01')


@freeze_time(date)
def test_create_access_token_with_expiration():
    """Check whether token expiration date considers passed timedelta"""
    data = {
        'sub': 'some_username'
    }
    delta = timedelta(days=1)
    secret_key = 'notsosecret'

    with patch('app.auth.SECRET_KEY', secret_key):
        token = create_access_token(data, delta)

    decoded = jwt.decode(token, secret_key, algorithms=[ALGORITHM])

    assert decoded['sub'] == data['sub']
    assert decoded['exp'] == (date + delta).timestamp()


@freeze_time(date)
def test_create_access_token_with_default_expiration():
    """Check whether token expiration date is created with default timedelta"""
    data = {
        'sub': 'some_username'
    }
    secret_key = 'notsosecret'

    with patch('app.auth.SECRET_KEY', secret_key):
        token = create_access_token(data)

    decoded = jwt.decode(token, secret_key, algorithms=[ALGORITHM])

    assert decoded['sub'] == data['sub']
    assert decoded['exp'] == (date + timedelta(minutes=15)).timestamp()


def test_authenticate_user(example_user):
    example_user.hashed_password = pwd_context.hash('bababa')

    with patch('app.auth.get_user', return_value=example_user):
        user = authenticate_user(Mock(), email=example_user.email, password='bababa')

    assert user == example_user


def test_authenticate_user_wrong_password(example_user):
    example_user.hashed_password = pwd_context.hash('bababa')

    with patch('app.auth.get_user', return_value=example_user):
        user = authenticate_user(Mock(), email=example_user.email, password='wrong')

    assert user is None


def test_authenticate_user_wrong_user(example_user):
    example_user.hashed_password = pwd_context.hash('bababa')

    with patch('app.auth.get_user', return_value=None):
        user = authenticate_user(Mock(), email=example_user.email, password='bababa')

    assert user is None


def test_get_current_user(example_user):
    db_mock = Mock()
    secret_key = 'notsosecret'
    data = {
        'sub': example_user.username,
        'exp': datetime.utcnow() + timedelta(days=10)
    }

    with patch('app.auth.SECRET_KEY', secret_key):
        token = jwt.encode(data, secret_key, algorithm=ALGORITHM)

        with patch('app.auth.get_user', return_value=example_user) as get_user_mock:
            user = get_current_user(db_mock, token)

    get_user_mock.assert_called_once_with(db_mock, example_user.username)

    assert user == example_user


def test_get_current_with_user_expired_token():
    secret_key = 'notsosecret'
    data = {
        'sub': 'tester',
        'exp': datetime.utcnow() - timedelta(days=1)
    }

    with patch('app.auth.SECRET_KEY', secret_key):
        token = jwt.encode(data, secret_key, algorithm=ALGORITHM)

        with pytest.raises(HTTPException):
            get_current_user(Mock(), token)


def test_get_current_user_invalid_token(example_user):
    db_mock = Mock()

    with pytest.raises(HTTPException) as exc:
        with patch('app.auth.get_user', return_value=example_user) as get_user_mock:
            get_current_user(db_mock, 'invalid_token')

    get_user_mock.assert_not_called()

    assert exc.value.status_code == 401
    assert exc.value.detail == 'Invalid authentication credentials'
    assert exc.value.headers == {'Authenticate': 'Bearer'}
