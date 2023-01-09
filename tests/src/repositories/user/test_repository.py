from unittest.mock import patch, AsyncMock

from etria_logger import Gladsheim
from pytest import mark, raises
from decouple import Config

from func.src.domain.exceptions.model import InternalServerError
from func.src.domain.models.user_data.model import UserData

with patch.object(Config, "__call__"):
    from func.src.repositories.user.repository import UserRepository


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
    assert collection_mock.update_one.called
    assert not etria_error_mock.called


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(UserRepository, "_UserRepository__get_collection")
async def test_update_user_when_exception_happens(
    get_collection_mock, etria_error_mock
):
    get_collection_mock.side_effect = Exception()
    with raises(InternalServerError):
        result = await UserRepository.update_user(user_data_dummy)
    assert etria_error_mock.called


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(UserRepository, "_UserRepository__get_collection")
async def test_verify_if_user_has_suitability_when_is_not_high(
    get_collection_mock, etria_error_mock
):
    collection_mock = AsyncMock()
    collection_mock.find_one.return_value = {"suitability": None}
    get_collection_mock.return_value = collection_mock
    result = await UserRepository.verify_if_user_has_suitability(
        user_data_dummy
    )
    expected_result = False
    assert result == expected_result
    assert not etria_error_mock.called


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(UserRepository, "_UserRepository__get_collection")
async def test_verify_if_user_has_suitability_when_is_high(
    get_collection_mock, etria_error_mock
):
    collection_mock = AsyncMock()
    collection_mock.find_one.return_value = {"suitability": {"score": 1}}
    get_collection_mock.return_value = collection_mock
    result = await UserRepository.verify_if_user_has_suitability(
        user_data_dummy
    )
    expected_result = True
    collection_mock.find_one.assert_called_once_with(
        {"unique_id": user_data_dummy.unique_id}, {"suitability": True}
    )
    assert result == expected_result
    assert not etria_error_mock.called


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(UserRepository, "_UserRepository__get_collection")
async def test_verify_if_user_has_suitability_when_exception_happens(
    get_collection_mock, etria_error_mock
):
    get_collection_mock.side_effect = Exception()
    with raises(InternalServerError):
        result = await UserRepository.verify_if_user_has_suitability(
            user_data_dummy
        )
    assert etria_error_mock.called
