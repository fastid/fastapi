import re
from datetime import date
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .. import repositories, services, typing
from ..exceptions import BadRequestException, NotFoundException
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


@decorator_trace(name='services.users.signin')
async def signin(email: typing.Email, password: typing.Password) -> models.Session:
    user = await services.users.get_by_email(email=email)
    if user is None:
        raise NotFoundException(message='User not found', i18n='user_not_found')

    try:
        await services.password_hasher.verify(password_hash=user.password, password=password)
    except BadRequestException as err:
        raise BadRequestException(i18n='email_or_password_incorrect', message='Email or password is incorrect') from err

    session = await services.session.create(
        expire_time_second=300,
        data={'user_id': user.user_id, 'type': 'signin'},
    )
    return models.Session.model_validate(session)


@decorator_trace(name='services.users.signin_session')
async def signin_session(session_key: str) -> models.Token:
    session = await services.session.get_by_session_key(session_key=session_key)
    if session is None:
        raise NotFoundException(message='Session not found', i18n='session_not_found')

    await services.session.delete_by_id(session_id=session.session_id)
    return await services.tokens.create(user_id=typing.UserID(session.data.get('user_id')), audience='internal')
