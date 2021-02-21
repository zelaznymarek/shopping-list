import pytest


def test_get_lists_returns_all(client, shopping_list, token):
    res = client.get('/lists', headers={'Authorization': f'Bearer {token}'})

    assert len(res.json()) == 1

    response_shopping_list = res.json()[0]

    assert res.status_code == 200
    assert response_shopping_list['id'] == shopping_list.id
    assert response_shopping_list['name'] == shopping_list.name
    assert response_shopping_list['category_id'] == shopping_list.category_id


@pytest.mark.parametrize('headers', [
    {'Authorization': 'Bearer invalid'},
    {'Authorization': 'invalid'},
    {'X-Custom': 'Bearer invalid'},
    {}
])
def test_get_lists_unavailable_for_unauthorised(client, headers):
    res = client.get('/lists', headers=headers)

    assert res.status_code == 401


def test_get_list_returns_one(client, shopping_list, token):
    res = client.get(f'/lists/{shopping_list.id}', headers={'Authorization': f'Bearer {token}'})

    response_shopping_list = res.json()

    assert res.status_code == 200
    assert response_shopping_list['id'] == shopping_list.id
    assert response_shopping_list['name'] == shopping_list.name


def test_get_list_returns_not_found(client, token):
    res = client.get(f'/lists/1', headers={'Authorization': f'Bearer {token}'})

    assert res.status_code == 404


@pytest.mark.parametrize('headers', [
    {'Authorization': 'Bearer invalid'},
    {'Authorization': 'invalid'},
    {'X-Custom': 'Bearer invalid'},
    {}
])
def test_get_list_unavailable_for_unauthorised(client, headers):
    res = client.get('/lists/1', headers=headers)

    assert res.status_code == 401


def test_add_list(client, category_meat, token):
    shopping_list_data = {
        'name': 'chicken',
        'category_id': category_meat.id
    }

    res = client.post(
        '/lists',
        json=shopping_list_data,
        headers={'Authorization': f'Bearer {token}'},
        allow_redirects=True
    )

    assert res.status_code == 200

    returned_shopping_list = res.json()

    assert returned_shopping_list['id'] == 1
    assert returned_shopping_list['name'] == shopping_list_data['name']
    assert returned_shopping_list['category_id'] == shopping_list_data['category_id']


def test_add_list_returns_unprocessable_entity(client, token):
    res = client.post(
        '/lists',
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
def test_get_list_unavailable_for_unauthorised(client, headers):
    res = client.post('/lists', json={}, headers=headers, allow_redirects=True)

    assert res.status_code == 401


def test_remove_list(client, shopping_list, token):
    res = client.delete(f'/lists/{shopping_list.id}', headers={'Authorization': f'Bearer {token}'})

    assert res.status_code == 200
    assert res.json() is None


def test_remove_list_returns_not_found(client, token):
    res = client.delete('/lists/1', headers={'Authorization': f'Bearer {token}'})

    assert res.status_code == 404


@pytest.mark.parametrize('headers', [
    {'Authorization': 'Bearer invalid'},
    {'Authorization': 'invalid'},
    {'X-Custom': 'Bearer invalid'},
    {}
])
def test_remove_list_unavailable_for_unauthorised(client, headers):
    res = client.delete('/lists/1',  headers=headers)

    assert res.status_code == 401
