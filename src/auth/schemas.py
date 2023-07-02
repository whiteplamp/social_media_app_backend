from pydantic import BaseModel, validator, root_validator, validate_email


class UserSignUp(BaseModel):
    username: str
    full_name: str
    email: str
    password: str

    @root_validator(pre=True)
    def validate_fields(cls, values):
        for key in values:
            if not values[key]:
                raise ValueError(f"{key} is empty")
        return values

    @validator("email")
    def check_email(cls, value):
        try:
            validate_email(value)
        except Exception:
            raise ValueError("Wrong email")
        return value


class UserSignIn(BaseModel):
    username: str
    password: str

    @root_validator(pre=True)
    def validate_fields(cls, values):
        for key in values:
            if not values[key]:
                raise ValueError(f"{key} is empty")
        return values


class UserInSystem(BaseModel):
    id: str
    username: str
