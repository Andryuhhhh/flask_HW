from pydantic import BaseModel, field_validator

from errors import HttpError


class BaseUser(BaseModel):
    name: str
    password: str

    @field_validator("password")
    @classmethod
    def check_password(cls, v):
        if len(v) < 8:
            raise ValueError("password must be at least 8 characters long")
        return v


class CreateUser(BaseUser):
    pass


class UpdateUser(BaseUser):
    name: str | None = None
    password: str | None = None


def validate(schema_cls, json_data):
    try:
        return schema_cls(**json_data).model_dump(exclude_unset=True)
    except ValueError as e:
        raise HttpError(400, str(e))
