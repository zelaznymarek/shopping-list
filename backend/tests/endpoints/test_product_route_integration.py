import pytest


@pytest.mark.usefixtures("products")
def test_get_products_returns_all(client, token):
    res = client.get("/products", headers={"Authorization": f"Bearer {token}"})

    assert len(res.json()) == 3
    assert res.status_code == 200


@pytest.mark.parametrize(
    "headers",
    [
        {"Authorization": "Bearer invalid"},
        {"Authorization": "invalid"},
        {"X-Custom": "Bearer invalid"},
        {},
    ],
)
def test_get_products_unavailable_for_unauthorised(client, headers):
    res = client.get("/products", headers=headers)

    assert res.status_code == 401


def test_get_product_returns_one(client, product, token):
    res = client.get(
        f"/products/{product.id}", headers={"Authorization": f"Bearer {token}"}
    )

    response_product = res.json()

    assert res.status_code == 200
    assert response_product["id"] == product.id
    assert response_product["name"] == product.name


def test_get_product_returns_not_found(client, token):
    res = client.get(f"/products/1", headers={"Authorization": f"Bearer {token}"})

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
def test_get_product_unavailable_for_unauthorised(client, headers):
    res = client.get("/products/1", headers=headers)

    assert res.status_code == 401


def test_add_product(client, category_meat, token):
    product_data = {"name": "chicken", "category_id": category_meat.id}

    res = client.post(
        "/products",
        json=product_data,
        headers={"Authorization": f"Bearer {token}"},
        allow_redirects=True,
    )

    assert res.status_code == 200

    returned_product = res.json()

    assert returned_product["id"] == 1
    assert returned_product["name"] == product_data["name"]
    assert returned_product["category_id"] == product_data["category_id"]


def test_add_product_returns_unprocessable_entity(client, token):
    res = client.post(
        "/products",
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
def test_add_product_unavailable_for_unauthorised(client, headers):
    res = client.post("/products", json={}, headers=headers, allow_redirects=True)

    assert res.status_code == 401


def test_remove_product(client, product, token):
    res = client.delete(
        f"/products/{product.id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 200
    assert res.json() is None


def test_remove_product_returns_not_found(client, token):
    res = client.delete("/products/1", headers={"Authorization": f"Bearer {token}"})

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
def test_remove_product_unavailable_for_unauthorised(client, headers):
    res = client.delete("/products/1", headers=headers)

    assert res.status_code == 401


def test_update_product_name(client, product, token):
    product_to_update = {"name": "pork"}

    res = client.put(
        f"/products/{product.id}",
        json=product_to_update,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 200

    updated = res.json()
    assert updated["id"] == product.id
    assert updated["name"] == product_to_update["name"]
    assert updated["category_id"] == product.category_id


def test_update_product_category(client, product, category_sweets, token):
    product_to_update = {"category_id": category_sweets.id}

    res = client.put(
        f"/products/{product.id}",
        json=product_to_update,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 200

    updated = res.json()
    assert updated["id"] == product.id
    assert updated["name"] == product.name
    assert updated["category_id"] == category_sweets.id


def test_update_product_returns_not_found(client, token):
    product_to_update = {"name": "changed"}

    res = client.put(
        "/products/1",
        json=product_to_update,
        headers={"Authorization": f"Bearer {token}"},
    )

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
def test_update_product_unavailable_for_unauthorised(client, headers):
    product_to_update = {"name": "changed"}

    res = client.put("/products/1", json=product_to_update, headers=headers)

    assert res.status_code == 401
