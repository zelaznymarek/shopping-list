import pytest


@pytest.mark.usefixtures("shopping_lists")
def test_get_lists_returns_all(client, token):
    res = client.get("/lists", headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 200
    assert len(res.json()) == 2


@pytest.mark.parametrize(
    "headers",
    [
        {"Authorization": "Bearer invalid"},
        {"Authorization": "invalid"},
        {"X-Custom": "Bearer invalid"},
        {},
    ],
)
def test_get_lists_unavailable_for_unauthorised(client, headers):
    res = client.get("/lists", headers=headers)

    assert res.status_code == 401


def test_get_list_returns_one(client, shopping_lists, token):
    shopping_list = shopping_lists[0]
    res = client.get(
        f"/lists/{shopping_list.id}", headers={"Authorization": f"Bearer {token}"}
    )

    response_shopping_list = res.json()

    assert res.status_code == 200
    assert response_shopping_list["id"] == shopping_list.id
    assert response_shopping_list["name"] == shopping_list.name


def test_get_list_returns_not_found(client, token):
    res = client.get(f"/lists/1", headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 404


@pytest.mark.parametrize(
    "headers",
    [
        {"Authorization": "Bearer invalid"},
        {"Authorization": "invalid"},
        {"X-Custom": "Bearer invalid"},
        {},
    ],
)
def test_get_list_unavailable_for_unauthorised(client, headers):
    res = client.get("/lists/1", headers=headers)

    assert res.status_code == 401


def test_add_list(client, products, token):
    shopping_list_data = {"name": "list_one", "product_ids": [p.id for p in products]}

    res = client.post(
        "/lists",
        json=shopping_list_data,
        headers={"Authorization": f"Bearer {token}"},
        allow_redirects=True,
    )

    assert res.status_code == 200

    returned_shopping_list = res.json()

    assert returned_shopping_list["id"] == 1
    assert returned_shopping_list["name"] == shopping_list_data["name"]
    assert returned_shopping_list["user_id"]
    assert len(returned_shopping_list["products"]) == 3


def test_add_list_returns_bad_request(client, token):
    """Check whether a BAD REQUEST response is returned when product with provided id does not exist."""
    shopping_list_data = {"name": "list_one", "product_ids": [1]}

    res = client.post(
        "/lists",
        json=shopping_list_data,
        headers={"Authorization": f"Bearer {token}"},
        allow_redirects=True,
    )

    assert res.status_code == 400
    assert res.json()["detail"] == "Provided products does not exist in the system"


def test_add_list_returns_unprocessable_entity(client, token):
    """Check whether an UNPROCESSABLE ENTITY response is returned when POST body is invalid"""
    res = client.post(
        "/lists",
        json={},
        headers={"Authorization": f"Bearer {token}"},
        allow_redirects=True,
    )

    assert res.status_code == 422


@pytest.mark.parametrize(
    "headers",
    [
        {"Authorization": "Bearer invalid"},
        {"Authorization": "invalid"},
        {"X-Custom": "Bearer invalid"},
        {},
    ],
)
def test_get_list_unavailable_for_unauthorised(client, headers):
    res = client.post("/lists", json={}, headers=headers, allow_redirects=True)

    assert res.status_code == 401


def test_remove_list(client, shopping_list, token):
    res = client.delete(
        f"/lists/{shopping_list.id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 200
    assert res.json() is None

    res = client.get(f"/lists", headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 200
    assert not res.json()


def test_remove_list_returns_not_found(client, token):
    res = client.delete("/lists/1", headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 404


@pytest.mark.parametrize(
    "headers",
    [
        {"Authorization": "Bearer invalid"},
        {"Authorization": "invalid"},
        {"X-Custom": "Bearer invalid"},
        {},
    ],
)
def test_remove_list_unavailable_for_unauthorised(client, headers):
    res = client.delete("/lists/1", headers=headers)

    assert res.status_code == 401
