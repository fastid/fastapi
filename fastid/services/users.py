from .. import repositories, services, typing
from ..exceptions import BadRequestException
from ..trace import decorator_trace
from . import models


@decorator_trace(name='services.users.create')
async def create(*, email: typing.Email, password: typing.Password) -> typing.UserID | None:
    return await repositories.users.create(email=email, password=password)


@decorator_trace(name='services.users.get_by_email')
async def get_by_email(*, email: typing.Email) -> models.User | None:
    user = await repositories.users.get_by_email(email=email)
    if user is None:
        return None

    return models.User(user_id=user.user_id, email=user.email, password=user.password)


@decorator_trace(name='services.users.get_by_id')
async def get_by_id(*, user_id: typing.UserID) -> models.User | None:
    user = await repositories.users.get_by_id(user_id=user_id)
    if user is None:
        return None

    return models.User(user_id=user.user_id, email=user.email, password=user.password)


@decorator_trace(name='services.users.signin')
async def signin(*, email: typing.Email, password: typing.Password) -> models.Token | None:
    user = await get_by_email(email=email)
    if not user:
        raise BadRequestException(
            i18n='email_or_password_incorrect',
            params={'email': email},
            message='Email or password is incorrect',
        )

    try:
        await services.password_hasher.verify(password_hash=user.password, password=password)
    except BadRequestException as err:
        raise BadRequestException(i18n='email_or_password_incorrect', message='Email or password is incorrect') from err

    return await services.tokens.create(user_id=user.user_id, audience='internal')
