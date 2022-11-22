class UnauthorizedError(Exception):
    pass


class InvalidStepError(Exception):
    pass


class InvalidRiskProfileError(Exception):
    pass


class InternalServerError(Exception):
    pass


class DeviceInfoRequestFailed(Exception):
    pass


class DeviceInfoNotSupplied(Exception):
    pass
