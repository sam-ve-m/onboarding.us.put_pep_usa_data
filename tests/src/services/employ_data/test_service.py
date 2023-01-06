from unittest.mock import patch

import pytest
from decouple import Config
from persephone_client import Persephone

from func.src.domain.exceptions.model import (
    InternalServerError,
    InvalidStepError,
    SuitabilityRequiredError,
)
from func.src.domain.models.request.model import (
    PoliticallyExposedCondition,
    PoliticallyExposedRequest,
)
from func.src.domain.models.user_data.device_info.model import DeviceInfo
from func.src.domain.models.user_data.onboarding_step.model import UserOnboardingStep
from func.src.domain.models.user_data.politically_exposed.model import PoliticallyExposedData
from func.src.repositories.user.repository import UserRepository
from func.src.services.employ_data.service import PoliticallyExposedService
from func.src.transport.user_step.transport import StepChecker

politically_exposed_model_dummy = PoliticallyExposedCondition(
    **{"is_politically_exposed": True, "politically_exposed_names": ["Giogio"]}
)
stub_device_info = DeviceInfo({"precision": 1}, "")
politically_exposed_request_dummy = PoliticallyExposedRequest(
    x_thebes_answer="x_thebes_answer",
    unique_id="unique_id",
    politically_exposed=politically_exposed_model_dummy,
    device_info=stub_device_info,
)
politically_exposed_data_dummy = PoliticallyExposedData(
    unique_id=politically_exposed_request_dummy.unique_id,
    is_politically_exposed=politically_exposed_model_dummy.is_politically_exposed,
    politically_exposed_names=politically_exposed_model_dummy.politically_exposed_names,
)
onboarding_step_correct_stub = UserOnboardingStep("finished", "politically_exposed")
onboarding_step_incorrect_stub = UserOnboardingStep("finished", "some_step")


def test___model_company_director_data_to_persephone():
    result = PoliticallyExposedService._PoliticallyExposedService__model_politically_exposed_data_to_persephone(
        politically_exposed_data_dummy, stub_device_info
    )
    expected_result = {
        "unique_id": politically_exposed_data_dummy.unique_id,
        "politically_exposed": politically_exposed_data_dummy.is_politically_exposed,
        "politically_exposed_names": politically_exposed_data_dummy.politically_exposed_names,
        "device_info": stub_device_info.device_info,
        "device_id": stub_device_info.device_id,
    }
    assert result == expected_result


@pytest.mark.asyncio
@patch.object(Config, "__call__")
@patch.object(UserRepository, "verify_if_user_has_suitability")
@patch.object(UserRepository, "update_user")
@patch.object(Persephone, "send_to_persephone")
@patch.object(StepChecker, "get_onboarding_step")
async def test_update_politically_exposed_data_for_us(
    get_onboarding_step_mock,
    persephone_client_mock,
    update_user_mock,
    verify_risk,
    mocked_env,
):
    verify_risk.return_value = True
    get_onboarding_step_mock.return_value = onboarding_step_correct_stub
    persephone_client_mock.return_value = (True, 0)
    update_user_mock.return_value = True
    result = await PoliticallyExposedService.update_politically_exposed_data_for_us(
        politically_exposed_request_dummy
    )
    expected_result = None

    assert result == expected_result
    assert get_onboarding_step_mock.called
    assert persephone_client_mock.called
    assert update_user_mock.called


@pytest.mark.asyncio
@patch.object(UserRepository, "verify_if_user_has_suitability")
@patch.object(UserRepository, "update_user")
@patch.object(Persephone, "send_to_persephone")
@patch.object(StepChecker, "get_onboarding_step")
async def test_update_politically_exposed_data_for_us_when_user_is_in_wrong_step(
    get_onboarding_step_mock, persephone_client_mock, update_user_mock, verify_risk
):
    verify_risk.return_value = True
    get_onboarding_step_mock.return_value = onboarding_step_incorrect_stub
    persephone_client_mock.return_value = (True, 0)
    update_user_mock.return_value = True
    with pytest.raises(InvalidStepError):
        result = await PoliticallyExposedService.update_politically_exposed_data_for_us(
            politically_exposed_request_dummy
        )

    assert get_onboarding_step_mock.called
    assert not persephone_client_mock.called
    assert not update_user_mock.called


@pytest.mark.asyncio
@patch.object(Config, "__call__")
@patch.object(UserRepository, "verify_if_user_has_suitability")
@patch.object(UserRepository, "update_user")
@patch.object(Persephone, "send_to_persephone")
@patch.object(StepChecker, "get_onboarding_step")
async def test_update_politically_exposed_data_for_us_when_cant_send_to_persephone(
    get_onboarding_step_mock,
    persephone_client_mock,
    update_user_mock,
    verify_risk,
    mocked_env,
):
    verify_risk.return_value = True
    get_onboarding_step_mock.return_value = onboarding_step_correct_stub
    persephone_client_mock.return_value = (False, 0)
    update_user_mock.return_value = True
    with pytest.raises(InternalServerError):
        result = await PoliticallyExposedService.update_politically_exposed_data_for_us(
            politically_exposed_request_dummy
        )

    assert get_onboarding_step_mock.called
    assert persephone_client_mock.called
    assert not update_user_mock.called


@pytest.mark.asyncio
@patch.object(UserRepository, "verify_if_user_has_suitability")
@patch.object(UserRepository, "update_user")
@patch.object(Persephone, "send_to_persephone")
@patch.object(StepChecker, "get_onboarding_step")
async def test_update_politically_exposed_data_for_us_when_user_doesnt_have_high_risk_tolerance(
    get_onboarding_step_mock, persephone_client_mock, update_user_mock, verify_risk
):
    verify_risk.return_value = False
    get_onboarding_step_mock.return_value = onboarding_step_correct_stub
    persephone_client_mock.return_value = (True, 0)
    update_user_mock.return_value = False
    with pytest.raises(SuitabilityRequiredError):
        result = await PoliticallyExposedService.update_politically_exposed_data_for_us(
            politically_exposed_request_dummy
        )

    assert get_onboarding_step_mock.called
    assert not persephone_client_mock.called
    assert not update_user_mock.called
