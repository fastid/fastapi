from dataclasses import dataclass
from enum import Enum

from .. import services, typing


class CaptchaType(Enum):
    captcha = 'recaptcha'


class CaptchaUsage(Enum):
    signin = 'signin'
    signup = 'signup'


@dataclass
class Config:
    is_setup: bool
    captcha: CaptchaType | None
    captcha_usage: list[CaptchaUsage]
    recaptcha_site_key: str | None
    jwt_iss: str


@dataclass
class Token:
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'
    expires_in: int = 3600


@dataclass
class User:
    user_id: typing.UserID
    email: typing.Email
    password: typing.Password

    async def verify_password(self, password: typing.Password) -> bool:
        return await services.password_hasher.verify(password_hash=self.password, password=password)
