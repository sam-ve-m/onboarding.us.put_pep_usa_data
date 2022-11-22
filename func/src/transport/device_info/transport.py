import asyncio
from http import HTTPStatus

from decouple import config
from httpx import AsyncClient

from ...domain.exceptions.model import (
    DeviceInfoRequestFailed,
    DeviceInfoNotSupplied,
)
from ...domain.models.user_data.device_info.model import DeviceInfo


class DeviceSecurity:
    @staticmethod
    async def decrypt_device_info(device_info: str) -> dict:
        if not device_info:
            raise DeviceInfoNotSupplied()
        body = {"deviceInfo": device_info}
        async with AsyncClient() as httpx_client:
            request_result = await httpx_client.post(
                config("DEVICE_SECURITY_DECRYPT_DEVICE_INFO_URL"), json=body
            )
            if request_result.status_code != HTTPStatus.OK:
                raise DeviceInfoRequestFailed()
        device_info_decrypted = request_result.json().get("deviceInfo")
        return device_info_decrypted

    @staticmethod
    async def generate_device_id(device_info: str) -> str:
        if not device_info:
            raise DeviceInfoNotSupplied()
        body = {"deviceInfo": device_info}
        async with AsyncClient() as httpx_client:
            request_result = await httpx_client.post(
                config("DEVICE_SECURITY_DEVICE_ID_URL"), json=body
            )
            if request_result.status_code != HTTPStatus.OK:
                raise DeviceInfoRequestFailed()
        device_id = request_result.json().get("deviceID")
        return device_id

    @classmethod
    async def get_device_info(cls, device_info: str) -> DeviceInfo:
        device_information_coroutine = cls.decrypt_device_info(device_info)
        device_id_coroutine = cls.generate_device_id(device_info)
        device_information, device_id = await asyncio.gather(
            device_information_coroutine, device_id_coroutine
        )
        device_info_object = DeviceInfo(
            device_info=device_information, device_id=device_id
        )
        return device_info_object
