from .v1 import AnimalCreateV1
from pydantic import ConfigDict, Field
from typing import Literal


class AnimalCreateV2(AnimalCreateV1):
    health_status: Literal["healthy", "sick"] = Field(
        ...,
        description="The health status of the animal",
        json_schema_extra={"example": "healthy"},
    )


class AnimalResponseV2(AnimalCreateV2):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(
        ...,
        description="The id of the animal",
        json_schema_extra={"example": "23"},
    )
