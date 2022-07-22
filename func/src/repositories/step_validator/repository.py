import asyncio
from decouple import config
from etria_logger import Gladsheim

from src.domain.exceptions.model import InvalidStepError
from src.infrastructures.iohttp.infrastructure import RequestInfrastructure


class StepValidator(RequestInfrastructure):
    expected_step_br = "finished"
    expected_step_us = "politically_exposed"

    @classmethod
    async def validate_step_br(cls, x_thebes_answer):
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

        is_correct_step = step == cls.expected_step_br
        return is_correct_step

    @classmethod
    async def validate_step_us(cls, x_thebes_answer):
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

        is_correct_step = step == cls.expected_step_us
        return is_correct_step

    @classmethod
    async def validate_onboarding_step(cls, x_thebes_answer):
        is_correct_step_br = cls.validate_step_br(x_thebes_answer=x_thebes_answer)
        is_correct_step_us = cls.validate_step_us(x_thebes_answer=x_thebes_answer)
        steps_correct = await asyncio.gather(is_correct_step_br, is_correct_step_us)
        if not all(steps_correct):
            raise InvalidStepError(
                f"Step BR: {is_correct_step_br} | Step US: {is_correct_step_us}"
            )
