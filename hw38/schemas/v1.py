from pydantic import BaseModel, ConfigDict, Field, field_validator
import string


class AnimalCreateV1(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        description="The name of the animal",
        json_schema_extra={"example": "musya"},
    )
    age: float = Field(
        ...,
        gt=0,
        le=30,
        description="The age of the animal",
        json_schema_extra={"example": "3.5"},
    )
    adopted: bool = Field(
        ...,
        description="Is the animal adopted",
        json_schema_extra={"example": "yes"},
    )

    @field_validator("name")
    @classmethod
    def no_digits(cls, v: str) -> str:
        if any(map(lambda x: x in string.digits, v)):
            raise ValueError("Name shouldn't have digits")
        return v


class AnimalResponseV1(AnimalCreateV1):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(
        ...,
        description="The id of the animal",
        json_schema_extra={"example": "23"},
    )
