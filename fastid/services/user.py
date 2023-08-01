from argon2 import PasswordHasher

from .. import services, typing
from ..logger import logger
from ..trace import decorator_trace


@decorator_trace(name='services.user.create_by_email')
async def create_by_email(email: typing.Email, password: typing.Password) -> None:
    ph = PasswordHasher()

    jwt_token = await services.session.create(
        expire_time_second=60 * 5,
        audience='confirmation of the user email',
        data={
            'email': email,
            'password': ph.hash(password),
        },
    )
    logger.debug(f'{jwt_token}')
