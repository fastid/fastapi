from datetime import date, datetime

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

from .. import services, typing
from ..depends import auth_user_depends
from ..exceptions import exception_responses

router = APIRouter(prefix='/users', responses=exception_responses)


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
    profile: _UserInfoProfile | None = None


@router.get(
    path='/info/',
    name='Info user',
)
async def info(user_id: auth_user_depends) -> ResponseUserInfo:
    user = await services.users.get_by_id(user_id=typing.UserID(user_id))
    return ResponseUserInfo.model_validate(user)
