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

    captcha: CaptchaType | None = None
    recaptcha_site_key: str | None = None
    captcha_usage: list[CaptchaUsage] = []
    jwt_iss: str
    password_policy_max_length: int
    password_policy_min_length: int


class RequestUsersRefreshToken(BaseModel):
    refresh_token: str


class ResponseUsersRefreshToken(BaseModel):
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
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = 'Bearer'


class ResponseUserInfo(BaseModel):
    email: typing.Email
    user_id: typing.UserID
