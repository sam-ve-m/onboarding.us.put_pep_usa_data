from typing import Optional, Dict, Any, List

from pydantic import BaseModel, root_validator, constr


class PoliticallyExposedCondition(BaseModel):
    is_politically_exposed: bool
    politically_exposed_names: Optional[List[constr(min_length=1, max_length=100)]] = []

    @root_validator()
    def validate_composition(cls, values: Dict[str, Any]):
        is_politically_exposed = values.get("is_politically_exposed")
        if not is_politically_exposed:
            values["politically_exposed_names"] = []
            return values

        politically_exposed_names = values.get("politically_exposed_names")
        if is_politically_exposed and not politically_exposed_names:
            raise ValueError(
                "You need inform the field politically_exposed_names if you are politically exposed person"
            )
        return values
