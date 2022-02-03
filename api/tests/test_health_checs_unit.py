from unittest.mock import patch

from shopping_list.endpoints.health import is_db_healthy


@patch("shopping_list.health_checks.logger")
def test_is_db_healthy_logs_error(logger_mock, invalid_db_session):
    is_db_healthy(invalid_db_session)

    logger_mock.error.assert_called_once()
