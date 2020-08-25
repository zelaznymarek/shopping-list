from unittest.mock import patch

from app.routers.health import health_check


@patch('app.routers.health.is_db_healthy', return_value=True)
def test_health_check_when_db_is_alive(_is_healthy):
    health = health_check()

    assert health.database is True


@patch('app.routers.health.is_db_healthy', return_value=False)
def test_health_check_when_db_is_dead(_is_healthy):
    health = health_check()

    assert health.database is False
