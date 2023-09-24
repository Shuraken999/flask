import typing

import pydantic


class CreateAds(pydantic.BaseModel):
    user: int
    heading: str
    description: str


class UpdateAds(pydantic.BaseModel):
    user: typing.Optional[int]
    heading: typing.Optional[str]
    description: typing.Optional[str]




class CreateUser(pydantic.BaseModel):
    email: str
    password: str
    owner: str

    @pydantic.validator("password")
    def secure_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password is short")
        return value


class UpdateUser(pydantic.BaseModel):
    email: typing.Optional[str]
    password: typing.Optional[str]
    owner: typing.Optional[str]

    @pydantic.validator("password")
    def secure_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password is short")
        return value




