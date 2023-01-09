# OUTSIDE LIBRARIES
from func.src.infrastructures.iohttp.infrastructure import RequestInfrastructure
from unittest.mock import MagicMock
import aiohttp


dummy_env = "dummy env"


def test_get_session(monkeypatch):
    dummy_connection = "dummy connection"
    mock_connection = MagicMock(return_value=dummy_connection)
    monkeypatch.setattr(aiohttp, "ClientSession", mock_connection)

    new_connection_created = RequestInfrastructure.get_session()
    assert new_connection_created == dummy_connection
    mock_connection.assert_called_once_with()

    reused_client = RequestInfrastructure.get_session()
    assert reused_client == new_connection_created
    mock_connection.assert_called_once_with()
    RequestInfrastructure._RequestInfrastructure__session = None
