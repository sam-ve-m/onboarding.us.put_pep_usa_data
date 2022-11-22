from http import HTTPStatus
from unittest.mock import MagicMock, patch, AsyncMock

import pytest

from decouple import config, Config
from etria_logger import Gladsheim
from httpx import AsyncClient

from func.src.domain.exceptions.model import (
    DeviceInfoNotSupplied,
    DeviceInfoRequestFailed,
)
from func.src.transport.device_info.transport import DeviceSecurity


dummy_value = MagicMock()


@pytest.mark.asyncio
@patch.object(AsyncClient, "__init__", return_value=None)
@patch.object(AsyncClient, "__aenter__")
@patch.object(AsyncClient, "__aexit__")
@patch.object(Config, "__call__")
@patch.object(Gladsheim, "error")
async def test_generate_device_id(
    mocked_logger,
    mocked_env,
    mocked_client_exit,
    mocked_client_enter,
    mocked_client_instance,
):
    mocked_client_enter.return_value.post = AsyncMock()
    mocked_client_enter.return_value.post.return_value = MagicMock()
    mocked_client_enter.return_value.post.return_value.status_code = HTTPStatus.OK
    result = await DeviceSecurity.generate_device_id(dummy_value)
    mocked_client_enter.return_value.post.assert_called_once_with(
        mocked_env.return_value, json={"deviceInfo": dummy_value}
    )
    mocked_logger.assert_not_called()
    assert result == (
        mocked_client_enter.return_value.post.return_value.json.return_value.get.return_value
    )


def raise_second(*args):
    raise args[1]


@pytest.mark.asyncio
@patch.object(AsyncClient, "__init__", return_value=None)
@patch.object(AsyncClient, "__aenter__")
@patch.object(AsyncClient, "__aexit__", side_effect=raise_second)
@patch.object(Config, "__call__")
@patch.object(Gladsheim, "error")
async def test_generate_device_id_with_error(
    mocked_logger,
    mocked_env,
    mocked_client_exit,
    mocked_client_enter,
    mocked_client_instance,
):
    mocked_client_enter.return_value.post = AsyncMock()
    mocked_client_enter.return_value.post.return_value = MagicMock()
    mocked_client_enter.return_value.post.return_value.status_code = (
        HTTPStatus.INTERNAL_SERVER_ERROR
    )
    with pytest.raises(DeviceInfoRequestFailed):
        await DeviceSecurity.generate_device_id(dummy_value)
    mocked_client_enter.return_value.post.assert_called_once_with(
        mocked_env.return_value, json={"deviceInfo": dummy_value}
    )


@pytest.mark.asyncio
@patch.object(AsyncClient, "__init__", return_value=None)
@patch.object(AsyncClient, "__aenter__")
@patch.object(AsyncClient, "__aexit__", side_effect=raise_second)
@patch.object(Config, "__call__")
@patch.object(Gladsheim, "error")
async def test_generate_device_id_when_device_info_is_not_supplied(
    mocked_logger,
    mocked_env,
    mocked_client_exit,
    mocked_client_enter,
    mocked_client_instance,
):
    mocked_client_enter.return_value.post = AsyncMock()
    mocked_client_enter.return_value.post.return_value = MagicMock()
    mocked_client_enter.return_value.post.return_value.status_code = (
        HTTPStatus.INTERNAL_SERVER_ERROR
    )
    with pytest.raises(DeviceInfoNotSupplied):
        await DeviceSecurity.generate_device_id(None)


@pytest.mark.asyncio
@patch.object(AsyncClient, "__init__", return_value=None)
@patch.object(AsyncClient, "__aenter__")
@patch.object(AsyncClient, "__aexit__")
@patch.object(Config, "__call__")
@patch.object(Gladsheim, "error")
async def test_decrypt_device_info(
    mocked_logger,
    mocked_env,
    mocked_client_exit,
    mocked_client_enter,
    mocked_client_instance,
):
    mocked_client_enter.return_value.post = AsyncMock()
    mocked_client_enter.return_value.post.return_value = MagicMock()
    mocked_client_enter.return_value.post.return_value.status_code = HTTPStatus.OK
    await DeviceSecurity.decrypt_device_info(dummy_value)
    mocked_client_enter.return_value.post.assert_called_once_with(
        mocked_env.return_value, json={"deviceInfo": dummy_value}
    )
    mocked_logger.assert_not_called()
    (
        mocked_client_enter.return_value.post.return_value.json.return_value.get.assert_called_once()
    )


def raise_second(*args):
    raise args[1]


@pytest.mark.asyncio
@patch.object(AsyncClient, "__init__", return_value=None)
@patch.object(AsyncClient, "__aenter__")
@patch.object(AsyncClient, "__aexit__", side_effect=raise_second)
@patch.object(Config, "__call__")
@patch.object(Gladsheim, "error")
async def test_decrypt_device_info_with_error(
    mocked_logger,
    mocked_env,
    mocked_client_exit,
    mocked_client_enter,
    mocked_client_instance,
):
    mocked_client_enter.return_value.post = AsyncMock()
    mocked_client_enter.return_value.post.return_value = MagicMock()
    mocked_client_enter.return_value.post.return_value.status_code = (
        HTTPStatus.INTERNAL_SERVER_ERROR
    )
    with pytest.raises(DeviceInfoRequestFailed):
        await DeviceSecurity.decrypt_device_info(dummy_value)
    mocked_client_enter.return_value.post.assert_called_once_with(
        mocked_env.return_value, json={"deviceInfo": dummy_value}
    )


@pytest.mark.asyncio
@patch.object(AsyncClient, "__init__", return_value=None)
@patch.object(AsyncClient, "__aenter__")
@patch.object(AsyncClient, "__aexit__", side_effect=raise_second)
@patch.object(Config, "__call__")
@patch.object(Gladsheim, "error")
async def test_decrypt_device_info_when_device_info_is_not_supplied(
    mocked_logger,
    mocked_env,
    mocked_client_exit,
    mocked_client_enter,
    mocked_client_instance,
):
    mocked_client_enter.return_value.post = AsyncMock()
    mocked_client_enter.return_value.post.return_value = MagicMock()
    mocked_client_enter.return_value.post.return_value.status_code = (
        HTTPStatus.INTERNAL_SERVER_ERROR
    )
    with pytest.raises(DeviceInfoNotSupplied):
        await DeviceSecurity.decrypt_device_info(None)
