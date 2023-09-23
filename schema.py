import typing

import pydantic


class CreateUser(pydantic.BaseModel):
    email: str
    password: str

    @pydantic.validator("password")
    def secure_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password is short")
        return value


class UpdateUser(pydantic.BaseModel):
    email: typing.Optional[str]
    password: typing.Optional[str]

    @pydantic.validator("password")
    def secure_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password is short")
        return value


class CreateAds(pydantic.BaseModel):
    heading: str
    description: str

class UpdateAds(pydantic.BaseModel):
    heading: typing.Optional[str]
    description: typing.Optional[str]

    # @pydantic.validator("password")
    # def secure_password(cls, value):
    #     if len(value) < 8:
    #         raise ValueError("Password is short")
    #     return value

