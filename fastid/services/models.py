from dataclasses import dataclass
from enum import Enum

from .. import typing
from ..settings import Captcha


class CaptchaUsage(str, Enum):
    signin: str = 'signin'
    signup: str = 'signup'


@dataclass
class Config:
    captcha_usage: list[str]
    recaptcha_site_key: str | None
    jwt_iss: str
    password_policy_max_length: int
    password_policy_min_length: int
    captcha: Captcha | None = None
    link_github: bool = True
    logo_url: str | None = None
    logo_title: str | None = None


@dataclass
class Token:
    access_token: str
    refresh_token: str
    user_id: typing.UserID
    token_id: typing.TokenID
    token_type: str = 'Bearer'
    expires_in: int = 3600


@dataclass
class User:
    user_id: typing.UserID
    email: typing.Email
    password: typing.Password
