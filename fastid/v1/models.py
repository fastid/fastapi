from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from .. import typing
from ..settings import settings


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
    password_policy_max_length: int
    password_policy_min_length: int


class RequestCreateAdminUser(BaseModel):
    email: typing.Email = Field(..., title='Email address', description='Email address')
    password: typing.Password = Field(
        ...,
        title='Password',
        description='Password',
        min_length=settings.password_policy_min_length,
        max_length=settings.password_policy_max_length,
    )


class ResponseCreateAdminUser(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = 'Bearer'


class RequestUsersRefreshToken(BaseModel):
    refresh_token: str


class ResponseUsersRefreshToken(ResponseCreateAdminUser):
    pass
