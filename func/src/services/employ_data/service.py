from typing import List

from decouple import config
from persephone_client import Persephone

from src.domain.enums.persephone_queue import PersephoneQueue
from src.domain.exceptions.model import InternalServerError
from src.domain.models.request.model import PoliticallyExposedCondition
from src.repositories.step_validator.repository import StepValidator
from src.repositories.user.repository import UserRepository


class PoliticallyExposedService:
    persephone_client = Persephone

    @staticmethod
    def __model_politically_exposed_data_to_persephone(
        politically_exposed: bool, unique_id: str, politically_exposed_names: List[str]
    ) -> dict:
        data = {
            "unique_id": unique_id,
            "politically_exposed": politically_exposed,
            "politically_exposed_names": politically_exposed_names,
        }
        return data

    @classmethod
    async def update_politically_exposed_data_for_us(
        cls, company_director_data: PoliticallyExposedCondition, payload: dict
    ) -> None:

        await StepValidator.validate_onboarding_step(
            x_thebes_answer=payload["x_thebes_answer"]
        )

        unique_id = payload["data"]["user"]["unique_id"]

        user_is_politically_exposed = company_director_data.is_politically_exposed
        user_politically_exposed_names = company_director_data.politically_exposed_names

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await cls.persephone_client.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_POLITICALLY_EXPOSED_IN_US.value,
            message=cls.__model_politically_exposed_data_to_persephone(
                politically_exposed=user_is_politically_exposed,
                politically_exposed_names=user_politically_exposed_names,
                unique_id=unique_id,
            ),
            schema_name="user_politically_exposed_us_schema",
        )
        if sent_to_persephone is False:
            raise InternalServerError("Error sending data to Persephone")

        was_updated = await UserRepository.update_user(
            unique_id=unique_id,
            new={
                "external_exchange_requirements.us.is_politically_exposed": user_is_politically_exposed,
                "external_exchange_requirements.us.politically_exposed_names": user_politically_exposed_names,
            },
        )
        if not was_updated:
            raise InternalServerError("Error updating user data")
