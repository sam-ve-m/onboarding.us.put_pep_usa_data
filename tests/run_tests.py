import pytest
from unittest.mock import patch
import decouple
import os

project_path = os.environ["PROJECT_PATH"]


@patch.object(decouple, "config")
def run_tests_with_config_mock(config_mock):
    retcode = pytest.main(["-vv", project_path])


run_tests_with_config_mock()
