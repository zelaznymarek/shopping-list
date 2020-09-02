from unittest.mock import patch

from app.endpoints.health import health_check, is_db_healthy


@patch('app.endpoints.health.is_db_healthy', return_value=True)
def test_health_check_when_db_is_alive(_is_healthy):
    health = health_check()

    assert health.database is True


@patch('app.endpoints.health.is_db_healthy', return_value=False)
def test_health_check_when_db_is_dead(_is_healthy):
    health = health_check()

    assert health.database is False


@patch('app.endpoints.health.logger')
def test_is_db_healthy_logs_error(logger_mock, invalid_db_session):
    is_db_healthy(invalid_db_session)

    logger_mock.error.assert_called_once_with('Database error: could not translate host name "invalid_host" to address: Name or service not known\n')
