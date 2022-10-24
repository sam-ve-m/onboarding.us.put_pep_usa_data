import aiohttp


class RequestInfrastructure:
    __session = None

    @classmethod
    def get_session(cls):
        if cls.__session is None:
            client_session = aiohttp.ClientSession()
            cls.__session = client_session
        return cls.__session
