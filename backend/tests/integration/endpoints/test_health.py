from app.endpoints.health import is_db_healthy


def test_is_db_healthy_returns_true(db_session):
    assert is_db_healthy(db_session) is True


def test_is_db_healthy_returns_false(invalid_db_session):
    assert is_db_healthy(invalid_db_session) is False
