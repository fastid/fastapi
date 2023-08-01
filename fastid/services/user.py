from random import randint

from .. import services, typing
from ..logger import logger
from ..trace import decorator_trace


@decorator_trace(name='services.user.create_by_email')
async def create_by_email(*, email: typing.Email, password: typing.Password) -> None:
    code = randint(1000, 9999)

    jwt_token = await services.session.create(
        expire_time_second=60 * 5,
        audience='confirmation of the user email',
        data={
            'code': code,
            'email': email,
            'password': await services.password_hasher.hasher(password=password),
        },
    )

    await services.sendmail.send(email=email, template='signup.html', subject='Sign Up', params={'code': code})

    logger.debug(f'{jwt_token}')
