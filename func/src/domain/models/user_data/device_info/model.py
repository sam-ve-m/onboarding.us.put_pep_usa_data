from decouple import config


class DeviceInfo:
    def __init__(
        self,
        device_info: dict,
        device_id: str,
    ):
        self.device_info = device_info
        self.device_id = device_id
        if device_info.get("precision") is None:
            self.device_info.update(
                {"precision": float(config("DEFAULT_PRECISION_VALUE"))}
            )
