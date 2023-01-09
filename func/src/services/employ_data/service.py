from decouple import config
from persephone_client import Persephone

from func.src.domain.enums.persephone_queue import PersephoneQueue
from func.src.domain.exceptions.model import (
    InternalServerError,
    InvalidStepError,
    SuitabilityRequiredError,
)
from func.src.domain.models.request.model import PoliticallyExposedRequest
from func.src.domain.models.user_data.device_info.model import DeviceInfo
from func.src.domain.models.user_data.politically_exposed.model import PoliticallyExposedData
from func.src.repositories.user.repository import UserRepository
from func.src.transport.user_step.transport import StepChecker


class PoliticallyExposedService:
    persephone_client = Persephone

    @staticmethod
    def __model_politically_exposed_data_to_persephone(
        politically_exposed_data: PoliticallyExposedData, device_info: DeviceInfo
    ) -> dict:
        data = {
            "unique_id": politically_exposed_data.unique_id,
            "politically_exposed": politically_exposed_data.is_politically_exposed,
            "politically_exposed_names": politically_exposed_data.politically_exposed_names,
            "device_info": device_info.device_info,
            "device_id": device_info.device_id,
        }
        return data

    @classmethod
    async def update_politically_exposed_data_for_us(
        cls, politically_exposed_request: PoliticallyExposedRequest
    ):

        user_step = await StepChecker.get_onboarding_step(
            x_thebes_answer=politically_exposed_request.x_thebes_answer
        )
        if not user_step.is_in_correct_step():
            raise InvalidStepError(
                f"Step BR: {user_step.step_br} | Step US: {user_step.step_us}"
            )

        politically_exposed = politically_exposed_request.politically_exposed
        politically_exposed_data = PoliticallyExposedData(
            unique_id=politically_exposed_request.unique_id,
            is_politically_exposed=politically_exposed.is_politically_exposed,
            politically_exposed_names=politically_exposed.politically_exposed_names,
        )

        user_has_suitability = (
            await UserRepository.verify_if_user_has_suitability(
                politically_exposed_data
            )
        )
        if not user_has_suitability:
            raise SuitabilityRequiredError()

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await cls.persephone_client.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_POLITICALLY_EXPOSED_IN_US.value,
            message=cls.__model_politically_exposed_data_to_persephone(
                politically_exposed_data=politically_exposed_data,
                device_info=politically_exposed_request.device_info,
            ),
            schema_name="user_politically_exposed_us_schema",
        )
        if sent_to_persephone is False:
            raise InternalServerError("Error sending data to Persephone")

        await UserRepository.update_user(politically_exposed_data)
