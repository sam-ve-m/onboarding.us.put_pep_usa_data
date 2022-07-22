from unittest.mock import patch

import pytest
from persephone_client import Persephone

from src.domain.exceptions.model import InternalServerError
from src.domain.models.request.model import PoliticallyExposedCondition
from src.repositories.step_validator.repository import StepValidator
from src.repositories.user.repository import UserRepository
from src.services.employ_data.service import PoliticallyExposedService

tax_residence_model_dummy = PoliticallyExposedCondition(
    **{"is_politically_exposed": True, "politically_exposed_names": ["Giogio"]}
)

payload_dummy = {
    "x_thebes_answer": "x_thebes_answer",
    "data": {"user": {"unique_id": "unique_id"}},
}


def test___model_politically_exposed_data_to_persephone():
    politically_exposed = True
    politically_exposed_names = ["string"]
    unique_id = "string"
    result = PoliticallyExposedService._PoliticallyExposedService__model_politically_exposed_data_to_persephone(
        politically_exposed=politically_exposed,
        politically_exposed_names=politically_exposed_names,
        unique_id=unique_id,
    )
    expected_result = {
        "unique_id": unique_id,
        "politically_exposed": politically_exposed,
        "politically_exposed_names": politically_exposed_names,
    }
    assert result == expected_result


@pytest.mark.asyncio
@patch.object(UserRepository, "update_user")
@patch.object(Persephone, "send_to_persephone")
@patch.object(StepValidator, "validate_onboarding_step")
async def test_update_politically_exposed_data_for_us(
    step_validator_mock, persephone_client_mock, update_user_mock
):
    persephone_client_mock.return_value = (True, 0)
    update_user_mock.return_value = True
    result = await PoliticallyExposedService.update_politically_exposed_data_for_us(
        tax_residence_model_dummy, payload_dummy
    )
    expected_result = None

    assert result == expected_result
    assert step_validator_mock.called
    assert persephone_client_mock.called
    assert update_user_mock.called


@pytest.mark.asyncio
@patch.object(UserRepository, "update_user")
@patch.object(Persephone, "send_to_persephone")
@patch.object(StepValidator, "validate_onboarding_step")
async def test_update_politically_exposed_data_for_us_when_cant_send_to_persephone(
    step_validator_mock, persephone_client_mock, update_user_mock
):
    persephone_client_mock.return_value = (False, 0)
    update_user_mock.return_value = True
    with pytest.raises(InternalServerError):
        result = await PoliticallyExposedService.update_politically_exposed_data_for_us(
            tax_residence_model_dummy, payload_dummy
        )

    assert step_validator_mock.called
    assert persephone_client_mock.called
    assert not update_user_mock.called


@pytest.mark.asyncio
@patch.object(UserRepository, "update_user")
@patch.object(Persephone, "send_to_persephone")
@patch.object(StepValidator, "validate_onboarding_step")
async def test_update_politically_exposed_data_for_us_when_cant_update_user_register(
    step_validator_mock, persephone_client_mock, update_user_mock
):
    persephone_client_mock.return_value = (True, 0)
    update_user_mock.return_value = False
    with pytest.raises(InternalServerError):
        result = await PoliticallyExposedService.update_politically_exposed_data_for_us(
            tax_residence_model_dummy, payload_dummy
        )

    assert step_validator_mock.called
    assert persephone_client_mock.called
    assert update_user_mock.called
