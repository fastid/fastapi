from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, HttpUrl

from .. import typing
from ..settings import Captcha


class CaptchaUsage(str, Enum):
    signin: str = 'signin'
    signup: str = 'signup'


class CommonModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Config(CommonModel):
    captcha_usage: list[str]
    recaptcha_site_key: str | None
    jwt_iss: str
    link_github: HttpUrl
    password_policy_max_length: int
    password_policy_min_length: int
    captcha: Captcha | None = None


class Language(CommonModel):
    name: str
    value: str


class Token(CommonModel):
    access_token: str
    refresh_token: str
    user_id: typing.UserID
    token_id: typing.TokenID
    token_type: str = 'Bearer'
    expires_in: int = 3600


class Profile(CommonModel):
    timezone: str
    first_name: str | None = None
    last_name: str | None = None
    date_birth: date | None = None
    gender: typing.Gender | None = None
    locate: typing.Locate = typing.Locate.EN_US
    language: typing.Language = typing.Language.EN


class User(CommonModel):
    user_id: typing.UserID
    email: typing.Email
    created_at: datetime
    updated_at: datetime
    password: typing.Password
    profile: Profile | None = None


class Timezone(CommonModel):
    en: str
    ru: str
    timezone: str
    offset: str
