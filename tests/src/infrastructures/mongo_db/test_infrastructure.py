# OUTSIDE LIBRARIES
from src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure
from unittest.mock import patch, MagicMock
from decouple import AutoConfig
from motor import motor_asyncio


dummy_env = "dummy env"


@patch.object(AutoConfig, "__call__", return_value=dummy_env)
def test_get_client(mocked_env, monkeypatch):
    dummy_connection = "dummy connection"
    mock_connection = MagicMock(return_value=dummy_connection)
    monkeypatch.setattr(motor_asyncio, "AsyncIOMotorClient", mock_connection)

    new_connection_created = MongoDBInfrastructure.get_client()
    assert new_connection_created == dummy_connection
    mock_connection.assert_called_once_with(dummy_env)
    mocked_env.assert_called_once()

    reused_client = MongoDBInfrastructure.get_client()
    assert reused_client == new_connection_created
    mock_connection.assert_called_once_with(dummy_env)
    mocked_env.assert_called_once()
    MongoDBInfrastructure.client = None
