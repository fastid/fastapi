from random import randint

from .. import services, typing
from ..trace import decorator_trace


@decorator_trace(name='services.auth.sending_confirmation_code')
async def sending_confirmation_code(*, email: typing.Email) -> str:
    code = randint(1000, 9999)

    jwt_token = await services.session.create(
        expire_time_second=60 * 5,
        audience='confirmation of the user email',
        data={
            'code': code,
            'email': email,
        },
    )

    await services.sendmail.send(email=email, template='signup.html', subject='Sign Up', params={'code': code})
    return jwt_token
