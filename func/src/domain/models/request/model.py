from typing import Optional, Dict, Any, List

from pydantic import BaseModel, root_validator, constr

from src.domain.models.jwt_data.model import Jwt


class PoliticallyExposedCondition(BaseModel):
    is_politically_exposed: bool
    politically_exposed_names: Optional[List[constr(min_length=1, max_length=100)]] = []

    @root_validator()
    def validate_composition(cls, values: Dict[str, Any]):
        if not (is_politically_exposed := values.get("is_politically_exposed")):
            values["politically_exposed_names"] = []
            return values

        politically_exposed_names = values.get("politically_exposed_names")
        if is_politically_exposed and not politically_exposed_names:
            raise ValueError(
                "You need inform the field politically_exposed_names if you are politically exposed person"
            )
        return values


class PoliticallyExposedRequest:
    def __init__(
        self,
        x_thebes_answer: str,
        unique_id: str,
        politically_exposed: PoliticallyExposedCondition,
    ):
        self.x_thebes_answer = x_thebes_answer
        self.unique_id = unique_id
        self.politically_exposed = politically_exposed

    @classmethod
    async def build(cls, x_thebes_answer: str, parameters: dict):
        jwt = await Jwt.build(jwt=x_thebes_answer)
        politically_exposed = PoliticallyExposedCondition(**parameters)
        return cls(
            x_thebes_answer=x_thebes_answer,
            unique_id=jwt.unique_id,
            politically_exposed=politically_exposed,
        )
