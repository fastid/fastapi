from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from .. import typing


class CaptchaType(Enum):
    captcha = 'recaptcha'


class CaptchaUsage(Enum):
    signin = 'signin'
    signup = 'signup'


class ResponseConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    is_setup: bool = False
    captcha: CaptchaType | None = None
    recaptcha_site_key: str | None = None
    captcha_usage: list[CaptchaUsage] = []
    jwt_iss: str


class RequestCreateAdminUser(BaseModel):
    email: typing.Email = Field(..., title='Email address', description='Email address')
    password: typing.Password = Field(..., title='Password', description='Password')


class ResponseCreateAdminUser(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = 'Bearer'


class RequestUsersRefreshToken(BaseModel):
    refresh_token: str


class ResponseUsersRefreshToken(ResponseCreateAdminUser):
    pass
