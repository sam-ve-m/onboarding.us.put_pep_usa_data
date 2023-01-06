from heimdall_client import Heimdall, HeimdallStatusResponses

from func.src.domain.exceptions.model import UnauthorizedError


class Jwt:
    def __init__(self, unique_id: str):
        self.unique_id = unique_id

    @staticmethod
    async def decode_and_validate_jwt(jwt: str):
        jwt_content, heimdall_status = await Heimdall.decode_payload(jwt=jwt)
        if heimdall_status != HeimdallStatusResponses.SUCCESS:
            raise UnauthorizedError()
        return jwt_content

    @classmethod
    async def build(cls, jwt: str):
        jwt_data = await cls.decode_and_validate_jwt(jwt=jwt)
        unique_id = jwt_data["decoded_jwt"]["user"]["unique_id"]
        return cls(unique_id=unique_id)
