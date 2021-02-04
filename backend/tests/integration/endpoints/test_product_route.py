import pytest

from tests.integration.endpoints.test_category_route import get_token


api_prefix = 'localhost:3000/products'


def test_get_products_returns_all(db_session, client, product):
    token = get_token(db_session, client)

    res = client.get('/products', headers={'Authorization': f'Bearer {token}'})

    assert len(res.json()) == 1

    response_product = res.json()[0]

    assert res.status_code == 200
    assert response_product['id'] == product.id
    assert response_product['name'] == product.name
    assert response_product['category_id'] == product.category_id


@pytest.mark.parametrize('headers', [
    {'Authorization': 'Bearer invalid'},
    {'Authorization': 'invalid'},
    {'X-Custom': 'Bearer invalid'},
    {}
])
def test_get_products_unavailable_for_unauthorised(client, headers):
    res = client.get('/products', headers=headers)

    assert res.status_code == 401


def test_get_product_returns_one(db_session, client, product):
    token = get_token(db_session, client)

    res = client.get(f'/products/{product.id}', headers={'Authorization': f'Bearer {token}'})

    response_product = res.json()

    assert res.status_code == 200
    assert response_product['id'] == product.id
    assert response_product['name'] == product.name


def test_get_product_returns_not_found(db_session, client):
    token = get_token(db_session, client)

    res = client.get(f'/products/1', headers={'Authorization': f'Bearer {token}'})

    assert res.status_code == 404


@pytest.mark.parametrize('headers', [
    {'Authorization': 'Bearer invalid'},
    {'Authorization': 'invalid'},
    {'X-Custom': 'Bearer invalid'},
    {}
])
def test_get_product_unavailable_for_unauthorised(client, headers):
    res = client.get('/products/1', headers=headers)

    assert res.status_code == 401


def test_add_product(db_session, client, category):
    token = get_token(db_session, client)
    product_data = {
        'name': 'chicken',
        'category_id': category.id
    }

    res = client.post(
        '/products',
        json=product_data,
        headers={'Authorization': f'Bearer {token}'},
        allow_redirects=True
    )

    assert res.status_code == 200

    returned_product = res.json()

    assert returned_product['id'] == 1
    assert returned_product['name'] == product_data['name']
    assert returned_product['category_id'] == product_data['category_id']


def test_add_product_returns_unprocessable_entity(db_session, client):
    token = get_token(db_session, client)

    res = client.post(
        '/products',
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
def test_get_product_unavailable_for_unauthorised(client, headers):
    res = client.post('/products', json={}, headers=headers, allow_redirects=True)

    assert res.status_code == 401


def test_remove_product(db_session, client, product):
    token = get_token(db_session, client)

    res = client.delete(f'/products/{product.id}', headers={'Authorization': f'Bearer {token}'})

    assert res.status_code == 200
    assert res.json() is None


def test_remove_product_returns_not_found(db_session, client):
    token = get_token(db_session, client)

    res = client.delete('/products/1', headers={'Authorization': f'Bearer {token}'})

    assert res.status_code == 404


@pytest.mark.parametrize('headers', [
    {'Authorization': 'Bearer invalid'},
    {'Authorization': 'invalid'},
    {'X-Custom': 'Bearer invalid'},
    {}
])
def test_remove_product_unavailable_for_unauthorised(client, headers):
    res = client.delete('/products/1',  headers=headers)

    assert res.status_code == 401


def test_update_product_name(db_session, client, product):
    token = get_token(db_session, client)
    product_to_update = {
        'name': 'pork'
    }

    res = client.put(
        f'/products/{product.id}',
        json=product_to_update,
        headers={'Authorization': f'Bearer {token}'}
    )

    assert res.status_code == 200

    updated = res.json()
    assert updated['id'] == product.id
    assert updated['name'] == product_to_update['name']
    assert updated['category_id'] == product.category_id


def test_update_product_category(db_session, client, product, sweets_category):
    token = get_token(db_session, client)
    product_to_update = {
        'category_id': sweets_category.id
    }

    res = client.put(
        f'/products/{product.id}',
        json=product_to_update,
        headers={'Authorization': f'Bearer {token}'}
    )

    assert res.status_code == 200

    updated = res.json()
    assert updated['id'] == product.id
    assert updated['name'] == product.name
    assert updated['category_id'] == product_to_update['category_id']


def test_update_product_returns_not_found(db_session, client):
    token = get_token(db_session, client)
    product_to_update = {
        'name': 'changed'
    }

    res = client.put(
        '/products/1',
        json=product_to_update,
        headers={'Authorization': f'Bearer {token}'}
    )

    assert res.status_code == 404


@pytest.mark.parametrize('headers', [
    {'Authorization': 'Bearer invalid'},
    {'Authorization': 'invalid'},
    {'X-Custom': 'Bearer invalid'},
    {}
])
def test_update_product_unavailable_for_unauthorised(client, headers):
    product_to_update = {
        'name': 'changed'
    }

    res = client.put('/products/1', json=product_to_update, headers=headers)

    assert res.status_code == 401
