from unittest.mock import patch, MagicMock
from func.src.domain.models.response.model import ResponseModel


@patch.object(ResponseModel, "to_dumps")
def test_instance(mocked_dumps):
    dummy_value = MagicMock()
    model = ResponseModel(dummy_value, dummy_value)
    assert model.message is None
    assert model.result is None
