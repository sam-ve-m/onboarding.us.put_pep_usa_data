from unittest.mock import patch, AsyncMock

from etria_logger import Gladsheim
from pytest import mark, raises

from src.domain.models.user_data.model import UserData
from src.repositories.user.repository import UserRepository


class UserDataDummy(UserData):
    unique_id = "unique_id"

    def get_data_representation(self):
        return


user_data_dummy = UserDataDummy()


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(UserRepository, "_UserRepository__get_collection")
async def test_update_user(get_collection_mock, etria_error_mock):
    collection_mock = AsyncMock()
    collection_mock.update_one.return_value = None
    get_collection_mock.return_value = collection_mock
    result = await UserRepository.update_user(user_data_dummy)
    expected_result = True
    assert result == expected_result
    assert not etria_error_mock.called


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(UserRepository, "_UserRepository__get_collection")
async def test_update_user_when_exception_happens(
    get_collection_mock, etria_error_mock
):
    get_collection_mock.side_effect = Exception()
    result = await UserRepository.update_user(user_data_dummy)
    expected_result = False
    assert result == expected_result
    assert etria_error_mock.called
