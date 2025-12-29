from pydantic import BaseModel, field_validator

from constants import Difficulty

class Grid(BaseModel):
    value: list[list[int]]


class Grids(BaseModel):
    value: list[list[int]]
    solution: list[list[int]]
    difficulty: Difficulty

    @field_validator("difficulty", mode="before")
    @classmethod
    def validate_difficulty(cls, v):
        if isinstance(v, Difficulty):
            return v
        return Difficulty.from_input(v)


class BoardObject(BaseModel):
    grids: Grids
    results: int
    message: str

    @field_validator("grids", mode="before")
    @classmethod
    def convert_grids_list_to_object(cls, value):
        if isinstance(value, list):
            if not value:
                raise ValueError("grids list is empty")
            return value[0]
        return value