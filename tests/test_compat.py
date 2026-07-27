from typing import Any

from nonebot.adapters.minecraft.compat import model_validator
from pydantic import BaseModel


def test_model_validator_before():
    class User(BaseModel):
        name: str

        @model_validator(mode="before")
        def normalize_name(cls, values: Any):
            if isinstance(values, dict):
                values["name"] = values["name"].strip()
            return values

    assert User(name=" Steve ").name == "Steve"
