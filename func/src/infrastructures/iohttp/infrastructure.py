from aiohttp import ClientSession


class RequestInfrastructure:
    __session = None

    @classmethod
    async def get_session(cls):
        if cls.__session is None:
            client_session = ClientSession()
            cls.__session = client_session
        return cls.__session
