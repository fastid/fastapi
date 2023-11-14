import re
from datetime import date
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .. import repositories, typing
from ..exceptions import NotFoundException
from ..trace import decorator_trace
from . import models, password_hasher


@decorator_trace(name='services.users.create')
async def create(*, email: typing.Email, password: typing.Password, admin: bool = False) -> models.User | None:
    password_hash = await password_hasher.hasher(password=password)
    user = await repositories.users.create(email=email, password=password_hash, admin=admin)
    return models.User.model_validate(user)


@decorator_trace(name='services.users.get_by_id')
async def get_by_id(*, user_id: typing.UserID) -> models.User | None:
    user = await repositories.users.get_by_id(user_id=user_id)
    if user is None:
        return None
    return models.User.model_validate(user)


@decorator_trace(name='services.users.get_by_email')
async def get_by_email(*, email: typing.Email) -> models.User | None:
    user = await repositories.users.get_by_email(email=email)
    if user is None:
        return None
    return await get_by_id(user_id=typing.UserID(user.user_id))


@decorator_trace(name='services.users.change_locate')
async def change_locate(*, user_id: typing.UserID, locate: typing.Locate) -> None:
    user = await repositories.users.get_by_id(user_id=user_id)
    if user is None:
        raise NotFoundException(message='User not found', i18n='user_not_found')

    if result := re.match('^([a-z]+)', locate.value):
        language = typing.Language(result.group(0))
        user.profile.locate = locate
        user.profile.language = language
        await user.profile.save()


@decorator_trace(name='services.users.change_timezone')
async def change_timezone(*, user_id: typing.UserID, timezone: str) -> None:
    user = await repositories.users.get_by_id(user_id=user_id)
    if user is None:
        raise NotFoundException(message='User not found', i18n='user_not_found')

    try:
        ZoneInfo(timezone)
    except ZoneInfoNotFoundError as err:
        raise NotFoundException(message='Timezone not found', i18n='timezone_not_found') from err

    user.profile.timezone = timezone
    await user.profile.save()


@decorator_trace(name='services.users.profile_save')
async def profile_save(
    *,
    user_id: typing.UserID,
    first_name: str,
    last_name: str,
    date_birth: date,
    gender: typing.Gender,
) -> models.User | None:
    user = await repositories.users.get_by_id(user_id=user_id)
    if user is None:
        raise NotFoundException(message='User not found', i18n='user_not_found')

    user.profile.first_name = first_name
    user.profile.last_name = last_name
    user.profile.date_birth = date_birth
    user.profile.gender = gender
    await user.profile.save()
    return await get_by_id(user_id=typing.UserID(user.user_id))
