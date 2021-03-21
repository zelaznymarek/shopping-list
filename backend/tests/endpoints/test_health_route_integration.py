def test_when_all_is_healthy(client):
    res = client.get('/health')

    assert res.status_code == 200

    for _, is_alive in res.json().items():
        assert is_alive
