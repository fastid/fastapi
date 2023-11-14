from datetime import date, datetime
from typing import Generic, TypeVar

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

from .. import services, typing
from ..depends import auth_user_depends
from ..exceptions import NotFoundException, exception_responses

router = APIRouter(prefix='/users', responses=exception_responses)

Results = TypeVar('Results')


class _UserInfoProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    language: typing.Language
    timezone: str
    locate: typing.Locate = typing.Locate.EN_US
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
    admin: bool
    profile: _UserInfoProfile | None = None


class Language(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    value: str


class Timezone(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    en: str
    ru: str
    timezone: str
    offset: str


class ResponseList(BaseModel, Generic[Results]):
    results: list[Results]


class RequestLanguage(BaseModel):
    locate: str


class RequestTimezone(BaseModel):
    timezone: str


class ResponseEmpty(BaseModel):
    pass


@router.get(
    path='/info/',
    summary='Info user',
)
async def info(user_id: auth_user_depends) -> ResponseUserInfo:
    user = await services.users.get_by_id(user_id=typing.UserID(user_id))
    return ResponseUserInfo.model_validate(user)


@router.get(
    path='/language/',
    summary='Get language list',
)
async def language_list() -> ResponseList[Language]:
    languages = await services.language.get_all()
    return ResponseList[Language].model_validate({'results': languages})


@router.post(
    path='/language/',
    summary='Save the user language and locate',
)
async def language_save(user_id: auth_user_depends, body: RequestLanguage) -> ResponseEmpty:
    if body.locate not in [locate.value for locate in typing.Locate]:
        raise NotFoundException(message='Language not found', i18n='language_not_found')

    await services.users.change_locate(user_id=user_id, locate=typing.Locate(body.locate))
    return ResponseEmpty()


@router.get(
    path='/timezone/',
    summary='Get timezone list',
)
async def timezone_list() -> ResponseList[Timezone]:
    timezone = await services.timezone.get_all()
    return ResponseList[Timezone].model_validate({'results': timezone})


@router.post(
    path='/timezone/',
    summary='Save the user timezone',
)
async def timezone_save(user_id: auth_user_depends, body: RequestTimezone) -> ResponseEmpty:
    await services.users.change_timezone(user_id=user_id, timezone=body.timezone)
    return ResponseEmpty()
