from dataclasses import dataclass
from enum import Enum


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
