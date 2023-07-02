import enum

from pydantic import BaseModel, root_validator


class Post(BaseModel):
    text: str

    @root_validator(pre=True)
    def validate_fields(cls, values):
        for key in values:
            if not values[key]:
                raise ValueError(f"{key} is empty")
        return values


class Actions(enum.Enum):
    like = 0
    dislike = 1

