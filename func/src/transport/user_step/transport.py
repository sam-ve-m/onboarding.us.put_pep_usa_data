import asyncio

from decouple import config
from etria_logger import Gladsheim

from src.domain.models.user_data.onboarding_step.model import UserOnboardingStep
from src.infrastructures.iohttp.infrastructure import RequestInfrastructure


class StepChecker(RequestInfrastructure):
    @classmethod
    async def _get_step_br(cls, x_thebes_answer):
        get_step_url = config("URL_ONBOARDING_STEP_BR")
        header = {"x_thebes_answer": x_thebes_answer}
        steps_response = None
        step = None
        try:
            session = await cls.get_session()
            async with session.get(get_step_url, headers=header) as response:
                steps_response = await response.json()
                step = steps_response["result"]["current_step"]
        except Exception as ex:
            message = "Error trying to get the onboarding step in BR"
            Gladsheim.error(error=ex, message=message, response=steps_response)
            raise ex

        return step

    @classmethod
    async def _get_step_us(cls, x_thebes_answer):
        get_step_url = config("URL_ONBOARDING_STEP_US")
        header = {"x_thebes_answer": x_thebes_answer}
        steps_response = None
        step = None
        try:
            session = await cls.get_session()
            async with session.get(get_step_url, headers=header) as response:
                steps_response = await response.json()
                step = steps_response["result"]["current_step"]
        except Exception as ex:
            message = "Error trying to get the onboarding step in US"
            Gladsheim.error(error=ex, message=message, response=steps_response)
            raise ex

        return step

    @classmethod
    async def get_onboarding_step(cls, x_thebes_answer):
        step_br = cls._get_step_br(x_thebes_answer=x_thebes_answer)
        step_us = cls._get_step_us(x_thebes_answer=x_thebes_answer)
        all_steps = await asyncio.gather(step_br, step_us)
        user_step = UserOnboardingStep(step_br=all_steps[0], step_us=all_steps[1])
        return user_step
