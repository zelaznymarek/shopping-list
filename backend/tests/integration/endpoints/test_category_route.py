import pytest
from sqlalchemy.orm import Session

from app.db.models import User
from app.auth import pwd_context


api_prefix = 'localhost:3000/categories'


def get_token(db_session: Session, client):
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


def test_get_categories_returns_all(db_session, client, category):
    token = get_token(db_session, client)

    res = client.get('/categories', headers={'Authorization': f'Bearer {token}'})

    assert len(res.json()) == 1

    response_category = res.json()[0]

    assert res.status_code == 200
    assert response_category['id'] == category.id
    assert response_category['name'] == category.name


@pytest.mark.parametrize('headers', [
    {'Authorization': 'Bearer invalid'},
    {'Authorization': 'invalid'},
    {'X-Custom': 'Bearer invalid'},
    {}
])
def test_get_categories_unavailable_for_unauthorised(client, headers):
    res = client.get('/categories', headers=headers)

    assert res.status_code == 401


def test_get_category_returns_one(db_session, client, category):
    token = get_token(db_session, client)

    res = client.get(f'/categories/{category.id}', headers={'Authorization': f'Bearer {token}'})

    response_category = res.json()

    assert res.status_code == 200
    assert response_category['id'] == category.id
    assert response_category['name'] == category.name


def test_get_category_returns_not_found(db_session, client):
    token = get_token(db_session, client)

    res = client.get(f'/categories/1', headers={'Authorization': f'Bearer {token}'})

    assert res.status_code == 404


@pytest.mark.parametrize('headers', [
    {'Authorization': 'Bearer invalid'},
    {'Authorization': 'invalid'},
    {'X-Custom': 'Bearer invalid'},
    {}
])
def test_get_category_unavailable_for_unauthorised(client, headers):
    res = client.get('/categories/1', headers=headers)

    assert res.status_code == 401


def test_add_category(db_session, client):
    token = get_token(db_session, client)
    category_data = {
        'name': 'sweets'
    }

    res = client.post(
        '/categories',
        json=category_data,
        headers={'Authorization': f'Bearer {token}'},
        allow_redirects=True
    )

    assert res.status_code == 200

    returned_category = res.json()

    assert returned_category['id'] == 1
    assert returned_category['name'] == category_data['name']


def test_add_category_returns_unprocessable_entity(db_session, client):
    token = get_token(db_session, client)

    res = client.post(
        '/categories',
        json={},
        headers={'Authorization': f'Bearer {token}'},
        allow_redirects=True
    )

    assert res.status_code == 422


@pytest.mark.parametrize('headers', [
    {'Authorization': 'Bearer invalid'},
    {'Authorization': 'invalid'},
    {'X-Custom': 'Bearer invalid'},
    {}
])
def test_get_category_unavailable_for_unauthorised(client, headers):
    res = client.post('/categories', json={}, headers=headers, allow_redirects=True)

    assert res.status_code == 401


def test_remove_category(db_session, client, category):
    token = get_token(db_session, client)

    res = client.delete(f'/categories/{category.id}', headers={'Authorization': f'Bearer {token}'})

    assert res.status_code == 200
    assert res.json() is None


def test_remove_category_returns_not_found(db_session, client):
    token = get_token(db_session, client)

    res = client.delete('/categories/1', headers={'Authorization': f'Bearer {token}'})

    assert res.status_code == 404


@pytest.mark.parametrize('headers', [
    {'Authorization': 'Bearer invalid'},
    {'Authorization': 'invalid'},
    {'X-Custom': 'Bearer invalid'},
    {}
])
def test_remove_category_unavailable_for_unauthorised(client, headers):
    res = client.delete('/categories/1',  headers=headers)

    assert res.status_code == 401


def test_update_category(db_session, client, category):
    token = get_token(db_session, client)
    category_to_update = {
        'name': 'changed'
    }

    res = client.put(
        f'/categories/{category.id}',
        json=category_to_update,
        headers={'Authorization': f'Bearer {token}'}
    )

    assert res.status_code == 200

    updated = res.json()
    assert updated['id'] == category.id
    assert updated['name'] == category_to_update['name']


def test_update_category_returns_not_found(db_session, client):
    token = get_token(db_session, client)
    category_to_update = {
        'name': 'changed'
    }

    res = client.put(
        '/categories/1',
        json=category_to_update,
        headers={'Authorization': f'Bearer {token}'}
    )

    assert res.status_code == 404


@pytest.mark.parametrize('headers', [
    {'Authorization': 'Bearer invalid'},
    {'Authorization': 'invalid'},
    {'X-Custom': 'Bearer invalid'},
    {}
])
def test_update_category_unavailable_for_unauthorised(client, headers):
    category_to_update = {
        'name': 'changed'
    }

    res = client.put('/categories/1', json=category_to_update, headers=headers)

    assert res.status_code == 401
