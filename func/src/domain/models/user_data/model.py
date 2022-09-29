from abc import abstractmethod, ABC


class UserData(ABC):
    unique_id: str

    @abstractmethod
    def get_data_representation(self) -> dict:
        pass
