from typing import Optional, List

from src.domain.models.user_data.model import UserData


class PoliticallyExposedData(UserData):
    def __init__(
        self,
        unique_id: str,
        is_politically_exposed: bool,
        politically_exposed_names: Optional[List[str]],
    ):
        self.unique_id = unique_id
        self.is_politically_exposed = is_politically_exposed
        self.politically_exposed_names = politically_exposed_names

    def get_data_representation(self) -> dict:
        data = {
            "external_exchange_requirements.us.is_politically_exposed": self.is_politically_exposed,
            "external_exchange_requirements.us.politically_exposed_names": self.politically_exposed_names,
        }
        return data
