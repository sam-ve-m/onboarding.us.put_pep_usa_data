from http import HTTPStatus

from etria_logger import Gladsheim
from flask import request, Request, Response

from src.domain.enums.response.code import InternalCode
from src.domain.exceptions.model import (
    UnauthorizedError,
    InternalServerError,
    InvalidStepError,
    InvalidRiskProfileError, DeviceInfoRequestFailed, DeviceInfoNotSupplied,
)
from src.domain.models.request.model import PoliticallyExposedRequest
from src.domain.models.response.model import ResponseModel
from src.services.employ_data.service import PoliticallyExposedService


async def update_politically_exposed_us(request: Request = request) -> Response:
    try:
        raw_params = request.json
        x_thebes_answer = request.headers.get("x-thebes-answer")
        x_device_info = request.headers.get("x-device-info")

        politically_exposed_request = await PoliticallyExposedRequest.build(
            x_thebes_answer=x_thebes_answer,
            x_device_info=x_device_info,
            parameters=raw_params,
        )

        politically_exposed = (
            await PoliticallyExposedService.update_politically_exposed_data_for_us(
                politically_exposed_request=politically_exposed_request
            )
        )

        response = ResponseModel(
            result=politically_exposed,
            success=True,
            code=InternalCode.SUCCESS,
            message="Register Updated.",
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ValueError as ex:
        message = "Invalid parameters"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message=message
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except UnauthorizedError as ex:
        message = "JWT invalid or not supplied"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID,
            message=message,
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except InvalidStepError as ex:
        message = "User in invalid onboarding step"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message=message
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except InvalidRiskProfileError as ex:
        message = (
            "The user needs to have high risk tolerance to do the onboarding in US"
        )
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message=message
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except DeviceInfoRequestFailed as ex:
        message = "Error trying to get device info"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message=message,
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except DeviceInfoNotSupplied as ex:
        message = "Device info not supplied"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS,
            message=message,
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except InternalServerError as ex:
        message = "Failed to update register"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=message
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except Exception as ex:
        message = "Unexpected error occurred"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=message
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
