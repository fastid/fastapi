from .. import repositories, services, typing
from ..exceptions import NotFoundException
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


@decorator_trace(name='services.users.signin')
async def signin(*, email: typing.Email) -> models.Token | None:
    user = await get_by_email(email=email)
    if not user:
        raise NotFoundException(i18n='user_not_found', params={'email': email}, message='User not found')

    return await services.tokens.create(user_id=user.user_id, audience='internal')
