from datetime import date, datetime
from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from .. import services, typing

DataT = TypeVar('DataT')


class CaptchaType(Enum):
    captcha = 'recaptcha'


class CaptchaUsage(Enum):
    signin = 'signin'
    signup = 'signup'


class Response:
    class Config(services.models.Config):
        pass

    class Empty(BaseModel):
        pass


class Request:
    class Empty(BaseModel):
        pass


class ResponseEmpty(BaseModel):
    pass


class RequestEmpty(BaseModel):
    pass


class ResponseList(BaseModel, Generic[DataT]):
    results: list[DataT]

    class Config:
        title = 'Response List'


class ResponseConfig(services.models.Config):
    pass


# class ResponseConfig(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#
#     captcha: CaptchaType | None = None
#     recaptcha_site_key: str | None = None
#     captcha_usage: list[CaptchaUsage] = []
#     jwt_iss: str
#     password_policy_max_length: int
#     password_policy_min_length: int
#     link_github: bool = True
#     logo_url: str | None = None
#     logo_title: str | None = None


class RequestUsersRefreshToken(BaseModel):
    refresh_token: str


class ResponseUsersRefreshToken(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = 'Bearer'


class RequestUserSignin(BaseModel):
    email: typing.Email = Field(..., title='Email address', description='Email address')
    password: typing.Password = Field(
        ...,
        title='Password',
        description='Password',
    )
    captcha: str | None = Field(
        None,
        title='Captcha',
        description='Captcha',
    )


class ResponseUserSignin(ResponseUsersRefreshToken):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = 'Bearer'


class ResponseUserInfoProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    language: typing.Language
    timezone: str
    locate: str = 'en-us'
    first_name: str | None = None
    last_name: str | None = None
    date_birth: date | None = None
    gender: typing.Gender | None = None


class ResponseUserInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime
    updated_at: datetime
    email: typing.Email
    user_id: typing.UserID
    profile: ResponseUserInfoProfile | None = None


class RequestLanguage(BaseModel):
    locate: str
    language: typing.Language


class ResponseLanguage(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    value: str
