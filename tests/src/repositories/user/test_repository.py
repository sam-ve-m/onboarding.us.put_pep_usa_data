from unittest.mock import patch, AsyncMock

from etria_logger import Gladsheim
from pytest import mark, raises

from src.repositories.user.repository import UserRepository


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(UserRepository, "_UserRepository__get_collection")
async def test_update_user(get_collection_mock, etria_error_mock):
    update_one_result_dummy = {"user": "data"}
    collection_mock = AsyncMock()
    collection_mock.update_one.return_value = update_one_result_dummy
    get_collection_mock.return_value = collection_mock
    result = await UserRepository.update_user(unique_id="unique_id", new={})
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
    with raises(Exception):
        result = await UserRepository.update_user({})
    etria_error_mock.assert_called()


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(UserRepository, "_UserRepository__get_collection")
async def test_update_user_when_exception_happens(
    get_collection_mock, etria_error_mock
):
    get_collection_mock.side_effect = Exception()
    result = await UserRepository.update_user(unique_id="unique_id", new={})
    expected_result = False
    assert result == expected_result
    assert etria_error_mock.called
