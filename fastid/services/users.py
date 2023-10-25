from .. import repositories, typing
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
