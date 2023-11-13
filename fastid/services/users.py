from .. import repositories, typing
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
